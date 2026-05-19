# 01 - LHS Valuation

Latin Hypercube Sampling Monte Carlo for venture
portfolio company valuation at Series A and B stage.

---

## Files

| File | Purpose |
|---|---|
| lhs_valuation_model.py | Core LHS Monte Carlo engine - runs simulation and generates outputs |
| inputs/venture_assumptions.json | Parameterized inputs for synthetic Series A target |
| outputs/valuation_distribution.png | Histogram of simulated enterprise values with P10/P50/P90 |
| outputs/valuation_summary.csv | Percentile table P5 through P95 with Expanded NPV |

---

## What This Model Does

Takes a set of uncertain input variables - revenue growth,
margin trajectory, exit multiple, discount rate - and
generates a full probability distribution of enterprise
values for a synthetic Series A venture target.

The output is a distribution that shows the full range of plausible
outcomes given the input uncertainty. The investment
committee uses the P10, P50, and P90 values as the
downside, base, and upside cases in the deal memo.

---

## Why LHS Over Pure Random Sampling

With 10,000 LHS iterations this model achieves tail
coverage equivalent to approximately 100,000 pure
random iterations. For illiquid Asia-Pacific assets
with wide and asymmetric input distributions, that
efficiency is critical. The tails matter most in
private markets valuation and LHS ensures they are
fully represented.

Full rationale in 00_framework/methodology_decision.md.

---

## Expanded NPV

The model calculates both static NPV from the DCF
baseline and Expanded NPV which adds the option value
of staged participation. A venture with negative static
NPV may have positive Expanded NPV when the compound
option structure of Series A to B staging is included.
This is the correct valuation framework for Meridian
Ventures investment decisions.

---

## Run

```bash
python 01_lhs_valuation/lhs_valuation_model.py
```

Outputs saved to 01_lhs_valuation/outputs/
