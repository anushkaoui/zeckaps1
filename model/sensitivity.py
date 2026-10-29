"""Sensitivity grids and tornado analysis for CAMS."""

from __future__ import annotations

from typing import Any

import pandas as pd

from .dcf import dcf_valuation
from .relative_valuation import forecast_company

TICKER = "CAMS"


def target_sensitivity_grid(
    financials: pd.DataFrame,
    market: pd.DataFrame,
    assumptions: dict[str, Any],
) -> pd.DataFrame:
    forecast = forecast_company(TICKER, financials, assumptions)
    fy28_eps = float(forecast.loc[forecast["fiscal_year"] == "FY28", "eps"].iloc[0])
    current = float(market.loc[TICKER, "price_inr"])
    rows = []
    for pe in [26, 28, 30, 32, 33, 34, 36, 38]:
        for eps_multiplier in [0.85, 0.90, 0.95, 1.00, 1.05, 1.10, 1.15]:
            target = pe * fy28_eps * eps_multiplier
            rows.append(
                {
                    "target_pe": pe,
                    "eps_multiplier": eps_multiplier,
                    "fy28_eps": fy28_eps * eps_multiplier,
                    "target_price": target,
                    "upside_pct": (target / current - 1) * 100,
                }
            )
    return pd.DataFrame(rows)


def _blended_target(relative_target: float, dcf_value: float, assumptions: dict[str, Any]) -> float:
    weight = assumptions["valuation"]["blend_weight_relative"]
    return weight * relative_target + (1 - weight) * dcf_value


def tornado_table(
    financials: pd.DataFrame,
    market: pd.DataFrame,
    assumptions: dict[str, Any],
) -> pd.DataFrame:
    cfg = assumptions["companies"][TICKER]
    base_forecast = forecast_company(TICKER, financials, assumptions)
    base_eps = float(base_forecast.loc[base_forecast["fiscal_year"] == "FY28", "eps"].iloc[0])
    base_relative = base_eps * cfg["base_target_pe"]
    base_dcf, _ = dcf_valuation(financials, market, assumptions)
    base_dcf_value = base_dcf["dcf_value_per_share"]
    base_target = _blended_target(base_relative, base_dcf_value, assumptions)

    rows: list[dict[str, Any]] = []

    def add(name: str, low: float, high: float, note: str) -> None:
        rows.append(
            {
                "driver": name,
                "low_target": low,
                "base_target": base_target,
                "high_target": high,
                "low_delta": low - base_target,
                "high_delta": high - base_target,
                "swing": high - low,
                "note": note,
            }
        )

    for shift, label in ((-0.02, "low"), (0.02, "high")):
        forecast = forecast_company(TICKER, financials, assumptions, growth_shift=shift)
        eps = float(forecast.loc[forecast["fiscal_year"] == "FY28", "eps"].iloc[0])
        target = _blended_target(eps * cfg["base_target_pe"], base_dcf_value, assumptions)
        if label == "low":
            growth_low = target
        else:
            growth_high = target
    add("revenue_growth_+/-200bps", growth_low, growth_high, "Five-year revenue growth shift")

    for shift, label in ((-0.02, "low"), (0.02, "high")):
        forecast = forecast_company(TICKER, financials, assumptions, margin_shift=shift)
        eps = float(forecast.loc[forecast["fiscal_year"] == "FY28", "eps"].iloc[0])
        target = _blended_target(eps * cfg["base_target_pe"], base_dcf_value, assumptions)
        if label == "low":
            margin_low = target
        else:
            margin_high = target
    add("ebitda_margin_+/-200bps", margin_low, margin_high, "FY27-FY31 EBITDA margin shift")

    pe_targets = [
        _blended_target(base_eps * (cfg["base_target_pe"] - 5), base_dcf_value, assumptions),
        _blended_target(base_eps * (cfg["base_target_pe"] + 5), base_dcf_value, assumptions),
    ]
    add("target_pe_+/-5x", pe_targets[0], pe_targets[1], "FY28 target P/E")

    dcf_low, _ = dcf_valuation(
        financials, market, assumptions, wacc=assumptions["valuation"]["wacc"] + 0.01
    )
    dcf_high, _ = dcf_valuation(
        financials, market, assumptions, wacc=assumptions["valuation"]["wacc"] - 0.01
    )
    add(
        "wacc_+/-100bps",
        _blended_target(base_relative, dcf_low["dcf_value_per_share"], assumptions),
        _blended_target(base_relative, dcf_high["dcf_value_per_share"], assumptions),
        "DCF discount rate",
    )

    dcf_g_low, _ = dcf_valuation(
        financials,
        market,
        assumptions,
        terminal_growth=assumptions["valuation"]["terminal_growth"] - 0.01,
    )
    dcf_g_high, _ = dcf_valuation(
        financials,
        market,
        assumptions,
        terminal_growth=assumptions["valuation"]["terminal_growth"] + 0.01,
    )
    add(
        "terminal_growth_+/-100bps",
        _blended_target(base_relative, dcf_g_low["dcf_value_per_share"], assumptions),
        _blended_target(base_relative, dcf_g_high["dcf_value_per_share"], assumptions),
        "DCF terminal growth",
    )

    net_cash = float(market.loc[TICKER, "net_cash_cr"])
    shares = float(market.loc[TICKER, "shares_cr"])
    dcf_nc_low = base_dcf_value - 0.20 * net_cash / shares
    dcf_nc_high = base_dcf_value + 0.20 * net_cash / shares
    add(
        "net_cash_+/-20pct",
        _blended_target(base_relative, dcf_nc_low, assumptions),
        _blended_target(base_relative, dcf_nc_high, assumptions),
        "Net-cash haircut",
    )

    add(
        "share_count_+/-2pct",
        base_target / 1.02,
        base_target / 0.98,
        "Diluted share count",
    )

    return pd.DataFrame(rows).sort_values("swing", ascending=False).reset_index(drop=True)
