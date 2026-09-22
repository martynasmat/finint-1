import datetime
import os

import alpaca.data
import dotenv
from alpaca.data import StockHistoricalDataClient, StockTradesRequest, StockLatestTradeRequest, StockBarsRequest, \
  TimeFrame
import matplotlib.dates as mdates
from matplotlib import pyplot as plt


class DataClient:
  def __init__(self, api_key, secret_key):
    self.client = StockHistoricalDataClient(api_key, secret_key)

  def fetch_tick_data(
          self,
          symbol: str,
          start_date: datetime.date,
          end_date: datetime.date,
          ticks: int = 100,
  ) -> alpaca.data.TradeSet:
    req = StockTradesRequest(
      symbol_or_symbols=symbol,
      limit=ticks,
      start=start_date,
      end=end_date,
    )
    return self.client.get_stock_trades(
      request_params=req,
    )

  def fetch_bar_data(
          self,
          symbol: str,
          start_date: datetime.date,
          end_date: datetime.date,
          limit: int = 100,
          tf: TimeFrame = TimeFrame.Day,
  ) -> alpaca.data.BarSet:
    """
    Returns bar data for a given stock ticker.
    :param symbol: Stock ticker
    :param start_date: Start date of data
    :param end_date: End date of data
    :param limit: Limit of bars to return
    :param tf: Timeframe for bar (day/minute)
    :return:
    """
    req = StockBarsRequest(
      symbol_or_symbols=symbol,
      timeframe=tf,
      limit=limit,
      start=start_date,
      end=end_date,
    )
    return self.client.get_stock_bars(
      request_params=req,
    )


START_DATE=datetime.date(2026, 8, 1)
END_DATE=datetime.date(2026, 9, 1)
TICKER="AAPL"

dotenv.load_dotenv()
client = DataClient(os.getenv("ALPACA_API_KEY"), os.getenv("ALPACA_SECRET"))

day_df = client.fetch_bar_data(
  TICKER,
  START_DATE,
  END_DATE,
  limit=100,
  tf=TimeFrame.Day).df

minute_df = client.fetch_bar_data(
  TICKER,
  START_DATE,
  END_DATE,
  limit=100000,
  tf=TimeFrame.Minute).df

tick_df = client.fetch_tick_data(
  TICKER,
  START_DATE,
  END_DATE,
  ticks=100000,
).df

if not day_df.empty:
  days = day_df.xs(TICKER, level="symbol").sort_index()
  ax = days[['open', 'high', 'low', 'close']].plot(
    x_compat=True,
    figsize=(30, 15),
  )
  ax.set_xticks([days.index[0], days.index[-1]])
  ax.xaxis.set_major_formatter(
    mdates.DateFormatter("%Y-%m-%d", tz=datetime.timezone.utc)
  )

if not minute_df.empty:
  minutes = minute_df.xs(TICKER, level="symbol").sort_index()
  ax = minutes[['open', 'high', 'low', 'close']].plot(
    x_compat=True,
    figsize=(30, 15),
  )
  ax.set_xticks([minutes.index[0], minutes.index[-1]])
  ax.xaxis.set_major_formatter(
    mdates.DateFormatter("%Y-%m-%d\n%H:%M:%S", tz=datetime.timezone.utc)
  )

if not tick_df.empty:
  ticks = tick_df.xs(TICKER, level="symbol").sort_index()
  ax = ticks[['price']].plot(
    x_compat=True,
    figsize=(30, 15),
  )
  ax.set_xticks([ticks.index[0], ticks.index[-1]])
  ax.xaxis.set_major_formatter(
    mdates.DateFormatter("%Y-%m-%d\n%H:%M:%S", tz=datetime.timezone.utc)
  )

plt.show()
