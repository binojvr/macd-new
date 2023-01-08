import pandas as pd
import yfinance as yf
import numpy as np


# find the exponential moving average(SMA) for specific window size(number of rows)
# EMA in  MACD is useful to understand the recent price movements and useful for identifying entry and exit
# Good for intraday trading
# should not be used for trend indications
def ema(df: pd.DataFrame(), col, w, n):
    df[n] = df[col].ewm(span=w).mean()


# find the simple moving average(SMA) for specific window size(number of rows)
# SMA in  MACD is useful to understand the trend as it gives equal weight to new and old prices in the model
# Good for longer-term trades
def sma(df: pd.DataFrame(), w, n):
    df[n] = df['Close'].rolling(window=w).mean()


# SMA & EMA are technical indicators used in MACD analysis,
# helping traders gain a better understanding of trends.

# find macd  indicator   and signal line
def macd(df: pd.DataFrame()):
    df['MACD'] = df['slowma'] - df['fastma']
    ema(df, 'MACD', SIGNAL_WINDOW, 'signal')
    df['signal'] = df['signal'].fillna(df['MACD'])
    df['histogram'] = df['MACD'] - df['signal']


def buy_sell_signal(df: pd.DataFrame()):
    df['upward'] = np.where(df['MACD'] > df['signal'], 1.0, 0.0)
    # Generate trading orders
    df['sell_signal'] = df['upward'].diff()
    df['downward'] = np.where(df['MACD'] < df['signal'], 1.0, 0)
    # Generate trading orders
    df['buy_signal'] = df['downward'].diff()


"""
　get the data for specific symbol
  drop few columns which are not required for macd
  find slow moving average (12 period)
  find fast moving average (26 period)
  calculate macd
  find signal line from 9 period moving average of macd
  get the buy and sell signal from macd and signal
"""

SIGNAL_WINDOW = 9
SHORT_WINDOW = 12
LONG_WINDOW = 26


def main(sym):
    df = yf.Ticker(sym).history(period='1d', interval='5m')
    pd.set_option('display.max_columns', None)
    df = df.drop(columns=['Open', 'High', 'Low', 'Dividends', 'Stock Splits'])
    ema(df, 'Close', SHORT_WINDOW, 'slowma')
    ema(df, 'Close', LONG_WINDOW, 'fastma')
    df = df[df['slowma'].notna()]
    df = df[df['fastma'].notna()]
    macd(df)
    buy_sell_signal(df)
    print(df.head(15))
    print(df.tail(15))


if __name__ == "__main__":
    main('AAPL')
