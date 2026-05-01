# spark-explainability — Cortex Code Extension

Model explainability and fairness. SHAP, LIME, feature importance, model cards, fairness audits, and regulatory compliance documentation. Requires spark-core installed.

## Available Agents

| Agent | When to use |
|---|---|
| `explainability-analyst` | User wants to explain model predictions using SHAP, LIME, PDP/ICE plots, or feature importance |
| `fairness-auditor` | User wants to audit a model for bias, compute fairness metrics, or detect disparate impact across groups |
| `model-card-writer` | User wants to create a model card, compliance report, or regulatory documentation |

## Available Skills

| Skill | Trigger |
|---|---|
| `/explain-model` | "explain this model", "SHAP values", "LIME explanations", "why did the model predict X" |
| `/feature-importance` | "feature importance", "which features matter most", "variable importance ranking" |
| `/pdp-ice` | "partial dependence plot", "PDP", "ICE plot", "how does feature X affect predictions" |
| `/fairness-audit` | "fairness audit", "check for bias", "disparate impact analysis", "demographic parity" |
| `/model-card` | "write a model card", "document the model", "model documentation" |
| `/compliance-report` | "compliance report", "regulatory documentation", "GDPR model documentation", "AI Act report" |

## Routing

- SHAP, LIME, PDP/ICE, feature importance → `explainability-analyst`
- Bias detection, fairness metrics → `fairness-auditor`
- Model cards, compliance docs → `model-card-writer`
- Fallback → spark-core orchestrator
