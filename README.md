# Meridian Monte Carlo

**Risk Quantification Layer | Meridian Private Bank | Singapore MAS**

---

## What This Is

This repository is the risk quantification infrastructure of
Meridian Private Bank. It contains three Monte Carlo models,
each selected for a specific analytical task, each justified
by the nature of the decision it serves.

This is not a generic simulation exercise. Every methodological
choice here, from Latin Hypercube Sampling for venture valuation
to Historical Simulation for LP reporting, is grounded in the
specific characteristics of Asia-Pacific private banking assets
and the institutional requirements of the audiences receiving
the outputs.

---

## The Three-Method Architecture

| Method | Application | Why This Method |
|---|---|---|
| Latin Hypercube Sampling Monte Carlo | Business valuation - venture portfolio pricing at Series A and B | Stratified sampling ensures full coverage of input distributions with fewer iterations. Critical for illiquid Asia-Pacific assets where input distributions are wide and asymmetric. |
| Scenario-Based Monte Carlo with Correlated Inputs | Macro stress testing - geopolitical and macro shock transmission | Primary stochastic variable is geopolitical shock duration. Transmission modeled through historically calibrated correlation matrices to oil prices, Asia-Pacific FX, yield curves, and credit spreads. |
| Historical Simulation Monte Carlo | LP reporting - portfolio-level risk and quarterly performance communication | Institutional LPs understand percentiles and drawdown distributions grounded in real market behavior. No distributional assumptions to defend. Output in LP language: VaR, expected shortfall, drawdown. |

---

## The Iran War Calibration Case

The Strait of Hormuz closure of Q1 2026 is the live validation
of the scenario-based macro stress methodology. This repo does
not treat that event as its structural thesis. It treats it as
evidence that probabilistic scenario modeling outperforms
point-estimate forecasting in institutional decision-making.

The calibration report in 02_macro_stress/outputs/ documents
what the model indicated before Q1 2026 and compares it to
what occurred. That comparison is the institutional credibility
demonstration.

---

## Repo Architecture

```
Meridian-Monte-Carlo/
|
|-- 00_framework/                      <- Methodology decisions before any model is built
|   |-- methodology_decision.md        <- Three-method decision with rationale for each
|   +-- data_spine_connection.md       <- How this repo draws from Meridian BI schema
|
|-- 01_lhs_valuation/                  <- Latin Hypercube Sampling valuation model
|   |-- lhs_valuation_model.py         <- Core LHS Monte Carlo engine
|   |-- inputs/
|   |   +-- venture_assumptions.json   <- Parameterized inputs for synthetic Series A target
|   +-- outputs/
|       |-- valuation_distribution.png <- Histogram with P10/P50/P90 labeled
|       +-- valuation_summary.csv      <- Percentile table P5 through P95
|
|-- 02_macro_stress/                   <- Scenario-based macro stress test model
|   |-- scenario_stress_model.py       <- Correlated input Monte Carlo engine
|   |-- inputs/
|   |   |-- correlation_matrix.json    <- Historical correlations across macro variables
|   |   +-- iran_war_calibration.json  <- Actual Q1 2026 observed values for validation
|   +-- outputs/
|       |-- stress_distribution.png    <- Full outcome distribution with scenario anchors
|       |-- portfolio_impact.csv       <- AUM impact by asset class and jurisdiction
|       +-- calibration_report.md      <- Model prediction vs actual Q1 2026 outcome
|
|-- 03_lp_reporting/                   <- Historical Simulation LP risk model
|   |-- historical_simulation_model.py <- Historical simulation engine
|   |-- inputs/
|   |   +-- historical_returns.csv     <- Synthetic Asia-Pacific return series, 10yr monthly
|   +-- outputs/
|       |-- lp_risk_report.pdf         <- Quarterly LP risk report template
|       |-- var_distribution.png       <- VaR at 95% and 99% confidence
|       +-- risk_summary.csv           <- Full percentile risk table by asset class
|
|-- 04_integration/                    <- How all three methods connect to other repos
|   |-- README.md                      <- Integration overview
|   +-- integration_map.md             <- Explicit output to downstream repo mapping
|
+-- docs/
    |-- methodology.md                 <- Complete methodology documentation
    |-- assumptions.md                 <- All model assumptions documented explicitly
    +-- CHANGELOG.md                   <- Version history
```

---

## How This Repo Connects to the Other Two

| Output | Feeds Into |
|---|---|
| LHS valuation P10/P50/P90 range | Meridian-Ventures 05_valuation - IC decision thresholds |
| Macro stress portfolio impact | Meridian-Ventures 08_lp_reporting - quarterly LP risk section |
| Historical simulation risk report | Meridian-Ventures LP report template |
| All three outputs | Series A and Series B pitchbooks |

The data inputs to all three models draw from the client entity
schema defined in Meridian-Business-Intelligence. AUM distribution,
portfolio allocations, and FX exposures from that repo feed
directly into the simulation inputs here.

---

## Setup

```bash
pip install -r requirements.txt
```

**Requirements:** numpy, pandas, scipy, matplotlib, seaborn, fpdf2

**Run sequence:**

```bash
python 01_lhs_valuation/lhs_valuation_model.py
python 02_macro_stress/scenario_stress_model.py
python 03_lp_reporting/historical_simulation_model.py
```

All outputs saved to respective outputs/ folders.

---

## Part of Meridian Private Bank

This repo is a portfolio artifact demonstrating founder-level
quantitative risk thinking in private banking.

**Singapore MAS Jurisdiction | Asia-Pacific Focus | Version 1.0**
All data synthetic. Not a licensed institution.
