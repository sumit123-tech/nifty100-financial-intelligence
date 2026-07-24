import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from src.screener.engine import ScreenerEngine

engine = ScreenerEngine()

df = engine.load_data()

print("Rows Loaded :", len(df))

filtered = engine.apply_filters(df)

print("Companies Passed :", len(filtered))

print(filtered.head(20))

engine.close()