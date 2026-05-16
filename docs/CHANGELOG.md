# CHANGELOG - Meridian Monte Carlo

All notable changes documented in reverse chronological order.

---

## [0.4.0] - Integration Layer

### Added
- 04_integration/README.md - integration principle and
  why three connected models outperform three isolated exercises
- 04_integration/integration_map.md - explicit mapping of
  every output file to its downstream consumer across
  all three Meridian repos with data flow diagram

---

## [0.3.0] - LP Reporting Model

### Added
- 03_lp_reporting/README.md - historical simulation rationale,
  LP communication standard, metric to LP language mapping
- 03_lp_reporting/inputs/historical_returns.csv - 10-year
  synthetic Asia-Pacific asset class return series calibrated
  to real market behavior including COVID drawdown and 2022
  rate shock
- 03_lp_reporting/historical_simulation_model.py - full
  historical simulation engine generating VaR at 95% and 99%,
  CVaR, maximum drawdown distribution, hurdle probability,
  risk summary CSV, VaR distribution chart, and LP risk
  report PDF

---

## [0.2.0] - Macro Stress Model

### Added
- 02_macro_stress/README.md - scenario-based correlated MC
  rationale and Iran war calibration case documentation
- 02_macro_stress/inputs/correlation_matrix.json - historically
  calibrated correlation matrix across eight macro variables
  with variable-level notes on correlation direction and magnitude
- 02_macro_stress/inputs/iran_war_calibration.json - actual
  Q1 2026 observed values from Morningstar Markets Observer
  for model validation
- 02_macro_stress/scenario_stress_model.py - full correlated
  Monte Carlo engine with Cholesky decomposition, lognormal
  disruption duration parameterization, six asset class
  impact calculations, stress distribution chart, portfolio
  impact CSV, and calibration report

---

## [0.1.0] - Foundation

### Added
- README.md - master overview, three-method architecture
  table, Iran war calibration case summary, repo structure,
  cross-repo connection map, setup instructions
- 00_framework/README.md - framework purpose and core question
- 00_framework/methodology_decision.md - complete three-method
  decision with what was chosen, what was rejected, and why
  for each of the three methods
- 00_framework/data_spine_connection.md - field-level mapping
  from Meridian BI client entity schema to Monte Carlo model inputs
- 01_lhs_valuation/README.md - LHS rationale, expanded NPV
  explanation, IC threshold connection
- 01_lhs_valuation/inputs/venture_assumptions.json - fully
  parameterized synthetic Series A target with input
  distributions, IC thresholds, and option value parameters
- 01_lhs_valuation/lhs_valuation_model.py - complete LHS
  Monte Carlo engine with scipy LHS sampler, triangular and
  normal distribution transforms, DCF valuation, expanded
  NPV calculation, IC assessment, distribution chart, and
  summary CSV
- docs/methodology.md - complete methodology documentation
  covering why Monte Carlo, method selection framework,
  statistical properties of each method, implementation
  details, and limitations
- docs/assumptions.md - all material model assumptions
  with justification and sensitivity assessment
- docs/CHANGELOG.md - this file

### Next
- Run all three models after Python environment setup
- Verify outputs against expected ranges
- Update integration map with actual output values
- Begin Meridian-Ventures skeleton