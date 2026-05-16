# 03 - LP Reporting

Historical Simulation Monte Carlo for portfolio-level
risk quantification and quarterly LP reporting.

---

## Files

| File | Purpose |
|---|---|
| historical_simulation_model.py | Historical simulation engine - VaR, CVaR, drawdown, hurdle probability |
| inputs/historical_returns.csv | Synthetic Asia-Pacific asset class return series - 10 year monthly |
| outputs/lp_risk_report.pdf | Quarterly LP risk report template |
| outputs/var_distribution.png | VaR at 95% and 99% confidence visualization |
| outputs/risk_summary.csv | Full percentile risk table by asset class and total portfolio |

---

## What This Model Does

Takes 10 years of synthetic monthly return history for
six Asia-Pacific asset classes and generates portfolio-level
risk metrics that institutional LPs use to evaluate their
private banking allocations.

The output answers four questions every LP investment
committee asks at every quarterly review:

1. What is the portfolio VaR at 95% and 99% confidence?
2. What is the expected shortfall if the tail is breached?
3. What is the maximum drawdown distribution?
4. What is the probability of meeting the 8% annual hurdle?

---

## Why Historical Simulation

Historical simulation uses actual return sequences rather
than assumed distributions. No parametric assumptions
to defend. No distribution fitting to challenge. The model
says: here is what happened in the past, here is the range
of outcomes that history implies for the future.

For a portfolio with alternatives, structured products,
and private credit - asset classes with fat-tailed and
negatively skewed return distributions - parametric VaR
using normal distribution assumptions systematically
underestimates tail risk. Historical simulation does not.

Full rationale in 00_framework/methodology_decision.md.

---

## LP Communication Standard

Every metric in this model output maps directly to
language institutional LPs use internally:

| Model Output | LP Committee Language |
|---|---|
| VaR 95% | 1-in-20 monthly loss threshold |
| VaR 99% | 1-in-100 monthly loss threshold |
| CVaR 95% | Expected loss when VaR is breached |
| Max drawdown P50 | Typical peak-to-trough in adverse conditions |
| Hurdle probability | Likelihood of meeting 8% annual return target |

---

## Run

```bash
python 03_lp_reporting/historical_simulation_model.py
```

Outputs saved to 03_lp_reporting/outputs/