#!/usr/bin/env python3
"""Static integration tests for the interface-design pipeline contract."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


PIPELINE = Path(__file__).parents[2]
REPOSITORY = Path(__file__).parents[4]
EXPECTED_STAGES = {
    "1-discovery-briefing": "dev-pipeline-1-discovery-briefing",
    "2-discovery-constitution": "dev-pipeline-2-discovery-constitution",
    "3-specification-specify": "dev-pipeline-3-specification-specify",
    "4-specification-clarify": "dev-pipeline-4-specification-clarify",
    "5-planning-plan": "dev-pipeline-5-planning-plan",
    "6-planning-interface-design": "dev-pipeline-6-planning-interface-design",
    "7-planning-checklist": "dev-pipeline-7-planning-checklist",
    "8-implementation-create-tasks": "dev-pipeline-8-implementation-create-tasks",
    "9-implementation-analyze": "dev-pipeline-9-implementation-analyze",
    "10-implementation-execute-task": "dev-pipeline-10-implementation-execute-task",
    "11-implementation-review-task": "dev-pipeline-11-implementation-review-task",
    "12-implementation-bugfix": "dev-pipeline-12-implementation-bugfix",
}
LEGACY_SKILL_NAMES = (
    "dev-pipeline-6-planning-checklist",
    "dev-pipeline-7-implementation-create-tasks",
    "dev-pipeline-8-implementation-analyze",
    "dev-pipeline-9-implementation-execute-task",
    "dev-pipeline-10-implementation-review-task",
    "dev-pipeline-11-implementation-bugfix",
)


def read(relative_path: str) -> str:
    return (REPOSITORY / relative_path).read_text(encoding="utf-8")


class DevPipelineInterfaceFlowTest(unittest.TestCase):
    def test_stage_directories_and_frontmatter_names_are_aligned(self) -> None:
        actual_stages = {path.name for path in PIPELINE.iterdir() if path.is_dir()}
        self.assertEqual(set(EXPECTED_STAGES), actual_stages)
        for directory, skill_name in EXPECTED_STAGES.items():
            skill_text = (PIPELINE / directory / "SKILL.md").read_text(encoding="utf-8")
            self.assertRegex(skill_text, rf"(?m)^name:\s*{re.escape(skill_name)}$")
            manifest = (PIPELINE / directory / "agents" / "openai.yaml").read_text(
                encoding="utf-8"
            )
            self.assertIn(f"${skill_name}", manifest)

    def test_pipeline_files_do_not_reference_legacy_skill_names(self) -> None:
        corpus = "\n".join(
            path.read_text(encoding="utf-8")
            for path in PIPELINE.rglob("*")
            if path.is_file()
            and path.suffix not in {".pyc", ".pyo"}
            and "__pycache__" not in path.parts
            and path.resolve() != Path(__file__).resolve()
        )
        for legacy_name in LEGACY_SKILL_NAMES:
            self.assertNotIn(legacy_name, corpus)

    def test_discovery_captures_channels_without_choosing_technology(self) -> None:
        guide = read(
            "skills/dev-pipeline/1-discovery-briefing/references/discovery-guide.md"
        )
        template = read(
            "skills/dev-pipeline/1-discovery-briefing/references/briefing-template.md"
        )
        self.assertIn("Discovery Guide: 8 Dimensões", guide)
        self.assertIn("Interfaces e Canais", guide)
        self.assertIn("Não é necessário escolher framework ou linguagem agora", guide)
        self.assertIn("Paridade Esperada", template)

    def test_spec_and_plan_separate_functional_and_technical_decisions(self) -> None:
        spec_template = read(
            "skills/dev-pipeline/3-specification-specify/templates/feature-spec.md"
        )
        plan_template = read(
            "skills/dev-pipeline/5-planning-plan/templates/plan.md"
        )
        catalog_template = read(
            "skills/dev-pipeline/5-planning-plan/templates/interaction-surfaces.md"
        )
        self.assertIn("## Interface Coverage", spec_template)
        self.assertIn("Do not include frameworks, languages", spec_template)
        self.assertIn("## Interaction Surface Architecture", plan_template)
        self.assertIn("Interface Design Applicability", plan_template)
        self.assertIn("Technology, Language and Runtime", catalog_template)

    def test_new_stage_has_required_resources_and_headless_contract(self) -> None:
        stage = PIPELINE / "6-planning-interface-design"
        for relative_path in (
            "templates/interface-spec.md",
            "references/graphical-ui.md",
            "references/cli-tui.md",
            "references/traceability.md",
            "scripts/validate-interface-spec.py",
        ):
            self.assertTrue((stage / relative_path).is_file(), relative_path)
        skill_text = (stage / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("N/A — sem superfície de interação humana", skill_text)
        self.assertIn("não criar `interface-spec.md` vazio", skill_text)

    def test_downstream_stages_consume_interface_contract(self) -> None:
        expectations = {
            "7-planning-checklist": ("interface-spec.md", "references/interface.md"),
            "8-implementation-create-tasks": ("interface-spec.md", "INT-*"),
            "9-implementation-analyze": ("interface-spec.md", "Cobertura de Superfícies"),
            "10-implementation-execute-task": ("interface-spec.md", "form factors"),
            "11-implementation-review-task": ("interface-spec.md", "INT-*"),
            "12-implementation-bugfix": ("interface-spec.md", "INT-*"),
        }
        for directory, fragments in expectations.items():
            skill_text = (PIPELINE / directory / "SKILL.md").read_text(encoding="utf-8")
            for fragment in fragments:
                self.assertIn(fragment, skill_text, f"{directory}: {fragment}")

    def test_traceability_reaches_tasks_and_verification_evidence(self) -> None:
        interface_template = read(
            "skills/dev-pipeline/6-planning-interface-design/templates/interface-spec.md"
        )
        tasks_skill = read(
            "skills/dev-pipeline/8-implementation-create-tasks/SKILL.md"
        )
        execute_skill = read(
            "skills/dev-pipeline/10-implementation-execute-task/SKILL.md"
        )
        review_skill = read(
            "skills/dev-pipeline/11-implementation-review-task/SKILL.md"
        )
        self.assertIn("Surface ID", interface_template)
        self.assertIn("Interaction ID", interface_template)
        self.assertIn("User Stories", interface_template)
        self.assertIn("Functional Requirements", interface_template)
        self.assertIn("Contracts", interface_template)
        self.assertIn("todo `INT-*` devem mapear", tasks_skill)
        self.assertIn("Evidências de Interface", execute_skill)
        self.assertIn("Interação sem evidência", review_skill)

    def test_readme_documents_new_sequence_and_migration(self) -> None:
        readme = read("SKILL.md")
        self.assertIn("Sapient AI Development", readme)
        self.assertIn("skills/dev-pipeline/", readme)


if __name__ == "__main__":
    unittest.main()
