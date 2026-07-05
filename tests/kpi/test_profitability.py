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
    return_on_assets
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


if __name__ == "__main__":
    unittest.main()