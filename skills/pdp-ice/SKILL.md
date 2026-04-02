---
name: pdp-ice
description: "Generate Partial Dependence and ICE plots. Visualize feature effects on predictions, detect interactions, and identify non-linear relationships."
aliases: [partial dependence, ice plot, feature effect, marginal effect, pdp plot]
extends: spark
user_invocable: true
---

# PDP-ICE

Generate Partial Dependence Plots (PDP) and Individual Conditional Expectation (ICE) plots for trained models. Visualizes marginal feature effects on predictions, detects feature interactions via 2D PDP, identifies non-linear relationships and threshold effects, and computes centered ICE plots to reveal heterogeneous effects hidden by averaging.

## When to Use

- You need to understand the marginal effect of a specific feature on predictions (e.g., "how does age affect approval probability?").
- You want to detect interaction effects between two features using 2D partial dependence surfaces.
- You suspect non-linear or threshold effects that global importance metrics cannot reveal.
- You need ICE plots to check whether the average PDP curve hides heterogeneous subgroup behavior.

## Workflow

1. **Environment Check** -- Verify numpy and model prediction interface. Check that the model exposes a `predict` method compatible with partial dependence computation.
2. **Feature Selection** -- If features are not specified, auto-select the top features by importance. Validate that requested features exist in the dataset. For interaction pairs, parse the `f1:f2` syntax.
3. **PDP and ICE Computation** -- For each feature, create a value grid (using quantiles or uniform spacing). Sweep the grid while holding other features constant. Record per-sample ICE curves and average them into PDP curves. For interaction pairs, compute 2D grids.
4. **Interaction Detection** -- Measure ICE curve heterogeneity (standard deviation across samples at each grid point). Flag features where heterogeneity is high, indicating interactions or subgroup effects. For specified interaction pairs, compute the H-statistic.

## Report Bus Integration

Produces `pdp_ice_report.json` with keys: `features_analyzed`, `pdp_values`, `ice_values`, `grid_values`, `interaction_flags`, `heterogeneity_scores`, `visualization_paths`.

## Full Specification

Usage: `/pdp-ice <model_path> --data <dataset> [--features <f1,f2>] [--interactions f1:f2]`

Delegated to agent: **explainability-analyst**

See `commands/pdp-ice.md` for the complete workflow.
