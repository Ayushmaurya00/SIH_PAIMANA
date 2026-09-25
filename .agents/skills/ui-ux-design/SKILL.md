---
name: ui-ux-design
description: >-
  Provides end-to-end UI/UX design workflows using StitchMCP, Tailwind CSS design systems,
  and executive component architectures for interactive web interfaces.
---

# UI/UX Design Workflow Skill

Use this skill when designing new screens, creating mockups, generating variants, or refining the user experience of PAIMANA AI.

## Available Design Tools in Antigravity

Antigravity has access to **StitchMCP**, which generates design screens directly into the `stitch_assets/` workspace directory:

Tool Name | Purpose | Example Use Case
:--- | :--- | :---
`generate_screen_from_text` | Creates high-fidelity design screens from natural language prompts | Wireframing new dashboards or modals
`create_design_system` | Establishes a unified color, font, and component token set | Harmonizing sovereign design palettes
`generate_variants` | Produces visual variations of an existing layout | Exploring alternative card or table layouts
`edit_screens` | Applies incremental design modifications | Adjusting typography, spacing, or accents

## Step-by-Step UI/UX Workflow

### Step 1: Design Specification
1. Define the user objective, persona (e.g. Cabinet Review Officer, Project Director), and required data points.
2. Select the key visual anchors (KPI counters, S-curve graphs, milestone status pills).

### Step 2: Wireframing with StitchMCP
1. Use `call_mcp_tool` with `ServerName: "StitchMCP"` and `ToolName: "generate_screen_from_text"`.
2. Save generated HTML/CSS artifacts into `stitch_assets/html/` for immediate preview.

### Step 3: Component Translation
1. Convert wireframe structures into modular React components adhering to the workspace 200-line limit.
2. Apply Tailwind utility classes matching the tokens in `frontend/tailwind.config.js`.
3. Add accessible states: focus rings, hover transitions, and keyboard navigation.

### Step 4: Visual Polish
1. Incorporate icons from `lucide-react`.
2. Add micro-interactions: smooth fade-ins (`animate-fade-in`), pulse skeletons for loading states, and badge counters.
