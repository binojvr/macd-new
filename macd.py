import pandas as pd
import yfinance as yf
import numpy as np

SIGNAL_WINDOW = 9
SHORT_WINDOW = 12
LONG_WINDOW = 26


# find the moving average for specific window size(number of rows)
def mov_avg(df: pd.DataFrame(), w, n):
    df[n] = df['Close'].rolling(window=w).mean()


# find macd and signal line
def macd(df: pd.DataFrame()):
    df['MACD'] = df['slowma'] - df['fastma']
    mov_avg(df, SIGNAL_WINDOW, 'signal')
    df['signal'] = df['signal'].fillna(df['MACD'])


def buy_sell_signal(df: pd.DataFrame()):
    df['buy'] = np.where(df['MACD'] > df['signal'], 1.0, 0.0)
    df['sell'] = np.where(df['MACD'] < df['signal'], 1.0, 0.0)


"""
　get the data for specific symbol
  drop few columns which are not required for macd
  find slow moving average (12 period)
  find fast moving average (26 period)
  calculate macd
  find signal line from 9 period moving average of macd
  get the buy and sell signal from macd and signal
"""


def main(sym):
    df = yf.Ticker(sym).history(period='1d', interval='5m')
    pd.set_option('display.max_columns', None)
    df = df.drop(columns=['Open', 'High', 'Low', 'Dividends', 'Stock Splits'])
    mov_avg(df, SHORT_WINDOW, 'slowma')
    mov_avg(df, LONG_WINDOW, 'fastma')
    df = df[df['slowma'].notna()]
    df = df[df['fastma'].notna()]
    macd(df)
    buy_sell_signal(df)
    print(df)


if __name__ == "__main__":
    main('AAPL')
