def net_profit_margin(net_profit, sales):
    """
    Net Profit Margin (%)

    Formula:
    (Net Profit / Sales) * 100

    Returns:
        None if sales is zero
    """

    if sales == 0:
        return None

    return round((net_profit / sales) * 100, 2)

def operating_profit_margin(operating_profit, sales):
    """
    Operating Profit Margin (%)

    Formula:
    (Operating Profit / Sales) * 100

    Returns:
        None if sales is zero
    """

    if sales == 0:
        return None

    return round((operating_profit / sales) * 100, 2)

def check_opm_difference(calculated_opm, source_opm):
    """
    Compare calculated OPM with source OPM.

    Returns:
        None -> if any value is None
        True -> if difference > 1%
        False -> otherwise
    """

    if calculated_opm is None or source_opm is None:
        return None

    difference = abs(calculated_opm - source_opm)

    return difference > 1


def return_on_equity(net_profit, equity_capital, reserves):
    """
    Return on Equity (ROE)

    Formula:
    (Net Profit / (Equity Capital + Reserves)) * 100

    Returns:
        None if equity + reserves <= 0
    """

    total_equity = equity_capital + reserves

    if total_equity <= 0:
        return None

    return round((net_profit / total_equity) * 100, 2)

def return_on_capital_employed(
    ebit,
    equity_capital,
    reserves,
    borrowings
):
    capital_employed = (
        equity_capital +
        reserves +
        borrowings
    )

    if capital_employed <= 0:
        return None

    return round((ebit / capital_employed) * 100, 2)

def return_on_assets(net_profit, total_assets):
    """
    Return on Assets (ROA)

    Formula:
    (Net Profit / Total Assets) * 100

    Returns:
        None if total_assets is zero
    """

    if total_assets == 0:
        return None

    return round((net_profit / total_assets) * 100, 2)

def debt_to_equity(borrowings, equity_capital, reserves):
    """
    Debt to Equity Ratio

    Formula:
    Borrowings / (Equity Capital + Reserves)

    Rules:
    - Return 0 if borrowings = 0
    - Return None if equity + reserves <= 0
    """

    if borrowings == 0:
        return 0

    total_equity = equity_capital + reserves

    if total_equity <= 0:
        return None

    return round(borrowings / total_equity, 2)

def high_leverage_flag(debt_to_equity_ratio, broad_sector):
    """
    High Leverage Flag

    Rule:
    D/E > 5 and NOT Financials sector
    """

    if debt_to_equity_ratio is None:
        return False

    if (
        debt_to_equity_ratio > 5
        and broad_sector != "Financials"
    ):
        return True

    return False

def interest_coverage_ratio(
    operating_profit,
    other_income,
    interest
):
    """
    Interest Coverage Ratio (ICR)

    Formula:
    (Operating Profit + Other Income) / Interest

    Returns:
        None if interest == 0
    """

    if interest == 0:
        return None

    ebit = operating_profit + other_income

    return round(ebit / interest, 2)

def icr_label(interest):
    """
    Interest Coverage Label

    Returns:
    'Debt Free' if interest == 0
    otherwise None
    """

    if interest == 0:
        return "Debt Free"

    return None

def icr_warning_flag(icr):
    """
    Interest Coverage Warning Flag

    Rule:
    ICR < 1.5 → True

    Returns False otherwise.
    """

    if icr is None:
        return False

    return icr < 1.5



def net_debt(borrowings, investments):
    """
    Net Debt

    Formula:
    Borrowings - Investments
    """

    return round(borrowings - investments, 2)


def asset_turnover(sales, total_assets):
    """
    Asset Turnover Ratio

    Formula:
    Sales / Total Assets

    Returns:
        None if total_assets == 0
    """

    if total_assets == 0:
        return None

    return round(sales / total_assets, 2)


def free_cash_flow(
    operating_activity,
    investing_activity
):
    """
    Free Cash Flow

    Formula:
    Operating Activity + Investing Activity

    Note:
    Investing activity is usually negative.
    Negative FCF is allowed.
    """

    return round(
        operating_activity + investing_activity,
        2
    )

def cfo_quality_score(cfo, pat):
    """
    CFO Quality Score

    Formula:
    CFO / PAT

    Classification:
    >1.0      -> High Quality
    0.5-1.0   -> Moderate
    <0.5      -> Accrual Risk

    Return None if PAT == 0
    """

    if pat == 0:
        return None

    score = cfo / pat

    if score > 1:
        return "High Quality"

    elif score >= 0.5:
        return "Moderate"

    else:
        return "Accrual Risk"
    

def capex_intensity(investing_activity, sales):
    """
    CapEx Intensity

    Formula:
    abs(Investing Activity) / Sales × 100

    Classification:
    <3      -> Asset Light
    3-8     -> Moderate
    >8      -> Capital Intensive

    Returns None if sales == 0
    """

    if sales == 0:
        return None

    intensity = (abs(investing_activity) / sales) * 100

    if intensity < 3:
        return "Asset Light"

    elif intensity <= 8:
        return "Moderate"

    else:
        return "Capital Intensive"
    

def fcf_conversion_rate(free_cash_flow, operating_profit):
    """
    FCF Conversion Rate

    Formula:
    FCF / Operating Profit × 100

    Returns:
        None if operating_profit == 0
    """

    if operating_profit == 0:
        return None

    return round(
        (free_cash_flow / operating_profit) * 100,
        2
    )


def capital_allocation_pattern(cfo, cfi, cff):
    """
    Capital Allocation Pattern Classification
    """

    cfo_sign = "+" if cfo >= 0 else "-"
    cfi_sign = "+" if cfi >= 0 else "-"
    cff_sign = "+" if cff >= 0 else "-"

    pattern = (cfo_sign, cfi_sign, cff_sign)

    mapping = {
        ("+", "-", "-"): "Reinvestor",
        ("+", "+", "-"): "Liquidating Assets",
        ("-", "+", "+"): "Distress Signal",
        ("-", "-", "+"): "Growth Funded by Debt",
        ("+", "+", "+"): "Cash Accumulator",
        ("-", "-", "-"): "Pre-Revenue",
        ("+", "-", "+"): "Mixed",
    }

    return mapping.get(pattern, "Unknown")


def composite_quality_score(
    roe,
    revenue_cagr,
    pat_cagr,
    eps_cagr,
):
    """
    Composite Quality Score
    Average of ROE, Revenue CAGR, PAT CAGR and EPS CAGR
    """

    values = []

    for value in [roe, revenue_cagr, pat_cagr, eps_cagr]:

        if value is not None:
            values.append(value)

    if len(values) == 0:
        return None

    return round(sum(values) / len(values), 2)