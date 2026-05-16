# Assumptions - Meridian Monte Carlo

All model assumptions documented explicitly.
Every assumption that materially affects model output
is listed here with its justification and its
sensitivity to revision.

---

## LHS Valuation Assumptions

### Revenue Growth - Year 1
Distribution: Triangular
Range: 40% to 150%, mode 75%
Justification: Asia-Pacific Series A wealthtech companies
at execution-evidence stage show wide growth variance.
The 75% mode reflects median observed growth in comparable
Singapore and Hong Kong fintech Series A transactions
2022 to 2025.
Sensitivity: High. Shifting mode from 75% to 60% reduces
P50 equity value by approximately 12 to 15%.

### Revenue Growth - Years 2 to 5
Distribution: Normal, mean 55%, std 20%, clipped 10% to 120%
Justification: Growth normalizes as the company scales.
Mean of 55% reflects the step-down from initial
hyper-growth phase. Std of 20% reflects execution
uncertainty over a 4-year forward period.
Sensitivity: Medium. Reducing mean from 55% to 45%
reduces P50 equity value by approximately 8 to 10%.

### Terminal EBITDA Margin
Distribution: Normal, mean 22%, std 8%, clipped 5% to 45%
Justification: 22% reflects mature Asia-Pacific wealthtech
platform margins. Lower than US SaaS benchmarks due to
higher client servicing costs in relationship-driven markets.
Sensitivity: High. Reducing mean from 22% to 18% reduces
P50 equity value by approximately 15 to 18%.

### Exit Multiple (EV/EBITDA)
Distribution: Triangular, min 8x, mode 14x, max 25x
Justification: Asia-Pacific fintech M&A transaction multiples
2021 to 2025. Mode of 14x reflects median observed exit
multiple. Min of 8x reflects distressed or strategic buyer
scenarios. Max of 25x reflects premium platform acquisitions.
Sensitivity: High. The exit multiple is the single most
sensitive input. Shifting mode from 14x to 11x reduces
P50 equity value by approximately 20 to 25%.

### WACC
Distribution: Normal, mean 18%, std 3%, clipped 12% to 28%
Justification: 18% reflects Series A stage illiquidity
premium plus Asia-Pacific risk premium over a USD risk-free
rate of approximately 4.5%. Std of 3% reflects uncertainty
in market conditions at exit.
Sensitivity: Medium. Increasing mean WACC from 18% to 22%
reduces P50 equity value by approximately 10 to 12%.

---

## Macro Stress Assumptions

### Strait of Hormuz Disruption Duration
Distribution: Lognormal, mean 45 days, std 30 days
Justification: Historical precedents for Strait of Hormuz
disruption risk calibrated from Iran-Iraq war period and
subsequent regional conflict episodes. Mean of 45 days
reflects a moderate disruption. Right skew reflects the
low-probability but high-impact extended closure scenario.
Sensitivity: Very high. All downstream variables are
functions of disruption duration. Doubling the mean
duration doubles the stressed portfolio impact at P50.

### Correlation Matrix
Source: Calibrated from historical conflict and supply shock
episodes 2000 to 2024 including 2003 Iraq war, 2011 Arab
Spring, 2019 Saudi Aramco attack, and 2022 Russia-Ukraine
conflict effects on commodity markets.
Sensitivity: Medium. The strongest sensitivities are the
oil-to-EM-spread correlation (0.52) and the equity-to-EM-spread
correlation (-0.62). These two parameters drive most of the
cross-asset stress transmission.
Revision trigger: If realized correlations during the Q1 2026
Iran war episode differ materially from modeled values,
the matrix should be updated to incorporate the new data point.

### Asset Class Return Sensitivities
Linear coefficients connecting disruption duration to
asset class returns are calibrated from historical
oil shock episodes. These are simplifications of
complex non-linear dynamics and carry model risk
during extreme events where non-linearities dominate.

---

## LP Reporting Assumptions

### Historical Return Series
Period: January 2016 to December 2025 - 120 monthly observations
Asset classes: Six classes matching Meridian portfolio structure
Calibration: Synthetic series calibrated to match statistical
properties of real Asia-Pacific asset class returns including
mean, standard deviation, skewness, and maximum drawdown
observed in the corresponding real asset class indices.
Key calibration events preserved: 2018 Q4 equity selloff,
2020 Q1 COVID drawdown and Q2 recovery, 2022 rate shock.

### Portfolio Weights
Source: Meridian synthetic BI universe weighted average
allocation across active client base from portfolios table.
These are the weights used: Equities 28%, Fixed Income 32%,
Alternatives 15%, Cash 8%, Structured Products 10%,
Private Credit 7%.
Revision trigger: If the BI repo data generation produces
materially different average allocations after execution,
portfolio weights should be updated before running the
LP reporting model.

### Bootstrap Resampling
Method: Standard bootstrap with replacement
Limitation: Does not preserve serial correlation structure
Justification: Monthly portfolio-level returns show low
serial autocorrelation, making standard bootstrap adequate.
If private credit allocation increases significantly above
10%, block bootstrap may become necessary given private
credit's return smoothing characteristics.

### Hurdle Rate
Rate: 8% per annum
Source: Meridian fund economics - Guidebook v1.0
This is the contractual LP hurdle rate. The probability
of meeting this hurdle is a direct output of the model
and a primary LP communication metric.