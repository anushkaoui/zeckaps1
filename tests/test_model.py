"""Automated checks for the Zeckathon model."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

import pandas as pd

from model.data_loader import ROOT, load_assumptions, load_financials, load_market, validate_data
from model.dcf import dcf_valuation
from model.decision import decision_matrix, weight_sensitivity
from model.portfolio import deployment_plan
from model.relative_valuation import forecast_all, relative_valuation_table
from model.scenarios import expected_value_table, scenario_table, shock_table
from model.three_statement import build_cams_model

OUTPUTS = ROOT / "outputs"


class ZeckathonModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.assumptions = load_assumptions()
        cls.financials = load_financials()
        cls.market = load_market()
        cls.forecasts = forecast_all(cls.financials, cls.assumptions)
        cls.comps = relative_valuation_table(
            cls.financials, cls.market, cls.forecasts, cls.assumptions
        )
        cls.scenarios = scenario_table(cls.financials, cls.market, cls.assumptions)
        cls.expected = expected_value_table(cls.scenarios)
        cls.cams_model = build_cams_model(cls.financials, cls.assumptions)
        cls.dcf_summary, _ = dcf_valuation(cls.financials, cls.market, cls.assumptions)

    def test_data_checks_have_no_failures(self) -> None:
        checks = pd.DataFrame(validate_data(self.financials, self.market, self.assumptions))
        failures = checks[checks["status"] == "FAIL"]
        self.assertEqual(len(failures), 0, failures.to_string(index=False))

    def test_forecast_horizon_and_positive_eps(self) -> None:
        self.assertEqual(len(self.forecasts), 20)
        self.assertTrue(self.forecasts["eps"].gt(0).all())
        counts = self.forecasts.groupby("ticker")["fiscal_year"].count()
        self.assertTrue((counts == 5).all())

    def test_common_date_multiples(self) -> None:
        self.assertEqual(len(self.comps), 4)
        self.assertTrue(self.comps["pe_fy27e"].gt(0).all())
        self.assertTrue(self.comps["ev_ebitda_fy26"].gt(0).all())
        self.assertTrue(self.comps["peg_fy27e"].gt(0).all())
        self.assertTrue((self.comps["eps_cagr_fy26_fy29_pct"] > 0).all())

    def test_cams_balance_sheet_balances(self) -> None:
        self.assertTrue((self.cams_model["balance_sheet_check"].abs() < 1e-6).all())
        self.assertTrue((self.cams_model["cash_roll_check"].abs() < 1e-6).all())
        self.assertTrue(self.cams_model["cash_and_investments"].gt(0).all())
        self.assertTrue(self.cams_model["net_cash"].gt(0).all())

    def test_dcf_value_and_terminal_share(self) -> None:
        value = self.dcf_summary["dcf_value_per_share"]
        self.assertGreater(value, 0)
        self.assertGreater(self.dcf_summary["wacc_pct"], self.dcf_summary["terminal_growth_pct"])
        self.assertLess(self.dcf_summary["terminal_value_share_of_ev_pct"], 85)

    def test_scenario_probabilities_and_expected_value(self) -> None:
        sums = self.scenarios.groupby("ticker")["probability"].sum()
        self.assertTrue((abs(sums - 1.0) < 1e-9).all())
        for _, row in self.expected.iterrows():
            group = self.scenarios[self.scenarios["ticker"] == row["ticker"]]
            weighted = (group["target_price"] * group["probability"]).sum()
            self.assertAlmostEqual(weighted, row["expected_target_price"], places=6)

    def test_mandatory_shocks_are_separate_and_signed(self) -> None:
        shocks = shock_table(self.financials, self.market, self.assumptions)
        self.assertEqual(len(shocks), 12)
        bse_fno = shocks[
            (shocks["ticker"] == "BSE") & (shocks["case"] == "fno_minus_30pct")
        ].iloc[0]
        self.assertAlmostEqual(bse_fno["revenue_impact_pct"], -21.0, places=6)
        cams_fno = shocks[
            (shocks["ticker"] == "CAMS") & (shocks["case"] == "fno_minus_30pct")
        ].iloc[0]
        self.assertLess(abs(cams_fno["revenue_impact_pct"]), 1.0)
        self.assertTrue(shocks["shocked_pat_fy27"].gt(0).all())
        self.assertTrue(shocks["shocked_fcf_fy27"].gt(0).all())

    def test_cams_forecast_and_linked_fcf_are_consistent(self) -> None:
        forecast = self.forecasts[
            (self.forecasts["ticker"] == "CAMS") & (self.forecasts["fiscal_year"] == "FY27")
        ].iloc[0]
        linked = self.cams_model[self.cams_model["fiscal_year"] == "FY27"].iloc[0]
        gap_pct = abs(forecast["fcf"] - linked["fcf"]) / linked["fcf"]
        self.assertLess(gap_pct, 0.02)
        bse_other_income = self.forecasts[self.forecasts["ticker"] == "BSE"]["other_income"]
        self.assertTrue(bse_other_income.le(30).all())

    def test_portfolio_sizing_is_whole_shares_and_within_cap(self) -> None:
        plan = deployment_plan(self.market, self.assumptions, ticker="CAMS")
        total = plan[plan["line"] == "total"].iloc[0]
        self.assertEqual(total["shares"], 286944)
        self.assertAlmostEqual(total["actual_value_cr"], 20.0, places=2)
        risk = plan[plan["line"] == "risk_limits"].iloc[0]
        self.assertLessEqual(risk["actual_value_cr"], 25.0)

    def test_decision_and_weight_sensitivity(self) -> None:
        decision = decision_matrix(self.assumptions, self.expected)
        self.assertEqual(decision.iloc[0]["ticker"], "CAMS")
        sensitivity = weight_sensitivity(self.assumptions)
        self.assertTrue((sensitivity["winner"] == "CAMS").all())

    def test_official_target_is_between_dcf_and_relative(self) -> None:
        with open(OUTPUTS / "valuation_summary.json", "r", encoding="utf-8") as handle:
            summary = json.load(handle)
        self.assertGreaterEqual(summary["official_target_inr"], summary["dcf_target_inr"])
        self.assertLessEqual(summary["official_target_inr"], summary["relative_target_inr"])
        self.assertEqual(summary["winner"], "CAMS")


if __name__ == "__main__":
    unittest.main()
