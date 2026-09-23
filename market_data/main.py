# Martynas Mataitis VU ISI III k. 2026.09.01
# Finansinis intelektas - 1 ND (2 ir 3 dalys + papildomos 4 ir 5 užduotys)

import datetime
import dotenv
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from concurrent.futures import ThreadPoolExecutor
from data_client import DataClient
from alpaca.data import TimeFrame
import mplfinance as mpf
from helper import rename_cols
import heapq as hq

START_DATE=datetime.date(2026, 8, 1)
END_DATE=datetime.date(2026, 9, 1)
TICKER="AAPL"

dotenv.load_dotenv()
client = DataClient(os.getenv("ALPACA_API_KEY"), os.getenv("ALPACA_SECRET"))

# Fetch concurrently
with ThreadPoolExecutor(max_workers=3) as executor:
    day = executor.submit(client.fetch_bar_data, TICKER, START_DATE, END_DATE, 100, TimeFrame.Day)
    minute = executor.submit(client.fetch_bar_data, TICKER, START_DATE, END_DATE, 100, TimeFrame.Minute)
    tick = executor.submit(client.fetch_tick_data, TICKER, START_DATE, END_DATE, 10000)

    day_df = day.result().df
    minute_df = minute.result().df
    tick_df = tick.result().df

if day_df.empty:
    print("No day data")
else:
    days = day_df.xs(TICKER, level="symbol").sort_index()
    days = rename_cols(days)
    mpf.plot(days, type="candle", style="yahoo", axtitle=f"{TICKER} daily candle chart", xlabel="Date")

if minute_df.empty:
    print("No minute data")
else:
    minutes = minute_df.xs(TICKER, level="symbol")
    minutes = rename_cols(minutes)
    mpf.plot(minutes, type="candle", style="yahoo", axtitle=f"{TICKER} minute candle chart", xlabel="Date")
if tick_df.empty:
    print("No tick data")
else:
    # Remove symbol from index
    ticks = tick_df.xs(TICKER, level="symbol")
    ax = ticks[['price']].plot(
        x_compat=True,
        figsize=(10, 5),
        title=f"{TICKER} tick chart",
        xlabel="Date",
        ylabel="Price",
    )
    # Show only the first and last timestamp labels
    ax.set_xticks([ticks.index[0], ticks.index[-1]])
    # Format x axis labels
    ax.xaxis.set_major_formatter(
        mdates.DateFormatter("%Y-%m-%d\n%H:%M:%S", tz=datetime.timezone.utc)
    )


# ------ 4 PAPILDOMA -------

if not tick_df.empty:
    ticks = tick_df.xs(TICKER, level="symbol").sort_index()
    prev_ts = None
    pauses = []
    hq.heapify(pauses)

    for timestamp, row in ticks.iterrows():
        if prev_ts is not None:
            gap_seconds = (timestamp - prev_ts).total_seconds()
            if len(pauses) < 10:
                hq.heappush(pauses, (gap_seconds, row.name))
            elif gap_seconds > pauses[0][0]:
                hq.heappushpop(pauses, (gap_seconds, row.name))


        prev_ts = timestamp

    print(f"10 didžiausių petraukų: ")
    for p in pauses:
        print(f"{p[0]}s @ {p[1]}")
else:
    print("No tick data")


# ------ 5 PAPILDOMA -------

if not tick_df.empty:
    ticks = tick_df.xs(TICKER, level="symbol").sort_index()
    hbars = ticks.resample("1min", closed="left", label="left").agg(
        Open=("price", "first"),
        High=("price", "max"),
        Low=("price", "min"),
        Close=("price", "last"),
    ).dropna(subset=["Open"])

    mpf.plot(hbars, type="candle", style="yahoo", title=f"{TICKER} Minutės žvakės iš tikinių duomenų", returnfig=True)
else:
    print("No tick data")

plt.show()
mpf.show()