# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 11:24:43 2024

@author: stefa
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def simulate_dca_and_lump_sum(ticker, start_date, end_date, dca_amount, lump_sum_amount):
    data = yf.download(ticker, start=start_date, end=end_date, progress=False)
    monthly_data = data.resample('MS').first()  # Resampling to monthly data for DCA
    
    # DCA strategy
    dca_investments = np.floor(dca_amount / monthly_data['Adj Close'])
    dca_total_shares = np.cumsum(dca_investments)
    dca_portfolio_value = dca_total_shares * monthly_data['Adj Close']
    
    # Lump Sum strategy
    lump_sum_shares = lump_sum_amount / monthly_data['Adj Close'][0]
    lump_sum_portfolio_value = lump_sum_shares * monthly_data['Adj Close']
    
    return dca_portfolio_value.iloc[-1], lump_sum_portfolio_value.iloc[-1]

# Configuration
ticker = 'SPY'
initial_start_date = pd.to_datetime('2000-01-01')
final_end_date = pd.to_datetime('2024-01-01')
dca_amount = 10000  # Monthly DCA investment
lump_sum_amount = 240000  # Lump Sum investment, equivalent to 2 years of DCA
period_length_years = 2

# Lists to store results
start_dates = []
performance_differences = []

# Loop through each period, moving start date by one month each iteration
current_start_date = initial_start_date
while current_start_date + pd.DateOffset(years=period_length_years) <= final_end_date:
    period_end_date = current_start_date + pd.DateOffset(years=period_length_years)
    dca_value, lump_sum_value = simulate_dca_and_lump_sum(ticker, current_start_date, period_end_date, dca_amount, lump_sum_amount)
    
    # Calculate performance difference in percentage
    performance_difference = ((dca_value - lump_sum_value) / lump_sum_value) * 100
    start_dates.append(current_start_date)
    performance_differences.append(performance_difference)
    
    current_start_date += pd.DateOffset(months=1)  # Increment start date by one month

# Convert start_dates to matplotlib dates
dates = mdates.date2num(start_dates)

# Plotting the bar chart with color coding
plt.figure(figsize=(14, 7))
bars = plt.bar(dates, performance_differences, width=30, color=['blue' if x > 0 else 'red' for x in performance_differences], edgecolor='black')
plt.axhline(0, color='black', linewidth=0.5)  # Add a line at y=0 for reference
plt.axhline(np.mean(performance_differences), color='green', linestyle='dashed', linewidth=2, label=f'Mean: {np.mean(performance_differences):.2f}%')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.gca().xaxis.set_major_locator(mdates.YearLocator())
plt.xlabel('Start Date of 2-Year Period')
plt.ylabel('Performance Difference (DCA - Lump Sum) %')
plt.title('Bar Chart of Performance Differences between DCA and Lump Sum')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
