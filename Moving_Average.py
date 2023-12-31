#%%
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

spy_ticker = yf.Ticker('bac')
bac = yf.download('bac')

fig, ax = plt.subplots(nrows=1, ncols=2, sharex=True, figsize=(15,5))
ax[0].set_title('bac Close', fontsize=15)
ax[0].plot(bac['Close'])
ax[1].set_title('bac Volume', fontsize=15)
ax[1].plot(bac['Volume'])



SMA20 = bac['Close'].rolling(window = 20).mean()
SMA50 = bac['Close'].rolling(window = 50).mean()
SMA200 = bac['Close'].rolling(window = 200).mean()


# taking last 300 trading days
plt.figure(figsize=(15, 6))
plt.plot(bac['Close'][-200:], label='bac')
plt.plot(SMA20[-200:], label='SMA20')
plt.plot(SMA50[-200:], label='SMA50')
plt.plot(SMA200[-200:], label='SMA200')
plt.legend(loc='upper right', fontsize=15)

def get_points_above(sma_low, sma_high):
    points_above = {}
    for pair in zip(sma_low, sma_high):
        if pair[0] >= pair[1]:
            date = sma_low[sma_low == pair[0]].index[0]
            points_above[date] = pair[0]
            
    points_above = pd.Series(points_above, name='Price_Points')
    points_above.index.name = 'Date'
            
    return points_above
points_above_SMA50 = get_points_above(SMA20, SMA50)

SMA20 = SMA20.reset_index()
SMA50 = SMA50.reset_index()

crossovers = pd.DataFrame()
crossovers['Dates'] = SMA20['Date']
crossovers['Price'] = [i for i in bac['Close']]
crossovers['SMA20'] = SMA20['Close']
crossovers['SMA50'] = SMA50['Close']
crossovers['position'] = crossovers['SMA20'] >= crossovers['SMA50']
crossovers['pre-position'] = crossovers['position'].shift(1)
crossovers['Crossover'] = np.where(crossovers['position'] == crossovers['pre-position'], False, True)
crossovers['Crossover'][0] = False
print(crossovers)


crossovers = crossovers.loc[crossovers['Crossover'] == True]
crossovers = crossovers.reset_index()
crossovers = crossovers.drop(['position', 'pre-position', 'Crossover', 'index'], axis=1)
crossovers['Signal'] = np.nan
crossovers['Binary_Signal'] = 0.0
for i in range(len(crossovers['SMA20'])):
    if crossovers['SMA20'][i] > crossovers['SMA50'][i]:
        crossovers['Binary_Signal'][i] = 1.0
        crossovers['Signal'][i] = 'Buy'
    else:
        crossovers['Signal'][i] = 'Sell'
print(crossovers)

# taking last 600 trading days
SMA20 = bac['Close'].rolling(window=20).mean()
SMA50 = bac['Close'].rolling(window=50).mean()
plt.figure(figsize=(17, 8))
plt.plot(bac['Close'][-200:], label='bac')
plt.plot(SMA20[-200:], label='SMA20')
plt.plot(SMA50[-200:], label='SMA50')
plt.plot(crossovers.loc[crossovers.Signal == 'Buy']['Dates'][-2:], 
         crossovers['SMA20'][crossovers.Signal == 'Buy'][-2:],
        '^', markersize=15, color='g', label='Buy')
plt.plot(crossovers.loc[crossovers.Signal == 'Sell']['Dates'][-2:], 
         crossovers['SMA20'][crossovers.Signal == 'Sell'][-2:],
        'v', markersize=15, color='r', label='Sell')
plt.legend(loc='upper right', fontsize=15)




# %%
