# /pdp-ice

Generate Partial Dependence and Individual Conditional Expectation (ICE) plots.

## Usage

```
/pdp-ice <model_path> --data <dataset> [--features <f1,f2,f3>] [--interactions f1:f2] [--grid-resolution 50] [--target-col <col>]
```

- `model_path`: path to fitted model (`.pkl`, `.joblib`, `.h5`, `.pt`)
- `--data`: dataset for computing partial dependence (CSV or Parquet)
- `--features`: comma-separated features to plot (default: top 6 by importance)
- `--interactions`: colon-separated feature pairs for 2D PDP (e.g., `age:income`)
- `--grid-resolution`: number of grid points per feature (default: 50)
- `--target-col`: target column name (auto-detected if not specified)

## Workflow

### Stage 0: Environment Check

1. Check if `ml_utils.py` exists in `src/` — if missing, copy from core plugin (`~/.claude/plugins/*/templates/ml_utils.py`)
2. Check if `explainability_utils.py` exists in `src/` — if missing, copy from this plugin's `templates/explainability_utils.py`
3. Verify model file exists and is loadable
4. Verify dataset contains specified features

### Stage 1: Feature Selection

1. If `--features` not specified:
   - Compute quick permutation importance
   - Select top 6 features by importance
2. Validate feature names exist in dataset
3. Determine feature types (numeric, categorical)
4. Report: selected features, feature types, grid resolution

### Stage 2: 1D Partial Dependence Plots

For each selected feature:

1. Create feature grid:
   - Numeric: `--grid-resolution` evenly spaced values between min and max
   - Categorical: all unique values
2. Compute partial dependence:
   - For each grid value: set all rows to that value, compute mean prediction
3. Compute ICE curves:
   - For each sample: compute prediction at each grid value
4. Generate combined PDP + ICE plot:
   - ICE curves as thin transparent lines
   - PDP as thick bold line (mean of ICE curves)
   - Mark feature distribution (rug plot)
5. Save plots to `reports/pdp_ice_plots/`

### Stage 3: 2D Partial Dependence (if --interactions provided)

For each feature pair:

1. Create 2D feature grid (grid_resolution x grid_resolution)
2. Compute partial dependence at each grid point
3. Generate contour plot / heatmap
4. Identify interaction effects (non-additive patterns)
5. Save to `reports/pdp_ice_plots/`

### Stage 4: Centered ICE (c-ICE) Plots

1. For each feature: subtract each ICE curve's value at the reference point
2. Reference point: feature median or user-specified
3. Generate c-ICE plots (reveals heterogeneous effects hidden in PDP)
4. Identify features with high ICE variance (strong interaction effects)

### Stage 5: Key Findings

1. Summarize relationship type per feature:
   - Monotonic increasing/decreasing
   - Non-linear (U-shape, threshold, step)
   - Flat (no effect)
2. Identify strongest interaction effects from 2D PDP
3. Flag features with high ICE heterogeneity (strong individual variation)

### Stage 6: Report

```python
from ml_utils import save_agent_report
save_agent_report("explainability-analyst", {
    "status": "completed",
    "features_analyzed": features,
    "relationship_types": feature_relationships,
    "interactions_analyzed": interaction_pairs,
    "ice_heterogeneity": heterogeneity_scores,
    "plot_files": plot_files,
    "key_findings": key_findings,
    "recommendations": recommendations
})
```

Write PDP/ICE report to `reports/pdp_ice_report.json`.
Print: feature relationships, interaction effects, high-heterogeneity flags, plot file paths.
