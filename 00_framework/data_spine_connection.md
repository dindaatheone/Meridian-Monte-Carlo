# Data Spine Connection - Meridian Monte Carlo

## Overview

This repo draws from the immutable client entity schema
defined in Meridian-Business-Intelligence. This document
maps exactly which fields from that schema feed which
models in this repo.

---

## Connection Map

| BI Repo Field | Monte Carlo Use |
|---|---|
| investable_aum_usd | Portfolio-level AUM input for LP risk model |
| equity_pct | Asset class allocation weight in stress test |
| fixed_income_pct | Asset class allocation weight in stress test |
| alternatives_pct | Asset class allocation weight in stress test |
| cash_pct | Asset class allocation weight in stress test |
| structured_pct | Asset class allocation weight in stress test |
| private_credit_pct | Asset class allocation weight in stress test |
| primary_currency | FX exposure input for macro stress transmission |
| jurisdiction | Corridor-level stress impact aggregation |
| client_tier | AUM weighting for LP portfolio-level risk report |
| co_investment_eligible_flag | Filters VHNW and UHNW clients for co-investment stress scenarios |
| shariah_compliant_flag | Isolates Shariah sleeve for separate stress path |

---

## LHS Valuation Connection

The LHS valuation model in 01_lhs_valuation does not
draw directly from the BI client schema. It draws from
venture_assumptions.json, which is parameterized using
comparable transaction data from the Asia-Pacific
Series A and B market. The connection to the BI repo
is indirect: the AUM distribution by tier informs
the co-investment ticket size assumptions in the
valuation model inputs.

---

## Macro Stress Connection

The scenario stress model in 02_macro_stress draws
portfolio allocation weights from the BI repo portfolios
table. The weighted average asset class exposure across
the active client base determines how a macro shock
transmits to total AUM. A book concentrated in equities
and alternatives experiences a different stress impact
than a book concentrated in fixed income and cash.

---

## LP Reporting Connection

The historical simulation model in 03_lp_reporting
uses the aggregate portfolio composition from the BI
repo to construct the fund-level return series that
feeds the simulation. Client-level AUM weights the
contribution of each asset class to the total portfolio
return distribution.

---

## Schema Immutability Note

No field is added to the BI repo schema without a
Guidebook version update. If a field appears in this
connection map and is absent from the BI schema, that
is a version mismatch that must be resolved before
the affected model is run. Check the Guidebook version
before running any model that depends on BI data.
