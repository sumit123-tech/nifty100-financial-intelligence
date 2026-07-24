from src.screener.engine import ScreenerEngine
from src.screener.ranking import StockRanker

engine = ScreenerEngine()

# Load data
df = engine.load_data()

# Calculate ranking
ranker = StockRanker()
ranked = ranker.calculate_score(df)

# Save scores into database
cursor = engine.conn.cursor()

for _, row in ranked.iterrows():
    cursor.execute(
        """
        UPDATE financial_ratios
        SET stock_score = ?
        WHERE company_id = ?
        AND year = ?
        """,
        (
            float(row["stock_score"]),
            row["company_id"],
            row["year"]
        )
    )

engine.conn.commit()

print("Stock scores saved successfully!\n")

print(
    ranked[
        [
            "company_id",
            "year",
            "return_on_equity_pct",
            "revenue_cagr_5yr",
            "pat_cagr_5yr",
            "free_cash_flow_cr",
            "stock_score"
        ]
    ].head(10)
)

engine.close()