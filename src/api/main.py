from fastapi import FastAPI
import sqlite3
import pandas as pd


app = FastAPI(
    title="Nifty100 Financial Intelligence API",
    version="1.0"
)

DB_PATH = "database/nifty100.db"


import numpy as np

def run_query(query):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(query, conn)
    conn.close()

    df = df.replace({np.nan: None})

    print(df.head())      # Debug
    print(df.dtypes)      # Debug

    return df.to_dict(orient="records")


@app.get("/")
def home():
    return {
        "project": "Nifty100 Financial Intelligence",
        "version": "1.0"
    }


@app.get("/health")
def health():
    return {"status": "OK"}


@app.get("/companies")
def companies():
    return run_query("""
        SELECT company_id, company_name
        FROM companies
        ORDER BY company_name
    """)


@app.get("/company/{ticker}")
def company(ticker: str):
    return run_query(f"""
        SELECT *
        FROM companies
        WHERE company_id='{ticker.upper()}'
    """)


@app.get("/ratios/{ticker}")
def ratios(ticker: str):
    data = run_query(f"""
        SELECT *
        FROM financial_ratios
        WHERE company_id='{ticker.upper()}'
        ORDER BY year
    """)

    print(type(data))
    print(data)

    return data


@app.get("/cashflow/{ticker}")
def cashflow(ticker: str):
    return run_query(f"""
        SELECT *
        FROM cashflow
        WHERE company_id='{ticker.upper()}'
        ORDER BY year
    """)


@app.get("/balancesheet/{ticker}")
def balancesheet(ticker: str):
    return run_query(f"""
        SELECT *
        FROM balancesheet
        WHERE company_id='{ticker.upper()}'
        ORDER BY year
    """)


@app.get("/valuation/{ticker}")
def valuation(ticker: str):
    return run_query(f"""
        SELECT *
        FROM market_cap
        WHERE company_id='{ticker.upper()}'
        ORDER BY year
    """)


@app.get("/sectors")
def sectors():
    return run_query("""
        SELECT broad_sector,
               COUNT(company_id) as companies
        FROM sectors
        GROUP BY broad_sector
    """)


@app.get("/sector/{name}")
def sector(name: str):
    return run_query(f"""
        SELECT s.company_id,
               c.company_name
        FROM sectors s
        JOIN companies c
        ON s.company_id=c.company_id
        WHERE s.broad_sector='{name}'
    """)


@app.get("/peers/{ticker}")
def peers(ticker: str):

    peer = run_query(f"""
        SELECT peer_group_name
        FROM peer_groups
        WHERE company_id='{ticker.upper()}'
    """)

    if not peer:
        return []

    group_name = peer[0]["peer_group_name"]

    return run_query(f"""
        SELECT *
        FROM peer_groups
        WHERE peer_group_name='{group_name}'
    """)


@app.get("/proscons/{ticker}")
def proscons(ticker: str):
    return run_query(f"""
        SELECT *
        FROM prosandcons
        WHERE company_id='{ticker.upper()}'
    """)


@app.get("/cluster/{ticker}")
def cluster(ticker: str):

    df = pd.read_csv("output/cluster_labels.csv")

    result = df[
        df["company_id"] == ticker.upper()
    ]

    return result.to_dict(orient="records")


@app.get("/capital/{ticker}")
def capital(ticker: str):

    df = pd.read_csv("output/capital_allocation.csv")

    result = df[
        df["company_id"] == ticker.upper()
    ]

    return result.to_dict(orient="records")


@app.get("/reports")
def reports():

    import os

    files = []

    for root, dirs, filenames in os.walk("reports"):
        for f in filenames:
            files.append(f)

    return files


@app.get("/screen")
def screen(
    roe: float = 15,
    de: float = 1
):
    return run_query(f"""
        SELECT company_id,
               year,
               return_on_equity_pct,
               debt_to_equity
        FROM financial_ratios
        WHERE year='Mar 2024'
        AND return_on_equity_pct >= {roe}
        AND debt_to_equity <= {de}
    """)