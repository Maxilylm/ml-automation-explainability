# /compliance-report

Generate regulatory compliance documentation for a model deployment.

## Usage

```
/compliance-report [--model <model_path>] [--framework eu-ai-act|sr-11-7|all] [--risk-level high|limited|minimal] [--format md|html|json]
```

- `--model`: path to fitted model (auto-detected from `models/` if not specified)
- `--framework`: regulatory framework (default: all)
- `--risk-level`: risk classification (auto-assessed if not specified)
- `--format`: output format (default: md)

## Workflow

### Stage 0: Environment Check

1. Check if `ml_utils.py` exists in `src/` — if missing, copy from core plugin (`~/.claude/plugins/*/templates/ml_utils.py`)
2. Check if `explainability_utils.py` exists in `src/` — if missing, copy from this plugin's `templates/explainability_utils.py`
3. Detect model artifacts and existing reports
4. Detect existing fairness audit, explainability, and model card reports

### Stage 1: Risk Assessment

1. Assess model risk level based on:
   - Use case domain (healthcare, finance, criminal justice = high risk)
   - Data sensitivity (PII, protected attributes = higher risk)
   - Decision impact (automated decisions affecting individuals = higher risk)
   - Model complexity (black-box models = higher documentation burden)
2. Map to EU AI Act risk categories:
   - **Unacceptable**: social scoring, real-time biometric identification
   - **High**: credit scoring, recruitment, education, law enforcement
   - **Limited**: chatbots, emotion recognition, deep fakes
   - **Minimal**: spam filters, recommendation systems
3. Report: assessed risk level, classification rationale

### Stage 2: EU AI Act Compliance (if framework includes eu-ai-act)

1. **Conformity Assessment**
   - Risk management system documentation
   - Data governance and dataset documentation
   - Technical documentation requirements
   - Record-keeping requirements
   - Transparency obligations
   - Human oversight provisions
   - Accuracy, robustness, and cybersecurity requirements

2. **Article 13 — Transparency**
   - Model description and intended purpose
   - Performance metrics and limitations
   - Human oversight instructions
   - Expected lifetime and maintenance schedule

3. **Article 17 — Quality Management**
   - Data management procedures
   - Model training and testing procedures
   - Monitoring and incident reporting procedures

### Stage 3: SR 11-7 Compliance (if framework includes sr-11-7)

1. **Model Development**
   - Conceptual soundness assessment
   - Data quality and representativeness
   - Developmental evidence documentation
   - Implementation verification

2. **Model Validation**
   - Independent validation requirements
   - Outcomes analysis
   - Benchmarking against alternatives
   - Sensitivity analysis documentation

3. **Model Use and Governance**
   - Model inventory entry
   - Usage and limitations documentation
   - Ongoing monitoring plan
   - Trigger-based review criteria
   - Model performance degradation thresholds

### Stage 4: Compliance Gap Analysis

1. Cross-reference existing documentation against regulatory requirements
2. Identify gaps:
   - Missing documentation sections
   - Insufficient evidence for requirements
   - Missing fairness assessments
   - Missing explainability artifacts
3. Generate remediation checklist with priority levels

### Stage 5: Report

```python
from ml_utils import save_agent_report
save_agent_report("model-card-writer", {
    "status": "completed",
    "risk_level": risk_level,
    "frameworks": frameworks_covered,
    "compliance_score": {
        "eu_ai_act": eu_score_pct,
        "sr_11_7": sr_score_pct
    },
    "gaps": compliance_gaps,
    "remediation_checklist": checklist,
    "output_files": output_files,
    "recommendations": recommendations
})
```

Write compliance report to `reports/compliance_report.{md|html|json}`.
Print: risk level, compliance scores per framework, gap count, top priority remediations.
