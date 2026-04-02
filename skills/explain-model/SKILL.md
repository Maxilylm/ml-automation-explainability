---
name: explain-model
description: "Generate SHAP and LIME explanations for trained ML models. Produces global feature importance, local prediction explanations, and interpretability artifacts."
aliases: [shap, lime, model explanation, explain predictions, model interpretability]
extends: spark
user_invocable: true
---

# Explain Model

Generate comprehensive model explanations using SHAP (TreeSHAP, KernelSHAP, DeepSHAP) and LIME. Produces global feature importance rankings, local prediction explanations (force plots, waterfall plots), feature interaction analysis, and cross-method importance comparison with rank correlation.

## When to Use

- You have a trained model and need to understand which features drive its predictions globally or for specific instances.
- Stakeholders or reviewers require interpretability artifacts (SHAP summary plots, LIME explanations) before a model can be approved for deployment.
- You want to compare SHAP and LIME explanations side-by-side to validate consistency of feature attributions.
- You are debugging unexpected predictions and need local explanation breakdowns for individual samples.

## Workflow

1. **Environment Check** -- Verify that shap, lime, and visualization dependencies are installed. Install missing packages automatically.
2. **Model and Data Loading** -- Load the serialized model and the dataset to explain. Validate compatibility (feature count, column names, dtypes).
3. **SHAP Values** -- Auto-detect the appropriate explainer (TreeSHAP for tree ensembles, LinearSHAP for linear models, DeepSHAP for neural nets, KernelSHAP as fallback). Compute global SHAP values, generate summary and dependence plots.
4. **LIME Explanations** -- Generate local LIME explanations for a configurable set of sample indices. Produce per-sample feature contribution tables.
5. **Visualization and Report** -- Render force plots, waterfall charts, and beeswarm plots. Compute cross-method rank correlation between SHAP and LIME importance rankings. Save all artifacts to `reports/`.

## Report Bus Integration

Produces `explainability_report.json` with keys: `shap_global_importance`, `lime_explanations`, `cross_method_correlation`, `method_used`, `samples_explained`, `visualization_paths`.

## Full Specification

Usage: `/explain-model <model_path> [--data <dataset>] [--method shap|lime|both] [--samples 100]`

Delegated to agent: **explainability-analyst**

See `commands/explain-model.md` for the complete workflow.
