"""Three-statement model for CAMS, the provisional winner."""

from __future__ import annotations

from typing import Any

import pandas as pd

from .data_loader import company_fy
from .relative_valuation import forecast_company

CAMS_START = {
    "net_fixed_assets": 494.0,
    "cash_and_investments": 970.0,
    "receivables": 58.0,
    "other_assets": 287.0,
    "total_debt": 64.0,
    "other_liabilities": 424.0,
    "equity": 1321.0,
}


def build_cams_model(financials: pd.DataFrame, assumptions: dict[str, Any]) -> pd.DataFrame:
    """Build linked P&L, balance sheet and cash flow for CAMS FY27-FY31."""

    base = company_fy(financials, "CAMS", "FY26")
    forecast = forecast_company("CAMS", financials, assumptions)
    tax_rate = float(assumptions["companies"]["CAMS"]["tax_rate"])
    payout = float(assumptions["companies"]["CAMS"]["dividend_payout"])

    nfa = CAMS_START["net_fixed_assets"]
    cash = CAMS_START["cash_and_investments"]
    receivables = CAMS_START["receivables"]
    other_assets = CAMS_START["other_assets"]
    debt = CAMS_START["total_debt"]
    other_liabilities = CAMS_START["other_liabilities"]
    equity = CAMS_START["equity"]

    base_revenue = float(base["revenue"])
    receivable_days = 14.0
    other_assets_pct = CAMS_START["other_assets"] / base_revenue
    other_liabilities_pct = CAMS_START["other_liabilities"] / base_revenue

    rows: list[dict[str, Any]] = []
    prior_cash = cash
    prior_ar = receivables
    prior_oa = other_assets
    prior_ol = other_liabilities
    prior_equity = equity
    prior_debt = debt
    debt_repayment = [14.0, 10.0, 10.0, 10.0, 10.0]

    for index, row in forecast.iterrows():
        revenue = float(row["revenue"])
        depreciation = float(row["depreciation"])
        capex = float(row["capex"])
        pat = float(row["pat"])
        ebit = float(row["ebit"])
        dividends = pat * payout

        nfa = nfa + capex - depreciation
        receivables = revenue * receivable_days / 365.0
        other_assets = revenue * other_assets_pct
        other_liabilities = revenue * other_liabilities_pct
        debt = max(prior_debt - debt_repayment[int(index)], 0.0)
        equity = prior_equity + pat - dividends

        total_assets = nfa + cash + receivables + other_assets
        total_liabilities = equity + debt + other_liabilities
        cash = total_liabilities - nfa - receivables - other_assets

        delta_ar = receivables - prior_ar
        delta_oa = other_assets - prior_oa
        delta_ol = other_liabilities - prior_ol
        delta_nwc = delta_ar + delta_oa - delta_ol
        cfo = pat + depreciation - delta_nwc
        cfi = -capex
        delta_debt = debt - prior_debt
        cff = -dividends + delta_debt
        delta_cash = cfo + cfi + cff
        cash_roll = prior_cash + delta_cash
        fcf = cfo - capex
        fcff = ebit * (1 - tax_rate) + depreciation - capex - delta_nwc

        rows.append(
            {
                "ticker": "CAMS",
                "fiscal_year": row["fiscal_year"],
                "revenue": revenue,
                "ebitda": row["ebitda"],
                "ebitda_margin_pct": row["ebitda_margin_pct"],
                "depreciation": depreciation,
                "ebit": ebit,
                "other_income": row["other_income"],
                "interest": row["interest"],
                "pbt": row["pbt"],
                "tax": row["tax"],
                "pat": pat,
                "eps": row["eps"],
                "dividends": dividends,
                "net_fixed_assets": nfa,
                "cash_and_investments": cash,
                "receivables": receivables,
                "other_assets": other_assets,
                "total_assets": nfa + cash + receivables + other_assets,
                "total_debt": debt,
                "other_liabilities": other_liabilities,
                "equity": equity,
                "total_liabilities": equity + debt + other_liabilities,
                "cfo": cfo,
                "capex": capex,
                "cfi": cfi,
                "cff": cff,
                "delta_cash": delta_cash,
                "fcf": fcf,
                "fcff": fcff,
                "net_cash": cash - debt,
                "nwc": receivables + other_assets - other_liabilities,
                "delta_nwc": delta_nwc,
                "balance_sheet_check": (nfa + cash + receivables + other_assets)
                - (equity + debt + other_liabilities),
                "cash_roll_check": cash - cash_roll,
            }
        )

        prior_cash = cash
        prior_ar = receivables
        prior_oa = other_assets
        prior_ol = other_liabilities
        prior_equity = equity
        prior_debt = debt

    return pd.DataFrame(rows)
