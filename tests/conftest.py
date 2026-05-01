"""Shared pytest fixtures for ml-automation-explainability."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any

import pytest


@pytest.fixture
def mock_llm_response() -> dict[str, Any]:
    """Return a mock LLM response for testing."""
    return {
        "id": "msg_test_12345",
        "type": "message",
        "role": "assistant",
        "content": [{"type": "text", "text": "Mock response from LLM"}],
        "model": "claude-3-5-sonnet-20241022",
        "stop_reason": "end_turn",
        "usage": {"input_tokens": 100, "output_tokens": 50},
    }


@pytest.fixture
def sample_dataset() -> dict[str, Any]:
    """Return a sample dataset for testing."""
    return {
        "features": ["age", "income", "credit_score", "employment_length"],
        "target": "loan_approved",
        "n_samples": 1000,
        "n_features": 4,
        "data": [
            {"age": 35, "income": 75000, "credit_score": 720, "employment_length": 5, "loan_approved": 1},
            {"age": 28, "income": 45000, "credit_score": 650, "employment_length": 2, "loan_approved": 0},
        ],
    }


@pytest.fixture
def temp_workspace(tmp_path: Path) -> Path:
    """Return a temporary workspace directory for testing."""
    workspace = tmp_path / "workspace"
    workspace.mkdir(exist_ok=True)

    # Create basic structure for testing
    (workspace / "models").mkdir(exist_ok=True)
    (workspace / "data").mkdir(exist_ok=True)
    (workspace / "reports").mkdir(exist_ok=True)

    return workspace
