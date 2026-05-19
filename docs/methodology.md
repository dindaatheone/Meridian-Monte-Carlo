# Methodology - Meridian Monte Carlo

Complete documentation of the analytical approach,
model selection rationale, and technical implementation
decisions across all three Monte Carlo methods.

---

## Why Monte Carlo for Private Banking Risk

Private banking portfolios contain asset classes with
return distributions that cannot be adequately captured
by deterministic models. Alternatives, structured products,
and private credit have fat tails, negative skewness,
and volatility clustering that mean-variance frameworks
systematically misrepresent.

Monte Carlo simulation generates a full distribution
of outcomes rather than a single point estimate. For
institutional decision-making, the distribution is the
answer. A P10 downside case and a P90 upside case
communicate more information than a single expected
return, and they communicate it in the language that
LP investment committees and internal risk functions
actually use.

---

## Method Selection Framework

The choice of Monte Carlo method has statistical properties that make it
more or less suitable for a given analytical task.
Three questions determine the correct method:

**Question 1: What is the nature of the inputs?**
Are inputs drawn from assumed distributions with
uncertain parameters, or from observed historical
sequences? Assumed distributions favor LHS or
scenario-based approaches. Historical sequences
favor historical simulation.

**Question 2: What is the correlation structure?**
Are inputs independent or correlated? Independent
inputs allow marginal sampling. Correlated inputs
require Cholesky decomposition or copula methods
to preserve the joint distribution.

**Question 3: Who receives the output?**
An investment committee needs P10/P50/P90 percentiles
that map to decision thresholds. LP investors need
VaR and drawdown metrics they can compare to their
own portfolio standards. The output format must match
the audience's decision language.

---

## Method 1 - Latin Hypercube Sampling

### Statistical Properties

LHS is a stratified sampling method. It partitions
the range of each input variable into N equal
probability intervals and draws exactly one sample
from each interval. This guarantees that the full
range of every input variable is represented in the
simulation regardless of iteration count.

For K input variables and N iterations, LHS produces
a sampling matrix of dimension N x K where each
column is a stratified sample from the corresponding
marginal distribution and columns are randomly
permuted to break artificial correlation between
variables.

### Implementation

The scipy.stats.qmc.LatinHypercube sampler generates
uniform samples in [0,1] with stratification. These
are transformed to the target distributions using
inverse CDF (percent point function) for each variable:
triangular distributions via scipy.stats.triang.ppf
for bounded, asymmetric inputs, and normal distributions
via scipy.stats.norm.ppf with clipping for inputs with
known plausible ranges.

### Iteration Count Justification

10,000 iterations is sufficient for stable percentile
estimates with LHS given the five-dimensional input
space. Convergence is verified by comparing P10 and
P90 estimates across subsamples of 2,500, 5,000, and
10,000 iterations. Stability within 2% across subsample
sizes confirms convergence.

---

## Method 2 - Scenario-Based Correlated Monte Carlo

### Statistical Properties

The correlated simulation approach uses Cholesky
decomposition of the correlation matrix to generate
correlated standard normal samples. For correlation
matrix C, the Cholesky factor L satisfies C = LL^T.
Multiplying uncorrelated standard normal samples Z
by L^T produces samples with the target correlation
structure: Z_corr = Z @ L^T.

The Cholesky decomposition requires C to be positive
semi-definite. The correlation matrix in
inputs/correlation_matrix.json has been verified to
satisfy this requirement. Any future updates to the
correlation matrix must pass positive semi-definiteness
validation before use.

### Marginal Distribution Parameterization

The primary stochastic variable, Strait of Hormuz
disruption duration in days, is parameterized as
lognormal. Lognormal is the correct choice because
disruption duration is strictly positive and right-skewed:
brief disruptions are common, extended closures are
rare but possible. The lognormal parameterization
reflects this asymmetry.

Secondary variables are parameterized as linear
functions of the primary variable plus a correlated
noise term. This simple functional form is intentional:
it makes the transmission mechanism explicit and
auditable, unlike black-box machine learning approaches
that would obscure the causal structure.

### Calibration Validation Standard

The calibration report compares modeled outcome
distributions to actual Q1 2026 observations. The
validation standard is: the actual outcome should
fall within the P10 to P90 range of the modeled
distribution for each variable. Outcomes outside
this range for multiple variables simultaneously
would indicate model misspecification requiring
parameter revision.

---

## Method 3 - Historical Simulation

### Statistical Properties

Historical simulation is a non-parametric method.
It makes no assumptions about the shape of the return
distribution. The empirical distribution of historical
returns is the model. This means all statistical
properties of real return series are automatically
preserved: fat tails, negative skewness, volatility
clustering, and cross-asset correlation dynamics
during stress periods.

### Bootstrap Resampling

The implementation uses bootstrap resampling with
replacement from the historical monthly return series.
Drawing with replacement generates 10,000 simulated
monthly outcomes and 10,000 simulated annual outcomes
from 12-month compounded draws. This preserves the
marginal distribution of returns while allowing
simulation of sample sizes larger than the historical
record.

Note: standard bootstrap resampling does not preserve
the serial correlation structure of returns. For
portfolios where autocorrelation is material, a
block bootstrap approach would be more appropriate.
For monthly returns at the portfolio level, serial
correlation is typically low and standard bootstrap
is adequate.

### VaR and CVaR Calculation

VaR at confidence level c is the c-th percentile of
the loss distribution: VaR_c = -Q_p(R) where p = 1-c
and Q_p is the p-th quantile of the return distribution.
CVaR at confidence level c is the expected value of
returns below VaR_c: CVaR_c = E[R | R <= VaR_c].

CVaR is a coherent risk measure. VaR is not. For
institutional LP reporting, both are provided because
LPs are familiar with VaR as a communication standard
and CVaR as the technically superior metric.

---

## Limitations

**LHS Valuation**
Input distributions are assumed, not empirically
estimated from dense transaction data. For Series A
ventures with limited comparable transactions, the
distributional assumptions carry significant model
risk. The wide triangular and normal distributions
used are intended to reflect this uncertainty honestly.

**Scenario-Based Stress**
The linear transmission functions are simplifications
of complex non-linear macro dynamics. During extreme
stress events, non-linearities and threshold effects
can cause outcomes to fall outside the modeled range.
The model is designed for planning and risk awareness,
not precise prediction.

**Historical Simulation**
The 10-year synthetic return series may not capture
tail events that occur less frequently than once per
decade. The 2020 COVID drawdown is included in the
series and provides the primary tail calibration.
Future tail events may differ in character from
historical precedents.
