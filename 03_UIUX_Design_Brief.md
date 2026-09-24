# UI/UX Design System & Visual Specification
## PAIMANA AI — Sovereign Decision-Support Interface for Infrastructure Projects
**Ministry of Statistics and Programme Implementation (MoSPI) — Infrastructure and Project Monitoring Division (IPMD)**
*Smart India Hackathon (SIH) 2024 — Verified Visual & Design System Specification (v3.0)*
*Last Updated: September 2026 | Status: Production-Ready*

---

## 1. Design Philosophy & Sovereign Aesthetic

**PAIMANA AI** is designed with the gravity and precision of an executive Cabinet-level intelligence terminal. It rejects toy-like consumer aesthetics and generic SaaS dashboard cliches in favor of a **Sovereign Design System** inspired by official Government of India publications, high-density financial terminals, and institutional decision-support systems.

### Core Visual Principles:
1. **Institutional Authority & Trust:** Restrained palette dominated by Deep Sovereign Blue (`#0F2B5B`), crisp borders (`#E2E8F0`), and high-contrast typography.
2. **Standard Indian Financial Notation:** All monetary figures are formatted in statutory Indian units (`₹ Lakh Cr`, `₹K Cr`, `₹ Cr`) instead of Western millions/billions.
3. **Absolute Data Provenance Transparency:** Clear visual separation between authentic MoSPI database records and synthetic demo illustrations.
4. **Explainability-First UI:** Risk scores are never displayed as naked numbers; they are always accompanied by TreeSHAP delay factor breakdowns (+X pts) and severity-calibrated administrative playbooks.
5. **High Information Density with Clear Hierarchy:** Scannable metric cards, tabular monospace layouts for numerical precision, and progressive disclosure for deep dossiers.

---

## 2. Sovereign Color Palette & Design Tokens

```
========================================================================================
PAIMANA AI — COLOR PALETTE SPECIFICATION
========================================================================================
  
  [ Sovereign Primary & Neutrals ]
  ████ Sovereign Blue     #0F2B5B   (Primary brand, headers, active states)
  ████ Slate Text Dark    #0F172A   (Primary headings, titles, high contrast)
  ████ Slate Text Muted   #64748B   (Secondary labels, subtitles, timestamps)
  ████ Surface Elevated   #FFFFFF   (Card backgrounds, modal surfaces)
  ████ Surface Canvas     #F8FAFC   (Application canvas, off-white background)
  ████ Border Rest        #E2E8F0   (Clean structural dividers, card borders)

  [ Semantic Risk & Status Tiers ]
  ████ Critical (High)    #DC2626 / #EF4444   (Risk >= 58, cost escalation > 20%)
  ████ Warning (Medium)   #D97706 / #F59E0B   (Risk 32-57, milestone slippage)
  ████ Safe (Low / Good)  #059669 / #10B981   (Risk < 32, on-track execution)
  ████ Stalled / Inactive #64748B / #94A3B8   (Unfunded / suspended projects)

  [ Demo Sandbox Isolation ]
  ████ Demo Amber Accent  #B45309 / #F59E0B   (Synthetic data indicators)
  ████ Demo Border Dashed #FCD34D             (Dashed isolation boundaries)
  ████ Demo Background    #FFFBEB             (Subtle amber tint for sandbox)
========================================================================================
```

### Detailed Token Map:

| Semantic Token | Hex Code | Tailwind Utility | Intended Usage |
|---|---|---|---|
| `color-primary-sovereign` | `#0F2B5B` | `bg-[#0F2B5B]`, `text-[#0F2B5B]` | Header, primary CTA, sovereign badges, key charts |
| `color-surface-canvas` | `#F8FAFC` | `bg-slate-50` | Full viewport background |
| `color-surface-card` | `#FFFFFF` | `bg-white` | Elevated data cards, tables, modal surfaces |
| `color-border-subtle` | `#E2E8F0` | `border-slate-200` | Grid separators, table row borders |
| `color-status-critical` | `#DC2626` | `text-red-600`, `bg-red-50` | High Risk (≥58), severe cost overruns, critical alerts |
| `color-status-warning` | `#D97706` | `text-amber-600`, `bg-amber-50` | Medium Risk (32–57), schedule warnings |
| `color-status-success` | `#059669` | `text-emerald-600`, `bg-emerald-50` | Low Risk (<32), completed milestones, on-track execution |
| `color-demo-accent` | `#B45309` | `text-amber-700`, `border-amber-300` | Demo Telemetry Sandbox headers, synthetic badges |

---

## 3. Typography & Numerical Formatting Standards

* **Primary Font Family:** Inter / system-ui (`sans-serif`) for crisp, legible UI elements.
* **Monospace Font Family:** JetBrains Mono / ui-monospace (`monospace`) for all Project IDs (`PRJ-XXXXXX`), financial sums, percentages, and dates.

### Indian Financial Notation Rules:
```javascript
// Implemented in frontend/src/utils/cn.js and OverviewPage.jsx
export function formatCurrency(val) {
  if (val === null || val === undefined || isNaN(val)) return '₹0 Cr';
  const num = Number(val);
  if (Math.abs(num) >= 100000) {
    return `₹${(num / 100000).toFixed(2)} Lakh Cr`;
  }
  return `₹${num.toLocaleString('en-IN', { maximumFractionDigits: 0 })} Cr`;
}
```

* Values $\ge ₹1,00,000\text{ Cr}$ render as: `₹35.38 Lakh Cr`
* Values $< ₹1,00,000\text{ Cr}$ render as: `₹24,580 Cr`
* Chart Axis formatters render as: `₹9.5 L Cr`, `₹500K Cr`, or `₹50 Cr`.

---

## 4. Key Component Specifications

### 4.1 Executive KPI Strip (`KPICard.jsx`)
* **Visual Form:** Clean white card with subtle slate border, uppercase muted category header, large bold monospace metric value, and contextual subtext.
* **Sovereign Accent:** Micro-icon aligned to right top corner with status-tinted background.

### 4.2 Calibrated Risk Badge (`RiskBadge.jsx`)
* **Visual Form:** Pill container with risk tier text and circular score indicator.
* **Tier Color Mappings:**
  - `High`: Red border (`border-red-300`), red text (`text-red-700`), red tinted background (`bg-red-50`).
  - `Medium`: Amber border (`border-amber-300`), amber text (`text-amber-700`), amber tinted background (`bg-amber-50`).
  - `Low`: Emerald border (`border-emerald-300`), emerald text (`text-emerald-700`), emerald tinted background (`bg-emerald-50`).

### 4.3 Current Financial Execution Bar Chart (`ProjectDetailPage.jsx`)
* **Visual Form:** Real Recharts `BarChart` comparing three distinct financial bars:
  - `Baseline Approved Cost`: Neutral slate grey (`#94A3B8`).
  - `Revised Outlay`: Deep slate (`#64748B`).
  - `Cumulative Expenditure`: Vibrant emerald green (`#059669`).
* **Tooltips:** Formatted in exact Indian Crores (`₹X,XXX Cr`).

### 4.4 Demo Telemetry Sandbox (Visual Isolation Pattern)
To ensure complete transparency regarding data provenance:
* **Section Border:** 2px dashed border in sovereign amber (`border-dashed border-amber-300`).
* **Section Background:** Gentle amber canvas tint (`bg-amber-50/30`).
* **Header Badge:** `FlaskConical` icon + `DEMO — Synthetic Illustration` pill.
* **Charts Contained:**
  1. **12-Month S-Curve Telemetry:** `ComposedChart` with gradient-filled area curves for Actual Progress (%) and Financial Burn (% of Approved) alongside a dashed Planned Baseline curve.
  2. **Project Phase Execution Tracker:** 5-phase structured timeline cards with dynamic progress bars and status indicators (`Completed`, `In Progress`, `Delayed`, `Not Started`).
* **Disclaimers:** Explicit footnotes explaining that historical monthly telemetry is interpolated from the genuine June 2026 MoSPI snapshot.

### 4.5 Grounded AI Copilot Drawer (`AIAssistantDrawer.jsx`)
* **Visual Form:** Slide-in right drawer with backdrop blur.
* **Header:** Sovereign Blue banner with MoSPI emblem styling and active project context pill.
* **Message Bubbles:**
  - User: Clean slate bubble with user icon.
  - Copilot: Sovereign Blue tinted bubble with structured markdown rendering, bold metrics, and clickable source reference pills (`[PRJ-618417]`).
* **Safety Pill:** Notice indicating local open-source LLM execution with zero external data transmission.

---

## 5. Screen Layout Wireframes

### 5.1 Executive Portfolio Overview (`/`)
```
┌───────────────────────────────────────────────────────────────────────────────────────┐
│ [Emblem] PAIMANA AI — IPMD Executive Dashboard             [Inquire with Copilot] (●) │
├───────────────────────────────────────────────────────────────────────────────────────┤
│ [ Total Outlay: ₹35.38 Lakh Cr ] [ Spent: ₹21.93 Lakh Cr ] [ Projects: 1,798 ] [ Risk ] │
├───────────────────────────────────────────┬───────────────────────────────────────────┤
│ Sectoral Capital Allocation (Bar Chart)   │ Ministry Risk Distribution (Bar Chart)   │
│ - Road Transport & Highways: ₹9.45 L Cr   │ - MoRTH: 966 Projects (High: 42%)         │
│ - Railways: ₹7.41 L Cr                    │ - Railways: 281 Projects (High: 46%)      │
│ - Power: ₹5.19 L Cr                       │ - Coal: 135 Projects (High: 38%)          │
├───────────────────────────────────────────┴───────────────────────────────────────────┤
│ Critical Portfolio Watchlist (Top At-Risk Infrastructure Projects)                    │
│ [PRJ-618417] Mumbai-Ahmedabad HSR     | Railways  | ₹1,08,000 Cr | Risk: 84 [High 🔴] │
│ [PRJ-701598] Vadodara-Mumbai Exp      | MoRTH     | ₹44,300 Cr   | Risk: 72 [High 🔴] │
└───────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Project Detail Dossier (`/project/:id`)
```
┌───────────────────────────────────────────────────────────────────────────────────────┐
│ ← Back to Central Sector Directory             [Inquire with Copilot] [Delete Project]│
├───────────────────────────────────────────────────────────────────────────────────────┤
│ [PRJ-618417] [Ministry of Railways] [High Speed Rail]                   [Risk: 84.0 🔴]│
│ Mumbai - Ahmedabad High Speed Rail Corridor (Bullet Train)                             │
│ State: Gujarat / Maharashtra | Scheduled Start: 2017-09 | Target Completion: 2028-12   │
├───────────────────────────────────────────────────────────────────────────────────────┤
│ [ Sanctioned: ₹1,08,000 Cr ] [ Revised: ₹1,65,000 Cr ] [ Spent: ₹62,400 Cr ] [ 38.5% ]│
├───────────────────────────────────────────────────────────────────────────────────────┤
│ Operational Bottleneck: Expenditure at 57.8% with physical progress lagging at 38.5%. │
│ Recommended Action: Escalate +52.8% cost deviation to Cabinet Committee on Economic   │
│ Affairs (CCEA) for revised financial sanction.                                        │
├───────────────────────────────────────────────────────────────────────────────────────┤
│ Key Operational Delay Drivers (SHAP)      │ Calibrated Outlay Forecast (90% CI)       │
│ • Land Acquisition in Palghar (+18.4 pts) │ • Predicted Cost Escalation: +45% to +58% │
│ • Forest & Coastal CRZ Clearances (+12.1) │ • Target Schedule Delay: +36 to +48 Months│
├───────────────────────────────────────────────────────────────────────────────────────┤
│ Current Financial Execution (June 2026) — Genuine Database Records                    │
│ [ Bar Chart: Approved (₹1.08L Cr) | Revised (₹1.65L Cr) | Expended (₹62.4K Cr) ]      │
├───────────────────────────────────────────────────────────────────────────────────────┤
│ Statutory & Civil Milestones Timeline                                                 │
│ [ Milestone Gantt: Feasibility ✓ | Land 70% ✓ | Civil Tenders ✓ | Commissioning ⏳ ]   │
├ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ┤
│ 🧪 DEMO TELEMETRY SANDBOX — Synthetic Illustration Only                               │
│ [ 12-Month S-Curve Chart (Recharts) ]   [ 5-Phase Project Execution Tracker ]         │
└ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ┘
```

---

## 6. Accessibility, Responsiveness & Print Readiness

* **Accessibility Standards (WCAG 2.1 AA):**
  - High-contrast text ratios ($\ge 4.5:1$ for body text, $\ge 3:1$ for large headings).
  - Risk states are never communicated solely by color; always paired with explicit text labels (`High`, `Medium`, `Low`) and numerical values.
  - Keyboard accessible tab navigation across all interactive tables, filters, and modals.
* **Print & Cabinet Briefing Export (`window.print()`):**
  - Dedicated print stylesheet hides interactive navigation bars, copilot triggers, and action buttons.
  - Automatically renders an official **MoSPI IPMD Executive Cabinet Briefing Header** with generation timestamp and confidential document classification.
