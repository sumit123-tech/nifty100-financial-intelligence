from src.screener.engine import ScreenerEngine

engine = ScreenerEngine()

result = engine.top_n(
    n=10,
    preset="Quality Compounder"
)

print(result[[
    "company_id",
    "year",
    "stock_score",
    "composite_quality_score",
    "broad_sector"
]])

engine.close()