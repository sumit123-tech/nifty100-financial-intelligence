import os
import sqlite3
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

DB_PATH = "database/nifty100.db"

REPORT_DIR = "reports/tearsheets"

os.makedirs(REPORT_DIR, exist_ok=True)

styles = getSampleStyleSheet()


# -----------------------------
# Database
# -----------------------------

conn = sqlite3.connect(DB_PATH)


def load_company(company_id):

    return pd.read_sql(
        f"""
        SELECT *
        FROM companies
        WHERE company_id='{company_id}'
        """,
        conn
    )


def load_ratios(company_id):

    return pd.read_sql(
        f"""
        SELECT *
        FROM financial_ratios
        WHERE company_id='{company_id}'
        ORDER BY year
        """,
        conn
    )


def load_pl(company_id):

    return pd.read_sql(
        f"""
        SELECT *
        FROM profitandloss
        WHERE company_id='{company_id}'
        ORDER BY year
        """,
        conn
    )


def load_bs(company_id):

    return pd.read_sql(
        f"""
        SELECT *
        FROM balancesheet
        WHERE company_id='{company_id}'
        ORDER BY year
        """,
        conn
    )


def load_cf(company_id):

    return pd.read_sql(
        f"""
        SELECT *
        FROM cashflow
        WHERE company_id='{company_id}'
        ORDER BY year
        """,
        conn
    )


def latest_ratio(df):

    if df.empty:
        return None

    return df.iloc[-1]


def safe(value):

    if pd.isna(value):
        return "N/A"

    return value



# -----------------------------
# KPI Table
# -----------------------------
def create_kpi_table(ratio):

    data = [
        ["Metric", "Value"],
        ["ROE (%)", safe(ratio["return_on_equity_pct"])],
        ["Net Profit Margin (%)", safe(ratio["net_profit_margin_pct"])],
        ["Operating Margin (%)", safe(ratio["operating_profit_margin_pct"])],
        ["Debt / Equity", safe(ratio["debt_to_equity"])],
        ["Interest Coverage", safe(ratio["interest_coverage"])],
        ["Revenue CAGR 5Y (%)", safe(ratio["revenue_cagr_5yr"])]
    ]

    table = Table(data, colWidths=[220, 120])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.darkblue),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),

        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),

        ("BACKGROUND", (0,1), (-1,-1), colors.whitesmoke),

        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTNAME", (0,1), (-1,-1), "Helvetica"),

        ("BOTTOMPADDING", (0,0), (-1,0), 10),

        ("ALIGN",(0,0),(-1,-1),"CENTER")
    ]))

    return table


# -----------------------------
# Revenue & Profit Table
# -----------------------------
def create_financial_table(pl):

    show = pl.tail(10)

    rows = [["Year","Revenue","Net Profit"]]

    for _, r in show.iterrows():

        rows.append([
            r["year"],
            safe(r["sales"]),
            safe(r["net_profit"])
        ])

    table = Table(rows)

    table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.green),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("GRID",(0,0),(-1,-1),0.4,colors.grey),

        ("BACKGROUND",(0,1),(-1,-1),colors.beige),

        ("ALIGN",(0,0),(-1,-1),"CENTER"),

        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold")

    ]))

    return table

# -----------------------------
# PDF Builder
# -----------------------------
def generate_tearsheet(company_id):

    company = load_company(company_id)

    ratios = load_ratios(company_id)

    pl = load_pl(company_id)

    if company.empty or ratios.empty:

        print(company_id, "Skipped")

        return

    latest = latest_ratio(ratios)

    pdf = SimpleDocTemplate(

        os.path.join(
            REPORT_DIR,
            f"{company_id}_tearsheet.pdf"
        )

    )

    story = []

    story.append(

        Paragraph(

            f"<b>{company.iloc[0]['company_name']}</b>",

            styles["Title"]

        )

    )

    story.append(

        Paragraph(

            company.iloc[0]["about_company"],

            styles["BodyText"]

        )

    )

    story.append(Spacer(1,20))

    story.append(create_kpi_table(latest))

    story.append(Spacer(1,20))

    story.append(create_financial_table(pl))

    pdf.build(story)

    print(company_id, "Done")

if __name__ == "__main__":

    companies = pd.read_sql(
        "SELECT company_id FROM companies ORDER BY company_id",
        conn
    )

    total = len(companies)

    print("=" * 50)
    print("Generating Company Tearsheets")
    print("=" * 50)

    for i, row in enumerate(companies.itertuples(), start=1):

        try:

            generate_tearsheet(row.company_id)

            print(f"[{i}/{total}] {row.company_id} ✔")

        except Exception as e:

            print(f"[{i}/{total}] {row.company_id} ❌ {e}")

    conn.close()

    print("\nAll PDFs Generated Successfully.")
