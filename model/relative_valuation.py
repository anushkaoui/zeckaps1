"""Relative valuation and five-year forecast drivers."""

from __future__ import annotations

from typing import Any

import pandas as pd

from .data_loader import company_fy


def forecast_company(
    ticker: str,
    financials: pd.DataFrame,
    assumptions: dict[str, Any],
    growth_shift: float = 0.0,
    margin_shift: float = 0.0,
) -> pd.DataFrame:
    """Build a five-year operating forecast from FY26 base and config drivers."""

    base = company_fy(financials, ticker, "FY26")
    cfg = assumptions["companies"][ticker]
    shares = float(base["shares_cr"])
    tax_rate = float(cfg["tax_rate"])

    rows: list[dict[str, Any]] = []
    revenue_prior = float(base["revenue"])
    for index in range(assumptions["valuation"]["forecast_years"]):
        growth = float(cfg["revenue_growth"][index]) + growth_shift
        revenue = revenue_prior * (1 + growth)
        margin = float(cfg["ebitda_margin"][index]) + margin_shift
        ebitda = revenue * margin
        depreciation = revenue * float(cfg["dep_pct_revenue"])
        ebit = ebitda - depreciation
        other_income = float(cfg["other_income"][index])
        interest = float(cfg["interest"][index])
        pbt = ebit + other_income - interest
        tax = pbt * tax_rate
        pat = pbt - tax
        eps = pat / shares

        delta_revenue = revenue - revenue_prior
        delta_nwc = float(cfg["nwc_pct_incremental_revenue"]) * delta_revenue
        cfo = pat + depreciation - delta_nwc
        capex = revenue * float(cfg["capex_pct_revenue"])
        fcf = cfo - capex
        dividends = pat * float(cfg["dividend_payout"])

        rows.append(
            {
                "ticker": ticker,
                "fiscal_year": f"FY{27 + index}",
                "year_index": index + 1,
                "revenue": revenue,
                "revenue_growth_pct": growth * 100,
                "ebitda": ebitda,
                "ebitda_margin_pct": margin * 100,
                "depreciation": depreciation,
                "ebit": ebit,
                "other_income": other_income,
                "interest": interest,
                "pbt": pbt,
                "tax": tax,
                "pat": pat,
                "eps": eps,
                "cfo": cfo,
                "capex": capex,
                "fcf": fcf,
                "dividends": dividends,
                "shares_cr": shares,
                "delta_nwc": delta_nwc,
            }
        )
        revenue_prior = revenue
    return pd.DataFrame(rows)


def forecast_all(financials: pd.DataFrame, assumptions: dict[str, Any]) -> pd.DataFrame:
    frames = [
        forecast_company(ticker, financials, assumptions)
        for ticker in ("BSE", "CDSL", "CAMS", "KFINTECH")
    ]
    return pd.concat(frames, ignore_index=True)


def relative_valuation_table(
    financials: pd.DataFrame,
    market: pd.DataFrame,
    forecasts: pd.DataFrame,
    assumptions: dict[str, Any],
) -> pd.DataFrame:
    """Trailing and forward multiples on a common date and share count."""

    rows: list[dict[str, Any]] = []
    for ticker in ("BSE", "CDSL", "CAMS", "KFINTECH"):
        base = company_fy(financials, ticker, "FY26")
        prior = company_fy(financials, ticker, "FY25")
        mkt = market.loc[ticker]
        company_forecast = forecasts[forecasts["ticker"] == ticker].reset_index(drop=True)
        fy27 = company_forecast.iloc[0]
        fy28 = company_forecast.iloc[1]
        fy29 = company_forecast.iloc[2]

        eps_cagr = (fy29["eps"] / base["eps"]) ** (1 / 3) - 1
        revenue_cagr = (fy29["revenue"] / base["revenue"]) ** (1 / 3) - 1
        pe_fy27 = mkt["price_inr"] / fy27["eps"]
        target_base = fy28["eps"] * assumptions["companies"][ticker]["base_target_pe"]

        rows.append(
            {
                "ticker": ticker,
                "company": base["company"],
                "price_inr": mkt["price_inr"],
                "market_cap_cr": mkt["market_cap_cr"],
                "ev_cr": mkt["ev_cr"],
                "net_cash_cr": mkt["net_cash_cr"],
                "revenue_fy26": base["revenue"],
                "ebitda_fy26": base["ebitda"],
                "pat_fy26": base["pat"],
                "eps_fy26": base["eps"],
                "eps_ttm": mkt["ttm_eps"],
                "eps_fy27e": fy27["eps"],
                "eps_fy28e": fy28["eps"],
                "eps_fy29e": fy29["eps"],
                "eps_cagr_fy26_fy29_pct": eps_cagr * 100,
                "revenue_cagr_fy26_fy29_pct": revenue_cagr * 100,
                "ebitda_margin_fy26_pct": base["ebitda"] / base["revenue"] * 100,
                "roe_fy26_pct": base["pat"] / ((base["equity"] + prior["equity"]) / 2) * 100,
                "roce_fy26_pct": base["ebit"] / (base["equity"] + base["total_debt"]) * 100,
                "fcf_fy26": base["fcf"],
                "pe_fy26": mkt["price_inr"] / base["eps"],
                "pe_ttm": mkt["price_inr"] / mkt["ttm_eps"],
                "pe_fy27e": pe_fy27,
                "pe_fy28e": mkt["price_inr"] / fy28["eps"],
                "ev_ebitda_fy26": mkt["ev_cr"] / base["ebitda"],
                "ev_ebit_fy26": mkt["ev_cr"] / base["ebit"],
                "p_fcf_fy26": mkt["market_cap_cr"] / base["fcf"],
                "fcf_yield_fy26_pct": base["fcf"] / mkt["market_cap_cr"] * 100,
                "peg_fy27e": pe_fy27 / (eps_cagr * 100),
                "target_pe_base": assumptions["companies"][ticker]["base_target_pe"],
                "target_price_base_relative": target_base,
                "upside_base_relative_pct": (target_base / mkt["price_inr"] - 1) * 100,
            }
        )
    return pd.DataFrame(rows)
