from src.screener.engine import ScreenerEngine

engine = ScreenerEngine()

df = engine.load_data()

sector = engine.filter_by_sector(
    df,
    "Information Technology"
)

print("Companies :", len(sector))
print()

print(
    sector[
        [
            "company_id",
            "year",
            "broad_sector"
        ]
    ].head(20)
)

engine.close()