"""Data loading and integrity checks for the Zeckathon model."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "processed"
CONFIG_PATH = ROOT / "config" / "assumptions.yaml"

REQUIRED_FIN_COLUMNS = {
    "company",
    "ticker",
    "period",
    "period_end",
    "revenue",
    "ebitda",
    "depreciation",
    "ebit",
    "other_income",
    "interest",
    "pbt",
    "tax_rate_pct",
    "pat",
    "eps",
    "cfo",
    "capex",
    "fcf",
    "investments",
    "total_debt",
    "equity",
    "shares_cr",
    "dps",
    "payout_pct",
    "source_id",
}

REQUIRED_MARKET_COLUMNS = {
    "company",
    "ticker",
    "price_date",
    "price_inr",
    "shares_cr",
    "market_cap_cr",
    "net_cash_cr",
    "net_debt_cr",
    "ev_cr",
    "dividend_yield_pct",
    "ttm_eps",
    "source_id",
}


def load_assumptions(path: Path | str = CONFIG_PATH) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_financials(path: Path | str = DATA_DIR / "company_financials.csv") -> pd.DataFrame:
    frame = pd.read_csv(path)
    missing = REQUIRED_FIN_COLUMNS.difference(frame.columns)
    if missing:
        raise ValueError(f"Financial data missing columns: {sorted(missing)}")
    frame["period_end"] = pd.to_datetime(frame["period_end"])
    return frame.sort_values(["ticker", "period_end"]).reset_index(drop=True)


def load_market(path: Path | str = DATA_DIR / "market_data.csv") -> pd.DataFrame:
    frame = pd.read_csv(path)
    missing = REQUIRED_MARKET_COLUMNS.difference(frame.columns)
    if missing:
        raise ValueError(f"Market data missing columns: {sorted(missing)}")
    frame["price_date"] = pd.to_datetime(frame["price_date"])
    return frame.set_index("ticker")


def load_quarterly(path: Path | str = DATA_DIR / "quarterly_data.csv") -> pd.DataFrame:
    return pd.read_csv(path)


def company_fy(financials: pd.DataFrame, ticker: str, period: str = "FY26") -> pd.Series:
    rows = financials[(financials["ticker"] == ticker) & (financials["period"] == period)]
    if len(rows) != 1:
        raise ValueError(f"Expected one row for {ticker} {period}, found {len(rows)}")
    return rows.iloc[0]


def validate_data(
    financials: pd.DataFrame | None = None,
    market: pd.DataFrame | None = None,
    assumptions: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Return a machine-readable check log. Raises only on structural issues."""

    financials = load_financials() if financials is None else financials
    market = load_market() if market is None else market
    assumptions = load_assumptions() if assumptions is None else assumptions

    checks: list[dict[str, Any]] = []

    def add(name: str, passed: bool, detail: str) -> None:
        checks.append({"check": name, "status": "PASS" if passed else "FAIL", "detail": detail})

    duplicates = financials.duplicated(subset=["ticker", "period"]).sum()
    add("no_duplicate_company_periods", duplicates == 0, f"{duplicates} duplicates")

    for _, row in financials.iterrows():
        key = f"{row['ticker']} {row['period']}"
        ebit_gap = abs(row["ebitda"] - row["depreciation"] - row["ebit"])
        add(f"ebit_bridge_{key}", ebit_gap <= 1.0, f"gap={ebit_gap:.2f}")

        pbt_gap = abs(row["ebit"] + row["other_income"] - row["interest"] - row["pbt"])
        add(f"pbt_bridge_{key}", pbt_gap <= 2.0, f"gap={pbt_gap:.2f}")

        implied_pat = row["pbt"] * (1 - row["tax_rate_pct"] / 100)
        pat_gap = abs(implied_pat - row["pat"])
        add(f"pat_tax_bridge_{key}", pat_gap <= 5.0, f"gap={pat_gap:.2f}")

        fcf_gap = abs(row["cfo"] - row["capex"] - row["fcf"])
        add(f"fcf_bridge_{key}", fcf_gap <= 1.0, f"gap={fcf_gap:.2f}")

        add(f"positive_revenue_{key}", row["revenue"] > 0, f"revenue={row['revenue']}")
        add(f"positive_shares_{key}", row["shares_cr"] > 0, f"shares={row['shares_cr']}")

    for ticker, row in market.iterrows():
        implied_cap = row["price_inr"] * row["shares_cr"]
        gap_pct = abs(implied_cap - row["market_cap_cr"]) / row["market_cap_cr"]
        add(f"market_cap_{ticker}", gap_pct <= 0.01, f"gap={gap_pct:.3%}")

        implied_ev = row["market_cap_cr"] + row["net_debt_cr"] - row["net_cash_cr"]
        ev_gap = abs(implied_ev - row["ev_cr"])
        add(f"ev_bridge_{ticker}", ev_gap <= 1.0, f"gap={ev_gap:.2f}")

        add(f"net_cash_{ticker}", row["net_cash_cr"] >= 0, f"net_cash={row['net_cash_cr']}")

    probability_sum = sum(assumptions["scenarios"][name]["probability"] for name in ("bull", "base", "bear"))
    add("scenario_probabilities_sum", abs(probability_sum - 1.0) < 1e-9, f"sum={probability_sum}")

    weights = assumptions["decision_matrix"]["weights"]
    add("decision_weights_sum", abs(sum(weights.values()) - 1.0) < 1e-9, f"sum={sum(weights.values())}")

    for scenario in ("bull", "base", "bear"):
        for ticker in ("BSE", "CDSL", "CAMS", "KFINTECH"):
            if ticker not in assumptions["scenarios"][scenario]["target_pe"]:
                add(f"scenario_pe_{scenario}_{ticker}", False, "missing")
    return checks


def checks_frame(checks: list[dict[str, Any]]) -> pd.DataFrame:
    return pd.DataFrame(checks)


if __name__ == "__main__":
    frame = checks_frame(validate_data())
    failures = frame[frame["status"] == "FAIL"]
    print(frame.to_string(index=False))
    print(f"\n{len(frame)} checks; {len(failures)} failures")
    if len(failures):
        raise SystemExit(1)
