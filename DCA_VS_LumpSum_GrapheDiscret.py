# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 10:38:27 2024

@author: stefa
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# Configuration des paramètres de simulation
ticker = 'SPY'
start_date = '2022-01-01'
end_date = '2024-01-01'
dca_amount = 10000
lump_sum_amount = 240000
interval = '1mo'

# Téléchargement des données historiques
data = yf.download(ticker, start=start_date, end=end_date, interval=interval)

# Simulation DCA
dca_dates = data.index[data.index >= pd.to_datetime(start_date)]
dca_investments = np.floor(dca_amount / data['Adj Close'][dca_dates])
dca_total_shares = dca_investments.cumsum()
dca_portfolio_value = dca_total_shares * data['Adj Close'][dca_dates]

print("DCA final portfolio value :")
print(dca_portfolio_value[-1])


# Simulation Lump Sum
lump_sum_shares = lump_sum_amount / data['Adj Close'][data.index[0]]
lump_sum_portfolio_value = lump_sum_shares * data['Adj Close']
print("Lump Sum final portfolio value :")
print(lump_sum_portfolio_value[-1])

# Configuration de l'animation
fig, ax = plt.subplots(figsize=(10, 6))

def update(frame):
    ax.clear()  # Nettoyer l'ancien frame avant de dessiner le nouveau
    # Mise à jour des données pour DCA et Lump Sum
    ax.plot_date(dca_dates[:frame], dca_portfolio_value[:frame], 'o-', label='Valeur du portefeuille DCA')
    ax.plot_date(data.index[:frame], lump_sum_portfolio_value[:frame], 'o-', label='Valeur du portefeuille Lump Sum', alpha=0.7)
    # Configuration de l'axe et de la légende
    ax.set(title='Comparaison DCA vs Lump Sum', xlabel='Date', ylabel='Valeur du portefeuille')
    ax.legend()

# Création de l'animation
ani = animation.FuncAnimation(fig, update, frames=max(len(dca_dates), len(data.index)), repeat=False)

# Enregistrement de l'animation
ani.save('dca_vs_lump_sum_combined_2ans_2022_2024.mp4', writer='ffmpeg', fps=30, dpi=(1080/9))

plt.close(fig)  # Fermer la figure pour libérer la mémoire

