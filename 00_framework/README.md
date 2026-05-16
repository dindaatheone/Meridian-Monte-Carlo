# 00 - Framework

Methodology decisions made before any model is built.
Every Monte Carlo implementation choice is documented
here with its rationale. A model without documented
methodology is not institutional work - it is a script.

---

## Files

| File | Purpose |
|---|---|
| methodology_decision.md | Three-method decision - what was chosen, what was rejected, and why |
| data_spine_connection.md | How this repo draws from Meridian BI client entity schema |

---

## The Core Question This Section Answers

Why these three methods and not others?

Monte Carlo simulation is not one method. It is a family
of approaches with meaningfully different properties.
Latin Hypercube Sampling, pure random sampling, Quasi
Monte Carlo, MCMC, scenario-based simulation, and
historical simulation all produce different outputs
for different reasons. Choosing correctly requires
understanding what each one is good at and what it
is not good at.

This framework section documents that choice process
so any reviewer - an LP, an interviewer, a technical
evaluator - can trace every implementation decision
back to a justified rationale.