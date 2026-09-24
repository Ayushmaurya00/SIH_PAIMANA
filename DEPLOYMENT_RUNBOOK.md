# Deployment & Operational Runbook
## PAIMANA AI — DevOps, Containerization & Production Guide
**Ministry of Statistics and Programme Implementation (MoSPI) — Infrastructure and Project Monitoring Division (IPMD)**
*Smart India Hackathon (SIH) 2024 — Verified DevOps & Reliability Runbook (v3.0)*
*Last Updated: September 2026 | Status: Production-Ready*

---

## 1. System Requirements & Architecture Overview

| Component | Minimum Specification | Recommended Specification |
|---|---|---|
| **Operating System** | Windows 10/11, Ubuntu 22.04 LTS, macOS Monterey+ | Linux x86_64 / Windows 11 64-bit |
| **CPU Architecture** | 4 Cores (x86_64 or ARM64) | 8+ Cores |
| **System Memory (RAM)** | 8 GB RAM | 16 GB RAM (for local LLM inference) |
| **Disk Storage** | 2 GB Free Storage | 10 GB Free SSD Storage |
| **Runtimes** | Python 3.10+ & Node.js 18+ | Python 3.11.x & Node.js 20 LTS |
| **Container Engine** | Docker 24.0+ & Docker Compose v2 | Docker Engine with Compose Plugin |

---

## 2. Deployment Methods

### Method A: Single-Command Native Execution (Fastest for Demos & Testing)

The repository includes pre-configured automation scripts that auto-detect Python, verify virtual environments, seed database tables if missing, and launch both FastAPI and Vite services concurrently.

```bash
# -------------------------------------------------------------
# 1. WINDOWS (Command Prompt / Double-Click):
# -------------------------------------------------------------
start.bat

# -------------------------------------------------------------
# 2. WINDOWS (PowerShell):
# -------------------------------------------------------------
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\start.ps1

# -------------------------------------------------------------
# 3. LINUX / MACOS (Bash / Zsh):
# -------------------------------------------------------------
chmod +x start.sh
./start.sh
```

* **Frontend Dashboard URL:** `http://localhost:5173`
* **FastAPI Backend URL:** `http://localhost:8000`
* **Interactive API Docs:** `http://localhost:8000/docs`

---

### Method B: Docker Multi-Container Orchestration (Production Standard)

The application includes multi-stage container definitions (`Dockerfile.api`, `frontend/Dockerfile`, and `docker-compose.yml`) enabling isolated, zero-dependency deployment.

```bash
# 1. Build and start containers in detached mode
docker compose up --build -d

# 2. Verify running container health
docker compose ps

# 3. View live combined logs
docker compose logs -f

# 4. Graceful shutdown
docker compose down
```

*Container Port Forwarding:*
* Frontend UI: `http://localhost:5173` and `http://localhost:80`
* Backend REST API: `http://localhost:8000`

---

## 3. Environment Variable Configuration (`.env`)

A sample configuration file is provided at `.env.example`. Copy it to `.env` to customize settings:

```ini
# ==============================================================================
# PAIMANA AI - SYSTEM CONFIGURATION
# ==============================================================================
ENVIRONMENT=production
LOG_LEVEL=INFO

# Security & CORS
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000,http://localhost:80

# Database Settings
DATABASE_PATH=paimana.db
DB_RETRY_ATTEMPTS=3
DB_RETRY_DELAY_SEC=0.2

# Google Gemini API Configuration (Google AI Studio Free Tier)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.6-flash
```

---

## 4. Operational Maintenance & Standard Operating Procedures (SOP)

### SOP-1: Ingesting a New Monthly MoSPI Flash Report PDF
When a new monthly Flash Report PDF is published by MoSPI:
```bash
# 1. Place the PDF in the data directory or ingest via script:
python scripts/ingest_flash_report.py

# 2. Run ministry deduplication:
python scripts/fix_ministry_names.py

# 3. Re-train ML models & re-compute conformal bands:
python src/models/train_and_evaluate.py

# 4. Recalibrate risk scores:
python scripts/recalibrate_scores.py

# 5. Execute 25-point system audit to confirm 100% data integrity:
python scripts/system_audit.py
```

---

### SOP-2: Automated System Audit & Health Check
Run the automated verification harness prior to any demonstration or production deployment:
```bash
python scripts/system_audit.py
```
*Expected Output:*
```text
======================================================================
SUMMARY: 25/25 PASS  |  0 WARN  |  0 FAIL
STATUS:  ALL ASSERTIONS PASSED -- System is production-ready.
======================================================================
```

---

### SOP-3: Database Backup & Recovery
To create a safe hot backup of the SQLite database:
```bash
# Backup:
sqlite3 paimana.db ".backup 'paimana_backup_$(date +%Y%m%d).db'"

# Restore:
cp paimana_backup_20260902.db paimana.db
python scripts/system_audit.py
```

---

## 5. Troubleshooting & Diagnostic Guide

| Issue / Symptom | Root Cause | Resolution Steps |
|---|---|---|
| `Port 8000 already in use` | Prior backend process still bound to port. | Windows: `netstat -ano \| findstr :8000` $\to$ `taskkill /PID <PID> /F`<br>Linux: `lsof -ti:8000 \| xargs kill -9` |
| `Gemini API quota/unreachable` | API key missing, invalid, or network unavailable. | Add your free API key in `.env` as `GEMINI_API_KEY`. The system automatically falls back to grounded deterministic templates if offline or unconfigured. |
| `Conformal bound violation` | Model predictions updated without bound clipping. | Execute `python scripts/recalibrate_scores.py` to enforce $\text{lower} \le \text{pred} \le \text{upper}$. |
| `Duplicate ministry in filter` | Variant spelling in raw PDF. | Run `python scripts/fix_ministry_names.py` to normalize all records to canonical statutory ministry keys. |
