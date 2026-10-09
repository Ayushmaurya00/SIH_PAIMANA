---
name: ponytail
description: >-
  Enforces the Ponytail minimalist coding philosophy to audit code for bloat,
  strip over-engineered abstractions, and streamline implementations using YAGNI.
---

# Ponytail Skill

Use this skill when auditing files for unnecessary complexity, refactoring bloated components, or when the user invokes Ponytail directly.

## Slash Workflows & Triggers

### 1. `/ponytail-audit [filepath]`
* Read the specified file.
* Identify over-engineered patterns:
  - Redundant abstraction layers or wrappers.
  - Speculative utility functions used in only one place.
  - Unused dependencies or dead code.
* Output a table of findings showing:
  - Current lines of code vs. Proposed lines of code.
  - Eliminated boilerplate.

### 2. `/ponytail-simplify [filepath]`
* Refactor the target file applying the Ponytail Decision Ladder:
  1. Replace custom logic with native JS/Python built-ins.
  2. Consolidate one-off wrapper functions into their call sites.
  3. Flatten nested control flow into early returns.
* Ensure all existing tests pass and contracts remain intact.

### 3. Intensity Modes
* **`lite`**: Standard cleanup; eliminates dead code and unused imports.
* **`full` (Default)**: Aggressively simplifies wrappers, flattens nesting, and consolidates helpers.
* **`ultra`**: Extreme minimalism; inlines single-use helpers, minimizes lines of code to the absolute essentials.

## Implementation Guidelines
* Never sacrifice safety, accessibility, error handling, or validation for brevity.
* Adhere strictly to the workspace 200-line modularity rule.
