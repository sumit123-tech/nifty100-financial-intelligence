import sqlite3
import pandas as pd
import yaml


class ScreenerEngine:

    def __init__(self):

        self.conn = sqlite3.connect("database/nifty100.db")

        with open(
            "config/screener_config.yaml",
            "r",
            encoding="utf-8"
        ) as f:

            self.config = yaml.safe_load(f)

        with open(
            "config/screener_presets.yaml",
            "r",
            encoding="utf-8"
        ) as f:

            self.presets = yaml.safe_load(f)

    def load_data(self):

        query = """
        SELECT

        f.company_id,
        f.year,

        f.return_on_equity_pct,
        f.debt_to_equity,
        f.free_cash_flow_cr,
        f.revenue_cagr_5yr,
        f.pat_cagr_5yr,
        f.operating_profit_margin_pct,
        f.interest_coverage,
        f.asset_turnover,
        f.composite_quality_score,
        f.stock_score,

        p.sales,
        p.net_profit,

        m.market_cap_crore,
        m.pe_ratio,
        m.pb_ratio,
        m.dividend_yield_pct,

        s.broad_sector

        FROM financial_ratios f

        LEFT JOIN profitandloss p
        ON f.company_id = p.company_id
        AND f.year = p.year

        LEFT JOIN market_cap m
        ON f.company_id = m.company_id
        AND substr(f.year,-4)=CAST(m.year AS TEXT)

        LEFT JOIN sectors s
        ON f.company_id = s.company_id
        """

        return pd.read_sql(query, self.conn)

    def apply_filters(self, df):

        filters = self.config["filters"]

        print("Initial :", len(df))

        if "roe_min" in filters:
            df = df[df["return_on_equity_pct"] >= filters["roe_min"]]
            print("ROE :", len(df))

        if "debt_to_equity_max" in filters:
            df = df[
                (df["debt_to_equity"] <= filters["debt_to_equity_max"])
                |
                (df["broad_sector"] == "Financials")
            ]
            print("D/E :", len(df))

        if "free_cash_flow_min" in filters:
            df = df[df["free_cash_flow_cr"] >= filters["free_cash_flow_min"]]
            print("FCF :", len(df))

        if "revenue_cagr_5yr_min" in filters:
            df = df[df["revenue_cagr_5yr"] >= filters["revenue_cagr_5yr_min"]]
            print("Revenue CAGR :", len(df))

        if "pat_cagr_5yr_min" in filters:
            df = df[df["pat_cagr_5yr"] >= filters["pat_cagr_5yr_min"]]
            print("PAT CAGR :", len(df))

        if "operating_profit_margin_min" in filters:
            df = df[
                df["operating_profit_margin_pct"] >=
                filters["operating_profit_margin_min"]
            ]
            print("OPM :", len(df))

        if "pe_max" in filters:
            df = df[df["pe_ratio"] <= filters["pe_max"]]
            print("PE :", len(df))

        if "pb_max" in filters:
            df = df[df["pb_ratio"] <= filters["pb_max"]]
            print("PB :", len(df))

        if "dividend_yield_min" in filters:
            df = df[
                df["dividend_yield_pct"] >=
                filters["dividend_yield_min"]
            ]
            print("Dividend :", len(df))

        if "interest_coverage_min" in filters:
            df = df[
                (df["interest_coverage"] >= filters["interest_coverage_min"])
                |
                (df["interest_coverage"].isna())
            ]
            print("ICR :", len(df))

        if "market_cap_min" in filters:
            df = df[
                df["market_cap_crore"] >=
                filters["market_cap_min"]
            ]
            print("Market Cap :", len(df))

        if "net_profit_min" in filters:
            df = df[df["net_profit"] >= filters["net_profit_min"]]
            print("Net Profit :", len(df))

        if "asset_turnover_min" in filters:
            df = df[
                df["asset_turnover"] >=
                filters["asset_turnover_min"]
            ]
            print("Asset Turnover :", len(df))

        if "sales_min" in filters:
            df = df[df["sales"] >= filters["sales_min"]]
            print("Sales :", len(df))

        if "dividend_payout_ratio_max" in filters and "dividend_payout_ratio_pct" in df.columns:
            df = df[
                df["dividend_payout_ratio_pct"] <=
                filters["dividend_payout_ratio_max"]
            ]
            print("Dividend Payout :", len(df))

        return df.sort_values(
            "composite_quality_score",
            ascending=False
        )
    
    def apply_preset(self, df, preset_name, sector=None):

        if preset_name not in self.presets:
            raise ValueError(
                f"Preset '{preset_name}' not found."
            )

        preset = self.presets[preset_name]

        old_config = self.config

        self.config = {
            "filters": preset
        }

        if sector:
            df = self.filter_by_sector(df, sector)

        result = self.apply_filters(df)

        self.config = old_config

        return result
    
    def filter_by_sector(self, df, sector_name):

        return df[
            df["broad_sector"] == sector_name
        ]
    
    def top_n(
    self,
    n=10,
    preset=None,
    sector=None
    ):

        df = self.load_data()

        if sector is not None:
            df = self.filter_by_sector(
                df,
                sector
            )

        if preset is not None:
            df = self.apply_preset(
                df,
                preset
            )

        latest = (
            df.groupby("company_id")["year"]
            .max()
            .reset_index()
        )

        df = df.merge(
            latest,
            on=["company_id", "year"]
        )

        if "stock_score" in df.columns:
            df = df.sort_values(
                "stock_score",
                ascending=False
            )
        else:
            df = df.sort_values(
                "composite_quality_score",
                ascending=False
            )

        return df.head(n)

    def close(self):

        self.conn.close()
    
    