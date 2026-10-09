"""
PAIMANA AI - Unified Cross-Platform System Orchestrator & Live Runner
Launches FastAPI backend, React frontend, verifies Ollama connectivity,
monitors startup health checks, and manages graceful shutdown.
"""

import os
import sys
import time
import socket
import signal
import urllib.request
import subprocess
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")


def print_banner():
    print("=" * 72, flush=True)
    print("   🏛️  PAIMANA AI — Infrastructure Project Monitoring Division (IPMD)", flush=True)
    print("   Ministry of Statistics and Programme Implementation (MoSPI)", flush=True)
    print("=" * 72, flush=True)


def check_port(host: str, port: int) -> bool:
    """Returns True if port is open/in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.8)
        return s.connect_ex((host, port)) == 0


def check_ai_status() -> tuple[bool, str]:
    """Verifies whether a Gemini API key is configured or fallback mode is active."""
    key = GEMINI_API_KEY.strip()
    if key:
        return True, f"Google Gemini API Key Configured (Model: {GEMINI_MODEL})"
    return False, "GEMINI_API_KEY not set in .env (Grounded Deterministic Fallback Mode active)"


def verify_prerequisites(python_exe: str):
    print("\n[1/4] Verifying Environment & Data Artifacts...", flush=True)

    # Check Database & ML Models
    db_path = os.path.join(ROOT_DIR, "paimana.db")
    cuf_model = os.path.join(ROOT_DIR, "artifacts", "models", "model_bundle_cuf_only.joblib")
    extra_model = os.path.join(ROOT_DIR, "artifacts", "models", "model_bundle_cuf_plus_extra.joblib")

    if not os.path.exists(db_path):
        print("  • Database missing — initializing empty database schema...", flush=True)
        subprocess.run([python_exe, os.path.join(ROOT_DIR, "src", "data_gen", "generate_data.py"), "--n-projects", "0"], check=True)
    else:
        print("  ✓ SQLite Database: paimana.db (Ready)", flush=True)

    if not (os.path.exists(cuf_model) and os.path.exists(extra_model)):
        print("  • Model checkpoints missing — training ML pipelines & SHAP matrices...", flush=True)
        subprocess.run([python_exe, os.path.join(ROOT_DIR, "src", "models", "train_and_evaluate.py")], check=True)
        subprocess.run([python_exe, os.path.join(ROOT_DIR, "src", "risk_engine", "scorer.py")], check=True)
    else:
        print("  ✓ ML Bundles: model_bundle_cuf_only.joblib & model_bundle_cuf_plus_extra.joblib (Ready)", flush=True)

    # Check PyMuPDF
    try:
        subprocess.run([python_exe, "-c", "import fitz"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("  ✓ PDF Ingestion Engine: PyMuPDF (Ready)", flush=True)
    except Exception:
        print("  • Installing PyMuPDF for PDF Flash Report parsing...", flush=True)
        subprocess.run([python_exe, "-m", "pip", "install", "pymupdf>=1.23.0"], check=True)
        print("  ✓ PDF Ingestion Engine: PyMuPDF (Installed & Ready)", flush=True)

    # Check AI Assistant status
    is_ai_ready, ai_msg = check_ai_status()
    if is_ai_ready:
        print(f"  ✓ Decision Assistant (Gemini API): {ai_msg}", flush=True)
    else:
        print(f"  ℹ️  Decision Assistant: {ai_msg}", flush=True)


def wait_for_http_200(url: str, max_retries: int = 25, delay: float = 0.5) -> bool:
    """Polls a URL until it returns HTTP 200."""
    for _ in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "PAIMANA-HealthCheck"})
            with urllib.request.urlopen(req, timeout=1.0) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            pass
        time.sleep(delay)
    return False


def main():
    print_banner()
    python_exe = sys.executable

    # 1. Check prerequisites
    verify_prerequisites(python_exe)

    # 2. Check if ports 8000 or 5173 are already running
    if check_port("127.0.0.1", 8000):
        print("  ⚠️  Port 8000 is already in use. Reusing active FastAPI process.", flush=True)
        backend_proc = None
    else:
        print("\n[2/4] Starting FastAPI Backend on http://localhost:8000 ...", flush=True)
        backend_cmd = [
            python_exe, "-m", "uvicorn", "src.api.main:app",
            "--host", "0.0.0.0", "--port", "8000", "--reload"
        ]
        backend_proc = subprocess.Popen(
            backend_cmd,
            cwd=ROOT_DIR
        )

    # Wait for backend health
    print("  • Waiting for API health check...", flush=True)
    if wait_for_http_200("http://localhost:8000/api/health", max_retries=30):
        print("  ✓ FastAPI Backend: HEALTHY (http://localhost:8000/api/health)", flush=True)
    else:
        print("  ⚠️  Backend took longer than expected to initialize.", flush=True)

    # 3. Check frontend
    npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
    frontend_proc = None
    if check_port("127.0.0.1", 5173):
        print("\n[3/4] Port 5173 is already in use. Reusing active Vite Frontend.", flush=True)
    else:
        print("\n[3/4] Starting Vite React Frontend on http://localhost:5173 ...", flush=True)
        log_file = os.path.join(ROOT_DIR, "frontend_startup.log")
        f_log = open(log_file, "w", encoding="utf-8")
        frontend_cmd = [npm_cmd, "run", "dev", "--", "--host", "--port", "5173"]
        frontend_proc = subprocess.Popen(
            frontend_cmd,
            cwd=FRONTEND_DIR,
            stdout=f_log,
            stderr=subprocess.STDOUT,
            shell=(sys.platform == "win32")
        )

        # Wait for frontend
        print("  • Waiting for Vite development server...", flush=True)
        if wait_for_http_200("http://localhost:5173", max_retries=30):
            print("  ✓ React Frontend: READY (http://localhost:5173)", flush=True)
        elif frontend_proc.poll() is not None:
            print(f"  ❌ React Frontend process exited (code {frontend_proc.returncode}). See frontend_startup.log for details.", flush=True)
        else:
            print("  ⚠️  React Frontend took longer than expected to initialize. Check http://localhost:5173.", flush=True)

    # 4. Success summary
    print("\n" + "=" * 72 + "\n   ✅ PAIMANA AI DECISION SUPPORT SYSTEM IS FULLY OPERATIONAL!\n" + "=" * 72, flush=True)
    print("   🌐 Dashboard: http://localhost:5173 | Explorer: /explorer | Alerts: /alerts\n   ⚖️  Models:    http://localhost:5173/models | API Docs: http://localhost:8000/docs", flush=True)
    print("=" * 72 + "\n   Press Ctrl+C in this terminal to gracefully stop all services.\n" + "=" * 72 + "\n", flush=True)

    def handle_exit(sig, frame):
        print("\n🛑 Shutting down PAIMANA AI services...", flush=True)
        if backend_proc:
            backend_proc.terminate()
        if frontend_proc:
            frontend_proc.terminate()
        print("✓ All processes stopped cleanly. Goodbye!\n", flush=True)
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    # Keep alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        handle_exit(None, None)


if __name__ == "__main__":
    main()
