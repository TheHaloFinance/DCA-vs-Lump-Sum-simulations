# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 11:24:43 2024

@author: stefa
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def simulate_dca_and_lump_sum(ticker, start_date, end_date, dca_amount, lump_sum_amount, interval_months=1):
    data = yf.download(ticker, start=start_date, end=end_date, progress=False)
    monthly_data = data.resample('MS').first()
    
    # Stratégies
    dca_investments = np.floor(dca_amount / monthly_data['Adj Close'])
    dca_total_shares = np.cumsum(dca_investments)
    dca_portfolio_value = dca_total_shares * monthly_data['Adj Close']
    
    lump_sum_shares = lump_sum_amount / monthly_data['Adj Close'][0]
    lump_sum_portfolio_value = lump_sum_shares * monthly_data['Adj Close']
    
    return dca_portfolio_value.iloc[-1], lump_sum_portfolio_value.iloc[-1]

# Paramètres
ticker = 'SPY'
initial_start_date = pd.to_datetime('2000-01-01')
final_end_date = pd.to_datetime('2024-01-01')
dca_amount = 10000
lump_sum_amount = 240000
period_length_years = 2
interval_months = 3 # Nouveau paramètre pour contrôler l'intervalle d'itération

# Préparation des données
start_dates = []
performance_differences = []

current_start_date = initial_start_date
while current_start_date + pd.DateOffset(years=period_length_years) <= final_end_date:
    period_end_date = current_start_date + pd.DateOffset(years=period_length_years)
    dca_value, lump_sum_value = simulate_dca_and_lump_sum(ticker, current_start_date, period_end_date, dca_amount, lump_sum_amount, interval_months)
    
    performance_difference = ((dca_value - lump_sum_value) / lump_sum_value) * 100
    start_dates.append(current_start_date.strftime('%Y-%m'))
    performance_differences.append(performance_difference)
    
    current_start_date += pd.DateOffset(months=interval_months)  # Utiliser le nouvel intervalle

# Initialisation de la figure pour l'animation
fig, ax = plt.subplots(figsize=(14, 7))

def update(frame):
    # Mise à jour de l'affichage pour l'animation
    frame_interval = frame * interval_months
    ax.clear()  # Nettoyer pour dessiner de nouveau
    ax.bar(start_dates[:frame+1], performance_differences[:frame+1], color=['blue' if x > 0 else 'red' for x in performance_differences[:frame+1]])
    avg_diff = np.mean(performance_differences[:frame+1]) if frame > 0 else 0
    ax.axhline(y=avg_diff, color='green', linestyle='--')
    ax.text(len(start_dates[:frame+1])-1, avg_diff, f'Mean: {avg_diff:.2f}%', verticalalignment='bottom', horizontalalignment='right')
    plt.xticks(rotation=90)
    plt.xlabel('Start Date of 2-Year Period')
    plt.ylabel('Performance Difference (DCA - Lump Sum) %')
    plt.title('Performance Difference between DCA and Lump Sum over Time')

# Créer et sauvegarder l'animation
ani = FuncAnimation(fig, update, frames=len(start_dates), repeat=False)
ani.save('dca_vs_lump_sum_animation.mp4', writer='ffmpeg', fps=30, dpi=(1080/9))

plt.show()