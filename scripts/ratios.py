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