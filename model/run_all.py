"""Run the full Zeckathon valuation workflow and write all outputs."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from .data_loader import (
    ROOT,
    checks_frame,
    load_assumptions,
    load_financials,
    load_market,
    validate_data,
)
from .dcf import cost_of_capital, dcf_sensitivity, dcf_valuation
from .decision import decision_matrix, weight_sensitivity
from .portfolio import deployment_plan
from .relative_valuation import forecast_all, relative_valuation_table
from .scenarios import expected_value_table, scenario_table, shock_table
from .sensitivity import target_sensitivity_grid, tornado_table
from .three_statement import build_cams_model

OUTPUTS = ROOT / "outputs"


def _round_target(value: float, step: float = 5.0) -> float:
    return round(value / step) * step


def main() -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)

    assumptions = load_assumptions()
    financials = load_financials()
    market = load_market()

    checks = checks_frame(validate_data(financials, market, assumptions))
    failures = checks[checks["status"] == "FAIL"]
    checks.to_csv(OUTPUTS / "data_checks.csv", index=False)
    with open(OUTPUTS / "model_checks.txt", "w", encoding="utf-8") as handle:
        handle.write("ZECKATHON MODEL CHECKS\n")
        handle.write("=" * 72 + "\n")
        handle.write(checks.to_string(index=False))
        handle.write(f"\n\nTotal checks: {len(checks)}; failures: {len(failures)}\n")
    if len(failures):
        raise SystemExit("Data checks failed; see outputs/model_checks.txt")

    forecasts = forecast_all(financials, assumptions)
    forecasts.to_csv(OUTPUTS / "forecast_summary.csv", index=False)

    comps = relative_valuation_table(financials, market, forecasts, assumptions)
    comps.to_csv(OUTPUTS / "comparable_valuation.csv", index=False)

    cams_model = build_cams_model(financials, assumptions)
    cams_model.to_csv(OUTPUTS / "cams_three_statement.csv", index=False)

    dcf_summary, dcf_schedule = dcf_valuation(financials, market, assumptions)
    dcf_schedule.to_csv(OUTPUTS / "cams_dcf_schedule.csv", index=False)
    with open(OUTPUTS / "cost_of_capital.json", "w", encoding="utf-8") as handle:
        json.dump(cost_of_capital(assumptions), handle, indent=2)

    dcf_grid = dcf_sensitivity(financials, market, assumptions)
    dcf_grid.to_csv(OUTPUTS / "sensitivity_dcf.csv", index=False)

    target_grid = target_sensitivity_grid(financials, market, assumptions)
    target_grid.to_csv(OUTPUTS / "sensitivity_target.csv", index=False)

    tornado = tornado_table(financials, market, assumptions)
    tornado.to_csv(OUTPUTS / "tornado.csv", index=False)

    scenarios = scenario_table(financials, market, assumptions)
    scenarios.to_csv(OUTPUTS / "scenario_results.csv", index=False)

    expected = expected_value_table(scenarios)
    expected.to_csv(OUTPUTS / "expected_returns.csv", index=False)

    shocks = shock_table(financials, market, assumptions)
    shocks.to_csv(OUTPUTS / "shock_results.csv", index=False)

    decision = decision_matrix(assumptions, expected)
    decision.to_csv(OUTPUTS / "decision_matrix.csv", index=False)

    weights = weight_sensitivity(assumptions)
    weights.to_csv(OUTPUTS / "weight_sensitivity.csv", index=False)

    plan = deployment_plan(market, assumptions, ticker="CAMS")
    plan.to_csv(OUTPUTS / "portfolio_plan.csv", index=False)

    cams_comp = comps.set_index("ticker").loc["CAMS"]
    relative_target = float(cams_comp["target_price_base_relative"])
    dcf_value = float(dcf_summary["dcf_value_per_share"])
    weight_relative = float(assumptions["valuation"]["blend_weight_relative"])
    blended_raw = weight_relative * relative_target + (1 - weight_relative) * dcf_value
    official_target = _round_target(blended_raw, 5)
    current = float(market.loc["CAMS", "price_inr"])
    dividend_yield = float(market.loc["CAMS", "dividend_yield_pct"])
    expected_row = expected.set_index("ticker").loc["CAMS"]

    summary_rows = []
    for _, row in comps.iterrows():
        ticker = row["ticker"]
        if ticker == "CAMS":
            target = official_target
            dcf_target = dcf_value
            target_method = "75% forward P/E, 25% DCF, rounded"
        else:
            target = _round_target(float(row["target_price_base_relative"]), 5)
            dcf_target = None
            target_method = "Forward P/E cross-check"
        price = float(row["price_inr"])
        expected_total = float(expected.set_index("ticker").loc[ticker, "expected_total_return_pct"])
        summary_rows.append(
            {
                "ticker": ticker,
                "company": row["company"],
                "current_price_inr": price,
                "relative_target_inr": float(row["target_price_base_relative"]),
                "dcf_target_inr": dcf_target,
                "official_target_inr": target,
                "price_upside_pct": (target / price - 1) * 100,
                "dividend_yield_pct": float(market.loc[ticker, "dividend_yield_pct"]),
                "total_return_pct": (target / price - 1) * 100
                + float(market.loc[ticker, "dividend_yield_pct"]),
                "expected_total_return_pct": expected_total,
                "bear_downside_pct": float(expected.set_index("ticker").loc[ticker, "bear_downside_pct"]),
                "bull_upside_pct": float(expected.set_index("ticker").loc[ticker, "bull_upside_pct"]),
                "target_method": target_method,
                "recommendation": "BUY" if ticker == "CAMS" else "REJECT",
            }
        )
    valuation_summary = pd.DataFrame(summary_rows).sort_values(
        "expected_total_return_pct", ascending=False
    )
    valuation_summary.to_csv(OUTPUTS / "valuation_summary.csv", index=False)

    metadata = {
        "winner": "CAMS",
        "current_price_inr": current,
        "relative_target_inr": relative_target,
        "dcf_target_inr": dcf_value,
        "blended_target_raw_inr": blended_raw,
        "official_target_inr": official_target,
        "price_upside_pct": (official_target / current - 1) * 100,
        "total_return_pct": (official_target / current - 1) * 100 + dividend_yield,
        "expected_total_return_pct": float(expected_row["expected_total_return_pct"]),
        "bear_target_inr": float(expected_row["bear_target_price"]),
        "bull_target_inr": float(expected_row["bull_target_price"]),
        "dcf": dcf_summary,
        "cost_of_capital": cost_of_capital(assumptions),
        "decision_winner": decision.iloc[0]["ticker"],
        "decision_winner_score": float(decision.iloc[0]["weighted_score"]),
    }
    with open(OUTPUTS / "valuation_summary.json", "w", encoding="utf-8") as handle:
        json.dump(metadata, handle, indent=2, default=float)

    print("Winner:", metadata["winner"])
    print(f"Current: ₹{current:,.0f} | Relative: ₹{relative_target:,.0f} | DCF: ₹{dcf_value:,.0f}")
    print(
        f"Target: ₹{official_target:,.0f} | Price upside: {metadata['price_upside_pct']:.1f}% "
        f"| Total return: {metadata['total_return_pct']:.1f}%"
    )
    print(f"Expected total return: {metadata['expected_total_return_pct']:.1f}%")
    print(f"Decision score: {metadata['decision_winner']} {metadata['decision_winner_score']:.2f}")
    print("\nValuation summary:")
    print(
        valuation_summary[
            [
                "ticker",
                "current_price_inr",
                "official_target_inr",
                "total_return_pct",
                "expected_total_return_pct",
                "recommendation",
            ]
        ].to_string(index=False)
    )
    print("\nOutputs written to", OUTPUTS)


if __name__ == "__main__":
    main()
