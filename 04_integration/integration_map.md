# Integration Map - Meridian Monte Carlo

Explicit mapping of every output file to its downstream
consumer across the three-repo Meridian architecture.

---

## LHS Valuation Outputs

### outputs/valuation_distribution.png

| Consumer | Usage |
|---|---|
| Meridian-Ventures/05_valuation/synthetic_valuation_case.md | Embedded as the visual evidence of the P10/P50/P90 range for the synthetic Series A deal memo |
| Series A Pitchbook | Demonstrates quantitative rigor in venture investment selection |
| Investment Committee | P10 vs IC threshold is the go/no-go decision input |

### outputs/valuation_summary.csv

| Consumer | Usage |
|---|---|
| Meridian-Ventures/03_investment_committee/decision_log_template.md | P10, P50, P90 values populate the IC decision log for each deal |
| Meridian-Ventures/05_valuation/valuation_framework.md | Expanded NPV calculation documented with actual model output |

---

## Macro Stress Outputs

### outputs/stress_distribution.png

| Consumer | Usage |
|---|---|
| Meridian-Ventures/08_lp_reporting/lp_report_template.md | Macro risk section of quarterly LP report |
| Series B Pitchbook | Demonstrates institutional preparedness for macro shocks |
| LinkedIn Portfolio Narrative | Iran war calibration case as methodology validation story |

### outputs/portfolio_impact.csv

| Consumer | Usage |
|---|---|
| Meridian-Ventures/08_lp_reporting | AUM impact by percentile feeds LP risk dashboard |
| Series A Pitchbook | Shows stress-tested AUM resilience under geopolitical shock |

### outputs/calibration_report.md

| Consumer | Usage |
|---|---|
| Series B Pitchbook | Primary evidence that the methodology was correctly specified before Q1 2026 |
| LinkedIn Portfolio Narrative | The single most compelling external communication proof point |
| docs/methodology.md | Referenced as live validation of scenario-based correlated MC approach |

---

## LP Reporting Outputs

### outputs/var_distribution.png

| Consumer | Usage |
|---|---|
| Meridian-Ventures/08_lp_reporting/lp_report_template.md | Risk dashboard visual for quarterly LP communication |
| Series A Pitchbook | Demonstrates risk quantification capability to prospective LPs |

### outputs/risk_summary.csv

| Consumer | Usage |
|---|---|
| Meridian-Ventures/08_lp_reporting/reporting_framework.md | All seven risk metrics populate the quarterly LP report table |
| Series B Pitchbook | Portfolio-level risk section with actual model output |

### outputs/lp_risk_report.pdf

| Consumer | Usage |
|---|---|
| Meridian-Ventures/08_lp_reporting | Template and working example of quarterly LP deliverable |
| Portfolio and LinkedIn | Demonstrates institutional-grade LP communication standard |

---

## Data Flow Summary

Meridian-Business-Intelligence
clients.csv, portfolios.csv
-> AUM distribution by tier
-> Portfolio allocation weights
-> FX exposure by corridor
-> 02_macro_stress inputs
-> 03_lp_reporting portfolio weights
01_lhs_valuation
venture_assumptions.json
-> lhs_valuation_model.py
-> valuation_distribution.png
-> valuation_summary.csv
-> Meridian-Ventures/05_valuation
-> IC decision logs
-> Series A pitchbook
02_macro_stress
correlation_matrix.json
iran_war_calibration.json
-> scenario_stress_model.py
-> stress_distribution.png
-> portfolio_impact.csv
-> calibration_report.md
-> Meridian-Ventures/08_lp_reporting
-> Series A and B pitchbooks
-> LinkedIn narrative
03_lp_reporting
historical_returns.csv
-> historical_simulation_model.py
-> var_distribution.png
-> risk_summary.csv
-> lp_risk_report.pdf
-> Meridian-Ventures/08_lp_reporting
-> Series A and B pitchbooks

---

## Version Consistency

All three models must run against the same version of
the Meridian Strategic Master Guidebook. If portfolio
weights change, all three models require re-run.
If the client entity schema changes in Meridian-Business-Intelligence,
the macro stress and LP reporting inputs require update.

Current version: Guidebook v1.0
Last full model run: to be updated after execution