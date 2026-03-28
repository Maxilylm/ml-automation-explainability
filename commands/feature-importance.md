# /feature-importance

Compute and visualize feature importance using multiple methods. Compare rankings across methods.

## Usage

```
/feature-importance <model_path> --data <dataset> [--methods permutation,shap,builtin] [--n-repeats 10] [--target-col <col>]
```

- `model_path`: path to fitted model (`.pkl`, `.joblib`, `.h5`, `.pt`)
- `--data`: dataset for computing importance (CSV or Parquet)
- `--methods`: comma-separated importance methods (default: all available)
- `--n-repeats`: number of repeats for permutation importance (default: 10)
- `--target-col`: target column name (auto-detected if not specified)

## Workflow

### Stage 0: Environment Check

1. Check if `ml_utils.py` exists in `src/` — if missing, copy from core plugin (`~/.claude/plugins/*/templates/ml_utils.py`)
2. Check if `explainability_utils.py` exists in `src/` — if missing, copy from this plugin's `templates/explainability_utils.py`
3. Verify model file exists and is loadable
4. Verify dataset file exists and feature names match model expectations

### Stage 1: Model and Data Loading

1. Load fitted model and identify type
2. Load dataset and separate features from target
3. Identify available importance methods for model type:
   - Tree-based: builtin, permutation, shap
   - Linear: coefficient-based, permutation, shap
   - Neural network: permutation, shap (gradient)
   - Any model: permutation, shap (kernel)
4. Report: model type, feature count, available methods

### Stage 2: Built-in Importance (tree-based / linear models)

1. Extract built-in feature importance:
   - Tree-based: `model.feature_importances_` (Gini/gain-based)
   - Linear: `abs(model.coef_)` (coefficient magnitude)
2. Rank features by importance
3. Report: top 20 features with importance scores

### Stage 3: Permutation Importance

1. Compute permutation importance:
   - For each feature: shuffle column, measure performance drop
   - Repeat `--n-repeats` times for stability
   - Scoring metric: model's default or user-specified
2. Compute mean and standard deviation per feature
3. Identify features with high variance (unstable importance)
4. Report: top 20 features with mean importance and CI

### Stage 4: SHAP-Based Importance

1. Compute SHAP values (using appropriate explainer for model type)
2. Derive global importance: mean |SHAP value| per feature
3. Report: top 20 features by SHAP importance

### Stage 5: Cross-Method Comparison

1. Build comparison table: feature x method importance ranking
2. Compute Spearman rank correlation between all method pairs
3. Identify features with high rank disagreement (rank difference > 10)
4. Identify consistently important features (top 10 across all methods)
5. Identify suspicious features (high in one method, low in others)
6. Generate consolidated importance visualization

### Stage 6: Report

```python
from ml_utils import save_agent_report
save_agent_report("explainability-analyst", {
    "status": "completed",
    "model_type": model_type,
    "methods_used": methods,
    "feature_count": feature_count,
    "top_features_consensus": consensus_top_10,
    "rank_correlations": rank_corr_matrix,
    "disagreement_features": disagreement_features,
    "importance_tables": importance_per_method,
    "recommendations": recommendations
})
```

Write importance report to `reports/feature_importance_report.json`.
Print: consensus top features, cross-method correlation, disagreement flags.
