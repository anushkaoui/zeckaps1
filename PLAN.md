# Implementation Plan

## 1. Analytical sequence

| Stage | Work | Deliverable | Gate |
|---|---|---|---|
| A | Lock mandate, cut-off, universe, currency/unit conventions, source hierarchy | `requirements_register.md`, this plan | Universe and dates fixed |
| B | Normalize FY22–FY26 financials and 29-Oct-2026 market data | `data/processed/company_financials.csv`, `market_data.csv` | Accounting identities and shares reconcile |
| C | Build industry/value-chain and regulatory evidence base | `reports/industry_report.md`, `research/regulatory_timeline.md` | Every material claim sourced |
| D | Write four falsifiable company theses; score moat, growth, financial quality, valuation, risk | `reports/company_comparison.md`, `research/company_notes/*.md` | Winner selected before detailed DCF |
| E | Build CAMS three-statement model and DCF; cross-check with multiples | `model/three_statement.py`, `model/dcf.py`, outputs | Balance sheet balances; cash reconciles; two valuation paths |
| F | Scenario all four, apply the two mandatory shocks, run sensitivities, size the position | `outputs/scenario_results.csv`, `outputs/sensitivity_tables.csv`, deployment plan | Bear case is credible and not mechanical |
| G | Adversarial review, IC memo, quality gate | `reports/adversarial_review.md`, `reports/investment_committee_memo.md` | All requirements evidenced |

## 2. Source hierarchy

1. Company audited annual reports and exchange filings.
2. Companies' investor presentations, press releases, transcripts and fact sheets.
3. SEBI, NSE, BSE, AMFI, NPCI and government primary releases.
4. Reputable financial press for corroboration only.
5. Aggregators (Screener, ETMoney, Trendlyne) for screening/cross-checks, never as the sole source for a material number.

Every model input is tagged with a `source_id` in `research/source_manifest.csv`. Where sources disagree, the model uses one consistent definition and discloses the alternative.

## 3. Unit and date conventions

- Currency: Indian rupees; flow items in ₹ crore; per-share items in ₹.
- Fiscal year: FY26 = year ended 31 March 2026.
- Market data: closing prices on 29 October 2026.
- Shares: fully diluted where disclosed; CAMS adjusted for the 10-for-2 split effective December 2025.
- EV: market cap + debt + lease liabilities + minorities − cash and liquid investments, with a disclosed haircut for restricted/regulatory balances.
- Target return: 12-month price return plus expected dividends; no buyback assumed unless announced.

## 4. Model architecture

```text
config/assumptions.yaml
        │
data/processed/*.csv ──► model/data_loader.py ──► validation
        │
        ├── model/relative_valuation.py ──► multiples, EV bridge
        ├── model/three_statement.py ─────► CAMS P&L/BS/CF FY27–FY31
        ├── model/dcf.py ─────────────────► FCFF, WACC, terminal value, TP
        ├── model/scenarios.py ───────────► bull/base/bear + shocks
        ├── model/sensitivity.py ─────────► grids and tornado
        └── model/portfolio.py ───────────► ₹500 crore deployment
        │
model/run_all.py ──► outputs/*.csv, reports/model_checks.txt
```

## 5. Winner model assumptions (initial; to be validated)

CAMS is the provisional winner. The integrated model will forecast:

- **Revenue:** split into MF asset-based, non-MF, and other. MF revenue grows with AUM and a modest fee-yield compression; non-MF grows faster off a small base.
- **AUM:** market-growth plus net-flow build, with a 20% drawdown shock in the bear case.
- **Margins:** EBITDA margin around 46–47%, with operating leverage partly offset by technology and compliance spend.
- **Tax:** 25.0–25.5% effective.
- **Capex:** ~2–3% of revenue; capitalised software treated consistently.
- **Working capital:** low, but receivables and unbilled revenue modelled.
- **Balance sheet:** net cash, lease liabilities, dividends, no material acquisitions in base case.
- **DCF:** explicit 5-year forecast plus fade; WACC built from risk-free rate, equity risk premium, beta and size/regulatory premium. Terminal growth below nominal GDP growth.
- **Target:** DCF value cross-checked against a forward P/E and EV/EBITDA framework; 12-month target rolls the valuation to the target date.

## 6. Decision framework

Weights (base case):

| Criterion | Weight | Why |
|---|---:|---|
| Moat durability | 20% | Determines terminal value and pricing power |
| Growth visibility | 20% | Primary 12-month return driver |
| Financial quality (ROIC, FCF, net cash) | 15% | Downside protection and funding independence |
| Valuation | 25% | Starting multiple drives 12-month return |
| Regulatory/execution risk | 20% | Sector-specific tail risk, especially F&O and fee regulation |

Scores are 1–5, anchored to evidence. The winner must survive a ±10 percentage-point weight sensitivity and a separate equal-weight test. If it does not, the decision is downgraded to "no position" or the ranking is explicitly labelled fragile.

## 7. Mandatory stress design

- **F&O shock:** −30% derivatives turnover. For BSE, map to transaction charges using disclosed derivatives share; for CDSL, map to transaction/clearing and KYC volumes; for CAMS, second-order AUM/volume effect; for KFin, issuer/international servicing effect.
- **Equity drawdown:** −20% market level. Map to average AUM, demat additions, IPO/issuer activity, and transaction volumes, with a lag.
- **Joint case:** apply both only where transmission is economically linked; avoid double-counting the same revenue line.
- **Outputs:** revenue, EBITDA, PAT, FCF, EPS, target price and return for each company under each case.

## 8. Position sizing and deployment

- Base position: 4.0% of the ₹500 crore sleeve (₹20 crore) if liquidity and conviction gates pass; maximum 5.0% (₹25 crore).
- Build in three tranches: 50% at initiation, 25% on Q2 FY27 confirmation, 25% on a valuation or operating trigger.
- Liquidity gate: position ≤10% of 20-day average daily traded value; otherwise stage over more days.
- Single-stock hard cap: 5% of the sleeve; sector cap: 100% (mandate is a single-name selection).
- Cash drag: uninvested balance in liquid instruments; no leverage.

## 9. Exactly three exit/thesis-review triggers

1. **Structural market-share loss:** CAMS MF RTA share falls below 63% for two consecutive quarters, or a top-5 client publicly migrates a material mandate.
2. **Fee/regulatory impairment:** SEBI or AMFI implements a binding RTA fee cap/panel that reduces CAMS's MF revenue yield by more than 10%, or a regulation removes the asset-based fee model.
3. **Valuation/earnings break:** forward P/E exceeds 45x while forward revenue growth falls below 8%, or the base-case target is reached (>₹950) with no upward revision to FY28 earnings.

## 10. Key risks to the plan

- CAMS Q2 FY27 results were not available at the cut-off; the model relies on Q1 and guidance.
- DCF may imply a value below the market price; this will be shown, not hidden, and reconciled with the relative-valuation target.
- BSE's F&O revenue concentration makes its bear case unusually wide; this is central to rejecting it despite higher growth.
- CDSL's regulatory/network moat is strong but its starting multiple and slowing earnings leave little margin of safety.
- KFin's international acquisition improves growth but complicates margin and cash-conversion analysis.

## 11. Immediate next actions

1. Write normalized financial and market CSVs.
2. Write source manifest and regulatory timeline.
3. Implement data validation and relative valuation.
4. Build CAMS three-statement/DCF.
5. Run scenarios, sensitivities and portfolio sizing.
6. Write reports and two-page IC memo.
7. Run tests and quality gate.
