"""
Create Database Tables
Nifty 100 Financial Intelligence Platform
"""

import sqlite3

conn = sqlite3.connect("database/nifty100.db")

cursor = conn.cursor()

# Companies Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS companies (
    company_id TEXT PRIMARY KEY,
    company_name TEXT,
    current_price REAL,
    market_cap REAL,
    pe_ratio REAL,
    dividend_yield REAL,
    roce_percentage REAL,
    roe_percentage REAL
)
""")

print("Companies table created successfully")

conn.commit()
conn.close()

print("Database schema initialized")