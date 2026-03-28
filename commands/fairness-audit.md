# /fairness-audit

Run fairness audit on model predictions across protected groups. Compute group and individual fairness metrics.

## Usage

```
/fairness-audit <model_path> --data <dataset> --protected <col1,col2> [--target-col <col>] [--threshold 0.8]
```

- `model_path`: path to fitted model (`.pkl`, `.joblib`, `.h5`, `.pt`)
- `--data`: dataset with features and protected attributes (CSV or Parquet)
- `--protected`: comma-separated list of protected attribute columns
- `--target-col`: target column name (auto-detected if not specified)
- `--threshold`: disparate impact threshold (default: 0.8, i.e., 4/5ths rule)

## Workflow

### Stage 0: Environment Check

1. Check if `ml_utils.py` exists in `src/` — if missing, copy from core plugin (`~/.claude/plugins/*/templates/ml_utils.py`)
2. Check if `explainability_utils.py` exists in `src/` — if missing, copy from this plugin's `templates/explainability_utils.py`
3. Verify model file exists and is loadable
4. Verify dataset contains specified protected attribute columns
5. If `--protected` not provided, auto-detect potential protected attributes

### Stage 1: Data Preparation

1. Load model and dataset
2. Generate predictions (class labels and probabilities)
3. Validate protected attributes:
   - Check group sizes (warn if any group has < 30 samples)
   - Check for missing values in protected columns
   - Encode categorical groups
4. If target column available, load ground truth labels
5. Report: group distribution per protected attribute, prediction distribution

### Stage 2: Group Fairness Metrics

For each protected attribute:

1. **Demographic Parity**
   - Positive prediction rate per group
   - Demographic parity difference (max - min)
   - Statistical significance test (chi-squared)

2. **Equalized Odds**
   - True positive rate (TPR) per group
   - False positive rate (FPR) per group
   - Equalized odds difference

3. **Equal Opportunity**
   - TPR per group
   - Equal opportunity difference

4. **Predictive Parity**
   - Precision per group
   - Predictive parity difference

5. **Calibration**
   - Expected vs. observed positive rate per probability bin per group
   - Calibration difference

### Stage 3: Individual Fairness Metrics

1. **Disparate Impact Ratio**
   - Ratio of positive rates: min(group_rate) / max(group_rate)
   - Flag if below `--threshold` (default: 0.8)

2. **Counterfactual Fairness** (if feasible)
   - For each sample: flip protected attribute value
   - Compute prediction change rate
   - Flag samples with prediction flip

3. **Consistency Score**
   - For each sample: find k nearest neighbors (excluding protected attributes)
   - Compute prediction agreement rate among neighbors

### Stage 4: Intersectional Analysis

1. Create intersectional groups (e.g., race x gender)
2. Compute demographic parity for intersectional groups
3. Identify most disadvantaged intersectional group
4. Flag intersectional disparities not visible in single-attribute analysis

### Stage 5: Bias Mitigation Recommendations

1. Based on audit findings, recommend:
   - **Pre-processing**: resampling, reweighting, feature removal
   - **In-processing**: fairness constraints, adversarial debiasing
   - **Post-processing**: threshold adjustment per group, reject option
2. Estimate performance-fairness trade-off
3. Generate actionable remediation plan

### Stage 6: Report

```python
from ml_utils import save_agent_report
save_agent_report("fairness-auditor", {
    "status": "completed",
    "protected_attributes": protected_attrs,
    "group_metrics": {
        attr: {
            "demographic_parity": dp_diff,
            "equalized_odds": eo_diff,
            "disparate_impact_ratio": di_ratio,
            "flagged": is_flagged
        } for attr in protected_attrs
    },
    "intersectional_findings": intersectional_results,
    "counterfactual_flip_rate": flip_rate,
    "mitigation_recommendations": recommendations,
    "regulatory_notes": regulatory_notes
})
```

Write fairness report to `reports/fairness_audit_report.json`.
Print: group metrics table, flagged violations, disparate impact ratios, recommendations.
