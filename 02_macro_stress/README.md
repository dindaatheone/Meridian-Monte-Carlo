# 02 - Macro Stress Testing

Scenario-based Monte Carlo with correlated inputs for
geopolitical and macro shock transmission modeling.

---

## Files

| File | Purpose |
|---|---|
| scenario_stress_model.py | Correlated input Monte Carlo engine |
| inputs/correlation_matrix.json | Historical correlations across macro variables |
| inputs/iran_war_calibration.json | Actual Q1 2026 observed values for model validation |
| outputs/stress_distribution.png | Full outcome distribution with scenario anchors |
| outputs/portfolio_impact.csv | AUM impact by asset class and jurisdiction |
| outputs/calibration_report.md | Model prediction vs actual Q1 2026 outcome |

---

## What This Model Does

Models the transmission of a geopolitical shock through
the financial system to Meridian's Asia-Pacific portfolio.
The primary stochastic variable is Strait of Hormuz
disruption duration in days. From that single variable
the model generates correlated paths for oil prices,
Asia-Pacific FX rates, yield curves, and credit spreads
using historically calibrated correlation matrices.

The output is a full probability distribution of portfolio
AUM impact across hundreds of correlated simulation paths.
Not three discrete scenarios. A full distribution with
confidence intervals.

---

## The Iran War Calibration Case

The Strait of Hormuz closure of Q1 2026 provides a live
calibration opportunity. The iran_war_calibration.json
file records actual observed values from Q1 2026. The
calibration_report.md documents whether the modeled
distribution covered the actual outcome.

This is not retrospective prediction. It is institutional
validation: demonstrating that the methodology was
correctly specified before the event occurred and that
the actual outcome fell within the modeled distribution.

---

## Run

```bash
python 02_macro_stress/scenario_stress_model.py
```

Outputs saved to 02_macro_stress/outputs/