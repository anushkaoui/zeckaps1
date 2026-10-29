"""Discounted cash flow for CAMS with explicit fade and sensitivity grid."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from .three_statement import build_cams_model


def cost_of_capital(assumptions: dict[str, Any]) -> dict[str, float]:
    val = assumptions["valuation"]
    cost_equity = val["risk_free"] + val["beta"] * val["equity_risk_premium"]
    after_tax_debt = val["cost_of_debt"] * (1 - val["tax_rate"])
    wacc = (1 - val["debt_weight"]) * cost_equity + val["debt_weight"] * after_tax_debt
    return {
        "risk_free_pct": val["risk_free"] * 100,
        "equity_risk_premium_pct": val["equity_risk_premium"] * 100,
        "beta": val["beta"],
        "cost_of_equity_pct": cost_equity * 100,
        "after_tax_cost_of_debt_pct": after_tax_debt * 100,
        "wacc_pct": wacc * 100,
        "terminal_growth_pct": val["terminal_growth"] * 100,
    }


def _fade_rows(
    model: pd.DataFrame,
    assumptions: dict[str, Any],
) -> pd.DataFrame:
    val = assumptions["valuation"]
    tax_rate = float(assumptions["companies"]["CAMS"]["tax_rate"])
    last = model.iloc[-1]
    revenue_prior = float(last["revenue"])
    nwc_prior = float(last["nwc"])

    rows: list[dict[str, Any]] = []
    for offset, (growth, margin) in enumerate(
        zip(val["fade_growth"], val["fade_margin"]), start=1
    ):
        revenue = revenue_prior * (1 + growth)
        depreciation = revenue * float(val["fade_dep_pct_revenue"])
        capex = revenue * float(val["fade_capex_pct_revenue"])
        ebit = revenue * margin - depreciation
        nwc = revenue * float(val["fade_nwc_pct_revenue"])
        delta_nwc = nwc - nwc_prior
        fcff = ebit * (1 - tax_rate) + depreciation - capex - delta_nwc
        rows.append(
            {
                "fiscal_year": f"FY{31 + offset}",
                "year_index": int(last["fiscal_year"].replace("FY", "")) + offset - 26,
                "revenue": revenue,
                "ebit": ebit,
                "fcff": fcff,
                "delta_nwc": delta_nwc,
            }
        )
        revenue_prior = revenue
        nwc_prior = nwc
    return pd.DataFrame(rows)


def dcf_valuation(
    financials: pd.DataFrame,
    market: pd.DataFrame,
    assumptions: dict[str, Any],
    wacc: float | None = None,
    terminal_growth: float | None = None,
) -> tuple[dict[str, float], pd.DataFrame]:
    val = assumptions["valuation"]
    wacc = val["wacc"] if wacc is None else wacc
    terminal_growth = val["terminal_growth"] if terminal_growth is None else terminal_growth
    if wacc <= terminal_growth:
        raise ValueError("WACC must exceed terminal growth")

    model = build_cams_model(financials, assumptions)
    fade = _fade_rows(model, assumptions)

    explicit = pd.concat(
        [
            model[["fiscal_year", "revenue", "ebit", "fcff"]],
            fade[["fiscal_year", "revenue", "ebit", "fcff"]],
        ],
        ignore_index=True,
    )
    explicit["year_index"] = range(1, len(explicit) + 1)
    explicit["discount_factor"] = 1 / (1 + wacc) ** explicit["year_index"]
    explicit["pv_fcff"] = explicit["fcff"] * explicit["discount_factor"]

    terminal_fcff = float(explicit.iloc[-1]["fcff"]) * (1 + terminal_growth)
    terminal_value = terminal_fcff / (wacc - terminal_growth)
    pv_terminal = terminal_value * float(explicit.iloc[-1]["discount_factor"])
    ev = float(explicit["pv_fcff"].sum()) + pv_terminal

    net_cash = float(market.loc["CAMS", "net_cash_cr"])
    equity_value = ev + net_cash
    shares = float(market.loc["CAMS", "shares_cr"])
    per_share = equity_value / shares

    pat_fy28 = float(model.loc[model["fiscal_year"] == "FY28", "pat"].iloc[0])
    eps_fy28 = float(model.loc[model["fiscal_year"] == "FY28", "eps"].iloc[0])
    summary = {
        "wacc_pct": wacc * 100,
        "terminal_growth_pct": terminal_growth * 100,
        "pv_explicit_fcff_cr": float(explicit["pv_fcff"].sum()),
        "terminal_value_cr": terminal_value,
        "pv_terminal_cr": pv_terminal,
        "enterprise_value_cr": ev,
        "net_cash_cr": net_cash,
        "equity_value_cr": equity_value,
        "shares_cr": shares,
        "dcf_value_per_share": per_share,
        "terminal_value_share_of_ev_pct": pv_terminal / ev * 100,
        "implied_pe_fy28": equity_value / pat_fy28,
        "eps_fy28": eps_fy28,
        "current_price_inr": float(market.loc["CAMS", "price_inr"]),
        "upside_vs_current_pct": (per_share / float(market.loc["CAMS", "price_inr"]) - 1) * 100,
    }
    explicit["terminal_value"] = np.nan
    explicit["pv_terminal"] = np.nan
    explicit.loc[explicit.index[-1], "terminal_value"] = terminal_value
    explicit.loc[explicit.index[-1], "pv_terminal"] = pv_terminal
    return summary, explicit


def dcf_sensitivity(
    financials: pd.DataFrame,
    market: pd.DataFrame,
    assumptions: dict[str, Any],
    wacc_range: list[float] | None = None,
    growth_range: list[float] | None = None,
) -> pd.DataFrame:
    waccs = wacc_range or [0.085, 0.090, 0.095, 0.100, 0.105, 0.110, 0.115]
    growths = growth_range or [0.045, 0.050, 0.055, 0.060, 0.065, 0.070]
    rows = []
    for wacc in waccs:
        for growth in growths:
            if wacc <= growth:
                value = None
            else:
                summary, _ = dcf_valuation(
                    financials, market, assumptions, wacc=wacc, terminal_growth=growth
                )
                value = summary["dcf_value_per_share"]
            rows.append(
                {
                    "wacc_pct": wacc * 100,
                    "terminal_growth_pct": growth * 100,
                    "dcf_value_per_share": value,
                }
            )
    return pd.DataFrame(rows)
