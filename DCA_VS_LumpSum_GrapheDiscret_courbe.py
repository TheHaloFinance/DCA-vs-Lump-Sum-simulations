# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 13:41:20 2024

@author: stefa
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def simulate_dca_and_lump_sum(ticker, start_date, end_date, dca_amount, lump_sum_amount):
    data = yf.download(ticker, start=start_date, end=end_date)
    monthly_data = data.resample('MS').first()  # Resampling to monthly data for DCA
    
    # DCA strategy
    dca_investments = np.floor(dca_amount / monthly_data['Adj Close'])
    dca_total_shares = np.cumsum(dca_investments)
    dca_portfolio_value = dca_total_shares * monthly_data['Adj Close']
    
    # Lump Sum strategy
    lump_sum_shares = lump_sum_amount / monthly_data['Adj Close'][0]
    lump_sum_portfolio_value = lump_sum_shares * monthly_data['Adj Close']
    
    return monthly_data.index, dca_portfolio_value, lump_sum_portfolio_value

# Configuration
ticker = 'SPY'
initial_start_date = pd.to_datetime('2020-01-01')
final_end_date = pd.to_datetime('2024-01-01')
dca_amount = 10000  # Monthly DCA investment
lump_sum_amount = 240000  # Lump Sum investment, equivalent to 2 years of DCA
period_length_years = 2

# Lists to store results for plotting
dca_wins = 0
lump_sum_wins = 0
start_dates = []
dca_final_values = []
lump_sum_final_values = []

# Loop through each period, moving start date by one month each iteration
current_start_date = initial_start_date
while current_start_date + pd.DateOffset(years=period_length_years) <= final_end_date:
    period_end_date = current_start_date + pd.DateOffset(years=period_length_years)
    dates, dca_values, lump_sum_values = simulate_dca_and_lump_sum(ticker, current_start_date, period_end_date, dca_amount, lump_sum_amount)
    
    dca_final_value = dca_values[-1]
    lump_sum_final_value = lump_sum_values[-1]
    
    # Update win counts
    if dca_final_value > lump_sum_final_value:
        dca_wins += 1
    elif lump_sum_final_value > dca_final_value:
        lump_sum_wins += 1
    
    # Store results for plotting
    start_dates.append(current_start_date)
    dca_final_values.append(dca_final_value)
    lump_sum_final_values.append(lump_sum_final_value)
    
    current_start_date += pd.DateOffset(months=1)  # Increment start date by one month

# Plotting
plt.figure(figsize=(14, 7))
plt.plot(start_dates, dca_final_values, label='DCA Final Value', alpha=0.7)
plt.plot(start_dates, lump_sum_final_values, label='Lump Sum Final Value', alpha=0.7)
plt.xlabel('Start Date of 2-Year Period')
plt.ylabel('Final Portfolio Value')
plt.title('DCA vs. Lump Sum over Multiple 2-Year Periods Starting Monthly')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print(f"DCA wins: {dca_wins}")
print(f"Lump Sum wins: {lump_sum_wins}")
