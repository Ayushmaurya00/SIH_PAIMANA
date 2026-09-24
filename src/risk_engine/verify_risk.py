"""
Quick verification of risk_scores and alerts in paimana.db
"""
import sys
import json
import sqlite3
import pandas as pd

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('paimana.db')
df_risk = pd.read_sql('SELECT * FROM risk_scores LIMIT 6', conn)
df_alerts = pd.read_sql('SELECT * FROM alerts LIMIT 6', conn)
conn.close()

print("=" * 65)
print("SAMPLE RISK SCORES & TOP 3 EXPLAINABILITY FACTORS")
print("=" * 65)
for _, r in df_risk.iterrows():
    print(f"• Project {r['project_id']}: Score = {r['score']}/100 [{r['risk_level']} Risk] (Prev: {r['previous_score']})")
    raw = r['top_factors']
    factors = json.loads(raw) if isinstance(raw, str) else (raw or [])
    if isinstance(factors, str):
        factors = json.loads(factors)
    for f in factors:
        print(f"    - {f['factor']} (+{f['contribution']} pts): {f['detail']}")
    print()

print("=" * 65)
print("SAMPLE EARLY WARNING ALERTS")
print("=" * 65)
for _, a in df_alerts.iterrows():
    print(f"• [{a['severity']} Alert - {a['status']}] {a['project_id']}: {a['trigger_reason']}")
print("=" * 65)
