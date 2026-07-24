import os
import sqlite3
import pandas as pd

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

DB_PATH = "database/nifty100.db"

OUTPUT_DIR = "reports/portfolio"

os.makedirs(OUTPUT_DIR, exist_ok=True)

styles = getSampleStyleSheet()

conn = sqlite3.connect(DB_PATH)

companies = pd.read_sql("""

SELECT
    c.company_id,
    c.company_name,
    s.broad_sector,
    r.return_on_equity_pct,
    r.operating_profit_margin_pct,
    r.net_profit_margin_pct,
    r.debt_to_equity,
    r.revenue_cagr_5yr,
    r.stock_score

FROM companies c

LEFT JOIN sectors s
ON c.company_id=s.company_id

LEFT JOIN financial_ratios r
ON c.company_id=r.company_id

WHERE r.year='Mar 2024'

ORDER BY c.company_name

""", conn)


pdf = SimpleDocTemplate(

    os.path.join(

        OUTPUT_DIR,

        "portfolio_summary.pdf"

    )

)

story = []

for _, row in companies.iterrows():

    story.append(

        Paragraph(

            f"<b>{row.company_name}</b> ({row.company_id})",

            styles["Title"]

        )

    )

    story.append(

        Paragraph(

            f"Sector : {row.broad_sector}",

            styles["Heading2"]

        )

    )

    story.append(Spacer(1,12))

    table_data = [

        ["Metric","Value"],

        ["ROE",row.return_on_equity_pct],

        ["OPM",row.operating_profit_margin_pct],

        ["Net Margin",row.net_profit_margin_pct],

        ["Debt / Equity",row.debt_to_equity],

        ["Revenue CAGR 5Y",row.revenue_cagr_5yr],

        ["Stock Score",row.stock_score]

    ]

    table = Table(table_data)

    table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("GRID",(0,0),(-1,-1),0.5,colors.black),

            ("BACKGROUND",(0,1),(-1,-1),colors.beige),

            ("FONTSIZE",(0,0),(-1,-1),10)

        ])

    )

    story.append(table)

    story.append(PageBreak())

pdf.build(story)

conn.close()

print("="*50)
print("Portfolio Summary Generated")
print("="*50)

print(f"Companies : {len(companies)}")
print("Saved -> reports/portfolio/portfolio_summary.pdf")