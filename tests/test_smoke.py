"""Smoke tests for ml-automation-explainability — validate plugin layout invariants."""
from __future__ import annotations

import json
import re
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent


def test_manifest_validity() -> None:
    """Validate .cortex-plugin/plugin.json parses and has required fields."""
    manifest_path = PLUGIN_ROOT / ".cortex-plugin" / "plugin.json"

    assert manifest_path.exists(), f"Manifest not found at {manifest_path}"

    with open(manifest_path) as f:
        manifest = json.load(f)

    required_fields = ["name", "version", "description", "cortex"]
    for field in required_fields:
        assert field in manifest, f"Missing required field: {field}"

    assert manifest["name"].startswith("spark-"), f"Plugin name must start with 'spark-', got: {manifest['name']}"

    cortex = manifest.get("cortex", {})
    assert isinstance(cortex, dict), "cortex field must be a dict"


def test_agents_md_referential_integrity() -> None:
    """Validate that every agents/*.md stem and skills/*/ dir is mentioned in AGENTS.md."""
    agents_md_path = PLUGIN_ROOT / "AGENTS.md"
    assert agents_md_path.exists(), f"AGENTS.md not found at {agents_md_path}"

    with open(agents_md_path) as f:
        agents_md_text = f.read()

    # Check that all agent files are mentioned in AGENTS.md
    agents_dir = PLUGIN_ROOT / "agents"
    if agents_dir.exists():
        agent_files = sorted([f.stem for f in agents_dir.glob("*.md")])
        for agent_name in agent_files:
            assert agent_name in agents_md_text, f"Agent '{agent_name}' not referenced in AGENTS.md"

    # Check that all skill directories are mentioned in AGENTS.md
    skills_dir = PLUGIN_ROOT / "skills"
    if skills_dir.exists():
        skill_dirs = sorted([d.name for d in skills_dir.iterdir() if d.is_dir()])
        for skill_name in skill_dirs:
            # Skills are referenced with a leading slash in AGENTS.md (e.g., `/skill-name`)
            assert f"`/{skill_name}`" in agents_md_text, f"Skill '{skill_name}' not referenced in AGENTS.md"
