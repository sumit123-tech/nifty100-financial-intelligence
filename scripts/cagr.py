def calculate_cagr(start_value, end_value, years):
    """
    Compound Annual Growth Rate (CAGR)

    Formula:
    ((End / Start) ** (1 / Years) - 1) * 100

    Returns:
    (value, flag)
    """

    # Less than required years
    if years <= 0:
        return None, "INSUFFICIENT"

    # Zero base
    if start_value == 0:
        return None, "ZERO_BASE"

    # Positive → Negative
    if start_value > 0 and end_value < 0:
        return None, "DECLINE_TO_LOSS"

    # Negative → Positive
    if start_value < 0 and end_value > 0:
        return None, "TURNAROUND"

    # Negative → Negative
    if start_value < 0 and end_value < 0:
        return None, "BOTH_NEGATIVE"

    cagr = ((end_value / start_value) ** (1 / years) - 1) * 100

    return round(cagr, 2), "NORMAL"

def revenue_cagr_3yr(start_sales, end_sales):
    return calculate_cagr(start_sales, end_sales, 3)


def revenue_cagr_5yr(start_sales, end_sales):
    return calculate_cagr(start_sales, end_sales, 5)


def revenue_cagr_10yr(start_sales, end_sales):
    return calculate_cagr(start_sales, end_sales, 10)

def pat_cagr_3yr(start_pat, end_pat):
    return calculate_cagr(start_pat, end_pat, 3)


def pat_cagr_5yr(start_pat, end_pat):
    return calculate_cagr(start_pat, end_pat, 5)


def pat_cagr_10yr(start_pat, end_pat):
    return calculate_cagr(start_pat, end_pat, 10)


def eps_cagr_3yr(start_eps, end_eps):
    return calculate_cagr(start_eps, end_eps, 3)


def eps_cagr_5yr(start_eps, end_eps):
    return calculate_cagr(start_eps, end_eps, 5)


def eps_cagr_10yr(start_eps, end_eps):
    return calculate_cagr(start_eps, end_eps, 10)