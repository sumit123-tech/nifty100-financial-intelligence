from src.screener.engine import ScreenerEngine

engine = ScreenerEngine()

df = engine.load_data()

result = engine.apply_preset(
    df,
    "Quality Compounder",
    sector="Information Technology"
)

print(result[
    [
        "company_id",
        "year",
        "return_on_equity_pct",
        "revenue_cagr_5yr",
        "free_cash_flow_cr",
        "broad_sector"
    ]
])

print()
print("Companies Found :", len(result))

engine.close()