import sqlite3

conn = sqlite3.connect('paimana.db')
cur = conn.cursor()

rows = cur.execute("""
    SELECT prediction_id,
           cost_overrun_pct_pred, cost_overrun_pct_lower, cost_overrun_pct_upper,
           time_overrun_months_pred, time_delay_lower_months, time_delay_upper_months
    FROM model_predictions
""").fetchall()

fixed = 0
for row in rows:
    pred_id, c_pred, c_low, c_up, t_pred, t_low, t_up = row
    c_pred = round(float(c_pred or 0), 2)
    c_low  = round(float(c_low  or 0), 2)
    c_up   = round(float(c_up   or 0), 2)
    t_pred = round(float(t_pred or 0), 1)
    t_low  = round(float(t_low  or 0), 1)
    t_up   = round(float(t_up   or 0), 1)

    # Fix: upper must be >= max(lower, point prediction)
    new_c_low = max(0.0, c_low)
    new_c_up  = round(max(new_c_low, c_pred, c_up), 2)
    new_c_low = round(new_c_low, 2)

    new_t_low = max(0.0, t_low)
    new_t_up  = round(max(new_t_low, t_pred, t_up), 1)
    new_t_low = round(new_t_low, 1)

    if new_c_up != c_up or new_c_low != c_low or new_t_up != t_up or new_t_low != t_low:
        cur.execute("""
            UPDATE model_predictions
            SET cost_overrun_pct_lower=?, cost_overrun_pct_upper=?,
                time_delay_lower_months=?, time_delay_upper_months=?
            WHERE prediction_id=?
        """, (new_c_low, new_c_up, new_t_low, new_t_up, pred_id))
        fixed += 1

conn.commit()
print(f"Fixed {fixed} additional rows.")

bad = conn.execute("""
    SELECT COUNT(*) FROM model_predictions
    WHERE round(cost_overrun_pct_lower,2) > round(cost_overrun_pct_pred,2)
       OR round(cost_overrun_pct_pred,2) > round(cost_overrun_pct_upper,2)
""").fetchone()[0]
print(f"Remaining cost violations (rounded): {bad}")

bad_t = conn.execute("""
    SELECT COUNT(*) FROM model_predictions
    WHERE round(time_delay_lower_months,1) > round(time_overrun_months_pred,1)
       OR round(time_overrun_months_pred,1) > round(time_delay_upper_months,1)
""").fetchone()[0]
print(f"Remaining time violations (rounded): {bad_t}")
conn.close()
