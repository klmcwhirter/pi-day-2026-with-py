
<!--
Sync Impact Report
Version change: 0.0.0 → 1.0.0
Modified principles: All placeholders replaced with concrete principles
Added sections: Non-Functional Requirements (NFRs)
Removed sections: None
Templates requiring updates: plan-template.md (✅), spec-template.md (✅), tasks-template.md (✅), checklist-template.md (✅), agent-file-template.md (✅)
-->

# pi-day-2026-with-py Constitution


## Core Principles

### I. Python & Django Foundation
Every application component MUST be implemented in Python (>=3.14) using Django (>=5.2) as the primary web framework. All code must follow Django and typical Python standards, with project-specific overrides as documented in NFRs.

### II. Command-Line and Web Interface
All major features MUST be accessible via both Django web UI and command-line interface (CLI) where feasible. CLI tools must use `uv` and `uvextras` from $PATH. Web UI must use TailwindCSS (>=4.1) utility classes for styling.

### III. Test-First Discipline (NON-NEGOTIABLE)
Test-driven development is mandatory. All business logic MUST be covered by tests before implementation. UI testing is discouraged; focus on business logic. Red-Green-Refactor cycle is strictly enforced.

### IV. Observability & Simplicity
Structured logging MUST be implemented for all critical operations. Simplicity is prioritized: avoid unnecessary abstraction, prefer clear and direct solutions. TailwindCSS utility classes are preferred over custom CSS.

### V. Versioning & Breaking Changes
Semantic versioning (MAJOR.MINOR.PATCH) is required. Any breaking change or principle redefinition triggers a MAJOR version bump. New principles or expanded guidance require a MINOR bump. Clarifications or non-semantic refinements are PATCH.


## Non-Functional Requirements (NFRs)

- Python >= 3.14
- Django >= 5.2
- uv (cli from $PATH)
- uvextras (cli from $PATH)
- tailwindcss >= 4.1
- npm (cli from $PATH)
- Prefer single-quote chars over double-quote chars
- Allow 140 char line lengths
- Use Django and Python standards, with above overrides
- Prefer tailwindcss utility classes over custom CSS
- Focus on testing business logic only; discourage UI testing


## Development Workflow & Quality Gates

- All code must be peer-reviewed for compliance with this constitution and NFRs.
- Feature specifications must include independently testable user stories.
- Implementation plans must document technology stack, dependencies, and constraints.
- Tasks must be organized by user story for independent delivery and testing.
- All PRs must pass constitution and NFR checks before merge.


## Governance

- This constitution supersedes all other project practices.
- Amendments require documentation, approval, and a migration plan.
- All changes must be versioned per the Versioning principle.
- Compliance reviews are required for every release.
- Use README.md and NFRs.md for runtime development guidance.


**Version**: 1.0.0 | **Ratified**: 2025-11-06 | **Last Amended**: 2025-11-06
