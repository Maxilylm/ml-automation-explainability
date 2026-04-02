---
name: fairness-audit
description: "Audit models for bias and fairness across protected groups. Demographic parity, equalized odds, disparate impact, intersectional analysis."
aliases: [bias audit, fairness check, model bias, responsible ai audit, discrimination check]
extends: spark
user_invocable: true
---

# Fairness Audit

Run comprehensive fairness audit on model predictions across protected groups. Computes group fairness metrics (demographic parity, equalized odds, equal opportunity, predictive parity), individual fairness metrics (disparate impact ratio, counterfactual fairness), intersectional analysis, and generates bias mitigation recommendations.

## When to Use

- You need to verify that a model does not discriminate against protected groups before production deployment.
- Regulatory or internal policy requires documented fairness evidence (e.g., 4/5ths rule for disparate impact).
- You want intersectional analysis across multiple protected attributes (e.g., race x gender) to catch compounding bias.
- A model is being retrained and you need to compare fairness metrics against a previous baseline.

## Workflow

1. **Environment Check** -- Verify required packages (numpy, pandas). Warn if optional fairness libraries (fairlearn, aif360) are available for extended analysis.
2. **Data Preparation** -- Load model predictions and ground-truth labels. Identify and validate protected attribute columns. Encode categorical groups and flag low-count groups that may produce unreliable metrics.
3. **Group Metrics Computation** -- For each protected group, compute positive prediction rate, true positive rate, false positive rate, and precision. Derive demographic parity difference, equalized odds difference, equal opportunity difference, and disparate impact ratio.
4. **Intersectional Analysis** -- Cross protected attributes to form intersectional subgroups. Recompute all fairness metrics at the intersectional level. Flag subgroups where disparity exceeds the configured threshold.
5. **Recommendations** -- Generate prioritized mitigation recommendations: re-sampling, threshold tuning, adversarial debiasing, or post-processing calibration. Map each recommendation to the specific metric it addresses.

## Report Bus Integration

Produces `fairness_report.json` with keys: `group_metrics`, `demographic_parity_difference`, `equalized_odds_difference`, `disparate_impact_ratio`, `intersectional_results`, `flags`, `is_fair`, `recommendations`.

## Full Specification

Usage: `/fairness-audit <model_path> --data <dataset> --protected <col1,col2> [--threshold 0.8]`

Delegated to agent: **fairness-auditor**

See `commands/fairness-audit.md` for the complete workflow.
