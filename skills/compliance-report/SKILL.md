---
name: compliance-report
description: "Generate regulatory compliance documentation. EU AI Act, SR 11-7 (OCC), model risk management, conformity assessment, and gap analysis."
aliases: [regulatory compliance, eu ai act, sr 11-7, model risk, model governance, compliance check]
extends: ml-automation
user_invocable: true
---

# Compliance Report

Generate regulatory compliance documentation for model deployments. Covers EU AI Act (risk classification, conformity assessment, transparency obligations), SR 11-7 (model development, validation, governance), and general model risk management. Includes automated risk assessment, compliance gap analysis, and prioritized remediation checklists.

## When to Use

- A model is being deployed in a regulated domain (financial services, healthcare, hiring) and needs documented compliance evidence.
- You need to assess EU AI Act risk classification (high, limited, minimal) and generate the corresponding conformity assessment checklist.
- Internal model risk management requires SR 11-7 style documentation covering development, validation, and ongoing monitoring.
- You want a gap analysis that cross-references existing project artifacts against regulatory requirements and highlights what is missing.

## Workflow

1. **Environment Check** -- Verify output directory. Scan for existing report bus artifacts (model card, fairness report, explainability report) that can serve as compliance evidence.
2. **Risk Assessment** -- Classify the model by use case into the appropriate risk tier (EU AI Act: unacceptable, high, limited, minimal; SR 11-7: critical, high, medium, low). Factor in data sensitivity, decision impact, and autonomy level.
3. **Framework Mapping** -- For each selected regulatory framework, enumerate the applicable requirements. Map existing artifacts and documentation to specific requirements, noting which are satisfied.
4. **Gap Analysis** -- Identify requirements that lack supporting evidence. Prioritize gaps by severity (blocking vs. advisory). Generate remediation actions with effort estimates.
5. **Report Generation** -- Assemble the compliance report with executive summary, risk classification, per-framework requirement matrices, gap analysis, and remediation checklist. Output in the requested format.

## Report Bus Integration

Consumes `model_card_report.json`, `fairness_report.json`, `explainability_report.json` when available. Produces `compliance_report.json` with keys: `risk_classification`, `framework`, `requirements_met`, `requirements_gaps`, `remediation_checklist`, `compliance_score`.

## Full Specification

Usage: `/compliance-report [--model <path>] [--framework eu-ai-act|sr-11-7|all] [--risk-level high|limited|minimal]`

Delegated to agent: **model-card-writer**

See `commands/compliance-report.md` for the complete workflow.
