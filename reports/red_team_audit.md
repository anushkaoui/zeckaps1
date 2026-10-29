# Independent Red-Team Audit

**Date:** 29 October 2026 | **Scope:** all four companies, model, scenarios, reports and recommendation | **Auditor stance:** hostile IC reviewer

## 1. Verdict

The recommendation survives the audit: **BUY CAMS, 12-month target ₹800, 4% of the ₹500 crore sleeve, three tranches.** The audit found and corrected two material modelling issues (BSE other income and the FCF definition) and several presentation/data issues. None changes the winner.

Updated numbers:

| Company | Price (₹) | Official target (₹) | Total return | Expected total return | Recommendation |
|---|---:|---:|---:|---:|---|
| **CAMS** | **697** | **800** | **+16.6%** | **+15.2%** | **BUY** |
| KFin | 860 | 935 | +10.1% | +10.3% | Reject |
| BSE | 3,502 | 3,460 | −0.9% | −5.0% | Reject |
| CDSL | 1,282 | 1,190 | −6.2% | −6.0% | Reject |

## 2. Material corrections

### 2.1 BSE other-income forecast was unsupported

**Finding:** the model forecast BSE other income at ₹450–500 crore, versus ₹24 crore in FY26 and ₹22 crore in FY25 in the normalized data. The ₹450 line was not anchored to any historical normalized figure. It inflated BSE FY27 PBT, EPS, target and expected return.

**Primary-source check:** BSE's FY26 media release reports total revenue of ₹5,148 crore, comprising ₹4,834 crore from operations and ₹314 crore investment/other income. Screener's normalized line is ₹5,124 crore sales + ₹24 crore other income = ₹5,148 crore. The normalized ₹5,124 crore therefore already contains ~₹290 crore of the ₹314 crore investment/other income. Adding ₹330–450 crore of other income on top would double-count it.

**Correction:** BSE other income is now ₹24/25/26/27/28 crore (5% growth), consistent with the normalized revenue series and with total revenue growing ~20% in FY27. BSE's FY26 operating EBITDA is ₹3,079 crore (64% margin) on ₹4,834 crore revenue from operations; the normalized ₹3,480 crore/67.9% margin is not like-for-like and is now footnoted.

**Impact:** BSE FY27E EPS falls from ₹80.6 to ₹72.7, FY28E EPS from ₹90.6 to ₹82.4, and the base target from ₹3,805 to ₹3,460. BSE's official total return falls from +8.9% to −0.9%; expected total return from +4.4% to −5.0%. BSE remains rejected, now more decisively.

### 2.2 FCF definition was inconsistent

**Finding:** `forecast_company` used `CFO = EBITDA − tax − ΔNWC`, while the linked CAMS three-statement used `CFO = PAT + depreciation − ΔNWC`. CAMS FY27 FCF was ₹501 crore in `forecast_summary.csv` but ₹558 crore in `cams_three_statement.csv`; reports cited the higher figure while shock tables used the lower one. The ₹57 crore gap was other income (₹57 crore) − interest (₹6 crore) + a ₹6 crore NWC difference.

**Correction:** `forecast_company` now uses `CFO = PAT + depreciation − ΔNWC`, and CAMS working capital is set to −5% of incremental revenue to match the linked balance sheet (which implies ~−5.1%). CAMS FY27 simplified FCF is now ₹558.17 crore versus ₹558.42 crore in the linked statement, a 0.04% gap. A regression test enforces a <2% gap. The equity-drawdown shock FCF rises from ₹430 crore to ₹478 crore; the F&O shock FCF from ₹498 crore to ₹554 crore. Targets are unaffected because the DCF uses FCFF and the target is EPS-based.

### 2.3 CAMS market data and cash label

**Finding:** the model used ₹695, 24.86 crore shares and a note saying "FY26 cash ~₹970 crore." Screener's 29 October close was ₹697; the company's share-capital audit reports 24,82,04,728 shares (24.82 crore); FY26 cash was ₹854.45 crore and Q1 FY27 cash was ₹971.45 crore.

**Correction:** CAMS price ₹697, shares 24.82 crore, market cap ₹17,300 crore, EV ₹16,394 crore, dividend yield 1.79%. Net cash remains ₹906 crore (Q1 cash ₹971.45 crore less ₹64 crore debt); the ₹64 crore debt appears to be lease liabilities, and the note now says so. The target remains ₹800; total return is +16.6%, not +17.0%.

### 2.4 KFin price

**Finding:** the model used ₹862 versus Screener's 29 October close of ₹860. **Correction:** price ₹860, market cap ₹14,878 crore, EV ₹14,433 crore, dividend yield 1.39%. The target is unchanged at ₹935; total return +10.1%, expected +10.3%.

## 3. Primary-source reconciliation

### BSE FY26

| Item | BSE media release | Normalized model | Comment |
|---|---:|---:|---|
| Total revenue | 5,148 | 5,148 (5,124 + 24) | Reconciles exactly |
| Revenue from operations | 4,834 | 5,124 | ~₹290 crore investment income reclassified into sales |
| Operating EBITDA | 3,079 | 3,480 | ₹401 crore difference; margin 64% vs 67.9% |
| Investment/other income | 314 | 24 | Most of it sits in normalized sales |
| Depreciation/interest | 159 | 193 | Definitional |
| PBT | 3,234 | 3,311 | +₹77 crore (+2.4%) |
| Associates | 65 | — | Not separately modelled |
| Tax | 824 | 828 | Close |
| PAT | 2,487 | 2,487 | Matches |

The normalized series is internally consistent and PAT reconciles, but BSE's margin and other-income lines are not comparable with peers without the footnote now added.

### CAMS FY26 and Q1 FY27

- FY26 annual report: total income ₹1,567.42 crore; revenue from operations ₹1,516.25 crore; PAT after NCI ₹476.01 crore; EPS ₹19.23; cash ₹854.45 crore; no external debt.
- Normalized model: revenue ₹1,516 crore; PAT ₹472 crore; EPS ₹19.20. The ₹4 crore gap is negative NCI; forward EPS is therefore conservative by <1%. No forecast change.
- Q1 FY27: revenue ₹395.03 crore; EBITDA ₹183 crore (46.4%); PBT ₹173.97 crore; PAT owners ₹128.02 crore (total ₹127.10 crore); EPS ₹5.16. The model's ₹127.1 crore is total PAT and is consistent.
- Q4 FY26 press release: EBITDA ₹183.66 crore; margin 46.5%; highest-ever quarterly revenue.
- Q2 FY27 results were scheduled for 29 October 2026 and were not available at the cut-off. This remains the key near-term gate.

### Market data

| Company | Model price | Screener 29 Oct | Difference | Action |
|---|---:|---:|---:|---|
| BSE | 3,502 | 3,502 | 0.0% | None |
| CDSL | 1,282 | 1,282 | 0.0% | None |
| CAMS | 695 | 697 | +0.3% | Corrected |
| KFin | 862 | 860 | −0.2% | Corrected |

## 4. Other findings and judgements

1. **ERP 4.5% is low.** A 5.5–6.0% ERP would lower the DCF to roughly ₹550–590 and the blended target to ~₹760–770. The DCF is a cross-check; the target relies on the forward multiple. Disclosed in the valuation report and adversarial review.
2. **DDM only supports ~8% perpetual growth.** At 7.5% growth the DDM is ~₹651; at 8.0%, ~₹803. It corroborates the target only under an optimistic perpetual-growth assumption.
3. **BSE Q1 FY27 definition conflict is unresolved.** Screener shows ₹1,566 crore revenue/₹1,046 crore EBITDA; the company presentation shows ₹1,706.8 crore/₹1,186.7 crore. The FY26 media release confirms classification differences are real, not a one-quarter anomaly.
4. **CAMS share count is now resolved to 24.82 crore** from the 30 June 2026 share-capital audit. The earlier 24.65–24.86 crore range was caused by Screener's market-cap rounding and stale share data.
5. **CAMS restricted cash** is not separately disclosed in the reviewed materials. The ₹906 crore net cash is a haircut-free cash-less-debt figure; part may be regulatory/operating. This is conservative relative to BSE/CDSL/KFin, which are explicitly haircut.
6. **BSE's FY26 PAT is ₹2,487 crore, not ₹2,497 crore.** The prior draft contained a ₹10 crore typo; corrected everywhere.
7. **CAMS FY26 owners' PAT ₹476.01 crore vs model ₹472 crore.** Negative NCI; immaterial for a 12-month call.
8. **BSE normalized FY26 other income ₹24 crore vs FY24 ₹417 crore.** The classification is unstable; the forecast no longer extrapolates a one-year spike.

## 5. Verification

- `python3 -m model.run_all`: completes; 135 data/accounting checks, 0 failures.
- `python3 -m unittest discover -s tests -v`: 11 tests, all pass.
- CAMS balance-sheet and cash-roll checks: zero in all five forecast years.
- CAMS simplified FCF vs linked three-statement FCF: ₹558.17 crore vs ₹558.42 crore (FY27), <0.1% gap.
- Scenario probabilities sum to 1; expected values recomputed.
- Portfolio: 2,86,944 shares for ₹20 crore at ₹697; hard cap 3,58,680 shares/₹25 crore.

## 6. Residual open items

1. CAMS Q2 FY27 results (29 October 2026) were not available; the second tranche is gated on them.
2. CAMS 20-day ADV is not exchange-verified; ₹50 crore is a planning assumption.
3. Annual-report RPT, contingent liabilities, lease maturities and auditor qualifications were not line-by-line verified.
4. BSE's Q1 FY27 revenue/EBITDA definition remains unresolved.
5. Exact restricted/regulatory cash for BSE/CDSL/KFin is approximated by judgemental haircuts.
6. The uploaded PDF problem statement could not be parsed; the inline mandate is authoritative and PDF-only requirements may be missing.

## 7. Conclusion

The audit improves the model's integrity without changing the decision. BSE's rejection is now based on a correctly normalized other-income line, not an inflated one. CAMS's FCF is internally consistent, its share count and price are current, and its target remains ₹800. The recommendation is **BUY CAMS**, with **moderate conviction**, staged entry, and the three published exit triggers.
