---
name: explain-model
description: "Generate SHAP and LIME explanations for trained ML models. Produces global feature importance, local prediction explanations, and interpretability artifacts."
aliases: [shap, lime, model explanation, explain predictions, model interpretability]
extends: ml-automation
user_invocable: true
---

# Explain Model

Generate comprehensive model explanations using SHAP (TreeSHAP, KernelSHAP, DeepSHAP) and LIME. Produces global feature importance rankings, local prediction explanations (force plots, waterfall plots), feature interaction analysis, and cross-method importance comparison with rank correlation.

## Full Specification

See `commands/explain-model.md` for the complete workflow.
