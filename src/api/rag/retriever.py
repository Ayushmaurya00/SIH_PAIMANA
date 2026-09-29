"""
Hybrid Database & BM25 Keyword Search Retriever
"""

import re
import json
import sqlite3
import pandas as pd
from typing import Dict, Any, List


def safe_parse_json(raw_val: Any) -> List[Any]:
    """Safely unpacks JSON lists or strings handling double-serialization and nulls."""
    if not raw_val:
        return []
    if isinstance(raw_val, list):
        return raw_val
    try:
        val = json.loads(raw_val)
        if isinstance(val, str):
            val = json.loads(val)
        return val if isinstance(val, list) else ([val] if val else [])
    except Exception:
        return []


class HybridRetriever:
    """Keyword & metadata search over project database."""
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def search_projects(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        import logging
        logger = logging.getLogger("PAIMANA_RAG")
        tokens = [t.strip().lower() for t in re.findall(r'\b\w+\b', query) if len(t.strip()) > 2]
        if not tokens:
            tokens = ['infrastructure']
        # Cap tokens to avoid OR explosion (HIGH-10, MEDIUM-10)
        tokens = tokens[:6]

        conditions = []
        params = []
        for t in tokens:
            # Sanitize token: alphanumeric only, max 30 chars
            t_clean = re.sub(r"[^a-z0-9]", "", t)[:30]
            if not t_clean:
                continue
            conditions.append("""
                (LOWER(p.project_name) LIKE ? OR
                 LOWER(p.sector) LIKE ? OR
                 LOWER(p.ministry) LIKE ? OR
                 LOWER(p.implementing_agency) LIKE ? OR
                 LOWER(p.state) LIKE ?)
            """)
            term = f"%{t_clean}%"
            params.extend([term, term, term, term, term])
        if not conditions:
            logger.warning(f"No valid tokens from query: {query[:100]}")
            conditions.append("LOWER(p.project_name) LIKE ?")
            params.append("%infrastructure%")

        where_clause = " OR ".join(conditions)
        sql = f"""
            SELECT p.*, r.score, r.risk_level, r.top_factors, r.prescriptive_actions,
                   m.cost_overrun_prob, m.cost_overrun_pct_pred, m.cost_overrun_pct_lower, m.cost_overrun_pct_upper,
                   m.time_overrun_prob, m.time_overrun_months_pred, m.time_delay_lower_months, m.time_delay_upper_months
            FROM projects p
            LEFT JOIN risk_scores r ON p.project_id = r.project_id
            LEFT JOIN model_predictions m ON p.project_id = m.project_id AND m.feature_set = 'cuf_plus_extra'
            WHERE {where_clause}
            ORDER BY r.score DESC, p.approved_cost_cr DESC
            LIMIT ?
        """
        params.append(limit)
        df = pd.read_sql(sql, self.conn, params=params)
        return df.to_dict('records')
