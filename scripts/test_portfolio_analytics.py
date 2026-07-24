from src.screener.engine import ScreenerEngine
from src.screener.portfolio import PortfolioBuilder
from src.analytics.portfolio_analytics import PortfolioAnalytics

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

analytics = PortfolioAnalytics()

print("\nPortfolio Summary")
print("---------------------")

summary = analytics.summary(portfolio)

for k, v in summary.items():
    print(f"{k}: {v}")

print("\nSector Allocation")
print("---------------------")

print(
    analytics.sector_allocation(portfolio)
)

engine.close()