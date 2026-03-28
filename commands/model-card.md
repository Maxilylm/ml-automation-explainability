# /model-card

Generate a model card — standardized model documentation following the Google/Mitchell et al. framework.

## Usage

```
/model-card [--model <model_path>] [--format md|html|json] [--template standard|regulatory]
```

- `--model`: path to fitted model (auto-detected from `models/` if not specified)
- `--format`: output format (default: md)
- `--template`: card template (default: standard)

## Workflow

### Stage 0: Environment Check

1. Check if `ml_utils.py` exists in `src/` — if missing, copy from core plugin (`~/.claude/plugins/*/templates/ml_utils.py`)
2. Check if `explainability_utils.py` exists in `src/` — if missing, copy from this plugin's `templates/explainability_utils.py`
3. Detect model artifacts in `models/` directory
4. Detect existing reports from other agents (evaluation, fairness, explainability)

### Stage 1: Information Gathering

1. Scan project for model metadata:
   - Model files in `models/` — infer type, framework, size
   - Training scripts — infer hyperparameters, training process
   - Data files in `data/` — infer dataset characteristics
   - Evaluation reports — extract performance metrics
   - Fairness audit reports — extract fairness metrics
   - Explainability reports — extract feature importance
2. Scan for README, docstrings, and configuration files
3. Identify information gaps that require user input
4. Report: gathered metadata, missing information list

### Stage 2: Model Card Assembly

Build model card sections:

1. **Model Details**
   - Model name and version
   - Model type and architecture
   - Framework and library versions
   - Training date and author
   - License

2. **Intended Use**
   - Primary intended uses
   - Primary intended users
   - Out-of-scope uses

3. **Factors**
   - Relevant factors (demographic, environmental, instrumental)
   - Evaluation factors

4. **Metrics**
   - Performance metrics with values and confidence intervals
   - Decision thresholds and variation approaches
   - Performance across subgroups (from fairness report)

5. **Training Data**
   - Dataset description, size, features
   - Preprocessing steps
   - Feature engineering summary

6. **Evaluation Data**
   - Test set description
   - Evaluation methodology
   - Cross-validation strategy

7. **Ethical Considerations**
   - Bias analysis summary (from fairness audit)
   - Fairness metrics
   - Known limitations and failure modes

8. **Caveats and Recommendations**
   - Known caveats
   - Deployment recommendations
   - Monitoring requirements

### Stage 3: Formatting

Based on `--format`:

- **Markdown**: generate `model_card.md` with headers, tables, badge indicators
- **HTML**: generate `model_card.html` with styled layout, charts, expandable sections
- **JSON**: generate `model_card.json` with structured machine-readable format

### Stage 4: Report

```python
from ml_utils import save_agent_report
save_agent_report("model-card-writer", {
    "status": "completed",
    "model_name": model_name,
    "format": output_format,
    "output_file": output_path,
    "sections_completed": completed_sections,
    "sections_with_gaps": sections_with_gaps,
    "completeness_score": completeness_pct,
    "recommendations": recommendations
})
```

Write model card to `reports/model_card.{md|html|json}`.
Print: completeness score, sections with gaps, output file path.
