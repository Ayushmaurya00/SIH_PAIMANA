# Ponytail — Anti-Overengineering Rule for Antigravity

This rule enforces the **Ponytail** minimalist development philosophy across all code generation, refactoring, and pair programming turns.

## The Ponytail Decision Ladder
Before writing any new function, file, hook, or abstraction, you MUST climb down this ladder in order:

1. **Does this need to exist at all? (YAGNI)**
   - If a feature, edge-case handler, or abstraction is speculative or not strictly requested, do NOT build it.
2. **Does the codebase already have it?**
   - Search the existing codebase before creating a new utility or helper. Reuse existing functions and components.
3. **Does the language/platform standard library handle it?**
   - Prefer standard JavaScript / Python built-ins over custom utility packages (e.g. `Array.prototype.find`, native `fetch`, native `<dialog>`).
4. **Does an existing dependency in `package.json` solve it?**
   - Do not propose new npm packages or Python libraries if an installed tool (e.g. `lucide-react`, `recharts`, `axios`) already covers the requirement.
5. **Can this be 1–3 lines?**
   - If logic can be handled with an inline expression or standard ternary, do not write a separate 30-line custom hook or wrapper class.
6. **Only then: write the minimum necessary code.**
   - Write simple, direct code. Avoid premature layers of indirection, unnecessary factory patterns, and boilerplate.

## Concrete Guardrails
* **No Speculative Abstractions:** Do not create interfaces or classes for "future extensibility" that is not currently required.
* **Component Budget:** Do not split a component into 5 micro-files unless modularity or line-count rules strictly demand it.
* **Early Returns:** Use guard clauses and early returns instead of deeply nested `if/else` structures.
* **Zero Dead Weight:** Never leave unused imports, uncalled parameters, or placeholder comments.
