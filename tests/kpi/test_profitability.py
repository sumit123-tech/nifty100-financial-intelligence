import unittest
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "scripts"
        )
    )
)

from ratios import (
    net_profit_margin,
    operating_profit_margin,
    check_opm_difference,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    debt_to_equity,
    high_leverage_flag,
    interest_coverage_ratio,
    icr_label,
    icr_warning_flag,
    net_debt,
    asset_turnover,
    free_cash_flow,
    cfo_quality_score,
    capex_intensity,
    fcf_conversion_rate,
    capital_allocation_pattern
)


class TestProfitabilityRatios(unittest.TestCase):

    def test_net_profit_margin(self):
        self.assertEqual(net_profit_margin(100, 1000), 10.0)

    def test_zero_sales(self):
        self.assertIsNone(net_profit_margin(100, 0))

    def test_operating_profit_margin(self):
        self.assertEqual(operating_profit_margin(250, 1000), 25.0)

    def test_opm_crosscheck(self):
        self.assertTrue(check_opm_difference(25, 27))

    def test_opm_crosscheck_ok(self):
        self.assertFalse(check_opm_difference(25, 25.5))

    def test_roe(self):
        self.assertEqual(return_on_equity(200, 500, 500), 20.0)

    def test_negative_equity(self):
        self.assertIsNone(return_on_equity(100, -100, 50))

    def test_roce(self):
        self.assertEqual(
            return_on_capital_employed(
                300,
                500,
                500,
                500
            ),
            20.0
        )

    def test_roa(self):
        self.assertEqual(return_on_assets(200, 1000), 20.0)

    def test_debt_to_equity(self):
        self.assertEqual(
        debt_to_equity(
            200,
            500,
            500
        ),
        0.2
    )

    def test_debt_free_company(self):
        self.assertEqual(
            debt_to_equity(
                0,
                500,
                500
            ),
            0
        )

    def test_negative_equity_de(self):
        self.assertIsNone(
            debt_to_equity(
                100,
                -100,
                50
            )
        )

    def test_negative_equity_de(self):
        self.assertIsNone(
            debt_to_equity(
                100,
                -100,
                50
            )
        )

    def test_high_leverage_flag(self):
        self.assertTrue(
            high_leverage_flag(
                6,
                "Industrials"
            )
        )

    def test_financial_sector_no_flag(self):
        self.assertFalse(
            high_leverage_flag(
                10,
                "Financials"
            )
        )

    def test_low_de_flag(self):
        self.assertFalse(
            high_leverage_flag(
                2,
                "Industrials"
            )
        )


    def test_interest_coverage_ratio(self):
        self.assertEqual(
            interest_coverage_ratio(
                500,
                100,
                100
            ),
            6.0
        )

    def test_interest_zero(self):
        self.assertIsNone(
            interest_coverage_ratio(
                500,
                100,
                0
            )
        )

    def test_interest_coverage_small(self):
        self.assertEqual(
            interest_coverage_ratio(
                300,
                0,
                200
            ),
            1.5
        )

    def test_icr_label_debt_free(self):
        self.assertEqual(
            icr_label(0),
            "Debt Free"
        )

    def test_icr_label_normal(self):
        self.assertIsNone(
            icr_label(50)
        )

    def test_icr_warning(self):
        self.assertTrue(
            icr_warning_flag(1.2)
        )

    def test_icr_safe(self):
        self.assertFalse(
            icr_warning_flag(3.5)
        )

    def test_icr_none(self):
        self.assertFalse(
            icr_warning_flag(None)
        )

    def test_net_debt(self):
        self.assertEqual(
            net_debt(500, 200),
            300
        )

    def test_zero_net_debt(self):
        self.assertEqual(
            net_debt(200, 200),
            0
        )

    def test_negative_net_debt(self):
        self.assertEqual(
            net_debt(100, 300),
            -200
        )

    def test_asset_turnover(self):
        self.assertEqual(
            asset_turnover(1000, 500),
            2.0
        )

    def test_asset_turnover_fraction(self):
        self.assertEqual(
            asset_turnover(600, 1200),
            0.5
        )

    def test_asset_turnover_zero_assets(self):
        self.assertIsNone(
            asset_turnover(1000, 0)
        )

    def test_free_cash_flow(self):
        self.assertEqual(
            free_cash_flow(
                1000,
                -300
            ),
            700
        )


    def test_negative_free_cash_flow(self):
        self.assertEqual(
            free_cash_flow(
                200,
                -500
            ),
            -300
        )


    def test_zero_free_cash_flow(self):
        self.assertEqual(
            free_cash_flow(
                300,
                -300
            ),
            0
        )

    def test_cfo_high_quality(self):
        self.assertEqual(
            cfo_quality_score(
                1200,
                1000
            ),
            "High Quality"
        )


    def test_cfo_moderate(self):
        self.assertEqual(
            cfo_quality_score(
                700,
                1000
            ),
            "Moderate"
        )


    def test_cfo_accrual_risk(self):
        self.assertEqual(
            cfo_quality_score(
                300,
                1000
            ),
            "Accrual Risk"
        )


    def test_cfo_pat_zero(self):
        self.assertIsNone(
            cfo_quality_score(
                100,
                0
            )
        )


    def test_capex_asset_light(self):
        self.assertEqual(
            capex_intensity(
                -20,
                1000
            ),
            "Asset Light"
        )


    def test_capex_moderate(self):
        self.assertEqual(
            capex_intensity(
                -50,
                1000
            ),
            "Moderate"
        )


    def test_capex_capital_intensive(self):
        self.assertEqual(
            capex_intensity(
                -150,
                1000
            ),
            "Capital Intensive"
        )


    def test_capex_zero_sales(self):
        self.assertIsNone(
            capex_intensity(
                -100,
                0
            )
        )

    def test_fcf_conversion_rate(self):
        self.assertEqual(
            fcf_conversion_rate(
                500,
                1000
            ),
            50.0
        )


    def test_fcf_conversion_rate_full(self):
        self.assertEqual(
            fcf_conversion_rate(
                1000,
                1000
            ),
            100.0
        )


    def test_fcf_conversion_negative(self):
        self.assertEqual(
            fcf_conversion_rate(
                -200,
                1000
            ),
            -20.0
        )


    def test_fcf_conversion_zero_profit(self):
        self.assertIsNone(
            fcf_conversion_rate(
                100,
                0
            )
        )

    def test_reinvestor(self):
        self.assertEqual(
            capital_allocation_pattern(
                100,
                -50,
                -30
            ),
            "Reinvestor"
        )


    def test_distress(self):
        self.assertEqual(
            capital_allocation_pattern(
                -100,
                50,
                20
            ),
            "Distress Signal"
        )


    def test_growth_debt(self):
        self.assertEqual(
            capital_allocation_pattern(
                -100,
                -50,
                80
            ),
            "Growth Funded by Debt"
        )


    def test_cash_accumulator(self):
        self.assertEqual(
            capital_allocation_pattern(
                100,
                50,
                30
            ),
            "Cash Accumulator"
        )


    def test_pre_revenue(self):
        self.assertEqual(
            capital_allocation_pattern(
                -100,
                -50,
                -30
            ),
            "Pre-Revenue"
        )


    def test_mixed(self):
        self.assertEqual(
            capital_allocation_pattern(
                100,
                -50,
                80
            ),
            "Mixed"
        )


if __name__ == "__main__":
    unittest.main()