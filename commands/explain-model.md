# /explain-model

Generate SHAP/LIME explanations for a trained model. Produces global and local interpretability artifacts.

## Usage

```
/explain-model <model_path> [--data <dataset>] [--method shap|lime|both] [--samples 100] [--target-col <col>]
```

- `model_path`: path to fitted model (`.pkl`, `.joblib`, `.h5`, `.pt`, `.onnx`)
- `--data`: dataset used for explanation background (CSV or Parquet)
- `--method`: explanation method (default: shap)
- `--samples`: number of background samples for SHAP/LIME (default: 100)
- `--target-col`: target column name (auto-detected if not specified)

## Workflow

### Stage 0: Environment Check

1. Check if `ml_utils.py` exists in `src/` — if missing, copy from core plugin (`~/.claude/plugins/*/templates/ml_utils.py`)
2. Check if `explainability_utils.py` exists in `src/` — if missing, copy from this plugin's `templates/explainability_utils.py`
3. Verify model file exists and is loadable
4. Verify dataset file exists and is readable

### Stage 1: Model and Data Loading

1. Load fitted model from `model_path`:
   - `.pkl` / `.joblib` — scikit-learn, XGBoost, LightGBM via pickle/joblib
   - `.h5` — TensorFlow/Keras
   - `.pt` — PyTorch
   - `.onnx` — ONNX Runtime
2. Load dataset from `--data` (or auto-detect from `data/` directory)
3. Identify model type (tree-based, linear, neural network, ensemble)
4. Identify feature names and types from dataset
5. Report: model type, feature count, sample count, target variable

### Stage 2: SHAP Explanations (if method includes shap)

1. Select SHAP explainer based on model type:
   - Tree-based: `shap.TreeExplainer` (exact, fast)
   - Linear: `shap.LinearExplainer`
   - Neural network: `shap.DeepExplainer` or `shap.GradientExplainer`
   - Any model: `shap.KernelExplainer` (model-agnostic fallback)
2. Compute SHAP values for background samples
3. Generate global explanations:
   - Beeswarm plot (feature importance with direction)
   - Bar plot (mean absolute SHAP values)
   - SHAP interaction values (top feature pairs)
4. Generate local explanations for top 5 interesting predictions:
   - Force plot per prediction
   - Waterfall plot per prediction
5. Save plots to `reports/shap_plots/`
6. Save SHAP values matrix to `reports/shap_values.csv`

### Stage 3: LIME Explanations (if method includes lime)

1. Configure LIME explainer:
   - `LimeTabularExplainer` for structured data
   - Feature discretization settings
   - Number of perturbation samples (`--samples`)
2. Generate explanations for representative predictions:
   - Top 5 most confident predictions
   - Top 5 least confident predictions
   - Top 5 predictions closest to decision boundary
3. Extract per-prediction feature contributions
4. Save explanation HTML files to `reports/lime_explanations/`
5. Save feature contribution summary to `reports/lime_summary.csv`

### Stage 4: Feature Importance Comparison

1. Compute importance from multiple methods:
   - SHAP-based (mean |SHAP value|)
   - Permutation importance (model-agnostic)
   - Built-in importance (if tree-based model)
2. Rank features by each method
3. Compute rank correlation (Spearman) between methods
4. Identify features with high rank disagreement
5. Generate consolidated importance table

### Stage 5: Report

```python
from ml_utils import save_agent_report
save_agent_report("explainability-analyst", {
    "status": "completed",
    "model_type": model_type,
    "method": method,
    "feature_count": feature_count,
    "top_features": top_10_features,
    "shap_summary": shap_summary,
    "lime_summary": lime_summary,
    "importance_rank_correlation": rank_corr,
    "plot_files": plot_files,
    "recommendations": recommendations
})
```

Write explanation report to `reports/explainability_report.json`.
Print: top features, key SHAP findings, feature importance ranking, generated artifacts.
