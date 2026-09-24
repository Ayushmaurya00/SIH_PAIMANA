"""
Flash Report & CUF Data Import Ingestion Router
"""

import os
import re
import time
import json
import logging
import pathlib
from typing import Optional, List
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks, Depends
from src.api.db import get_db, ROOT_DIR, DB_PATH
from src.api.auth import get_current_user

logger = logging.getLogger("PAIMANA_API.Import")
router = APIRouter(tags=["Import"])


def _run_post_ingestion_scoring():
    """Runs ML inference and falls back to rule-based scoring for unscored projects."""
    try:
        from src.models.train_and_evaluate import run_fast_inference
        from src.risk_engine.scorer import calculate_risk_scores, load_project_data
        run_fast_inference(DB_PATH)
        df_p, df_s, df_m, df_preds = load_project_data(DB_PATH)
        scores, alerts = calculate_risk_scores(df_p, df_s, df_m, df_preds)
        conn = get_db()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM risk_scores")
            cur.execute("DELETE FROM alerts")
            for s in scores:
                cur.execute("""
                    INSERT INTO risk_scores (project_id, score, risk_level, top_factors, prescriptive_actions, computed_at, previous_score)
                    VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?)
                """, (s['project_id'], s.get('score', s.get('risk_score', 50.0)), s['risk_level'], json.dumps(s.get('top_factors', [])), json.dumps(s.get('prescriptive_actions', [])), s.get('previous_score', 0.0)))
            for a in alerts:
                cur.execute("""
                    INSERT INTO alerts (project_id, triggered_at, trigger_reason, severity, status, prescriptive_action, lead_time_months)
                    VALUES (?, CURRENT_TIMESTAMP, ?, ?, ?, ?, ?)
                """, (a['project_id'], a['trigger_reason'], a['severity'], a['status'], a.get('prescriptive_action', ''), a.get('lead_time_months', 6.0)))
            conn.commit()
        finally:
            conn.close()
    except Exception as ml_err:
        logger.warning(f"Post-ingestion ML scoring note: {ml_err}")

    # Rule-based fallback for any remaining unscored projects
    try:
        conn = get_db()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT p.project_id, p.status, p.physical_progress_pct, p.revised_cost_cr, p.approved_cost_cr
                FROM projects p WHERE NOT EXISTS (SELECT 1 FROM risk_scores r WHERE r.project_id = p.project_id)
            """)
            unscored = cur.fetchall()
            for row in unscored:
                pid_u, status_u, prog_u, rev_u, app_u = row[0], row[1], float(row[2] or 0), float(row[3] or 0), float(row[4] or 1)
                overrun_pct = ((rev_u - app_u) / max(app_u, 1)) * 100.0
                base_map = {"Stalled": 82.0, "Delayed": 68.0, "Completed": 12.0}
                base = base_map.get(status_u, 30.0)
                score_u = round(min(100.0, base + min(overrun_pct * 0.3, 20.0) - min(prog_u * 0.2, 15.0)), 1)
                level_u = "High" if score_u >= 58 else ("Medium" if score_u >= 32 else "Low")
                factors = [{"factor": f"Status: {status_u}", "impact": score_u}]
                actions = ["Escalate to Ministry Secretary within 30 days."] if level_u == "High" else ["Continue monthly monitoring."]
                cur.execute("""
                    INSERT INTO risk_scores (project_id, score, risk_level, top_factors, prescriptive_actions, computed_at, previous_score)
                    VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, 0.0)
                """, (pid_u, score_u, level_u, json.dumps(factors), json.dumps(actions)))
            if unscored:
                conn.commit()
        finally:
            conn.close()
    except Exception as fallback_err:
        logger.warning(f"Rule-based fallback scoring note: {fallback_err}")


@router.post("/api/import/report")
async def import_flash_reports(
    background_tasks: BackgroundTasks,
    files: Optional[List[UploadFile]] = File(None),
    file: Optional[UploadFile] = File(None),
    reference_month: Optional[str] = Form(None),
    user=Depends(get_current_user),
):
    upload_list = [f for f in (files or []) if f.filename]
    if file and file.filename and file not in upload_list:
        upload_list.append(file)
    if not upload_list:
        raise HTTPException(status_code=400, detail="No files uploaded. Please select one or more .pdf or .csv files.")

    temp_dir = os.path.join(ROOT_DIR, "data", "uploads")
    os.makedirs(temp_dir, exist_ok=True)
    total_projects, total_snapshots, file_details, temp_paths = 0, 0, [], []

    try:
        for idx, ufile in enumerate(upload_list):
            raw_filename = ufile.filename or f"report_{idx+1}"
            # Sanitize filename: prevent path traversal and special chars
            safe_base = pathlib.Path(raw_filename).name
            safe_base = re.sub(r"[^a-zA-Z0-9._-]", "_", safe_base)[:100]
            if not safe_base:
                safe_base = f"report_{idx+1}.pdf"
            ext = os.path.splitext(safe_base)[1].lower()
            if ext not in ['.csv', '.pdf']:
                file_details.append({"filename": safe_base, "status": "skipped", "reason": "Unsupported format"})
                continue
            # Validate content-type and size (10MB limit)
            contents = await ufile.read()
            if len(contents) > 10 * 1024 * 1024:
                file_details.append({"filename": safe_base, "status": "skipped", "reason": "File too large (>10MB)"})
                continue
            if ext == '.pdf' and not contents.startswith(b'%PDF'):
                file_details.append({"filename": safe_base, "status": "skipped", "reason": "Invalid PDF header"})
                continue

            filename = safe_base
            temp_path = os.path.join(temp_dir, f"upload_{int(time.time())}_{idx}_{filename}")
            # Ensure temp_path is inside temp_dir
            if os.path.commonpath([os.path.abspath(temp_path), os.path.abspath(temp_dir)]) != os.path.abspath(temp_dir):
                file_details.append({"filename": filename, "status": "skipped", "reason": "Invalid path"})
                continue
            temp_paths.append(temp_path)
            with open(temp_path, "wb") as f:
                f.write(contents)
            try:
                os.chmod(temp_path, 0o600)
            except Exception:
                pass

            if ext == '.pdf':
                from src.etl.pdf_ingestion import ingest_pdf_file
                res = ingest_pdf_file(temp_path, DB_PATH, reference_month=reference_month)
                file_type = "MoSPI Flash Report PDF"
            else:
                from src.etl.csv_importer import ingest_csv_file
                res = ingest_csv_file(temp_path, DB_PATH, reference_month=reference_month)
                file_type = "CUF Data CSV"

            p_cnt = res.get("projects_upserted", 0)
            s_cnt = res.get("snapshots_inserted", 0)
            file_warnings = res.get("warnings", [])
            total_projects += p_cnt
            total_snapshots += s_cnt
            file_details.append({
                "filename": filename, "file_type": file_type, "projects_processed": p_cnt,
                "snapshots_recorded": s_cnt, "warnings": file_warnings, "warnings_count": len(file_warnings), "status": "success"
            })

        # Offload scoring to background to avoid blocking HTTP response (HIGH-10)
        background_tasks.add_task(_run_post_ingestion_scoring)
        all_warnings = [w for f in file_details for w in f.get('warnings', [])]
        return {
            "status": "success", "files_processed": len(upload_list), "projects_processed": total_projects,
            "snapshots_recorded": total_snapshots, "file_details": file_details, "warnings": all_warnings,
            "warnings_count": len(all_warnings), "message": f"Successfully ingested {total_projects} projects and {total_snapshots} snapshots. Scoring running in background.",
            "scoring_status": "background"
        }
    except Exception as e:
        logger.error(f"Error ingesting batch reports: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to parse and ingest files: {str(e)}")
    finally:
        for p in temp_paths:
            if os.path.exists(p):
                try:
                    os.remove(p)
                except Exception:
                    pass
