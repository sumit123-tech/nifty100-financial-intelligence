import pandas as pd


class PortfolioAnalytics:

    def __init__(self):
        pass

    def sector_allocation(self, portfolio):

        allocation = (
            portfolio.groupby("broad_sector")
            .size()
            .reset_index(name="companies")
        )

        allocation["weight_percent"] = round(
            allocation["companies"] /
            allocation["companies"].sum() * 100,
            2
        )

        return allocation


    def summary(self, portfolio):

        summary = {

            "Total Stocks":
            len(portfolio),

            "Average Stock Score":
            round(
                portfolio["stock_score"].mean(),
                2
            ),

            "Highest Score":
            round(
                portfolio["stock_score"].max(),
                2
            ),

            "Lowest Score":
            round(
                portfolio["stock_score"].min(),
                2
            ),

            "Average Weight":
            round(
                portfolio["weight"].mean(),
                2
            )
        }

        return summary