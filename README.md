# ml-automation-explainability

Model explainability and fairness extension for [ml-automation](https://github.com/Maxilylm/ml-automation-core).

## Prerequisites

- [ml-automation](https://github.com/Maxilylm/ml-automation-core) core plugin (>= v1.8.0)
- Claude Code CLI
- Python ML libraries (scikit-learn, XGBoost, LightGBM, etc.) for model loading
- SHAP/LIME packages for explanation generation

## Installation

```bash
claude plugin add /path/to/ml-automation-explainability
```

## What's Included

### Agents

| Agent | Purpose | Hooks Into |
|---|---|---|
| `explainability-analyst` | SHAP, LIME, feature importance, PDP/ICE plots | `after-evaluation` |
| `fairness-auditor` | Bias audits, demographic parity, equalized odds, disparate impact | `after-evaluation` |
| `model-card-writer` | Model cards, regulatory compliance documentation | *(direct invocation)* |

### Commands

| Command | Purpose |
|---|---|
| `/explain-model` | Generate SHAP/LIME explanations for a trained model |
| `/fairness-audit` | Run fairness audit on model predictions across protected groups |
| `/model-card` | Generate a model card (standardized model documentation) |
| `/feature-importance` | Compute and visualize feature importance (permutation, SHAP, built-in) |
| `/pdp-ice` | Generate Partial Dependence and ICE plots |
| `/compliance-report` | Generate regulatory compliance documentation |

## Getting Started

```bash
# Generate SHAP explanations
/explain-model models/classifier.pkl --data data/test.csv --method shap

# Run fairness audit
/fairness-audit models/classifier.pkl --data data/test.csv --protected gender,race

# Generate a model card
/model-card --model models/classifier.pkl --format md

# Compute feature importance
/feature-importance models/classifier.pkl --data data/test.csv --methods permutation,shap,builtin

# Generate PDP/ICE plots
/pdp-ice models/classifier.pkl --data data/test.csv --features age,income,credit_score

# Generate compliance report
/compliance-report --model models/classifier.pkl --framework eu-ai-act,sr-11-7
```

## How It Integrates

When installed alongside the core plugin:

1. **Automatic routing** -- Tasks mentioning explainability, fairness, SHAP, LIME, model cards, or bias are routed to explainability agents
2. **Core workflow hooks** -- When running `/team-coldstart`:
   - `explainability-analyst` fires at `after-evaluation` to generate model explanations
   - `fairness-auditor` fires at `after-evaluation` to audit for bias
3. **Core agent reuse** -- Commands use eda-analyst, developer, ml-theory-advisor from core

## License

MIT
