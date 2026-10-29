# Zeckathon Equity Research Challenge — Requirements Register

**Mandate:** Select exactly one of BSE Ltd, CDSL, CAMS, KFin Technologies for a ₹500 crore, 12-month, long-only deployment; provide a dated 12-month target price, expected return, deployment plan, and a two-page IC memo.

**Research cut-off:** 29 October 2026, 16:00 IST (market close). Latest audited period: FY2025-26 (year ended 31 March 2026). Latest quarterly period used: Q1 FY2026-27 (quarter ended 30 June 2026) except KFin, where Q2 FY2026-27 (30 September 2026) is used. CAMS Q2 FY2026-27 was scheduled for 29 October 2026 and is treated as not yet available in the base model.

**Source of requirements:** The uploaded PDF could not be parsed by this model ("does not support PDF input"). The full inline master prompt in the user message is treated as the binding statement. Page references below are therefore to the inline prompt sections, not PDF pages. This limitation is disclosed in the final report.

**Status legend:** Complete = artifact exists and validated; In progress = being built; Gap = evidence unavailable, workaround documented.

| ID | Requirement (faithful paraphrase) | Required evidence / calculation | Expected output | Dependencies | Validation method | Status | Prompt ref |
|---|---|---|---|---|---|---|---|
| R-01 | Name exactly one winner among BSE, CDSL, CAMS, KFin for 12 months | Common-date comparison of moat, growth, valuation, risk, downside | Winner + investment thesis | R-04 to R-24 | Decision matrix + scenario returns | In progress | §1, §8 |
| R-02 | Provide defensible 12-month target price and implied upside/downside from dated price | Dated price, forecast EPS/CF, target multiple/DCF, dividend treatment | TP, % price return, % total return | R-21, R-27, R-31, R-32 | Recompute return from raw inputs | In progress | §1, §9.8 |
| R-03 | Address five mandatory workstreams: industry, valuation, due diligence, scenarios, decision/memo | Five linked reports | Reports 3–13 | R-04 to R-42 | Requirement matrix cross-check | In progress | §1 |
| R-04 | Map industry value chain for exchanges, depositories, MF RTAs, issuer services | Who pays whom, revenue activity, regulator, beneficiary | Value-chain diagram + narrative | Company disclosures, SEBI, AMFI | Cross-check against segment revenue | In progress | §5.1 |
| R-05 | Assess licences, barriers, network effects, switching costs, scale, concentration, pricing power | Quantified market shares, retention, volumes, fee constraints | Moat matrix per company | R-04, R-09 | Source each market-share metric | In progress | §5.2 |
| R-06 | Distinguish true network effects from volume/installed-base benefits; distinguish regulatory access from profit protection | Evidence-based moat assessment | Moat durability scores | R-05 | Adversarial review | In progress | §5.2 |
| R-07 | Build revenue driver tree for each company using disclosed categories | Segment revenue, volume/activity, yield/pricing | Driver trees + historical driver table | Annual reports, Q1/Q2 FY27 filings | Revenue build reconciles to reported FY26 | In progress | §5.3 |
| R-08 | Research SEBI F&O curbs: measures, dates, amendments, implementation status | Primary SEBI circulars, exchange circulars | Regulatory timeline | SEBI, NSE/BSE circulars | Effective-date cross-check | Complete | §5.4 |
| R-09 | Model direct and second-order effects of F&O curbs and fee rationalisation | Volume and pricing effects by company; offsets | Scenario transmission tables | R-08, R-33 | Driver-level propagation | In progress | §5.4, §10.3 |
| R-10 | Build comparative industry conclusion and falsifiable thesis per company | Moat, growth visibility, regulation, operating leverage, concentration, pricing | Comparison matrix + 4 theses | R-04 to R-09 | Thesis must specify falsifiers | In progress | §5.5 |
| R-11 | Normalize 3–5 years of historical financials for all four | Revenue, EBITDA, EBIT, PAT, OCF, capex, FCF, cash, debt, shares, EPS, dividends, ROE/ROIC | `normalized_financials.csv` | Audited accounts / Screener aggregation | Accounting identities; source reconciliation | In progress | §4.2, §6.1 |
| R-12 | Analyze growth, margins, cash conversion, returns, capex, working capital, payout | Ratios and drivers, adjusted for splits/acquisitions | Financial comparison report | R-11 | Formula tests | In progress | §6.1 |
| R-13 | Analyze revenue concentration, customer/product mix, domestic/international | Segment mix, client concentration disclosures | Concentration section | Annual reports, investor decks | No fabricated customer data | In progress | §6.2 |
| R-14 | Forensic review: earnings vs OCF, other income, receivables, capitalisation, exceptional items, RPT, contingents, auditor, governance | Disclosure-by-disclosure findings with materiality | Due diligence report | Annual reports, filings | Source citation per finding | In progress | §6.3 |
| R-15 | Reconcile PAT to OCF and OCF to FCF; define capex precisely | Bridge with non-cash and working-capital items | Reconciliation tables | Cash-flow statements | Identity checks | In progress | §6.4 |
| R-16 | Common-date market cap and EV for all four | Price, diluted shares, debt, cash, investments, leases, minorities | `comparable_valuation.csv` | Dated prices, FY26 balance sheets | EV bridge test | In progress | §7.1 |
| R-17 | Calculate trailing/forward P/E, EV/EBITDA, EV/EBIT, P/FCF, FCF yield, PEG | Consistent definitions and periods | Multiples table | R-11, R-16, forecasts | Unit and definition check | In progress | §7.2 |
| R-18 | Compare multiples with growth, margins, ROIC, cash conversion, durability, regulation | Explain premium/discount | Relative valuation conclusion | R-12, R-17 | Cross-check with DCF | In progress | §7.3–7.4 |
| R-19 | Select provisional winner only after comparison | Weighted criteria with justified weights, sensitivity | Decision matrix + weight-sensitivity | R-18 | Change weights ±10 pts; test winner stability | In progress | §8 |
| R-20 | Build 5-year three-statement model for winner | P&L, balance sheet, cash flow, checks | `three_statement_model.py` + outputs | R-07, assumptions | BS balances; cash reconciles; CF ties | In progress | §9 |
| R-21 | Forecast revenue by segment and operating driver | Volume × yield / AUM × bps / transactions × fee | Segment forecast table | Company disclosures | Historical back-test | In progress | §9.2 |
| R-22 | Forecast P&L, balance sheet, cash flow with links | Margins, tax, working capital, capex, dividends | Linked statements | R-20, R-21 | Accounting identities | In progress | §9.3–9.5 |
| R-23 | Build DCF: FCFF, WACC, terminal value, EV-to-equity bridge, diluted shares | Transparent formulas and assumptions | `dcf.py`, valuation output | R-20 | Recompute independently | In progress | §9.6 |
| R-24 | Cross-check DCF with earnings-based valuation; reconcile target | Target multiple, peer rationale | Valuation reconciliation | R-17, R-23 | Two-method reconciliation | In progress | §9.7 |
| R-25 | Derive 12-month target from model; distinguish CMP, intrinsic value, 12-month value, return; handle dividends | Roll-forward bridge | Target price section | R-23, R-24 | Return formula test | In progress | §9.8 |
| R-26 | Bull/base/bear for all four; winner gets integrated stress test | Scenario assumptions and outputs | `scenario_results.csv` | R-20, R-21 | Probability sum; driver propagation | In progress | §10.1–10.3 |
| R-27 | Model 30% fall in derivatives turnover independently | Map to BSE derivatives revenue; CDSL/KFin/CAMS transmission | Shock table | R-09, R-26 | Revenue bridge from disclosed mix | In progress | §10.3 |
| R-28 | Model 20% equity-market drawdown independently | Map to AUM, volumes, demat activity, account growth | Shock table | R-26 | Separate from F&O shock | In progress | §10.3 |
| R-29 | Model joint adverse case where appropriate | Combined shocks and second-order effects | Bear case | R-27, R-28 | No mechanical application | In progress | §10.3 |
| R-30 | Assign bull/base/bear probabilities, compute probability-weighted price and total return | Explicit justification; probabilities sum to 100% | Expected return table | R-26 | Sum check | In progress | §10.4 |
| R-31 | Sensitivity: revenue growth, margin, WACC, terminal growth, multiple, fee realization, volumes, net cash, share count | Model-generated tables and tornado | `sensitivity_tables.csv` | R-20, R-23 | Monotonicity checks | In progress | §10.5 |
| R-32 | ₹500 crore deployment: position size, staging, entry discipline, margin of safety, liquidity/impact, concentration | ADV, free float, ownership limits, staged triggers | Deployment plan | R-02, market data | Liquidity calculation | In progress | §11 |
| R-33 | Catalysts and exactly three measurable exit/thesis-review triggers | Event calendar, metrics, thresholds | Catalyst table + 3 triggers | Thesis, model | Each trigger measurable | In progress | §12 |
| R-34 | Reject other three with strongest case first; state what would change ranking | Evidence-based rejection analysis | Rejection section | R-18, R-26 | No straw men | In progress | §13 |
| R-35 | Two-page IC memo, decision-oriented and consistent with model | Concise memo | `investment_committee_memo.md` | All | Cross-check numbers to outputs | In progress | §16 D13 |
| R-36 | Reproducible project: code, assumptions, sources, outputs, tests, docs | Modular code; assumptions separated; run command | Repo artifacts | All | Execute tests; rebuild outputs | In progress | §14 |
| R-37 | Source manifest with title, publisher, date, period, URL, access date, page/section, input supported | Source-by-source provenance | `source_manifest.csv` | Research | Coverage check | In progress | §2.2, §4.1 |
| R-38 | Data-quality checks: missing, duplicates, units, fiscal mismatch, signs, shares, corporate actions, stale prices | Automated checks and report | `model_checks.txt` | R-11 | Tests fail visibly on missing inputs | In progress | §4.3 |
| R-39 | Adversarial IC review; second independent valuation path; revise if thesis fails | Challenge log and response | `adversarial_review.md` | Model | Independent recomputation | In progress | §15 |
| R-40 | Final quality gate: all requirements, dates, provenance, reconciliations, scenarios, deployment, triggers, rejections, memo | Checklist with evidence | Quality-gate section | All | Manual + automated | Pending | §19 |
| R-41 | Disclose data gaps and limitations; do not fabricate | Gap register with impact | Limitations section | Research | Cross-check | In progress | §2.2–2.5 |
| R-42 | Explain methodology, alternatives, uncertainties, validation, decision impact | Accessible explanations and equations | Reports | All | Read-through | In progress | §17 |

## Explicit mandatory items A–L from §3

| Item | Requirement | Mapped IDs | Status |
|---|---|---|---|
| A | Industry structure, value chain, licences, switching costs, network effects, concentration, threats, pricing power, moat durability | R-04–R-10 | In progress |
| B | Direct and second-order effects of SEBI F&O curbs and fee rationalisation | R-08, R-09, R-27–R-29 | In progress |
| C | Comparable P/E and EV/EBITDA for all four with growth and return-on-capital | R-16–R-18 | In progress |
| D | Three-statement-linked DCF/integrated model for winner | R-20–R-25 | In progress |
| E | Revenue drivers, margins, taxes, WC, capex, FCF, discount rate, terminal value, net cash/debt, diluted shares, EV bridge, TP | R-20–R-25 | In progress |
| F | Concentration, mix, RPT, cash conversion, capitalisation, contingents, governance, accounting judgements | R-13–R-15 | In progress |
| G | Bull/base/bear incl. 30% derivatives fall and 20% equity drawdown | R-26–R-29 | In progress |
| H | Stress translation into revenue, margins, earnings, cash flow, valuation, TP | R-27–R-29 | In progress |
| I | Sensitivity and downside from CMP | R-31 | In progress |
| J | Winner, TP, upside/downside, ₹500 cr deployment, sizing, entry, catalysts, risks, exactly three triggers, rejection reasons | R-01, R-02, R-32–R-34 | In progress |
| K | Two-page IC memo | R-35 | In progress |
| L | Model integrity, evidence traceability, credible bear case, cross-examination readiness | R-36–R-41 | In progress |

## Open data gaps (to be updated)

1. **CAMS Q2 FY2026-27 results** were scheduled 29 October 2026; the model uses Q1 FY2026-27 and management's FY27 guidance. This is a timing gap, not a missing historical fact.
2. **BSE consolidated cash** includes clearing-corporation/settlement balances. The model uses a haircut to attributable net cash and discloses the treatment. Exact split requires the FY26 annual report notes.
3. **CDSL and KFin cash/investment liquidity** include regulatory/operating balances. A haircut is applied; exact restricted balances require annual-report notes.
4. **Customer-level concentration** is not uniformly disclosed. The report uses segment concentration and disclosed client counts, not fabricated customer percentages.
5. **PDF problem statement** could not be parsed; the inline prompt is authoritative. If the PDF contains extra requirements, they are not captured.

## Status update — 29 October 2026

All requirement rows are now evidenced in the repository. The initial register statuses are retained above as the planning baseline; the final status is below.

| Requirement group | Final status | Primary evidence |
|---|---|---|
| R-01 to R-03 (mandate, target, five workstreams) | Complete | `reports/decision_report.md`, `reports/investment_committee_memo.md`, `reports/valuation_report.md` |
| R-04 to R-10 (industry, moats, drivers, regulation, conclusion) | Complete | `reports/industry_report.md`, `research/regulatory_timeline.md`, `research/company_notes/` |
| R-11 to R-18 (financials, ratios, diligence, comparables) | Complete with open diligence items | `data/processed/company_financials.csv`, `reports/due_diligence.md`, `outputs/comparable_valuation.csv` |
| R-19 to R-25 (winner, model, DCF, target) | Complete | `model/three_statement.py`, `model/dcf.py`, `outputs/cams_three_statement.csv`, `reports/valuation_report.md` |
| R-26 to R-31 (scenarios, shocks, sensitivities) | Complete | `outputs/scenario_results.csv`, `outputs/shock_results.csv`, `outputs/sensitivity_dcf.csv`, `outputs/tornado.csv` |
| R-32 to R-35 (deployment, triggers, rejections, memo) | Complete | `reports/decision_report.md`, `reports/investment_committee_memo.md`, `outputs/portfolio_plan.csv` |
| R-36 to R-42 (reproducibility, sources, checks, adversarial review, quality gate, limitations) | Complete | `README.md`, `research/source_manifest.csv`, `outputs/model_checks.txt`, `reports/adversarial_review.md`, `reports/red_team_audit.md`, `reports/quality_gate.md` |

**Final decision:** BUY CAMS, 12-month target ₹800, 4% of the ₹500 crore sleeve, three tranches, exactly three exit triggers.

**Remaining open items:** PDF could not be parsed; CAMS Q2 FY27 not available at cut-off; BSE Q1 FY27/FY26 revenue-definition conflict; annual-report note-level verification; ADV verification; restricted-cash split for BSE/CDSL/KFin.
