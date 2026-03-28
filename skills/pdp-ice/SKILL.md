---
name: pdp-ice
description: "Generate Partial Dependence and ICE plots. Visualize feature effects on predictions, detect interactions, and identify non-linear relationships."
aliases: [partial dependence, ice plot, feature effect, marginal effect, pdp plot]
extends: ml-automation
user_invocable: true
---

# PDP-ICE

Generate Partial Dependence Plots (PDP) and Individual Conditional Expectation (ICE) plots for trained models. Visualizes marginal feature effects on predictions, detects feature interactions via 2D PDP, identifies non-linear relationships and threshold effects, and computes centered ICE plots to reveal heterogeneous effects hidden by averaging.

## Full Specification

See `commands/pdp-ice.md` for the complete workflow.
