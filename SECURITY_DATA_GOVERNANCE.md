# Security, Ethical AI & Data Governance Policy
## PAIMANA AI — Sovereign Decision-Support System
**Ministry of Statistics and Programme Implementation (MoSPI) — Infrastructure and Project Monitoring Division (IPMD)**
*Smart India Hackathon (SIH) 2024 — Official Governance & Trust Framework (v3.0)*
*Last Updated: September 2026 | Status: Production-Ready*

---

## 1. Executive Security & Sovereign Air-Gap Architecture

**PAIMANA AI** is designed to meet strict sovereign data confidentiality, integrity, and privacy standards required by Government of India digital infrastructure policies (including the *National Data Governance Framework Policy (NDGFP)* and the *Digital Personal Data Protection (DPDP) Act*).

### Core Architectural Security Principles:
1. **Secure Grounded Inference:** Project inquiries are processed using a grounded RAG architecture with strict prompt isolation. When the Google Gemini API key is configured, only factual project monitoring attributes required for the prompt are supplied as grounding context.
2. **Configurable Cloud & Air-Gapped Fallback:** The assistant operates via Google Gemini API (`GEMINI_API_KEY`, using free tier models with automatic capacity failover) with a 100% air-gapped **Deterministic Administrative Fallback Mode** (pure local SQL queries) if unconfigured or offline.
3. **Deterministic Administrative Fallback:** If cloud API runtimes are offline, unconfigured, or unreachable, the system automatically falls back to deterministic rule-based SQL aggregation, preventing runtime failure while eliminating non-deterministic hallucination risk.
4. **Data Provenance Transparency:** Genuine MoSPI database records (1,798 authenticated projects) are strictly demarcated from synthetic demo illustrations (12-Month S-Curve & Phase Tracker) with explicit UI visual isolation and warning badges.

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                             SOVEREIGN TRUST BOUNDARY                                     │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  [ React 18 Sovereign UI ] ◄──► [ FastAPI 0.141 Backend ] ◄──► [ SQLite: paimana.db ]    │
│                                           │                                              │
│                                           ▼                                              │
│               [ Local ML & Grounded RAG (Gemini API / Local Fallback) ]                  │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Data Provenance & Authenticity Matrix

| Data Category | Data Origin / Source | Verification Method | Trust Level |
|---|---|---|---|
| **Central Sector Projects (1,798 rows)** | Official MoSPI Flash Report PDF — June 2026 Snapshot (Table 6) | Extracted via PyMuPDF with stateful ministry banner tracking | 🟢 **100% Authentic Government Data** |
| **Sanctioned Outlay (₹35.38 Lakh Cr)** | Direct summation of baseline project sanctions (`approved_cost_cr`) | Reconciled against official MoSPI aggregate (₹35.62 Lakh Cr $\pm 0.7\%$) | 🟢 **100% Authentic Government Data** |
| **Cumulative Expenditure (₹21.93 Lakh Cr)** | Direct extraction from Flash Report expenditure column | Reconciled against official MoSPI aggregate (₹21.97 Lakh Cr $\pm 0.2\%$) | 🟢 **100% Authentic Government Data** |
| **Canonical Ministry Classifications** | Statutory Central Ministries (MoRTH, Railways, Power, Coal, MoPNG, etc.) | Normalized via `MINISTRY_CANONICAL_MAP` in ETL | 🟢 **100% Verified Statutory Taxonomy** |
| **Predictive Overrun & Delay Bounds** | Dual XGBoost + Quantile Gradient Boosting Regressors (90% CI) | Enforced $\text{lower} \le \text{pred} \le \text{upper}$ (0 violations in `system_audit.py`) | 🟢 **Mathematically Verified ML Output** |
| **TreeSHAP Operational Bottlenecks** | Game-theoretic TreeExplainer attribution on 25 multi-factor features | Attributed feature contributions (+X pts) mapped per project | 🟢 **Explainable AI (XAI) Output** |
| **Demo 12-Month S-Curve Telemetry** | Back-calculated monthly S-curve progression from current real snapshot | Enclosed in **Demo Telemetry Sandbox** with `FlaskConical` badge | 🟡 **Synthetic Illustration Only** |
| **Demo Project Phase Execution Tracker** | Extrapolated 5-phase timeline from start/end dates and physical % | Enclosed in **Demo Telemetry Sandbox** with `FlaskConical` badge | 🟡 **Synthetic Illustration Only** |

---

## 3. Application Security & Defense Mechanisms

### 3.1 Input Validation & Anti-Tampering
* **Pydantic v2 Schema Enforcement:** All API payloads are strictly validated against strongly-typed Pydantic models before processing.
* **SQL Injection Prevention:** 100% of database queries use parameterized SQL bindings (`?` or named parameters) via Python's standard `sqlite3` driver; zero raw string concatenation.
* **Bounded Numerical Ranges:** Financial outlays are constrained to positive floats ($\ge 0$), and progress percentages are clamped to $[0.0, 100.0]\%$.

### 3.2 Rate Limiting & Denial-of-Service Protection
* **Sliding-Window Rate Limiter:** The FastAPI backend enforces a sliding-window rate limit (100 requests per minute per IP address) preventing automated scraping or denial-of-service degradation.
* **Sub-250ms Response Latency:** Pre-computed feature stores and indexed SQLite queries ensure rapid response times without high CPU load.

### 3.3 Prompt Injection Defense & LLM Guardrails
* **Structured Delimiter Isolation:** Prompts constructed for the LLM utilize structured system instructions and context delimiters to prevent user input from overriding administrative system instructions.
* **Database Schema Abstraction:** Raw database table structures, internal SQL commands, and system connection strings are completely abstracted and never exposed to the LLM prompt context.
* **Fact Grounding & Citation Mandate:** The assistant is instructed to cite explicit Project IDs (`[PRJ-XXXXXX]`) from the retrieved context and declare when a query falls outside the monitored dataset rather than hallucinating.

---

## 4. Ethical AI, Bias & Fair Governance

1. **Temporal Non-Contamination:** Model training strictly employs out-of-time chronological validation (800 historical train cohort vs. 200 out-of-time test cohort). No future data leakage is permitted into training matrices.
2. **Geographic & Sectoral Balance:** Feature matrices incorporate explicit state land friction and sector complexity weights to ensure high-density urban corridors and remote Himalayan projects are evaluated fairly according to their distinct engineering realities.
3. **Prescriptive Action Accountability:** Risk alerts map transparently to responsible statutory nodal authorities (MoEFCC, Railway Board, State Revenue), ensuring actionable accountability rather than ungrounded blame.
