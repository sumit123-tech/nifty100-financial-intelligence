from src.screener.engine import ScreenerEngine

engine = ScreenerEngine()

df = engine.load_data()

result = engine.apply_preset(
    df,
    "Quality Compounder"
)

print(result.head())

print()

print("Companies Found :", len(result))

engine.close()