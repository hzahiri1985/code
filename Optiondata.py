
import yfinance as yf
SPY= yf.Ticker('SPY')
SPY.options

#We can access any of the above dates by using the following:
chain = SPY.option_chain('2023-07-26').calls 
chain.head()

#OBTAINING CALLS

#import pandas (for concatenation) 
import pandas as pd
#call the symbol/ticker
SPY= yf.Ticker('SPY')
#create an empty list
calls_bucket = []
#iterate through dataframes for each expiration date
for i in range(0, len(SPY.options)):
  option = SPY.option_chain(SPY.options[i])
#append each dataframe to the list
  calls_bucket.append(option.calls)
#concatenate dataframes 
df_calls = pd.concat(calls_bucket)
df_calls.head()

#OBTAINING PUTS 

SPY= yf.Ticker('SPY')
puts_bucket = []
for i in range(0, len(SPY.options)):
  option = SPY.option_chain(SPY.options[i])
  puts_bucket.append(option.puts)
df_puts = pd.concat(puts_bucket)
df_puts.head()


#combine both datasets

df_calls['Side'] = 'C'
df_puts['Side'] = 'P'
calls_puts = pd.concat([df_calls, df_puts])
first_column = calls_puts.pop('Side')
calls_puts.insert(0, 'Side', first_column)
calls_puts.head()


calls_puts[(calls_puts.strike == 430.0) & (calls_puts.Side == 'P')].head(10)


# %%
