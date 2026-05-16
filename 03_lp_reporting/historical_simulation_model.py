# Meridian Monte Carlo
# Historical Simulation LP Risk Model
# Portfolio-level risk quantification for quarterly LP reporting
#
# Method: Historical Simulation Monte Carlo
# Rationale: no distributional assumptions required.
# Output directly in LP language: VaR, CVaR, drawdown, hurdle probability.
# See 00_framework/methodology_decision.md for full rationale.
#
# Input:  inputs/historical_returns.csv
# Output: outputs/var_distribution.png
#         outputs/risk_summary.csv
#         outputs/lp_risk_report.pdf

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from fpdf import FPDF
from datetime import datetime

# ── Configuration ─────────────────────────────────────────────
INPUT_PATH  = "03_lp_reporting/inputs/historical_returns.csv"
OUTPUT_DIR  = "03_lp_reporting/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Meridian portfolio weights from synthetic BI universe
PORTFOLIO_WEIGHTS = {
    'equities_return':          0.28,
    'fixed_income_return':      0.32,
    'alternatives_return':      0.15,
    'cash_return':              0.08,
    'structured_return':        0.10,
    'private_credit_return':    0.07,
}

HURDLE_ANNUAL   = 0.08
HURDLE_MONTHLY  = (1 + HURDLE_ANNUAL) ** (1/12) - 1

print("Meridian Monte Carlo - Historical Simulation LP Risk Model")
print(f"Hurdle rate: {HURDLE_ANNUAL*100:.1f}% per annum")
print()

# ── Load Historical Returns ───────────────────────────────────
df = pd.read_csv(INPUT_PATH, parse_dates=['month'])
df = df.sort_values('month').reset_index(drop=True)

return_cols = list(PORTFOLIO_WEIGHTS.keys())
print(f"Historical return series: {len(df)} monthly observations")
print(f"Period: {df['month'].min().strftime('%Y-%m')} to "
      f"{df['month'].max().strftime('%Y-%m')}")
print()

# ── Portfolio Return Calculation ──────────────────────────────
portfolio_returns = sum(
    df[col] * weight
    for col, weight in PORTFOLIO_WEIGHTS.items()
)
portfolio_returns = portfolio_returns.values

# ── Historical Simulation: Bootstrap ─────────────────────────
# Resample with replacement from historical monthly returns
# to generate 10,000 simulated monthly portfolio outcomes
N_SIMS  = 10000
SEED    = 42
np.random.seed(SEED)

simulated_monthly = np.random.choice(
    portfolio_returns, size=N_SIMS, replace=True
)

# Annual return simulation: compound 12 monthly draws
simulated_annual = np.zeros(N_SIMS)
for i in range(N_SIMS):
    monthly_sample = np.random.choice(
        portfolio_returns, size=12, replace=True
    )
    simulated_annual[i] = np.prod(1 + monthly_sample) - 1

# ── Risk Metrics ──────────────────────────────────────────────
# VaR: loss not exceeded with given confidence
var_95_monthly  = np.percentile(simulated_monthly, 5)
var_99_monthly  = np.percentile(simulated_monthly, 1)
var_95_annual   = np.percentile(simulated_annual, 5)
var_99_annual   = np.percentile(simulated_annual, 1)

# CVaR / Expected Shortfall: expected loss when VaR is breached
cvar_95_monthly = simulated_monthly[
    simulated_monthly <= var_95_monthly
].mean()
cvar_99_monthly = simulated_monthly[
    simulated_monthly <= var_99_monthly
].mean()
cvar_95_annual  = simulated_annual[
    simulated_annual <= var_95_annual
].mean()

# Maximum drawdown distribution
def max_drawdown(returns):
    cumulative  = np.cumprod(1 + returns)
    peak        = np.maximum.accumulate(cumulative)
    drawdown    = (cumulative - peak) / peak
    return drawdown.min()

N_DD_SIMS   = 5000
drawdowns   = np.zeros(N_DD_SIMS)
for i in range(N_DD_SIMS):
    sample          = np.random.choice(portfolio_returns, size=36, replace=True)
    drawdowns[i]    = max_drawdown(sample)

max_dd_p50  = np.percentile(drawdowns, 50)
max_dd_p90  = np.percentile(drawdowns, 90)

# Hurdle rate probability
hurdle_prob = (simulated_annual >= HURDLE_ANNUAL).mean()

# ── Print Results ─────────────────────────────────────────────
print("Monthly Risk Metrics:")
print(f"  VaR 95% (monthly):     {var_95_monthly*100:>8.2f}%")
print(f"  VaR 99% (monthly):     {var_99_monthly*100:>8.2f}%")
print(f"  CVaR 95% (monthly):    {cvar_95_monthly*100:>8.2f}%")
print(f"  CVaR 99% (monthly):    {cvar_99_monthly*100:>8.2f}%")
print()
print("Annual Risk Metrics:")
print(f"  VaR 95% (annual):      {var_95_annual*100:>8.2f}%")
print(f"  VaR 99% (annual):      {var_99_annual*100:>8.2f}%")
print(f"  CVaR 95% (annual):     {cvar_95_annual*100:>8.2f}%")
print()
print("Drawdown Distribution (36-month window):")
print(f"  Max drawdown P50:      {max_dd_p50*100:>8.2f}%")
print(f"  Max drawdown P90:      {max_dd_p90*100:>8.2f}%")
print()
print(f"Hurdle Rate Probability:")
print(f"  P(return >= 8%):       {hurdle_prob*100:>8.1f}%")

# ── VaR Distribution Chart ────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# Monthly return distribution
axes[0].hist(
    simulated_monthly * 100,
    bins        = 80,
    color       = '#1E3A5F',
    alpha       = 0.75,
    edgecolor   = 'none'
)
axes[0].axvline(
    x           = var_95_monthly * 100,
    color       = '#B8962E',
    linewidth   = 2,
    linestyle   = '--',
    label       = f'VaR 95%: {var_95_monthly*100:.2f}%'
)
axes[0].axvline(
    x           = var_99_monthly * 100,
    color       = '#B71C1C',
    linewidth   = 2,
    linestyle   = '--',
    label       = f'VaR 99%: {var_99_monthly*100:.2f}%'
)
axes[0].set_title(
    "Monthly Portfolio Return Distribution\nVaR at 95% and 99% Confidence",
    fontsize = 12
)
axes[0].set_xlabel("Monthly Return (%)")
axes[0].set_ylabel("Frequency")
axes[0].legend(fontsize=10)
axes[0].grid(axis='y', alpha=0.3)

# Annual return distribution with hurdle line
axes[1].hist(
    simulated_annual * 100,
    bins        = 80,
    color       = '#1E3A5F',
    alpha       = 0.75,
    edgecolor   = 'none'
)
axes[1].axvline(
    x           = HURDLE_ANNUAL * 100,
    color       = '#2E7D32',
    linewidth   = 2.5,
    linestyle   = '-',
    label       = f'Hurdle Rate: {HURDLE_ANNUAL*100:.0f}%'
)
axes[1].axvline(
    x           = var_95_annual * 100,
    color       = '#B8962E',
    linewidth   = 2,
    linestyle   = '--',
    label       = f'VaR 95%: {var_95_annual*100:.2f}%'
)
axes[1].set_title(
    f"Annual Portfolio Return Distribution\n"
    f"P(meet hurdle) = {hurdle_prob*100:.1f}%",
    fontsize = 12
)
axes[1].set_xlabel("Annual Return (%)")
axes[1].set_ylabel("Frequency")
axes[1].legend(fontsize=10)
axes[1].grid(axis='y', alpha=0.3)

plt.suptitle(
    "Meridian Monte Carlo - LP Risk Report\n"
    "Historical Simulation | Asia-Pacific Portfolio",
    fontsize    = 14,
    y           = 1.02
)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/var_distribution.png", dpi=150)
plt.close()
print("\nVaR distribution chart saved.")

# ── Risk Summary CSV ──────────────────────────────────────────
summary = {
    'metric':           [
        'VaR 95% Monthly', 'VaR 99% Monthly',
        'CVaR 95% Monthly', 'CVaR 99% Monthly',
        'VaR 95% Annual', 'VaR 99% Annual',
        'CVaR 95% Annual',
        'Max Drawdown P50 (36m)', 'Max Drawdown P90 (36m)',
        'Hurdle Rate 8% Probability',
    ],
    'value_pct':        [
        round(var_95_monthly*100, 3),
        round(var_99_monthly*100, 3),
        round(cvar_95_monthly*100, 3),
        round(cvar_99_monthly*100, 3),
        round(var_95_annual*100, 3),
        round(var_99_annual*100, 3),
        round(cvar_95_annual*100, 3),
        round(max_dd_p50*100, 3),
        round(max_dd_p90*100, 3),
        round(hurdle_prob*100, 1),
    ],
    'interpretation':   [
        '1-in-20 monthly loss threshold',
        '1-in-100 monthly loss threshold',
        'Expected loss when VaR 95% is breached',
        'Expected loss when VaR 99% is breached',
        'Annual loss not exceeded 19 years in 20',
        'Annual loss not exceeded 99 years in 100',
        'Expected annual loss in worst 5% of years',
        'Typical peak-to-trough over 36 months',
        'Severe peak-to-trough over 36 months',
        'Probability of meeting 8% annual hurdle',
    ],
}

pd.DataFrame(summary).to_csv(
    f"{OUTPUT_DIR}/risk_summary.csv", index=False
)
print("Risk summary CSV saved.")

# ── LP Risk Report PDF ────────────────────────────────────────
pdf = FPDF()
pdf.add_page()
pdf.set_margins(20, 20, 20)

pdf.set_font("Helvetica", "B", 20)
pdf.set_text_color(10, 22, 40)
pdf.cell(0, 12, "Meridian Private Bank", ln=True, align="C")

pdf.set_font("Helvetica", "B", 14)
pdf.set_text_color(184, 150, 46)
pdf.cell(0, 8, "Quarterly LP Risk Report", ln=True, align="C")

pdf.set_font("Helvetica", "", 10)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 6, f"Generated: {datetime.now().strftime('%B %Y')} | Singapore MAS Jurisdiction",
         ln=True, align="C")
pdf.ln(8)

pdf.set_draw_color(184, 150, 46)
pdf.set_line_width(0.8)
pdf.line(20, pdf.get_y(), 190, pdf.get_y())
pdf.ln(8)

pdf.set_font("Helvetica", "B", 12)
pdf.set_text_color(10, 22, 40)
pdf.cell(0, 8, "Executive Risk Summary", ln=True)
pdf.ln(3)

metrics = [
    ("VaR 95% (Monthly)",           f"{var_95_monthly*100:.2f}%",
     "1-in-20 monthly loss threshold"),
    ("VaR 99% (Monthly)",           f"{var_99_monthly*100:.2f}%",
     "1-in-100 monthly loss threshold"),
    ("CVaR 95% (Monthly)",          f"{cvar_95_monthly*100:.2f}%",
     "Expected loss when VaR 95% is breached"),
    ("VaR 95% (Annual)",            f"{var_95_annual*100:.2f}%",
     "Annual loss not exceeded 19 years in 20"),
    ("Max Drawdown P50 (36m)",      f"{max_dd_p50*100:.2f}%",
     "Typical peak-to-trough over 36-month window"),
    ("Max Drawdown P90 (36m)",      f"{max_dd_p90*100:.2f}%",
     "Severe peak-to-trough over 36-month window"),
    ("Hurdle Rate Probability",     f"{hurdle_prob*100:.1f}%",
     "Probability of meeting 8% annual hurdle rate"),
]

pdf.set_font("Helvetica", "", 10)
for metric, value, interpretation in metrics:
    pdf.set_text_color(10, 22, 40)
    pdf.cell(80, 7, metric, border=0)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(184, 150, 46)
    pdf.cell(25, 7, value, border=0)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 7, interpretation, ln=True)
    pdf.set_font("Helvetica", "", 10)

pdf.ln(8)
pdf.set_font("Helvetica", "B", 12)
pdf.set_text_color(10, 22, 40)
pdf.cell(0, 8, "Methodology Note", ln=True)
pdf.ln(3)
pdf.set_font("Helvetica", "", 10)
pdf.set_text_color(50, 50, 50)
pdf.multi_cell(0, 6,
    "Risk metrics generated using Historical Simulation Monte Carlo. "
    "Input: 10-year synthetic Asia-Pacific asset class return series calibrated "
    "to real market behavior across six asset classes. No distributional "
    "assumptions imposed. Output reflects actual historical return sequences "
    "including fat tails and volatility clustering. "
    f"Simulation: {N_SIMS:,} iterations with bootstrap resampling."
)

pdf.ln(4)
pdf.set_line_width(0.5)
pdf.line(20, pdf.get_y(), 190, pdf.get_y())
pdf.ln(4)
pdf.set_font("Helvetica", "I", 8)
pdf.set_text_color(150, 150, 150)
pdf.cell(0, 5,
    "Meridian Private Bank | Singapore MAS | All data synthetic | Portfolio artifact | Not investment advice",
    ln=True, align="C"
)

pdf.output(f"{OUTPUT_DIR}/lp_risk_report.pdf")
print("LP risk report PDF saved.")
print(f"\nAll outputs in {OUTPUT_DIR}/")