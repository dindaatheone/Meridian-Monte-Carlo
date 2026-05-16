# Meridian Monte Carlo
# Latin Hypercube Sampling Valuation Model
# Prices illiquid Asia-Pacific venture assets at Series A and B
#
# Method: Latin Hypercube Sampling Monte Carlo
# Rationale: stratified sampling ensures full coverage of wide,
# asymmetric input distributions with fewer iterations than
# pure random sampling. See 00_framework/methodology_decision.md
#
# Input:  inputs/venture_assumptions.json
# Output: outputs/valuation_distribution.png
#         outputs/valuation_summary.csv

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import json
import os
from scipy.stats import qmc, norm, triang

# ── Configuration ─────────────────────────────────────────────
INPUT_PATH  = "01_lhs_valuation/inputs/venture_assumptions.json"
OUTPUT_DIR  = "01_lhs_valuation/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Load Assumptions ──────────────────────────────────────────
with open(INPUT_PATH) as f:
    assumptions = json.load(f)

params      = assumptions["simulation_parameters"]
base        = assumptions["base_metrics"]
dists       = assumptions["input_distributions"]
option_params = assumptions["option_value_parameters"]
ic          = assumptions["ic_thresholds"]

N           = params["n_iterations"]
YEARS       = params["projection_years"]
SEED        = params["random_seed"]
np.random.seed(SEED)

print(f"Meridian Monte Carlo - LHS Valuation Model")
print(f"Target: {assumptions['target_name']}")
print(f"Iterations: {N:,}")
print(f"Projection: {YEARS} years")
print()

# ── Latin Hypercube Sampling ──────────────────────────────────
# Generate LHS samples in [0,1] for 5 input variables
sampler     = qmc.LatinHypercube(d=5, seed=SEED)
lhs_samples = sampler.random(n=N)

# ── Transform LHS Samples to Input Distributions ──────────────

def triangular_ppf(u, low, mode, high):
    c = (mode - low) / (high - low)
    return triang.ppf(u, c=c, loc=low, scale=high - low)

def normal_ppf(u, mean, std, min_clip, max_clip):
    raw = norm.ppf(u, loc=mean, scale=std)
    return np.clip(raw, min_clip, max_clip)

# Column 0: revenue growth year 1
d = dists["revenue_growth_year1"]
rev_growth_y1 = triangular_ppf(
    lhs_samples[:, 0], d["min"], d["mode"], d["max"]
)

# Column 1: revenue growth years 2 to 5
d = dists["revenue_growth_years2to5"]
rev_growth_y2to5 = normal_ppf(
    lhs_samples[:, 1], d["mean"], d["std"],
    d["min_clip"], d["max_clip"]
)

# Column 2: terminal EBITDA margin
d = dists["ebitda_margin_terminal"]
ebitda_margin = normal_ppf(
    lhs_samples[:, 2], d["mean"], d["std"],
    d["min_clip"], d["max_clip"]
)

# Column 3: exit multiple
d = dists["exit_multiple_ebitda"]
exit_multiple = triangular_ppf(
    lhs_samples[:, 3], d["min"], d["mode"], d["max"]
)

# Column 4: WACC
d = dists["wacc"]
wacc = normal_ppf(
    lhs_samples[:, 4], d["mean"], d["std"],
    d["min_clip"], d["max_clip"]
)

# ── Revenue Projection ────────────────────────────────────────
revenue = np.zeros((N, YEARS + 1))
revenue[:, 0] = base["current_revenue_usd"]
revenue[:, 1] = revenue[:, 0] * (1 + rev_growth_y1)
for yr in range(2, YEARS + 1):
    revenue[:, yr] = revenue[:, yr - 1] * (1 + rev_growth_y2to5)

# ── EBITDA at Terminal Year ───────────────────────────────────
# Linear margin improvement from current to terminal
current_margin  = base["current_ebitda_margin"]
margin_path     = np.linspace(current_margin, 1, YEARS + 1)
ebitda_terminal = revenue[:, YEARS] * ebitda_margin

# ── Enterprise Value at Exit ──────────────────────────────────
ev_exit = ebitda_terminal * exit_multiple

# ── Discount Back to Present ──────────────────────────────────
discount_factor = (1 + wacc) ** YEARS
ev_present      = ev_exit / discount_factor

# ── Adjust for Net Debt ───────────────────────────────────────
net_debt        = base["current_debt_usd"] - base["cash_usd"]
equity_value    = ev_present - net_debt

# ── Static NPV ────────────────────────────────────────────────
# Simplified: equity value minus implied Series A investment
series_a_investment = assumptions["ic_thresholds"]["minimum_p10_usd"]
static_npv          = equity_value - series_a_investment

# ── Expanded NPV: Static NPV + Option Value ───────────────────
option_value        = (option_params["series_b_probability"] *
                       option_params["series_b_option_value_usd"])
expanded_npv        = static_npv + option_value

# ── Output Statistics ─────────────────────────────────────────
percentiles = [5, 10, 25, 50, 75, 90, 95]
ev_percentiles = np.percentile(equity_value, percentiles)

print("Equity Value Distribution (USD):")
for p, v in zip(percentiles, ev_percentiles):
    print(f"  P{p:2d}: {v:>15,.0f}")

print(f"\nMean:   {equity_value.mean():>15,.0f}")
print(f"Median: {np.median(equity_value):>15,.0f}")
print(f"StdDev: {equity_value.std():>15,.0f}")
print(f"\nExpanded NPV (mean): {expanded_npv.mean():>12,.0f}")
print(f"Option Value:        {option_value:>12,.0f}")

p10 = np.percentile(equity_value, 10)
p50 = np.percentile(equity_value, 50)
p90 = np.percentile(equity_value, 90)

ic_pass = p10 >= ic["minimum_p10_usd"]
print(f"\nIC Assessment:")
print(f"  P10 threshold: USD {ic['minimum_p10_usd']:>12,.0f}")
print(f"  P10 result:    USD {p10:>12,.0f}")
print(f"  IC Decision:   {'PROCEED' if ic_pass else 'REJECT'}")

# ── Valuation Distribution Chart ──────────────────────────────
fig, ax = plt.subplots(figsize=(12, 7))

ax.hist(
    equity_value / 1_000_000,
    bins      = 80,
    color     = '#1E3A5F',
    alpha     = 0.75,
    edgecolor = 'none'
)

# P10, P50, P90 lines
for pct, val, label, color in [
    (10, p10, 'P10 Downside', '#B71C1C'),
    (50, p50, 'P50 Base Case', '#B8962E'),
    (90, p90, 'P90 Upside', '#2E7D32'),
]:
    ax.axvline(
        x         = val / 1_000_000,
        color     = color,
        linewidth = 2,
        linestyle = '--'
    )
    ax.text(
        val / 1_000_000 + 0.3,
        ax.get_ylim()[1] * 0.85 if ax.get_ylim()[1] > 0 else 100,
        f'{label}\nUSD {val/1_000_000:.1f}M',
        color     = color,
        fontsize  = 9,
        fontweight = 'bold'
    )

ax.set_title(
    f"Meridian Ventures - LHS Valuation Distribution\n"
    f"{assumptions['target_name']} | {N:,} Iterations",
    fontsize  = 13,
    pad       = 15
)
ax.set_xlabel("Equity Value (USD Millions)", fontsize=11)
ax.set_ylabel("Frequency", fontsize=11)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/valuation_distribution.png", dpi=150)
plt.close()
print(f"\nValuation distribution chart saved.")

# ── Summary CSV ───────────────────────────────────────────────
summary_rows = []
for p, v in zip(percentiles, ev_percentiles):
    summary_rows.append({
        'percentile':           f'P{p}',
        'equity_value_usd':     round(v, 0),
        'equity_value_usd_m':   round(v / 1_000_000, 2),
    })

summary_df = pd.DataFrame(summary_rows)
summary_df['static_npv_mean_usd']   = round(static_npv.mean(), 0)
summary_df['option_value_usd']      = round(option_value, 0)
summary_df['expanded_npv_mean_usd'] = round(expanded_npv.mean(), 0)
summary_df['ic_decision']           = 'PROCEED' if ic_pass else 'REJECT'

summary_df.to_csv(f"{OUTPUT_DIR}/valuation_summary.csv", index=False)
print(f"Valuation summary CSV saved.")
print(f"\nAll outputs in {OUTPUT_DIR}/")