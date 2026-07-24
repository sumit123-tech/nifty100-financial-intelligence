import os
import sqlite3
import pandas as pd

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

DB_PATH = "database/nifty100.db"

OUTPUT_DIR = "reports/sector"

os.makedirs(OUTPUT_DIR, exist_ok=True)

styles = getSampleStyleSheet()

conn = sqlite3.connect(DB_PATH)


def load_sector_data(sector):

    query = f"""
    SELECT
        s.company_id,
        c.company_name,
        r.return_on_equity_pct,
        r.operating_profit_margin_pct,
        r.net_profit_margin_pct,
        r.debt_to_equity,
        r.revenue_cagr_5yr,
        r.pat_cagr_5yr,
        r.interest_coverage
    FROM sectors s

    JOIN companies c
    ON s.company_id = c.company_id

    JOIN financial_ratios r
    ON s.company_id = r.company_id

    WHERE s.broad_sector = '{sector}'
    AND r.year = 'Mar 2024'

    ORDER BY c.company_name
    """

    return pd.read_sql(query, conn)

def build_pdf(sector):

    df = load_sector_data(sector)

    if df.empty:

        print(sector, "Skipped")

        return

    pdf = SimpleDocTemplate(

        os.path.join(

            OUTPUT_DIR,

            f"{sector}_report.pdf"

        )

    )

    story = []

    story.append(

        Paragraph(

            f"<b>{sector} Sector Report</b>",

            styles["Title"]

        )

    )

    story.append(Spacer(1,20))

    table_data = [list(df.columns)]

    table_data.extend(df.values.tolist())

    table = Table(table_data)

    table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("GRID",(0,0),(-1,-1),0.4,colors.grey),

            ("BACKGROUND",(0,1),(-1,-1),colors.beige),

            ("FONTSIZE",(0,0),(-1,-1),8)

        ])

    )

    story.append(table)

    pdf.build(story)

    print(sector, "Done")


if __name__ == "__main__":

    sectors = pd.read_sql(

        """
        SELECT DISTINCT broad_sector
        FROM sectors
        ORDER BY broad_sector
        """,

        conn

    )

    print("="*50)

    print("Generating Sector Reports")

    print("="*50)

    for sector in sectors["broad_sector"]:

        try:

            build_pdf(sector)

        except Exception as e:

            print(sector, e)

    conn.close()

    print("\nFinished.")