# UI/UX Design Rule for Antigravity

This rule establishes strict visual quality and user experience standards for all frontend pages, components, and design iterations in PAIMANA AI.

## 1. Aesthetic Standard & Executive Quality
* **No Bare-Bones MVPs:** All interfaces must look polished, authoritative, and credible for senior government officials and project directors.
* **Palette Fidelity:** Use the 3-tier sovereign palette:
  - Sovereign Deep Navy (`#0F2B5B`, `#1E3A8A`) for headers and primary CTAs.
  - Crisp elevated cards (`#FFFFFF`, `bg-slate-50/70`, border `slate-200/80`).
  - Semantic status indicators: Emerald (`#059669`) for on-track, Amber (`#B45309`) for watchlist, Crimson (`#DC2626`) for critical slippage.
* **Ambient Depth:** Use subtle backdrop blurs, delicate radial gradients, and layered shadows (`shadow-sm`, `shadow-xl shadow-slate-200/50`) instead of flat, harsh borders.

## 2. Ergonomics & Accessibility
* **Comfortable Touch Targets:** All clickable inputs and buttons must have a minimum height of `h-10` or `h-11` (40–44px) on interactive views.
* **Readable Typography:** Never default to microscopic `text-xs` (12px) for primary inputs or body copy. Body text should be `text-sm` (14px) or `text-base` (16px) with clean leading.
* **Input Usability:** Always provide contextual prefix icons (e.g. Mail, Lock, Search) and show/hide toggles for password fields.
* **No Layout Shrinking:** Never lock pages with `overflow: hidden; height: 100vh` if content might be clipped. Always allow responsive vertical scrolling (`min-h-screen`, `overflow-y: auto`).

## 3. Micro-Interactions & Feedback
* Provide visual feedback on hover (`hover:border-blue-300`, `hover:shadow-md`).
* Always display clear loading spinners and disabled states during asynchronous operations.
