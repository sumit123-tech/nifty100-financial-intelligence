"""
Create SQLite Database

Creates the main SQLite database file for the
Nifty 100 Financial Intelligence Platform.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path("database/nifty100.db")

conn = sqlite3.connect(DB_PATH)

print("Database Created Successfully")
print(f"Database Path: {DB_PATH}")

conn.close()