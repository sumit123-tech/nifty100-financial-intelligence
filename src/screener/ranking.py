import pandas as pd


class StockRanker:

    def __init__(self):
        pass

    def calculate_score(self, df):

        result = df.copy()

        cols = [
            "return_on_equity_pct",
            "revenue_cagr_5yr",
            "pat_cagr_5yr",
            "free_cash_flow_cr"
        ]

        result[cols] = result[cols].fillna(0)

        # Normalize each metric between 0 and 100
        for col in cols:

            minimum = result[col].min()
            maximum = result[col].max()

            if maximum != minimum:
                result[col + "_score"] = (
                    (result[col] - minimum)
                    / (maximum - minimum)
                ) * 100
            else:
                result[col + "_score"] = 100

        # Weighted score
        result["stock_score"] = (
            result["return_on_equity_pct_score"] * 0.35
            + result["revenue_cagr_5yr_score"] * 0.25
            + result["pat_cagr_5yr_score"] * 0.25
            + result["free_cash_flow_cr_score"] * 0.15
        )

        # Keep only the latest year for each company
        result = (
            result.sort_values("year")
                .groupby("company_id")
                .tail(1)
        )

        return result.sort_values(
            "stock_score",
            ascending=False
        )