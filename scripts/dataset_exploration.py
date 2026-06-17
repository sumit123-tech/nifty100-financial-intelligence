"""
Dataset Exploration Script
Nifty 100 Financial Intelligence Platform

Loads all datasets and displays:
- Shape
- Columns
- First 5 rows
"""

import pandas as pd
from pathlib import Path

data_path = Path("data/raw")

files = data_path.glob("*.xlsx")

for file in files:
    print("\n" + "=" * 80)
    print(f"Dataset: {file.name}")
    print("=" * 80)

    df = pd.read_excel(file)

    print(f"Shape: {df.shape}")

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst 5 Rows:")
    print(df.head())