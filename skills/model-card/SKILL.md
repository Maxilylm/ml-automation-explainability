---
name: model-card
description: "Generate standardized model cards (Google/Mitchell et al. format). Model details, intended use, metrics, ethical considerations, and caveats."
aliases: [model documentation, model sheet, model factsheet, model report]
extends: spark
user_invocable: true
---

# Model Card

Generate a standardized model card following the Google/Mitchell et al. framework. Aggregates model details, intended use cases, training and evaluation data descriptions, performance metrics with confidence intervals, ethical considerations, fairness analysis, known limitations, and deployment recommendations into a structured document.

## When to Use

- A model is approaching production readiness and needs formal documentation for review or handoff.
- Regulatory or governance requirements demand a standardized model factsheet (e.g., SR 11-7, EU AI Act transparency obligations).
- You want to auto-populate a model card by pulling from existing report bus artifacts (evaluation reports, fairness audits, explainability results).

## Workflow

1. **Environment Check** -- Verify output directory exists. Detect available report bus artifacts to pre-fill card sections.
2. **Information Gathering** -- Scan the project for model metadata (framework, type, hyperparameters), training data descriptions, evaluation metrics, fairness reports, and explainability artifacts. Prompt for any missing required fields (intended use, limitations).
3. **Card Generation** -- Assemble all sections into the chosen format (Markdown, HTML, or JSON). Compute a completeness score (0-1) and list missing sections. Write the output file to `reports/`.

## Report Bus Integration

Consumes `evaluation_report.json`, `fairness_report.json`, `explainability_report.json` when available. Produces `model_card_report.json` with keys: `content`, `format`, `completeness_score`, `missing_sections`.

## Full Specification

Usage: `/model-card [--model <path>] [--format md|html|json] [--template standard|regulatory]`

Delegated to agent: **model-card-writer**

See `commands/model-card.md` for the complete workflow.
