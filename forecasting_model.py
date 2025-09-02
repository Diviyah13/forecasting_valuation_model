import pandas as pd
import numpy as np
import numpy_financial as npf

# Assumptions
revenue_2025 = 4780   # in RM millions (starting revenue, base year 2025)
growth_rate = 0.06    # annual revenue growth (6%)
ebitda_margin = 0.205 # EBITDA margin (20.5%)
debt_ratio = 0.6      # 60% debt financing (LBO-style)
interest_rate = 0.06  # cost of debt (6%)
exit_multiple = 10    # exit multiple of EBITDA (valuation assumption)
holding_period = 5    #  investment horizon in years
entry_multiple = 10   # assume entry multiple same as exit for now

# Forecast Revenue & EBITDA
years = list(range(2025, 2025 + holding_period))
revenue = [revenue_2025 * ((1 + growth_rate) ** i) for i in range(holding_period)]
ebitda = [r * ebitda_margin for r in revenue]

# Entry & Exit Values
entry_enterprise_value = ebitda[0] * entry_multiple
entry_debt = entry_enterprise_value * debt_ratio
entry_equity = entry_enterprise_value - entry_debt

exit_value = ebitda[-1] * exit_multiple
exit_equity = exit_value - entry_debt  # assuming no debt paydown for simplicity

# IRR Calculation # IRR measures the return to equity investors over the holding period.
cashflows = [-entry_equity] + [0] * (holding_period - 1) + [exit_equity] 
irr = npf.irr(cashflows)

# Build DataFrame
df = pd.DataFrame({
    "Year": years,
    "Revenue (RM mil)": revenue,
    "EBITDA (RM mil)": ebitda
})

print(df)
print(f"\nEntry Enterprise Value: RM {entry_enterprise_value:.2f} mil")
print(f"Entry Equity: RM {entry_equity:.2f} mil, Entry Debt: RM {entry_debt:.2f} mil")
print(f"Exit Enterprise Value: RM {exit_value:.2f} mil, Exit Equity: RM {exit_equity:.2f} mil")
print(f"Estimated IRR: {irr*100:.2f}%")
