"""
Data Quality Check Script
Nifty 100 Financial Intelligence Platform

Checks:
- Rows and columns
- Missing values
- Duplicate rows
- Unique company count where company_id exists
"""

import pandas as pd
from pathlib import Path

data_path = Path("data/raw")
files = list(data_path.glob("*.xlsx"))

for file in files:
    print("\n" + "=" * 80)
    print(f"Dataset: {file.name}")
    print("=" * 80)

    try:
        # Core raw files have metadata row, actual header at row 2
        if file.stem in [
            "companies",
            "profitandloss",
            "balancesheet",
            "cashflow",
            "analysis",
            "documents",
            "prosandcons",
        ]:
            df = pd.read_excel(file, header=1)
        else:
            df = pd.read_excel(file)

        print(f"Rows: {df.shape[0]}")
        print(f"Columns: {df.shape[1]}")
        print(f"Total Missing Values: {df.isnull().sum().sum()}")
        print(f"Duplicate Rows: {df.duplicated().sum()}")

        if "company_id" in df.columns:
            print(f"Unique Companies: {df['company_id'].nunique()}")

        print("\nColumn-wise Missing Values:")
        print(df.isnull().sum())

    except Exception as e:
        print(f"Error reading {file.name}: {e}")