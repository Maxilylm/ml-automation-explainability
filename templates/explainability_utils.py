"""
Explainability utilities for the ml-automation-explainability extension plugin.

Requires ml_utils.py from the ml-automation core plugin to be present
in the same directory (copied via Stage 0 of explainability commands).
"""

import os
import json
import re
from pathlib import Path


# --- Relevance Detection ---

EXPLAINABILITY_INDICATORS = {
    "sklearn",
    "xgboost",
    "lightgbm",
    "catboost",
    "tensorflow",
    "torch",
    "keras",
    "shap",
    "lime",
    "interpret",
    "alibi",
    "eli5",
    "aif360",
    "fairlearn",
}

MODEL_FILE_EXTENSIONS = [".pkl", ".joblib", ".h5", ".pt", ".onnx", ".pmml", ".cbm"]

PROTECTED_ATTRIBUTE_PATTERNS = [
    r"(?i)^(gender|sex|race|ethnicity|religion|age|disability|nationality)$",
    r"(?i)^(marital_status|sexual_orientation|veteran_status|pregnancy)$",
    r"(?i)^(national_origin|citizenship|genetic_information)$",
    r"(?i).*(protected|sensitive|demographic).*",
]


def detect_explainability_relevance(project_path="."):
    """Check if project has model explainability indicators for relevance gating.

    Checks: ML library imports, model files, training data, evaluation reports,
    protected attributes in datasets.

    Args:
        project_path: root directory of the project

    Returns:
        dict with 'is_relevant': bool, 'indicators': list of found indicators,
        'has_model': bool, 'has_protected_attrs': bool
    """
    indicators = []
    project = Path(project_path)
    has_model = False
    has_protected_attrs = False

    # Check for model files
    models_dir = project / "models"
    if models_dir.is_dir():
        for ext in MODEL_FILE_EXTENSIONS:
            model_files = list(models_dir.glob(f"*{ext}"))
            if model_files:
                indicators.append(f"{len(model_files)} {ext} model files in models/")
                has_model = True

    # Check for model files in project root
    for ext in MODEL_FILE_EXTENSIONS:
        root_models = list(project.glob(f"*{ext}"))
        if root_models:
            indicators.append(f"{len(root_models)} {ext} files in project root")
            has_model = True

    # Check requirements for ML packages
    for req_file in ["requirements.txt", "pyproject.toml", "setup.py", "Pipfile"]:
        req_path = project / req_file
        if req_path.exists():
            content = req_path.read_text().lower()
            for pkg in EXPLAINABILITY_INDICATORS:
                if pkg in content:
                    indicators.append(f"{pkg} in {req_file}")

    # Check Python files for ML imports
    py_files = list(project.glob("**/*.py"))[:50]  # limit scan
    for py_file in py_files:
        try:
            content = py_file.read_text()
            for pkg in EXPLAINABILITY_INDICATORS:
                if f"import {pkg}" in content or f"from {pkg}" in content:
                    indicators.append(f"{pkg} import in {py_file.name}")
                    break
        except (UnicodeDecodeError, PermissionError):
            continue

    # Check for datasets with potential protected attributes
    csv_files = list(project.glob("**/*.csv"))[:10]
    for csv_file in csv_files:
        try:
            with open(csv_file) as f:
                header = f.readline().strip()
                columns = [c.strip().strip('"').strip("'") for c in header.split(",")]
                for col in columns:
                    for pattern in PROTECTED_ATTRIBUTE_PATTERNS:
                        if re.match(pattern, col):
                            indicators.append(f"Protected attribute '{col}' in {csv_file.name}")
                            has_protected_attrs = True
                            break
        except (UnicodeDecodeError, PermissionError):
            continue

    # Check for existing evaluation reports
    reports_dir = project / "reports"
    if reports_dir.is_dir():
        eval_reports = list(reports_dir.glob("*evaluation*"))
        if eval_reports:
            indicators.append(f"Evaluation reports found in reports/")

    return {
        "is_relevant": len(indicators) > 0,
        "indicators": indicators,
        "has_model": has_model,
        "has_protected_attrs": has_protected_attrs,
    }


# --- SHAP Computation ---

def compute_shap_values(model, X, method="auto", n_samples=100):
    """Compute SHAP values for a model and dataset.

    Selects the appropriate SHAP explainer based on model type.

    Args:
        model: fitted model object
        X: feature matrix (pandas DataFrame or numpy array)
        method: 'tree', 'linear', 'kernel', 'deep', or 'auto' (auto-detect)
        n_samples: number of background samples for KernelSHAP (default: 100)

    Returns:
        dict with 'shap_values' (numpy array), 'expected_value' (float or array),
        'feature_names' (list), 'method_used' (str),
        'global_importance' (dict: feature -> mean |SHAP|)
    """
    try:
        import shap
        import numpy as np
    except ImportError:
        raise ImportError("shap required. Install with: pip install shap")

    feature_names = list(X.columns) if hasattr(X, "columns") else [
        f"feature_{i}" for i in range(X.shape[1])
    ]

    # Auto-detect explainer
    if method == "auto":
        method = _detect_shap_method(model)

    # Select background data
    if hasattr(X, "iloc"):
        bg_idx = np.random.choice(len(X), min(n_samples, len(X)), replace=False)
        background = X.iloc[bg_idx]
    else:
        bg_idx = np.random.choice(len(X), min(n_samples, len(X)), replace=False)
        background = X[bg_idx]

    # Create explainer
    if method == "tree":
        explainer = shap.TreeExplainer(model)
        sv = explainer.shap_values(X)
    elif method == "linear":
        explainer = shap.LinearExplainer(model, background)
        sv = explainer.shap_values(X)
    elif method == "deep":
        explainer = shap.DeepExplainer(model, background)
        sv = explainer.shap_values(X)
    elif method == "kernel":
        explainer = shap.KernelExplainer(model.predict, background)
        sv = explainer.shap_values(X)
    else:
        raise ValueError(f"Unknown SHAP method: {method}")

    # Handle multi-output (classification)
    if isinstance(sv, list):
        # Use class 1 for binary classification, or stack for multi-class
        shap_values = sv[1] if len(sv) == 2 else np.stack(sv)
    else:
        shap_values = sv

    # Compute global importance
    if shap_values.ndim == 2:
        mean_abs_shap = np.mean(np.abs(shap_values), axis=0)
    else:
        mean_abs_shap = np.mean(np.abs(shap_values), axis=(0, -1))

    global_importance = {
        name: round(float(val), 6)
        for name, val in sorted(
            zip(feature_names, mean_abs_shap),
            key=lambda x: x[1],
            reverse=True,
        )
    }

    return {
        "shap_values": shap_values,
        "expected_value": explainer.expected_value,
        "feature_names": feature_names,
        "method_used": method,
        "global_importance": global_importance,
    }


def _detect_shap_method(model):
    """Detect the best SHAP method for a model type."""
    model_type = type(model).__name__.lower()
    module = type(model).__module__.lower() if type(model).__module__ else ""

    tree_types = [
        "randomforest", "gradientboosting", "xgb", "lgbm", "catboost",
        "decisiontree", "extratree", "adaboost",
    ]
    linear_types = ["linear", "logistic", "ridge", "lasso", "elasticnet", "sgd"]
    deep_types = ["sequential", "module", "model"]

    for t in tree_types:
        if t in model_type or t in module:
            return "tree"

    for t in linear_types:
        if t in model_type:
            return "linear"

    for t in deep_types:
        if t in model_type and ("torch" in module or "tensorflow" in module or "keras" in module):
            return "deep"

    return "kernel"


# --- LIME Computation ---

def compute_lime_explanations(model, X, n_samples=5000, num_features=10,
                               sample_indices=None):
    """Compute LIME explanations for selected predictions.

    Args:
        model: fitted model object with predict_proba or predict method
        X: feature matrix (pandas DataFrame or numpy array)
        n_samples: number of perturbation samples (default: 5000)
        num_features: number of features to show per explanation (default: 10)
        sample_indices: indices of samples to explain (default: first 5)

    Returns:
        dict with 'explanations' (list of per-sample dicts),
        'feature_names' (list), 'num_features': int
    """
    try:
        import lime
        import lime.lime_tabular
        import numpy as np
    except ImportError:
        raise ImportError("lime required. Install with: pip install lime")

    feature_names = list(X.columns) if hasattr(X, "columns") else [
        f"feature_{i}" for i in range(X.shape[1])
    ]

    X_arr = X.values if hasattr(X, "values") else X

    # Determine prediction function
    if hasattr(model, "predict_proba"):
        predict_fn = model.predict_proba
        mode = "classification"
    else:
        predict_fn = model.predict
        mode = "regression"

    # Create LIME explainer
    explainer = lime.lime_tabular.LimeTabularExplainer(
        X_arr,
        feature_names=feature_names,
        mode=mode,
        discretize_continuous=True,
    )

    # Select samples to explain
    if sample_indices is None:
        sample_indices = list(range(min(5, len(X_arr))))

    explanations = []
    for idx in sample_indices:
        exp = explainer.explain_instance(
            X_arr[idx],
            predict_fn,
            num_features=num_features,
            num_samples=n_samples,
        )

        feature_contributions = {
            feat: round(weight, 6) for feat, weight in exp.as_list()
        }

        explanations.append({
            "sample_index": int(idx),
            "prediction": float(predict_fn(X_arr[idx:idx + 1]).ravel()[0])
                if mode == "regression"
                else predict_fn(X_arr[idx:idx + 1]).tolist()[0],
            "feature_contributions": feature_contributions,
            "intercept": float(exp.intercept[0]) if hasattr(exp, "intercept") else None,
            "score": float(exp.score) if hasattr(exp, "score") else None,
        })

    return {
        "explanations": explanations,
        "feature_names": feature_names,
        "num_features": num_features,
    }


# --- Fairness Metrics ---

def compute_fairness_metrics(y_true, y_pred, protected_attr,
                              y_prob=None, threshold=0.8):
    """Compute group and individual fairness metrics.

    Args:
        y_true: ground truth labels (binary: 0/1)
        y_pred: predicted labels (binary: 0/1)
        protected_attr: protected attribute values (categorical)
        y_prob: predicted probabilities (optional, for calibration)
        threshold: disparate impact threshold (default: 0.8)

    Returns:
        dict with group metrics per group, overall metrics, and flags
    """
    import numpy as np

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    protected_attr = np.array(protected_attr)

    groups = sorted(set(protected_attr))
    group_metrics = {}

    for group in groups:
        mask = protected_attr == group
        n = mask.sum()
        y_t = y_true[mask]
        y_p = y_pred[mask]

        # Positive prediction rate
        ppr = y_p.mean() if n > 0 else 0.0

        # True positive rate (sensitivity / recall)
        positives = y_t == 1
        tpr = y_p[positives].mean() if positives.sum() > 0 else 0.0

        # False positive rate
        negatives = y_t == 0
        fpr = y_p[negatives].mean() if negatives.sum() > 0 else 0.0

        # Precision
        pred_pos = y_p == 1
        precision = y_t[pred_pos].mean() if pred_pos.sum() > 0 else 0.0

        group_metrics[str(group)] = {
            "count": int(n),
            "positive_prediction_rate": round(float(ppr), 4),
            "true_positive_rate": round(float(tpr), 4),
            "false_positive_rate": round(float(fpr), 4),
            "precision": round(float(precision), 4),
        }

    # Demographic parity
    pprs = [m["positive_prediction_rate"] for m in group_metrics.values()]
    dp_diff = round(max(pprs) - min(pprs), 4) if pprs else 0.0

    # Equalized odds
    tprs = [m["true_positive_rate"] for m in group_metrics.values()]
    fprs = [m["false_positive_rate"] for m in group_metrics.values()]
    eo_diff = round(
        max(max(tprs) - min(tprs), max(fprs) - min(fprs)), 4
    ) if tprs and fprs else 0.0

    # Equal opportunity
    eop_diff = round(max(tprs) - min(tprs), 4) if tprs else 0.0

    # Disparate impact ratio
    di_ratio = round(min(pprs) / max(pprs), 4) if pprs and max(pprs) > 0 else 0.0

    # Predictive parity
    precs = [m["precision"] for m in group_metrics.values()]
    pp_diff = round(max(precs) - min(precs), 4) if precs else 0.0

    # Flags
    flags = []
    if di_ratio < threshold:
        flags.append(f"Disparate impact ratio {di_ratio} < {threshold} (4/5ths rule)")
    if dp_diff > 0.1:
        flags.append(f"Demographic parity difference {dp_diff} > 0.1")
    if eo_diff > 0.1:
        flags.append(f"Equalized odds difference {eo_diff} > 0.1")

    return {
        "group_metrics": group_metrics,
        "demographic_parity_difference": dp_diff,
        "equalized_odds_difference": eo_diff,
        "equal_opportunity_difference": eop_diff,
        "disparate_impact_ratio": di_ratio,
        "predictive_parity_difference": pp_diff,
        "flags": flags,
        "threshold": threshold,
        "is_fair": len(flags) == 0,
    }


# --- Model Card Generation ---

def generate_model_card(model_info, metrics=None, fairness_info=None,
                         explainability_info=None, format="md"):
    """Generate a model card document.

    Args:
        model_info: dict with model metadata (name, version, type, framework,
                    intended_use, training_data, limitations)
        metrics: dict with performance metrics (optional)
        fairness_info: dict with fairness audit results (optional)
        explainability_info: dict with explainability results (optional)
        format: output format ('md', 'json', 'html')

    Returns:
        dict with 'content' (str), 'format' (str),
        'completeness_score' (float 0-1), 'missing_sections' (list)
    """
    sections = {}
    missing = []

    # Model Details
    if model_info.get("name"):
        sections["model_details"] = {
            "name": model_info.get("name", "Unknown"),
            "version": model_info.get("version", "1.0"),
            "type": model_info.get("type", "Unknown"),
            "framework": model_info.get("framework", "Unknown"),
            "author": model_info.get("author", "Unknown"),
            "date": model_info.get("date", "Unknown"),
            "license": model_info.get("license", "Not specified"),
        }
    else:
        missing.append("model_details")

    # Intended Use
    if model_info.get("intended_use"):
        sections["intended_use"] = {
            "primary_uses": model_info.get("intended_use", []),
            "out_of_scope": model_info.get("out_of_scope_use", []),
            "users": model_info.get("intended_users", []),
        }
    else:
        missing.append("intended_use")

    # Training Data
    if model_info.get("training_data"):
        sections["training_data"] = model_info["training_data"]
    else:
        missing.append("training_data")

    # Metrics
    if metrics:
        sections["metrics"] = metrics
    else:
        missing.append("metrics")

    # Ethical Considerations
    if fairness_info:
        sections["ethical_considerations"] = {
            "fairness_metrics": fairness_info,
            "bias_analysis": "See fairness audit report for details",
        }
    else:
        missing.append("ethical_considerations")

    # Explainability
    if explainability_info:
        sections["explainability"] = explainability_info
    else:
        missing.append("explainability")

    # Limitations
    if model_info.get("limitations"):
        sections["caveats_and_recommendations"] = {
            "limitations": model_info["limitations"],
            "recommendations": model_info.get("recommendations", []),
        }
    else:
        missing.append("caveats_and_recommendations")

    total_sections = 7
    completeness = round((total_sections - len(missing)) / total_sections, 2)

    if format == "json":
        content = json.dumps({"model_card": sections, "missing": missing}, indent=2)
    elif format == "html":
        content = _model_card_to_html(sections, missing)
    else:
        content = _model_card_to_markdown(sections, missing)

    return {
        "content": content,
        "format": format,
        "completeness_score": completeness,
        "missing_sections": missing,
    }


def _model_card_to_markdown(sections, missing):
    """Convert model card sections to Markdown format."""
    lines = ["# Model Card", ""]

    if "model_details" in sections:
        d = sections["model_details"]
        lines.extend([
            "## Model Details", "",
            f"- **Name:** {d['name']}",
            f"- **Version:** {d['version']}",
            f"- **Type:** {d['type']}",
            f"- **Framework:** {d['framework']}",
            f"- **Author:** {d['author']}",
            f"- **Date:** {d['date']}",
            f"- **License:** {d['license']}",
            "",
        ])

    if "intended_use" in sections:
        d = sections["intended_use"]
        lines.extend(["## Intended Use", ""])
        if d.get("primary_uses"):
            lines.append("### Primary Uses")
            for use in d["primary_uses"]:
                lines.append(f"- {use}")
            lines.append("")
        if d.get("out_of_scope"):
            lines.append("### Out-of-Scope Uses")
            for use in d["out_of_scope"]:
                lines.append(f"- {use}")
            lines.append("")

    if "training_data" in sections:
        d = sections["training_data"]
        lines.extend(["## Training Data", ""])
        if isinstance(d, dict):
            for k, v in d.items():
                lines.append(f"- **{k}:** {v}")
        else:
            lines.append(str(d))
        lines.append("")

    if "metrics" in sections:
        lines.extend(["## Metrics", ""])
        m = sections["metrics"]
        if isinstance(m, dict):
            lines.append("| Metric | Value |")
            lines.append("|---|---|")
            for k, v in m.items():
                lines.append(f"| {k} | {v} |")
        lines.append("")

    if "ethical_considerations" in sections:
        lines.extend(["## Ethical Considerations", ""])
        d = sections["ethical_considerations"]
        if isinstance(d.get("fairness_metrics"), dict):
            for k, v in d["fairness_metrics"].items():
                lines.append(f"- **{k}:** {v}")
        lines.append("")

    if "explainability" in sections:
        lines.extend(["## Explainability", ""])
        d = sections["explainability"]
        if isinstance(d, dict):
            for k, v in d.items():
                lines.append(f"- **{k}:** {v}")
        lines.append("")

    if "caveats_and_recommendations" in sections:
        d = sections["caveats_and_recommendations"]
        lines.extend(["## Caveats and Recommendations", ""])
        if d.get("limitations"):
            lines.append("### Limitations")
            for lim in d["limitations"]:
                lines.append(f"- {lim}")
            lines.append("")
        if d.get("recommendations"):
            lines.append("### Recommendations")
            for rec in d["recommendations"]:
                lines.append(f"- {rec}")
            lines.append("")

    if missing:
        lines.extend([
            "## Incomplete Sections", "",
            "The following sections require additional information:", "",
        ])
        for m in missing:
            lines.append(f"- {m}")
        lines.append("")

    return "\n".join(lines)


def _model_card_to_html(sections, missing):
    """Convert model card sections to HTML format."""
    html_parts = [
        "<!DOCTYPE html>",
        "<html><head>",
        "<meta charset='utf-8'>",
        "<title>Model Card</title>",
        "<style>",
        "body { font-family: -apple-system, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }",
        "h1 { color: #047857; border-bottom: 2px solid #047857; }",
        "h2 { color: #059669; }",
        "table { border-collapse: collapse; width: 100%; }",
        "th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }",
        "th { background-color: #10B981; color: white; }",
        ".warning { background-color: #FEF3C7; border-left: 4px solid #F59E0B; padding: 12px; margin: 10px 0; }",
        "</style>",
        "</head><body>",
        "<h1>Model Card</h1>",
    ]

    if "model_details" in sections:
        d = sections["model_details"]
        html_parts.append("<h2>Model Details</h2><ul>")
        for k, v in d.items():
            html_parts.append(f"<li><strong>{k}:</strong> {v}</li>")
        html_parts.append("</ul>")

    if "metrics" in sections:
        m = sections["metrics"]
        html_parts.append("<h2>Metrics</h2>")
        if isinstance(m, dict):
            html_parts.append("<table><tr><th>Metric</th><th>Value</th></tr>")
            for k, v in m.items():
                html_parts.append(f"<tr><td>{k}</td><td>{v}</td></tr>")
            html_parts.append("</table>")

    if missing:
        html_parts.append("<div class='warning'><strong>Incomplete sections:</strong> "
                          + ", ".join(missing) + "</div>")

    html_parts.append("</body></html>")
    return "\n".join(html_parts)


# --- Partial Dependence ---

def compute_partial_dependence(model, X, features, grid_resolution=50):
    """Compute partial dependence for specified features.

    Args:
        model: fitted model with predict method
        X: feature matrix (pandas DataFrame or numpy array)
        features: list of feature names or indices to compute PDP for
        grid_resolution: number of grid points per feature (default: 50)

    Returns:
        dict with per-feature results: 'grid_values', 'pdp_values',
        'ice_values' (per-sample), 'feature_name'
    """
    import numpy as np

    feature_names = list(X.columns) if hasattr(X, "columns") else [
        f"feature_{i}" for i in range(X.shape[1])
    ]

    X_arr = X.values if hasattr(X, "values") else np.array(X)
    results = {}

    for feature in features:
        # Resolve feature index
        if isinstance(feature, str):
            if feature in feature_names:
                feat_idx = feature_names.index(feature)
                feat_name = feature
            else:
                raise ValueError(f"Feature '{feature}' not found")
        else:
            feat_idx = feature
            feat_name = feature_names[feat_idx] if feat_idx < len(feature_names) else f"feature_{feat_idx}"

        # Create grid
        feat_values = X_arr[:, feat_idx]
        unique_vals = np.unique(feat_values)

        if len(unique_vals) <= grid_resolution:
            grid = np.sort(unique_vals)
        else:
            grid = np.linspace(feat_values.min(), feat_values.max(), grid_resolution)

        # Compute ICE curves (per sample)
        ice_values = np.zeros((len(X_arr), len(grid)))

        for i, val in enumerate(grid):
            X_temp = X_arr.copy()
            X_temp[:, feat_idx] = val
            preds = model.predict(X_temp)
            if preds.ndim > 1:
                preds = preds[:, -1]  # use last class for classification
            ice_values[:, i] = preds

        # PDP is the mean of ICE curves
        pdp_values = ice_values.mean(axis=0)

        results[feat_name] = {
            "grid_values": grid.tolist(),
            "pdp_values": pdp_values.tolist(),
            "ice_values": ice_values.tolist(),
            "feature_name": feat_name,
            "feature_index": feat_idx,
        }

    return results
