import sqlite3
c = sqlite3.connect('paimana.db')
tables = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
print("Tables:", tables)
cnt = c.execute("SELECT COUNT(*) FROM projects").fetchone()[0]
print("Projects count:", cnt)
c.close()
