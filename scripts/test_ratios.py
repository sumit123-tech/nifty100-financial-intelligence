from ratios import net_profit_margin, operating_profit_margin ,check_opm_difference, return_on_capital_employed, return_on_equity, return_on_assets

print("----- Net Profit Margin -----")
print(net_profit_margin(100, 1000))
print(net_profit_margin(0, 1000))
print(net_profit_margin(100, 0))

print("\n----- Operating Profit Margin -----")
print(operating_profit_margin(250, 1000))
print(operating_profit_margin(0, 1000))
print(operating_profit_margin(250, 0))

print("\n----- OPM Cross Check -----")

print(check_opm_difference(25.0, 25.2))
print(check_opm_difference(25.0, 26.5))
print(check_opm_difference(None, 25.0))

print("\n----- Return on Equity -----")

print(return_on_equity(200, 500, 500))
print(return_on_equity(150, 300, 200))
print(return_on_equity(100, -100, 50))
print(return_on_equity(100, 0, 0))

print("\n----- Return on Capital Employed -----")

print(return_on_capital_employed(300, 500, 500, 500))
print(return_on_capital_employed(180, 300, 200, 100))
print(return_on_capital_employed(100, -100, 0, 0))
print(return_on_capital_employed(100, 0, 0, 0))

print("\n----- Return on Assets -----")

print(return_on_assets(200, 1000))
print(return_on_assets(150, 500))
print(return_on_assets(100, 0))