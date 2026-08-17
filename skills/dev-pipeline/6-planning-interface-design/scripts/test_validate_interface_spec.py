#!/usr/bin/env python3
"""Tests for validate-interface-spec.py."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("validate-interface-spec.py")
SKILL = Path(__file__).parents[1] / "SKILL.md"
STATES = (
    "initial",
    "loading",
    "empty",
    "ready",
    "processing",
    "success",
    "validation-error",
    "remote-error",
    "offline",
    "access-denied",
    "partial-stale",
)


def detail(
    interaction_id: str,
    surface_id: str,
    surface_type: str,
    change_type: str = "NEW",
    wireframe_requirement: str = "OPTIONAL",
    wireframe: str = "N/A — text is sufficient",
) -> str:
    state_rows = "\n".join(
        f"| {state} | Defined behavior | Retry or continue | Defined transition |"
        for state in STATES
    )
    return f"""### {interaction_id} — Example

**Surface**: {surface_id}
**Surface Type**: {surface_type}
**Change Type**: {change_type}
**Purpose**: Complete the user outcome
**Actors and Permissions**: Authorized operator
**Entry and Navigation**: Main menu to feature route
**Content and Data**: Required domain fields from the declared contract
**Actions and Behavior**: Submit, cancel, retry and return
**Validation and Feedback**: Inline validation and safe remote error
**Responsive/Adaptive Behavior**: Declared form factors and input methods
**Accessibility**: Keyboard, focus, labels, contrast and reduced motion
**Localization**: Message keys and regional formats
**Components and Design System**: Existing components and tokens
**Integration and Contracts**: contracts/example.md operation Example
**Telemetry**: Open and completion events without sensitive data
**Wireframe Requirement**: {wireframe_requirement}
**Wireframe**: {wireframe}

**States**:

| State | Expected Presentation | Available Actions | Transition/Exit |
|-------|-----------------------|-------------------|-----------------|
{state_rows}
"""


def document(
    surfaces: list[tuple[str, str, str]],
    interactions: list[tuple[str, str, str, str]],
    details: list[str] | None = None,
) -> str:
    coverage_rows = "\n".join(
        f"| {surface_id} | {surface_type} | Operator | {coverage} | Feature | None |"
        for surface_id, surface_type, coverage in surfaces
    )
    inventory_rows = "\n".join(
        f"| {interaction_id} | {surface_id} | SCREEN | {change_type} | Example | Main |"
        for interaction_id, surface_id, _, change_type in interactions
    )
    if details is None:
        details = [
            detail(interaction_id, surface_id, surface_type, change_type)
            for interaction_id, surface_id, surface_type, change_type in interactions
        ]
    trace_rows = "\n".join(
        f"| {interaction_id} | US-001 | FR-001 | SC-001 | contracts/example.md |"
        for interaction_id, *_ in interactions
    )
    return f"""# Interface Specification: Example Feature

**Feature**: `example-feature`
**Created**: 2026-07-22
**Status**: Draft
**Spec**: spec.md
**Plan**: plan.md
**Surface Catalog**: ../../architecture/interaction-surfaces.md

## Interface Coverage

| Surface ID | Type | Users | Coverage | Included Scope | Deferred or Excluded Scope |
|------------|------|-------|----------|----------------|----------------------------|
{coverage_rows}

## Interaction Inventory

| Interaction ID | Surface ID | Kind | Change Type | Name | Entry Point |
|----------------|------------|------|-------------|------|-------------|
{inventory_rows}

## Interaction Details

{"".join(details)}

## Traceability

| Interaction ID | User Stories | Functional Requirements | Success Criteria | Contracts |
|----------------|--------------|-------------------------|------------------|-----------|
{trace_rows}

## Validation Summary

- Coverage matrix reviewed: yes
- All inventory items detailed: yes
- Canonical states resolved: yes
- Required wireframes present: yes
- Accessibility requirements resolved: yes
- Contract mappings verified: yes
- Placeholders or open decisions remaining: 0
"""


class InterfaceSpecValidatorTest(unittest.TestCase):
    def run_validator(self, content: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as temporary_directory:
            spec_path = Path(temporary_directory) / "interface-spec.md"
            spec_path.write_text(content, encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(SCRIPT), str(spec_path)],
                check=False,
                capture_output=True,
                text=True,
            )

    def test_accepts_responsive_web_and_native_mobile_coverage(self) -> None:
        surfaces = [
            ("SURF-WEB-ADMIN", "WEB", "FULL"),
            ("SURF-ANDROID-CUSTOMER", "ANDROID", "PARTIAL"),
            ("SURF-IOS-CUSTOMER", "IOS", "DEFERRED"),
        ]
        interactions = [
            ("INT-WEB-001", "SURF-WEB-ADMIN", "WEB", "NEW"),
            (
                "INT-ANDROID-001",
                "SURF-ANDROID-CUSTOMER",
                "ANDROID",
                "NEW",
            ),
        ]
        responsive_web = detail("INT-WEB-001", "SURF-WEB-ADMIN", "WEB").replace(
            "Declared form factors and input methods",
            "Desktop 1440px with keyboard, tablet 768px and phone 390px with touch",
        )
        partial_android = detail(
            "INT-ANDROID-001", "SURF-ANDROID-CUSTOMER", "ANDROID"
        ).replace(
            "Existing components and tokens",
            "Kotlin and Jetpack Compose components from the Android design system",
        )
        result = self.run_validator(
            document(surfaces, interactions, [responsive_web, partial_android])
        )
        self.assertEqual(0, result.returncode, result.stderr)

    def test_accepts_android_and_ios_with_distinct_native_technologies(self) -> None:
        interactions = [
            ("INT-ANDROID-001", "SURF-ANDROID-CUSTOMER", "ANDROID", "NEW"),
            ("INT-IOS-001", "SURF-IOS-CUSTOMER", "IOS", "NEW"),
        ]
        android = detail(
            "INT-ANDROID-001", "SURF-ANDROID-CUSTOMER", "ANDROID"
        ).replace(
            "Existing components and tokens",
            "Kotlin and Jetpack Compose components from the Android design system",
        )
        ios = detail("INT-IOS-001", "SURF-IOS-CUSTOMER", "IOS").replace(
            "Existing components and tokens",
            "Swift and SwiftUI components from the iOS design system",
        )
        result = self.run_validator(
            document(
                [
                    ("SURF-ANDROID-CUSTOMER", "ANDROID", "FULL"),
                    ("SURF-IOS-CUSTOMER", "IOS", "FULL"),
                ],
                interactions,
                [android, ios],
            )
        )
        self.assertEqual(0, result.returncode, result.stderr)

    def test_accepts_cli_only_feature(self) -> None:
        result = self.run_validator(
            document(
                [("SURF-CLI-OPS", "CLI", "FULL")],
                [("INT-CLI-001", "SURF-CLI-OPS", "CLI", "NEW")],
            )
        )
        self.assertEqual(0, result.returncode, result.stderr)

    def test_accepts_modified_existing_screen(self) -> None:
        result = self.run_validator(
            document(
                [("SURF-DESKTOP-OPS", "DESKTOP", "FULL")],
                [
                    (
                        "INT-DESKTOP-001",
                        "SURF-DESKTOP-OPS",
                        "DESKTOP",
                        "MODIFIED",
                    )
                ],
            )
        )
        self.assertEqual(0, result.returncode, result.stderr)

    def test_rejects_full_surface_without_interaction(self) -> None:
        result = self.run_validator(
            document([("SURF-WEB-ADMIN", "WEB", "FULL")], [])
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("has no interaction inventory item", result.stderr)

    def test_rejects_duplicate_interaction_id(self) -> None:
        interactions = [
            ("INT-WEB-001", "SURF-WEB-ADMIN", "WEB", "NEW"),
            ("INT-WEB-001", "SURF-WEB-ADMIN", "WEB", "NEW"),
        ]
        result = self.run_validator(
            document([("SURF-WEB-ADMIN", "WEB", "FULL")], interactions)
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("duplicate Interaction ID", result.stderr)

    def test_rejects_missing_canonical_state(self) -> None:
        valid_detail = detail("INT-WEB-001", "SURF-WEB-ADMIN", "WEB")
        result = self.run_validator(
            document(
                [("SURF-WEB-ADMIN", "WEB", "FULL")],
                [("INT-WEB-001", "SURF-WEB-ADMIN", "WEB", "NEW")],
                [valid_detail.replace("| offline |", "| disconnected |")],
            )
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("missing canonical state: offline", result.stderr)

    def test_rejects_unresolved_placeholder(self) -> None:
        content = document(
            [("SURF-CLI-OPS", "CLI", "FULL")],
            [("INT-CLI-001", "SURF-CLI-OPS", "CLI", "NEW")],
        ).replace("Complete the user outcome", "[describe the user outcome]")
        result = self.run_validator(content)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("unresolved markers", result.stderr)

    def test_rejects_missing_required_wireframe(self) -> None:
        required_detail = detail(
            "INT-WEB-001",
            "SURF-WEB-ADMIN",
            "WEB",
            wireframe_requirement="REQUIRED",
            wireframe="wireframes/missing.md",
        )
        result = self.run_validator(
            document(
                [("SURF-WEB-ADMIN", "WEB", "FULL")],
                [("INT-WEB-001", "SURF-WEB-ADMIN", "WEB", "NEW")],
                [required_detail],
            )
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("required wireframe artifact does not exist", result.stderr)

    def test_accepts_embedded_required_wireframe(self) -> None:
        required_detail = detail(
            "INT-WEB-001",
            "SURF-WEB-ADMIN",
            "WEB",
            wireframe_requirement="REQUIRED",
            wireframe="EMBEDDED",
        )
        result = self.run_validator(
            document(
                [("SURF-WEB-ADMIN", "WEB", "FULL")],
                [("INT-WEB-001", "SURF-WEB-ADMIN", "WEB", "NEW")],
                [required_detail],
            )
        )
        self.assertEqual(0, result.returncode, result.stderr)

    def test_skill_declares_headless_feature_as_not_applicable(self) -> None:
        skill_text = SKILL.read_text(encoding="utf-8")
        self.assertIn("N/A — sem superfície de interação humana", skill_text)
        self.assertIn("não criar `interface-spec.md` vazio", skill_text)


if __name__ == "__main__":
    unittest.main()
