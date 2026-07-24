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

from cagr import (
    calculate_cagr,
    revenue_cagr_3yr,
    revenue_cagr_5yr,
    revenue_cagr_10yr,
    pat_cagr_3yr,
    pat_cagr_5yr,
    pat_cagr_10yr,
    eps_cagr_3yr,
    eps_cagr_5yr,
    eps_cagr_10yr
)


class TestCAGR(unittest.TestCase):

    def test_normal_case(self):
        value, flag = calculate_cagr(100, 200, 5)
        self.assertEqual(flag, "NORMAL")

    def test_zero_base(self):
        value, flag = calculate_cagr(0, 200, 5)
        self.assertEqual(flag, "ZERO_BASE")

    def test_turnaround(self):
        value, flag = calculate_cagr(-100, 200, 5)
        self.assertEqual(flag, "TURNAROUND")

    def test_decline_to_loss(self):
        value, flag = calculate_cagr(100, -50, 5)
        self.assertEqual(flag, "DECLINE_TO_LOSS")

    def test_both_negative(self):
        value, flag = calculate_cagr(-100, -50, 5)
        self.assertEqual(flag, "BOTH_NEGATIVE")

    def test_insufficient(self):
        value, flag = calculate_cagr(100, 200, 0)
        self.assertEqual(flag, "INSUFFICIENT")

    def test_revenue_cagr_3yr(self):
        value, flag = revenue_cagr_3yr(100, 150)
        self.assertEqual(flag, "NORMAL")


    def test_revenue_cagr_5yr(self):
        value, flag = revenue_cagr_5yr(100, 200)
        self.assertEqual(flag, "NORMAL")


    def test_revenue_cagr_10yr(self):
        value, flag = revenue_cagr_10yr(100, 300)
        self.assertEqual(flag, "NORMAL")


    def test_revenue_zero_base(self):
        value, flag = revenue_cagr_5yr(0, 200)
        self.assertEqual(flag, "ZERO_BASE")


    def test_pat_cagr_3yr(self):
        value, flag = pat_cagr_3yr(100, 150)
        self.assertEqual(flag, "NORMAL")


    def test_pat_cagr_5yr(self):
        value, flag = pat_cagr_5yr(100, 200)
        self.assertEqual(flag, "NORMAL")


    def test_pat_cagr_10yr(self):
        value, flag = pat_cagr_10yr(100, 300)
        self.assertEqual(flag, "NORMAL")


    def test_pat_turnaround(self):
        value, flag = pat_cagr_5yr(-100, 200)
        self.assertEqual(flag, "TURNAROUND")


    def test_eps_cagr_3yr(self):
        value, flag = eps_cagr_3yr(10, 20)
        self.assertEqual(flag, "NORMAL")


    def test_eps_cagr_5yr(self):
        value, flag = eps_cagr_5yr(10, 25)
        self.assertEqual(flag, "NORMAL")


    def test_eps_cagr_10yr(self):
        value, flag = eps_cagr_10yr(10, 40)
        self.assertEqual(flag, "NORMAL")


    def test_eps_decline_to_loss(self):
        value, flag = eps_cagr_5yr(10, -5)
        self.assertEqual(flag, "DECLINE_TO_LOSS")


if __name__ == "__main__":
    unittest.main()