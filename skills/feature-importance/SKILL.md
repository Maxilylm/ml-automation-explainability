---
name: feature-importance
description: "Compute and compare feature importance using multiple methods: permutation, SHAP, built-in. Cross-method rank correlation and consensus ranking."
aliases: [variable importance, feature ranking, feature selection importance, important features]
extends: ml-automation
user_invocable: true
---

# Feature Importance

Compute feature importance using multiple methods (permutation importance, SHAP-based importance, built-in model importance) and compare rankings across methods. Produces consensus top features, Spearman rank correlation between methods, disagreement flags for features with inconsistent rankings, and stability analysis via bootstrap confidence intervals.

## When to Use

- You want a robust feature ranking that does not rely on a single importance method, reducing the risk of method-specific artifacts.
- You need to identify which features are most influential before pruning, feature selection, or stakeholder presentation.
- You are comparing two model versions and want to see how feature rankings shifted between them.
- You suspect built-in importance (e.g., Gini) may be misleading for high-cardinality or correlated features and want cross-validation with permutation or SHAP.

## Workflow

1. **Environment Check** -- Verify that shap and scikit-learn are installed. Check model type to determine which methods are applicable (e.g., built-in importance is only available for tree-based models).
2. **Model and Data Loading** -- Load the serialized model and evaluation dataset. Validate feature alignment between model expectations and dataset columns.
3. **Multi-Method Computation** -- Run each requested method: permutation importance (with configurable repeats), SHAP-based mean absolute values, and built-in model attribute (feature_importances_ or coef_). Normalize all rankings to a common scale.
4. **Cross-Method Rank Correlation** -- Compute Spearman rank correlation between every pair of methods. Flag features where rank disagreement exceeds a configurable threshold. Produce a consensus ranking by averaging normalized ranks.

## Report Bus Integration

Produces `feature_importance_report.json` with keys: `rankings_per_method`, `consensus_ranking`, `spearman_correlations`, `disagreement_flags`, `top_features`, `methods_used`.

## Full Specification

Usage: `/feature-importance <model_path> --data <dataset> [--methods permutation,shap,builtin]`

Delegated to agent: **explainability-analyst**

See `commands/feature-importance.md` for the complete workflow.
