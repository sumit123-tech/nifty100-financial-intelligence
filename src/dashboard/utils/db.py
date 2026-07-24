import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = "database/nifty100.db"


@st.cache_data(ttl=600)
def run_query(query):

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(query, conn)

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_companies():

    return run_query("""
        SELECT *
        FROM companies
        ORDER BY company_name
    """)

@st.cache_data(ttl=600)
def get_ratios(year=None):

    query = """
        SELECT
            f.*,
            m.pe_ratio,
            m.pb_ratio,
            m.ev_ebitda,
            m.dividend_yield_pct
        FROM financial_ratios f

        LEFT JOIN market_cap m
        ON f.company_id = m.company_id
        AND substr(f.year,-4)=CAST(m.year AS TEXT)
    """

    if year:
        query += f"""
        WHERE f.year='{year}'
        """

    return run_query(query)

@st.cache_data(ttl=600)
def get_sectors():

    return run_query("""
        SELECT
            broad_sector,
            COUNT(company_id) AS companies
        FROM sectors
        GROUP BY broad_sector
        ORDER BY companies DESC
    """)