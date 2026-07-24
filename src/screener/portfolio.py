import pandas as pd


class PortfolioBuilder:

    def __init__(self):
        pass

    def build_portfolio(
        self,
        df,
        n=10,
        max_per_sector=2
    ):
        """
        Build a diversified portfolio.
        """

        if "stock_score" not in df.columns:
            raise ValueError(
                "stock_score column not found."
            )

        df = df.sort_values(
            "stock_score",
            ascending=False
        )

        portfolio = []

        sector_count = {}

        for _, row in df.iterrows():

            sector = row["broad_sector"]

            if sector not in sector_count:
                sector_count[sector] = 0

            if sector_count[sector] >= max_per_sector:
                continue

            portfolio.append(row)

            sector_count[sector] += 1

            if len(portfolio) == n:
                break

        portfolio = pd.DataFrame(portfolio)

        portfolio["weight"] = round(
            100 / len(portfolio),
            2
        )

        return portfolio