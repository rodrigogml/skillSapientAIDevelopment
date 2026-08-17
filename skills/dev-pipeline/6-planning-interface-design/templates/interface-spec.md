# Interface Specification: [FEATURE NAME]

**Feature**: `[feature-short-name]`
**Created**: [DATE]
**Status**: Draft
**Spec**: [relative link to spec.md]
**Plan**: [relative link to plan.md]
**Surface Catalog**: [relative link to docs/architecture/interaction-surfaces.md]

## Interface Coverage

| Surface ID | Type | Users | Coverage | Included Scope | Deferred or Excluded Scope |
|------------|------|-------|----------|----------------|----------------------------|
| SURF-WEB-ADMIN | WEB | [roles] | FULL | [capabilities] | None |

Allowed coverage: `FULL`, `PARTIAL`, `DEFERRED`, `N/A`.

## Current-State Evidence

| Surface ID | Existing Route, Command, or Component | Evidence | Current Behavior |
|------------|---------------------------------------|----------|------------------|
| SURF-WEB-ADMIN | [path or identifier] | [screenshot or source path] | [current behavior] |

Remove this section only when every interaction is new and no existing interface is affected.

## Interaction Inventory

| Interaction ID | Surface ID | Kind | Change Type | Name | Entry Point |
|----------------|------------|------|-------------|------|-------------|
| INT-WEB-001 | SURF-WEB-ADMIN | SCREEN | NEW | [name] | [route/navigation] |

Allowed change types: `NEW`, `MODIFIED`, `REMOVED`, `UNCHANGED`.

## Interaction Details

### INT-WEB-001 — [Interaction Name]

**Surface**: SURF-WEB-ADMIN
**Surface Type**: WEB
**Change Type**: NEW
**Purpose**: [user outcome]
**Actors and Permissions**: [roles, visibility and authorization]
**Entry and Navigation**: [route, menu, deep link, prior and next destinations]
**Content and Data**: [hierarchy, fields, values and source]
**Actions and Behavior**: [actions, transitions, confirmations and destructive behavior]
**Validation and Feedback**: [client/server validation, messages, retry and success feedback]
**Responsive/Adaptive Behavior**: [desktop, tablet, phone, orientation and input method]
**Accessibility**: [keyboard, focus, screen reader, contrast, reduced motion and touch target]
**Localization**: [message keys, formats, long text and RTL behavior]
**Components and Design System**: [reused/new components and token sources]
**Integration and Contracts**: [contract links, operations, payload fields consumed and stale/cache policy]
**Telemetry**: [events, properties and sensitive-data exclusions]
**Wireframe Requirement**: REQUIRED
**Wireframe**: [embedded diagram or relative path under wireframes/]

**States**:

| State | Expected Presentation | Available Actions | Transition/Exit |
|-------|-----------------------|-------------------|-----------------|
| initial | [behavior] | [actions] | [transition] |
| loading | [behavior or N/A — reason] | [actions] | [transition] |
| empty | [behavior or N/A — reason] | [actions] | [transition] |
| ready | [behavior] | [actions] | [transition] |
| processing | [behavior or N/A — reason] | [actions] | [transition] |
| success | [behavior or N/A — reason] | [actions] | [transition] |
| validation-error | [behavior or N/A — reason] | [actions] | [transition] |
| remote-error | [behavior or N/A — reason] | [actions] | [transition] |
| offline | [behavior or N/A — reason] | [actions] | [transition] |
| access-denied | [behavior or N/A — reason] | [actions] | [transition] |
| partial-stale | [behavior or N/A — reason] | [actions] | [transition] |

Duplicate the `### INT-*` section for each inventory item.

## Cross-Surface Rules

### Navigation and Parity

[Shared navigation, handoff and intentional parity differences.]

### Shared Content and Terminology

[Canonical labels, messages and domain terms.]

### Shared Accessibility and Input

[Project-level rules applied across surfaces.]

## Traceability

| Interaction ID | User Stories | Functional Requirements | Success Criteria | Contracts |
|----------------|--------------|-------------------------|------------------|-----------|
| INT-WEB-001 | US-001 | FR-001 | SC-001 | contracts/example.md |

## Wireframes

| Interaction ID | Requirement | Artifact | Notes |
|----------------|-------------|----------|-------|
| INT-WEB-001 | REQUIRED | wireframes/int-web-001.md | Low-fidelity layout |

## Validation Summary

- Coverage matrix reviewed: [yes/no]
- All inventory items detailed: [yes/no]
- Canonical states resolved: [yes/no]
- Required wireframes present: [yes/no]
- Accessibility requirements resolved: [yes/no]
- Contract mappings verified: [yes/no]
- Placeholders or open decisions remaining: [count]
