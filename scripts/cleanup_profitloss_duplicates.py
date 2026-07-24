import sqlite3

conn = sqlite3.connect("database/nifty100.db")
cursor = conn.cursor()

# Delete duplicate rows, keeping the smallest record_id
cursor.execute("""
DELETE FROM profitandloss
WHERE record_id NOT IN (
    SELECT MIN(record_id)
    FROM profitandloss
    GROUP BY company_id, year
)
""")

deleted = cursor.rowcount

conn.commit()

print(f"Rows Deleted : {deleted}")

remaining = cursor.execute("""
SELECT COUNT(*)
FROM (
    SELECT company_id, year
    FROM profitandloss
    GROUP BY company_id, year
    HAVING COUNT(*) > 1
)
""").fetchone()[0]

print(f"Remaining Duplicate Groups : {remaining}")

conn.close()