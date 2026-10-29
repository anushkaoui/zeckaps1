# Zeckathon Equity Research Challenge — CAMS

**Winner:** Computer Age Management Services (CAMS) | **Price (29 Oct 2026):** ₹697 | **12-month target:** ₹800 | **Upside:** +14.8% price, +16.6% total | **Position:** 4% of ₹500 crore sleeve

## What this repository contains

A reproducible, source-tagged valuation of BSE, CDSL, CAMS and KFin, with a full three-statement model and DCF for the winner, scenario/stress testing, sensitivity analysis, deployment plan and a two-page IC memo.

## Quick start

```bash
python3 -m model.run_all
python3 -m unittest discover -s tests -v
```

`model.run_all` writes all CSV/JSON outputs to `outputs/` and rebuilds the model checks. The tests validate data bridges, accounting identities, DCF, scenarios, shocks, position sizing and the decision.

## Key outputs

| File | Content |
|---|---|
| `reports/investment_committee_memo.md` | Two-page IC memo |
| `reports/decision_report.md` | Winner, deployment, three triggers, rejections |
| `reports/valuation_report.md` | CAMS relative valuation, DCF, sensitivity, target bridge |
| `reports/scenario_report.md` | Bull/base/bear and mandatory shocks for all four |
| `reports/company_comparison.md` | Comparative matrix and decision scores |
| `reports/industry_report.md` | Value chain, moats, growth, regulation |
| `reports/due_diligence.md` | Earnings quality, concentration, governance, open items |
| `reports/adversarial_review.md` | Hostile review and second valuation |
| `reports/red_team_audit.md` | Independent audit, corrections and residual open items |
| `research/regulatory_timeline.md` | SEBI F&O/fee timeline and implications |
| `research/company_notes/*.md` | Company-level theses and falsifiers |
| `research/source_manifest.csv` | Source IDs, URLs, dates and usage |
| `research/assumptions_register.csv` | 46 model inputs with basis, source, status |
| `outputs/comparable_valuation.csv` | Common-date multiples for all four |
| `outputs/scenario_results.csv` | Bull/base/bear targets and returns |
| `outputs/shock_results.csv` | −30% derivatives / −20% equity / joint shocks |
| `outputs/sensitivity_dcf.csv` | WACC × terminal-growth grid |
| `outputs/sensitivity_target.csv` | Target P/E × EPS grid |
| `outputs/tornado.csv` | Target drivers ranked by swing |
| `outputs/cams_three_statement.csv` | CAMS P&L, balance sheet, cash flow |
| `outputs/cams_dcf_schedule.csv` | Explicit FCFF and terminal value |
| `outputs/decision_matrix.csv` | Weighted scores and ranks |
| `outputs/weight_sensitivity.csv` | Winner stability under ±10 pp weights |
| `outputs/portfolio_plan.csv` | Tranches, shares, liquidity gate |
| `outputs/valuation_summary.csv` | Final targets and returns |
| `outputs/model_checks.txt` | Data and accounting checks |

## Project structure

```text
config/assumptions.yaml          # all model assumptions and scenario settings
data/processed/                  # normalized financials, market data, quarterly data
model/                           # data loader, relative valuation, 3-statement, DCF,
                                 # scenarios, sensitivity, decision, portfolio, runner
research/                        # source manifest, regulatory timeline, company notes
reports/                         # industry, comparison, diligence, valuation, scenarios,
                                 # decision, adversarial review, IC memo
tests/                           # automated unit/integration checks
outputs/                         # generated tables and checks
```

## Key assumptions

- Prices as of 29 October 2026; FY26 audited financials; Q1 FY27 for BSE/CDSL/CAMS, Q2 FY27 for KFin.
- CAMS 12-month target = 75% relative value (33x FY28E EPS ₹25.17 = ₹831) + 25% DCF (₹712); rounded to ₹800.
- DCF: 10.0% WACC (formula 10.07%), 6.0% terminal growth, five-year explicit forecast plus five-year fade.
- Scenario probabilities: 25% bull / 50% base / 25% bear.
- Mandatory shocks: −30% derivatives turnover and −20% equity drawdown, modelled separately and jointly.
- Net cash for BSE/CDSL/KFin is haircut for clearing/regulatory/client balances; CAMS uses reported cash less debt.
- Exactly three exit triggers: share loss below 63%, binding fee cap >10% revenue hit, or valuation/earnings break.

## Key results

| Company | Current | Official target | Official total return | Expected total return | Bear downside |
|---|---:|---:|---:|---:|---:|
| **CAMS** | ₹697 | ₹800 | +16.6% | **+15.2%** | −23.6% |
| KFin | ₹860 | ₹935 | +10.1% | +10.3% | −37.8% |
| BSE | ₹3,502 | ₹3,460 | −0.9% | −5.0% | −51.9% |
| CDSL | ₹1,282 | ₹1,190 | −6.2% | −6.0% | −44.9% |

## Data caveats

1. The uploaded PDF `fe8ab0853d2c40d5b5fd953578dd6f8c.pdf` could not be parsed by the model. The inline master prompt is treated as the binding mandate; PDF-only requirements may be missing.
2. CAMS Q2 FY27 results were scheduled for 29/30 October 2026 and were not available at the cut-off. The model uses Q1 FY27 and management guidance.
3. BSE's Q1 FY27 investor presentation reports ₹1,706.8 crore revenue and ₹1,186.7 crore EBITDA versus Screener's ₹1,566 crore/₹1,046 crore; the difference is flagged and not resolved. BSE's FY26 media release reports ₹5,148 crore total revenue and ₹3,079 crore operating EBITDA, versus ₹5,124 crore/₹3,480 crore normalized from Screener; the ₹290–400 crore gap is a classification difference, not a restatement.
4. CDSL's revenue mix is approximated from disclosed categories. BSE/CDSL/KFin net cash includes haircuts for restricted balances.
5. Annual-report related-party, contingent-liability, lease and auditor notes were not line-by-line verified; these are open diligence items.
6. The ₹50 crore ADV used for deployment is a planning assumption, not an exchange-verified figure. Verify before trading.

## Reproducibility

- Python 3.14.5, pandas 3.0.6, numpy 2.5.0, PyYAML.
- All calculations are deterministic; assumptions are separated in `config/assumptions.yaml`.
- Source IDs in data files map to `research/source_manifest.csv`.
- `tests/test_model.py` contains 11 automated checks; `outputs/model_checks.txt` contains 135 data/accounting checks with zero failures.
