"""Bull/base/bear scenarios and mandatory regulatory/market shocks."""

from __future__ import annotations

from typing import Any

import pandas as pd

from .relative_valuation import forecast_all


def scenario_table(
    financials: pd.DataFrame,
    market: pd.DataFrame,
    assumptions: dict[str, Any],
) -> pd.DataFrame:
    forecasts = forecast_all(financials, assumptions)
    rows: list[dict[str, Any]] = []

    for ticker in ("BSE", "CDSL", "CAMS", "KFINTECH"):
        mkt = market.loc[ticker]
        fy28 = forecasts[(forecasts["ticker"] == ticker) & (forecasts["fiscal_year"] == "FY28")].iloc[0]
        for scenario in ("bull", "base", "bear"):
            cfg = assumptions["scenarios"][scenario]
            target_eps = fy28["eps"] * cfg["eps_multiplier"][ticker]
            target_pe = cfg["target_pe"][ticker]
            target_price = target_eps * target_pe
            price_return = target_price / mkt["price_inr"] - 1
            total_return = price_return + mkt["dividend_yield_pct"] / 100
            rows.append(
                {
                    "ticker": ticker,
                    "scenario": scenario,
                    "probability": cfg["probability"],
                    "fy28_eps": target_eps,
                    "target_pe": target_pe,
                    "target_price": target_price,
                    "price_return_pct": price_return * 100,
                    "total_return_pct": total_return * 100,
                    "current_price": mkt["price_inr"],
                }
            )
    return pd.DataFrame(rows)


def expected_value_table(scenarios: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for ticker, group in scenarios.groupby("ticker", sort=False):
        probabilities = group["probability"]
        expected_price = (group["target_price"] * probabilities).sum()
        expected_price_return = (group["price_return_pct"] * probabilities).sum()
        expected_total_return = (group["total_return_pct"] * probabilities).sum()
        base = group[group["scenario"] == "base"].iloc[0]
        bear = group[group["scenario"] == "bear"].iloc[0]
        bull = group[group["scenario"] == "bull"].iloc[0]
        rows.append(
            {
                "ticker": ticker,
                "probability_sum": probabilities.sum(),
                "base_target_price": base["target_price"],
                "bull_target_price": bull["target_price"],
                "bear_target_price": bear["target_price"],
                "expected_target_price": expected_price,
                "base_price_return_pct": base["price_return_pct"],
                "expected_price_return_pct": expected_price_return,
                "expected_total_return_pct": expected_total_return,
                "bear_downside_pct": bear["price_return_pct"],
                "bull_upside_pct": bull["price_return_pct"],
            }
        )
    return pd.DataFrame(rows)


def shock_table(
    financials: pd.DataFrame,
    market: pd.DataFrame,
    assumptions: dict[str, Any],
) -> pd.DataFrame:
    forecasts = forecast_all(financials, assumptions)
    fno_shock = assumptions["shocks"]["fno_turnover_decline"]
    equity_shock = assumptions["shocks"]["equity_drawdown"]
    rows: list[dict[str, Any]] = []

    for ticker in ("BSE", "CDSL", "CAMS", "KFINTECH"):
        cfg = assumptions["companies"][ticker]
        mkt = market.loc[ticker]
        fy27 = forecasts[(forecasts["ticker"] == ticker) & (forecasts["fiscal_year"] == "FY27")].iloc[0]
        base_revenue = float(fy27["revenue"])
        base_ebitda = float(fy27["ebitda"])
        base_pat = float(fy27["pat"])
        base_eps = float(fy27["eps"])
        base_fcf = float(fy27["fcf"])
        shares = float(fy27["shares_cr"])

        fno_revenue_impact = base_revenue * cfg["shock_fno_revenue_elasticity"] * fno_shock
        equity_revenue_impact = base_revenue * cfg["shock_equity_revenue_elasticity"] * equity_shock
        joint_revenue_impact = fno_revenue_impact + equity_revenue_impact

        for case, revenue_impact in (
            ("fno_minus_30pct", fno_revenue_impact),
            ("equity_minus_20pct", equity_revenue_impact),
            ("joint_adverse", joint_revenue_impact),
        ):
            revenue_impact_pct = revenue_impact / base_revenue
            pat_impact_pct = revenue_impact_pct * cfg["shock_pat_elasticity"]
            shocked_pat = base_pat * (1 + pat_impact_pct)
            shocked_eps = shocked_pat / shares
            shocked_revenue = base_revenue + revenue_impact
            shocked_ebitda = base_ebitda * (1 + revenue_impact_pct * 1.15)
            shocked_fcf = base_fcf * (1 + pat_impact_pct)
            shocked_margin = shocked_ebitda / shocked_revenue * 100
            multiple_haircut = 1.0 if case != "joint_adverse" else 0.85
            shocked_target = shocked_eps * cfg["base_target_pe"] * multiple_haircut
            base_target_fy27 = base_eps * cfg["base_target_pe"]
            rows.append(
                {
                    "ticker": ticker,
                    "case": case,
                    "base_revenue_fy27": base_revenue,
                    "revenue_impact_cr": revenue_impact,
                    "revenue_impact_pct": revenue_impact_pct * 100,
                    "base_ebitda_fy27": base_ebitda,
                    "shocked_ebitda_fy27": shocked_ebitda,
                    "shocked_ebitda_margin_pct": shocked_margin,
                    "base_pat_fy27": base_pat,
                    "pat_impact_pct": pat_impact_pct * 100,
                    "shocked_pat_fy27": shocked_pat,
                    "base_eps_fy27": base_eps,
                    "shocked_eps_fy27": shocked_eps,
                    "base_fcf_fy27": base_fcf,
                    "shocked_fcf_fy27": shocked_fcf,
                    "base_target_price_fy27": base_target_fy27,
                    "target_pe_used": cfg["base_target_pe"] * multiple_haircut,
                    "shocked_target_price": shocked_target,
                    "target_change_vs_base_target_pct": (shocked_target / base_target_fy27 - 1) * 100,
                    "target_change_vs_current_pct": (shocked_target / mkt["price_inr"] - 1) * 100,
                }
            )
    return pd.DataFrame(rows)
