# Methodology Decision - Meridian Monte Carlo

## The Decision

Three Monte Carlo methods are used in this repo.
Each serves a different analytical task. Each was
chosen because its statistical properties match
the specific requirements of that task.

---

## Method 1 - Latin Hypercube Sampling for Business Valuation

### What it is

Latin Hypercube Sampling is a stratified Monte Carlo
sampling method. It divides the range of each input
variable into N equal probability intervals and samples
exactly once from each interval. This ensures the full
range of every input variable is represented in the
simulation, even with a relatively small number of
iterations.

### Why LHS for venture valuation

Meridian Ventures prices illiquid Asia-Pacific assets
at Series A and B stage. These assets have three
characteristics that make LHS the correct choice.

First, input distributions are wide and asymmetric.
Revenue growth rates, margin trajectories, and exit
multiples for early-stage Asia-Pacific ventures have
high variance and right-skewed distributions. Pure
random sampling with a small iteration count will
systematically underrepresent tail outcomes. LHS
eliminates that underrepresentation by construction.

Second, data is sparse. Series A and B companies
have limited operating history. The input assumptions
are derived from comparable transactions and analyst
judgment rather than dense historical datasets.
When data is sparse, sampling efficiency matters.
LHS achieves stable output distributions with
significantly fewer iterations than pure random
sampling - typically 10,000 LHS iterations produces
results comparable to 100,000 pure random iterations.

Third, the output needs to be defensible in an
investment committee context. LHS produces clean
percentile distributions - P10, P50, P90 - that
map directly to IC decision thresholds. The output
language matches the decision language.

### What was rejected and why

Pure random Monte Carlo was rejected because it
requires many more iterations to achieve stable
tail coverage on asymmetric distributions. For
illiquid assets with wide input ranges, pure random
sampling systematically misses the tails that matter
most for downside risk assessment.

Quasi Monte Carlo using low-discrepancy sequences
such as Sobol or Halton was considered. It achieves
even better coverage than LHS with fewer iterations.
It was rejected because its theoretical properties
are harder to explain to a non-technical IC audience
and the marginal improvement over LHS does not
justify the communication overhead in a private
banking context.

MCMC was rejected for valuation because it is
designed for posterior distribution sampling in
Bayesian inference, not for forward-looking
scenario generation from assumed input distributions.
Using MCMC here would be a methodological mismatch.

---

## Method 2 - Scenario-Based Monte Carlo with Correlated Inputs for Macro Stress Testing

### What it is

Scenario-based Monte Carlo models multiple correlated
stochastic variables simultaneously. Rather than
sampling each input independently, it uses a
correlation matrix to preserve the statistical
relationships between variables observed historically.
When oil prices spike, Asia-Pacific FX rates move
in predictable directions. When yields rise rapidly,
credit spreads widen. These relationships are captured
in the correlation matrix and honored in every
simulation path.

### Why scenario-based correlated MC for macro stress

The macro stress test models the transmission of a
geopolitical shock through the financial system to
Meridian's portfolio. This transmission is inherently
multivariate and correlated. An oil price spike does
not affect yield curves and FX rates independently.
They move together in patterns that historical data
documents. Ignoring those correlations would produce
stress scenarios that are statistically naive and
practically useless.

The primary stochastic variable is geopolitical shock
duration, specifically Strait of Hormuz disruption
length. From that single variable, the model generates
correlated paths for oil prices, CNY/USD, SGD/USD,
IDR/USD, 10-year UST yields, and EM credit spreads.
The output is a full probability distribution of
portfolio impact across hundreds of correlated paths,
not three discrete scenarios.

### The Iran War Calibration Case

The Strait of Hormuz closure of Q1 2026 provides a
live calibration opportunity. The model inputs are
parameterized using historical conflict precedents.
The iran_war_calibration.json file records the actual
observed values from Q1 2026: Brent at USD 118,
energy sector at plus 37.7%, 10-year UST yield at
4.30%, EM bond drawdown observed. The calibration
report documents whether the modeled distribution
covered the actual outcome. This is institutional
validation, not retrospective prediction.

### What was rejected and why

Simple scenario analysis with three discrete cases
was rejected because it produces false precision.
Labeling three outcomes as base, adverse, and severe
implies those are the only possibilities. A probability
distribution is honest about uncertainty in a way
that three discrete scenarios are not.

Pure random Monte Carlo without correlation structure
was rejected because it produces unrealistic joint
scenarios. An oil spike combined with SGD appreciation
and EM credit spread tightening is not a coherent
stress scenario. The correlation matrix prevents the
model from generating incoherent joint outcomes.

---

## Method 3 - Historical Simulation Monte Carlo for LP Reporting

### What it is

Historical simulation uses actual historical return
sequences as the simulation input rather than assuming
a parametric distribution such as normal or lognormal.
The simulation samples from the historical record
directly, preserving all the statistical properties
of real market behavior including fat tails, skewness,
and volatility clustering that parametric assumptions
systematically underestimate.

### Why historical simulation for LP reporting

Institutional LPs have two requirements for risk
reporting that make historical simulation the correct
choice.

First, they need outputs they can explain to their
own investment committees. VaR at 95% and 99%
confidence, expected shortfall, and maximum drawdown
distribution are metrics that LP investment committees
understand and use in their own portfolio construction.
Historical simulation produces these outputs directly
in the correct format.

Second, they need outputs grounded in observable
market behavior rather than model assumptions. A
parametric VaR model requires the LP to accept the
distributional assumption. Historical simulation
requires only that the past is a reasonable guide
to the range of future outcomes - a much easier
assumption to defend. There are no distributional
parameters to challenge in a quarterly review meeting.

### What was rejected and why

Parametric VaR using normal distribution assumptions
was rejected because private banking portfolios with
alternatives, structured products, and private credit
exposures have return distributions with fat tails
and negative skewness. Normal distribution assumptions
systematically underestimate tail risk for these
portfolios and would produce VaR figures that are
not credible to sophisticated LP investors.

MCMC for LP reporting was rejected because it is
computationally intensive, requires prior specification,
and produces outputs that are difficult to communicate
to a non-technical LP audience. The communication
overhead exceeds the analytical benefit for this
specific use case.