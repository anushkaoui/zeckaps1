# Final Quality Gate

**Decision:** BUY CAMS | **Target:** ₹800 | **Current:** ₹697 | **Total return:** +16.6% | **Position:** 4% of ₹500 crore

| # | Requirement | Evidence | Status |
|---|---|---|---|
| 1 | One winner, 12-month target, dated upside/downside | `reports/decision_report.md`, `outputs/valuation_summary.csv` | PASS |
| 2 | Industry value chain, licences, switching costs, network effects, concentration, pricing, moat durability | `reports/industry_report.md`, company notes | PASS |
| 3 | SEBI F&O curbs: measures, dates, amendments, implementation, direct/second-order effects | `research/regulatory_timeline.md`, `reports/scenario_report.md` | PASS |
| 4 | Comparative P/E and EV/EBITDA with growth and return on capital | `reports/company_comparison.md`, `outputs/comparable_valuation.csv` | PASS |
| 5 | Three-statement-linked DCF/integrated model for winner | `model/three_statement.py`, `model/dcf.py`, `outputs/cams_three_statement.csv`, `outputs/cams_dcf_schedule.csv` | PASS |
| 6 | Revenue drivers, margins, tax, WC, capex, FCF, discount rate, terminal value, net cash/debt, diluted shares, EV bridge, target | `reports/valuation_report.md` | PASS |
| 7 | Concentration, mix, related party, cash conversion, capitalisation, contingents, governance, accounting judgements | `reports/due_diligence.md` | PASS with open items |
| 8 | Bull/base/bear for all four | `reports/scenario_report.md`, `outputs/scenario_results.csv` | PASS |
| 9 | Mandatory −30% derivatives and −20% equity shocks, separate and joint | `outputs/shock_results.csv`, `reports/scenario_report.md` | PASS |
| 10 | Stress translation into revenue, EBITDA, PAT, FCF, valuation, target | `outputs/shock_results.csv` | PASS |
| 11 | Sensitivity and downside from CMP | `outputs/sensitivity_dcf.csv`, `outputs/sensitivity_target.csv`, `outputs/tornado.csv` | PASS |
| 12 | Winner, target, upside/downside, deployment, sizing, entry, catalysts, risks, exactly three triggers | `reports/decision_report.md` | PASS |
| 13 | Rejection reasons for the other three, strongest case first | `reports/decision_report.md` | PASS |
| 14 | Two-page IC memo | `reports/investment_committee_memo.md` | PASS |
| 15 | Reproducibility, assumptions separated, source manifest, tests | `README.md`, `config/assumptions.yaml`, `research/assumptions_register.csv`, `research/source_manifest.csv`, `tests/test_model.py` | PASS |
| 16 | Data-quality/accounting checks | `outputs/model_checks.txt` (135 checks, 0 failures) | PASS |
| 17 | Adversarial review and second valuation | `reports/adversarial_review.md` | PASS |
| 18 | Disclosed limitations | `README.md`, `reports/due_diligence.md`, source manifest | PASS with open items |
| 19 | Independent red-team audit | `reports/red_team_audit.md` | PASS |

## Automated checks

- `python3 -m unittest discover -s tests -v`: 11 tests, all pass.
- `python3 -m model.run_all`: completes; 135 data/accounting checks, 0 failures.
- CAMS balance sheet: zero check in all five years.
- CAMS cash roll: zero check in all five years.
- CAMS simplified FCF is within 2% of the linked three-statement FCF; BSE forecast other income is anchored to the normalized FY26 line.
- Scenario probabilities sum to 1; expected values recomputed.
- Portfolio: 2,86,944 shares for ₹20 crore; total value 19.9999 crore; cap 25 crore.

## Open items (disclosed, do not invalidate the decision)

1. **PDF statement:** the uploaded PDF could not be parsed; the inline mandate is authoritative. PDF-only requirements may be missing.
2. **CAMS Q2 FY27:** results were scheduled 29/30 October 2026; not available at the cut-off. The position is staged so Q2 is a gate.
3. **BSE revenue definition:** Q1 FY27 company presentation vs Screener differ, and FY26 media-release total revenue/operating EBITDA differ from the normalized Screener line; flagged, not resolved. BSE is rejected regardless.
4. **Annual-report notes:** RPT, contingent liabilities, leases, auditor qualifications were not line-by-line verified. Flagged as diligence items.
5. **ADV:** the ₹50 crore ADV is a planning assumption. Verify before execution.
6. **CDSL revenue mix:** approximate from disclosed categories.
7. **Net cash haircuts:** BSE/CDSL/KFin balances include restricted/regulatory amounts; haircuts are judgemental.

## Final decision

The model, scenarios and adversarial review support **BUY CAMS**, target **₹800**, 4% position, built in three tranches. The thesis survives the hostile review but with moderate conviction: the DCF is close to the current price, and the target relies on a modest forward-multiple re-rating. The three exit triggers are measurable and tied to the thesis.
