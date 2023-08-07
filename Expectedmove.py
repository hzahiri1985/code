import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")

def options_chain(symbol):
    '''Utility Method to Get Options for Stock'''
    tk = yf.Ticker(symbol)
    # Expiration dates
    exps = tk.options

    # Get options for each expiration
    options = pd.DataFrame()
    for e in exps:
        opt = tk.option_chain(e)
        opt = pd.DataFrame().append(opt.calls).append(opt.puts)
        opt['expirationDate'] = e
        options = options.append(opt, ignore_index=True)

    options['expirationDate'] = pd.to_datetime(options['expirationDate'])

    # Boolean column if the option is a CALL, to distinguish calls from puts
    options['CALL'] = options['contractSymbol'].str[4:].apply(lambda x: "C" in x)

    return options

def get_expected_move(stock, expiration_date):
    ticker = yf.Ticker(stock)
    current_price = ticker.info['currentPrice']

    data = options_chain(stock)
    dates = np.sort(data['expirationDate'].unique())

    closest = data[data['expirationDate'] == expiration_date]

    #to match stock's price with the strike price
    closest['abs'] = abs(current_price - closest['strike'])
    closest = closest.sort_values('abs')
    move = (closest[closest['CALL'] == True]['lastPrice'].iloc[0] + closest[closest['CALL'] == False]['lastPrice'].iloc[0]) * 1.25
    return current_price, move, expiration_date

move = get_expected_move('bac', '2023-8-4')
#move variable is a list
upper_move = move[0] + move[1]
lower_move = move[0] - move[1]
print("Expected price move between", upper_move, "and", lower_move, "until", move[2])


#extending time period into the future
b = pd.date_range(start ='2023-7-1', periods = 9)
data = yf.download('bac', start = '2023-7-01')
#adding the future dates into the data dataframe
data.index.append(b)
fig = px.line(data, x=data.index, y=data['Close'], title = 'Expected Move')
fig.update_xaxes(range=["2023-7-01", "2023-8-25" ])
fig.add_hline(y=upper_move, line = dict(color = 'red', width =2), line_dash="dot", annotation_text=upper_move,
              annotation_position="bottom right")
fig.add_hline(y=lower_move, line = dict(color = 'red', width =2), line_dash="dot", annotation_text=lower_move, 
              annotation_position="bottom right")
fig.update_yaxes(title_text="Stock Price")
fig.update_xaxes(title_text="Date")
fig.update_layout(height=700, width=1500, 
                  showlegend=False)

fig.show()