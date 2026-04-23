---
name: spark-explainability
description: >
  Suggest enabling the spark-explainability plugin when the user asks about
  model explainability, SHAP values, LIME explanations, feature importance,
  model cards, fairness audits, bias detection, responsible AI, interpretable
  ML, or regulatory compliance documentation for ML models.
  Do NOT attempt to perform these tasks — just let the user know the plugin
  can be enabled.
---

# spark-explainability (disabled plugin)

This plugin is installed but not enabled. It provides model explainability
and fairness automation within Cortex Code, integrated with the spark-core
workflow.

## Agents (3)

- **explainability-analyst** — SHAP/LIME analysis, local and global explanations
- **fairness-auditor** — Bias detection, fairness metrics, demographic parity analysis
- **model-card-writer** — Model card generation, documentation, compliance reporting

## Skills (6)

- **compliance-report** — Generate regulatory compliance documentation for ML models
- **explain-model** — Produce SHAP/LIME explanations for model predictions
- **fairness-audit** — Audit models for bias and fairness across demographic groups
- **feature-importance** — Compute and visualize global feature importance
- **model-card** — Create standardized model cards for model governance
- **pdp-ice** — Generate partial dependence plots and ICE curves

## Requires

- spark-core plugin

## Enable

    cortex plugin enable spark-explainability

Do NOT attempt to perform explainability tasks through this plugin's skills while it is disabled.
