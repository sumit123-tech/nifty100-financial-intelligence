from src.screener.engine import ScreenerEngine

engine = ScreenerEngine()

df = engine.load_data()

print("Total Companies:", len(df))
print()

for preset in engine.presets:

    print("=" * 50)
    print(preset)

    result = engine.apply_preset(df, preset)

    print("Companies Found:", len(result))
    print()

engine.close()