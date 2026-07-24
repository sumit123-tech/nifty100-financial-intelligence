from src.screener.engine import ScreenerEngine
from src.screener.portfolio import PortfolioBuilder

engine = ScreenerEngine()

df = engine.top_n(
    n=50,
    preset="Quality Compounder"
)

builder = PortfolioBuilder()

portfolio = builder.build_portfolio(
    df,
    n=10,
    max_per_sector=2
)

print(
    portfolio[
        [
            "company_id",
            "broad_sector",
            "stock_score",
            "weight"
        ]
    ]
)

engine.close()