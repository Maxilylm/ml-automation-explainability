---
name: feature-importance
description: "Compute and compare feature importance using multiple methods: permutation, SHAP, built-in. Cross-method rank correlation and consensus ranking."
aliases: [variable importance, feature ranking, feature selection importance, important features]
extends: ml-automation
user_invocable: true
---

# Feature Importance

Compute feature importance using multiple methods (permutation importance, SHAP-based importance, built-in model importance) and compare rankings across methods. Produces consensus top features, Spearman rank correlation between methods, disagreement flags for features with inconsistent rankings, and stability analysis via bootstrap confidence intervals.

## Full Specification

See `commands/feature-importance.md` for the complete workflow.
