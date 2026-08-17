#!/usr/bin/env python3
"""Validate the structural contract of a generated interface-spec.md."""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path


SURFACE_ID_PATTERN = r"SURF-(?:[A-Z0-9]+(?:-[A-Z0-9]+)*)"
INTERACTION_ID_PATTERN = r"INT-(?:[A-Z0-9]+-)+\d{3}"
ALLOWED_COVERAGE = {"FULL", "PARTIAL", "DEFERRED", "N/A"}
ALLOWED_CHANGE_TYPES = {"NEW", "MODIFIED", "REMOVED", "UNCHANGED"}
ALLOWED_SURFACE_TYPES = {
    "CLI",
    "TUI",
    "DESKTOP",
    "WEB",
    "MOBILE_WEB",
    "ANDROID",
    "IOS",
    "OTHER",
}
ALLOWED_WIREFRAME_REQUIREMENTS = {"REQUIRED", "OPTIONAL", "N/A"}
CANONICAL_STATES = (
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
REQUIRED_HEADINGS = (
    "## Interface Coverage",
    "## Interaction Inventory",
    "## Interaction Details",
    "## Traceability",
    "## Validation Summary",
)
REQUIRED_LABELS = (
    "Surface",
    "Surface Type",
    "Change Type",
    "Purpose",
    "Actors and Permissions",
    "Entry and Navigation",
    "Content and Data",
    "Actions and Behavior",
    "Validation and Feedback",
    "Responsive/Adaptive Behavior",
    "Accessibility",
    "Localization",
    "Components and Design System",
    "Integration and Contracts",
    "Telemetry",
    "Wireframe Requirement",
    "Wireframe",
)


def extract_section(text: str, heading: str) -> str:
    pattern = re.compile(
        rf"^{re.escape(heading)}\s*$\n(?P<body>.*?)(?=^##\s|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    return match.group("body") if match else ""


def parse_table(section: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in section.splitlines():
        stripped = line.strip()
        if not (stripped.startswith("|") and stripped.endswith("|")):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if not cells or all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        rows.append(cells)
    return rows


def parse_details(text: str) -> tuple[dict[str, str], list[str]]:
    pattern = re.compile(
        rf"^###\s+(?P<id>{INTERACTION_ID_PATTERN})\s+(?:—|-)\s+[^\r\n]*\r?\n"
        rf"(?P<body>.*?)(?=^###\s+{INTERACTION_ID_PATTERN}\s+(?:—|-)|^##\s|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    details: dict[str, str] = {}
    duplicate_ids: list[str] = []
    for match in pattern.finditer(text):
        interaction_id = match.group("id")
        if interaction_id in details:
            duplicate_ids.append(interaction_id)
        details[interaction_id] = match.group("body")
    return details, duplicate_ids


def extract_label(block: str, label: str) -> str | None:
    match = re.search(
        rf"^\*\*{re.escape(label)}\*\*:\s*(.*)$", block, re.MULTILINE
    )
    return match.group(1).strip() if match else None


def contains_placeholder(text: str) -> list[str]:
    findings: list[str] = []
    patterns = {
        "TODO": r"\bTODO\b",
        "TKTK": r"\bTKTK\b",
        "???": r"\?\?\?",
        "NEEDS CLARIFICATION": r"\[NEEDS CLARIFICATION(?::[^\]]+)?\]",
        "template placeholder": r"(?<!\!)\[(?![ xX~!]\])[^\]\r\n]{2,}\](?!\()",
    }
    for label, pattern in patterns.items():
        if re.search(pattern, text):
            findings.append(label)
    return findings


def validate_wireframe(spec_path: Path, requirement: str, value: str) -> str | None:
    normalized = value.strip().strip("`")
    if requirement != "REQUIRED":
        return None
    if not normalized or normalized.upper().startswith(("N/A", "NONE")):
        return "wireframe is REQUIRED but no artifact was provided"
    if normalized.upper() == "EMBEDDED" or "embedded" in normalized.lower():
        return None
    artifact = normalized.split()[0].strip("<>()[]")
    if not (spec_path.parent / artifact).is_file():
        return f"required wireframe artifact does not exist: {artifact}"
    return None


def validate(spec_path: Path) -> list[str]:
    errors: list[str] = []
    try:
        text = spec_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [f"cannot read UTF-8 document: {exc}"]

    if not re.search(r"^# Interface Specification:\s+\S", text, re.MULTILINE):
        errors.append("missing '# Interface Specification: <name>' title")

    for heading in REQUIRED_HEADINGS:
        if not re.search(rf"^{re.escape(heading)}\s*$", text, re.MULTILINE):
            errors.append(f"missing required heading: {heading}")

    placeholders = contains_placeholder(text)
    if placeholders:
        errors.append("unresolved markers: " + ", ".join(placeholders))

    coverage_rows = parse_table(extract_section(text, "## Interface Coverage"))
    if coverage_rows and coverage_rows[0][0] == "Surface ID":
        coverage_rows = coverage_rows[1:]
    coverage: dict[str, str] = {}
    for row_number, row in enumerate(coverage_rows, start=1):
        if len(row) < 4:
            errors.append(f"coverage row {row_number} has fewer than 4 columns")
            continue
        surface_id, status = row[0], row[3].upper()
        if not re.fullmatch(SURFACE_ID_PATTERN, surface_id):
            errors.append(f"invalid Surface ID in coverage: {surface_id}")
        if surface_id in coverage:
            errors.append(f"duplicate Surface ID in coverage: {surface_id}")
        if status not in ALLOWED_COVERAGE:
            errors.append(f"invalid coverage for {surface_id}: {row[3]}")
        coverage[surface_id] = status
    if not coverage:
        errors.append("Interface Coverage must contain at least one surface")

    inventory_rows = parse_table(extract_section(text, "## Interaction Inventory"))
    if inventory_rows and inventory_rows[0][0] == "Interaction ID":
        inventory_rows = inventory_rows[1:]
    inventory: dict[str, tuple[str, str]] = {}
    inventory_ids: list[str] = []
    for row_number, row in enumerate(inventory_rows, start=1):
        if len(row) < 6:
            errors.append(f"inventory row {row_number} has fewer than 6 columns")
            continue
        interaction_id, surface_id, change_type = row[0], row[1], row[3].upper()
        inventory_ids.append(interaction_id)
        if not re.fullmatch(INTERACTION_ID_PATTERN, interaction_id):
            errors.append(f"invalid Interaction ID in inventory: {interaction_id}")
        if surface_id not in coverage:
            errors.append(
                f"inventory {interaction_id} references unknown surface: {surface_id}"
            )
        if change_type not in ALLOWED_CHANGE_TYPES:
            errors.append(f"invalid change type for {interaction_id}: {row[3]}")
        inventory[interaction_id] = (surface_id, change_type)
    for interaction_id, count in Counter(inventory_ids).items():
        if count > 1:
            errors.append(f"duplicate Interaction ID in inventory: {interaction_id}")

    for surface_id, status in coverage.items():
        if status in {"FULL", "PARTIAL"} and not any(
            item_surface == surface_id for item_surface, _ in inventory.values()
        ):
            errors.append(
                f"surface {surface_id} is {status} but has no interaction inventory item"
            )

    details, duplicate_detail_ids = parse_details(text)
    for interaction_id in duplicate_detail_ids:
        errors.append(f"duplicate interaction detail section: {interaction_id}")
    missing_details = sorted(set(inventory) - set(details))
    extra_details = sorted(set(details) - set(inventory))
    if missing_details:
        errors.append("inventory items without details: " + ", ".join(missing_details))
    if extra_details:
        errors.append("detail items absent from inventory: " + ", ".join(extra_details))

    for interaction_id, block in details.items():
        labels = {label: extract_label(block, label) for label in REQUIRED_LABELS}
        for label, value in labels.items():
            if value is None or not value:
                errors.append(f"{interaction_id} missing required field: {label}")

        surface_id = labels.get("Surface")
        if interaction_id in inventory and surface_id != inventory[interaction_id][0]:
            errors.append(
                f"{interaction_id} surface differs between inventory and details"
            )
        surface_type = (labels.get("Surface Type") or "").upper()
        if surface_type not in ALLOWED_SURFACE_TYPES:
            errors.append(f"{interaction_id} has invalid Surface Type: {surface_type}")
        change_type = (labels.get("Change Type") or "").upper()
        if change_type not in ALLOWED_CHANGE_TYPES:
            errors.append(f"{interaction_id} has invalid Change Type: {change_type}")
        if interaction_id in inventory and change_type != inventory[interaction_id][1]:
            errors.append(
                f"{interaction_id} change type differs between inventory and details"
            )

        for state in CANONICAL_STATES:
            if not re.search(rf"^\|\s*{re.escape(state)}\s*\|", block, re.MULTILINE):
                errors.append(f"{interaction_id} missing canonical state: {state}")

        wireframe_requirement = (labels.get("Wireframe Requirement") or "").upper()
        if wireframe_requirement not in ALLOWED_WIREFRAME_REQUIREMENTS:
            errors.append(
                f"{interaction_id} has invalid Wireframe Requirement: "
                f"{wireframe_requirement}"
            )
        wireframe_value = labels.get("Wireframe") or ""
        wireframe_error = validate_wireframe(
            spec_path, wireframe_requirement, wireframe_value
        )
        if wireframe_error:
            errors.append(f"{interaction_id} {wireframe_error}")

    trace_rows = parse_table(extract_section(text, "## Traceability"))
    if trace_rows and trace_rows[0][0] == "Interaction ID":
        trace_rows = trace_rows[1:]
    trace_ids = [row[0] for row in trace_rows if row]
    for interaction_id, count in Counter(trace_ids).items():
        if count > 1:
            errors.append(f"duplicate Interaction ID in traceability: {interaction_id}")
    missing_trace = sorted(set(inventory) - set(trace_ids))
    extra_trace = sorted(set(trace_ids) - set(inventory))
    if missing_trace:
        errors.append("inventory items without traceability: " + ", ".join(missing_trace))
    if extra_trace:
        errors.append("traceability items absent from inventory: " + ", ".join(extra_trace))
    for row in trace_rows:
        if len(row) < 5:
            errors.append(f"traceability row for {row[0]} has fewer than 5 columns")
            continue
        if all(value.upper().startswith("N/A") for value in row[1:3]):
            errors.append(
                f"{row[0]} must map to at least one User Story or Functional Requirement"
            )

    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: validate-interface-spec.py INTERFACE_SPEC", file=sys.stderr)
        return 2
    spec_path = Path(argv[1]).resolve()
    errors = validate(spec_path)
    if errors:
        print(f"FAIL: {spec_path}", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"PASS: {spec_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
