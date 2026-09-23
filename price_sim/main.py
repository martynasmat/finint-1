# Martynas Mataitis VU ISI III k. 2026.09.01
# Finansinis intelektas - 1 ND (4 dalis)
import datetime
from zoneinfo import ZoneInfo
import random
import pandas as pd
from math import exp, trunc
import matplotlib.pyplot as plt
import mplfinance as mpf

# https://www.nyse.com/trade/hours-calendars
MARKET_OPEN = datetime.time(9, 30)
MARKET_CLOSE = datetime.time(16, 0)
MARKET_HOLIDAYS = [
    datetime.date(2026, 1, 1),
    datetime.date(2026, 1, 19),
    datetime.date(2026, 2, 16),
    datetime.date(2026, 4, 3),
    datetime.date(2026, 5, 25),
    datetime.date(2026, 6, 19),
    datetime.date(2026, 7, 3),
    datetime.date(2026, 9, 7),
    datetime.date(2026, 11, 26),
    datetime.date(2026, 12, 25),
]

class Simulation:
    def __init__(
            self,
            ticker: str,
            start_dt: datetime.datetime,
            end_dt: datetime.datetime,
            starting_price: float,
            market_holidays: list[datetime.date],
            burst_chance: int = 3000,
            market_open: datetime.time = MARKET_OPEN,
            market_close: datetime.time = MARKET_CLOSE,
            impact: float = 0.0005,
            trades_base_max: float = 10,
            tz: ZoneInfo = ZoneInfo("America/New_York"),
    ) -> None:
        """
        Simulates stock price data based on the given parameters.
        :param ticker: Stock ticker
        :param start_dt: Start date of the simulation
        :param end_dt: End date of the simulation
        :param starting_price: Starting price of the stock
        :param market_holidays: List of market holidays
        :param market_open: Time of market open
        :param market_close: Time of market close
        :param impact: Sensitivity of stock price to pressure
        :param trades_base_max: Maximum number of trades per second (without multiplier)
        :param tz: Timezone of the simulation
        """
        self.ticker = ticker
        if start_dt > end_dt:
            raise ValueError("Start date must be before end date")
        self.start_dt = start_dt
        self.end_dt = end_dt
        if starting_price <= 0:
            raise ValueError("Starting price must be positive")
        self.starting_price = starting_price
        self.market_open = market_open
        self.market_close = market_close
        self.market_holidays = market_holidays
        if trades_base_max <= 0:
            raise ValueError("Base trade amount must be positive")
        self.trades_base_max = trades_base_max
        self.tz = tz
        if impact <= 0:
            raise ValueError("Impact must be positive")
        self.impact = impact
        if burst_chance <= 0:
            raise ValueError("Burst chance must be positive")
        self.burst_chance = burst_chance

    def simulate(self) -> pd.DataFrame:
        noise = abs(random.gauss(0, 0.2) * 10)
        rows = []
        curr = self.start_dt.astimezone(self.tz)
        curr_price = self.starting_price
        while curr < self.end_dt.astimezone(self.tz):
            if not self.market_is_open(curr):
                curr = self.next_market_open(curr)
                if curr > self.end_dt.astimezone(self.tz):
                    break

            # Regenerate noise every 5 minutes
            if curr.minute % 5 == 0 and curr.second == 0:
                noise = abs(random.gauss(0, 0.2) * 10)

            trades_base = random.randint(1, self.trades_base_max)
            multiplier = self.get_multiplier(curr)
            # Imitates a burst in trading activity (1 in burst_chance odds), e.g., news, earnings announcements, etc.
            burst_trades = (random.randint(1, self.burst_chance) == 1) * self.trades_base_max * multiplier
            trades = trunc(trades_base * multiplier + burst_trades + noise)
            pressure = self.get_pressure(trades)

            # exp(pressure * self.impact) is needed for the stock price to not go below 0
            new_price = curr_price * exp(pressure * self.impact)
            rows.append((self.ticker, curr, new_price, trades * random.randint(1, 5)))
            curr_price = new_price

            curr = curr + datetime.timedelta(seconds=1)

        return pd.DataFrame(rows, columns=["symbol", "time", "price", "volume"]).set_index("time")

    def get_multiplier(self, t: datetime.datetime) -> float:
        # Multiplier to account for volume swings during the trading session (bigger on open/close, smaller midday)
        t = t.astimezone(self.tz)
        session_open = datetime.datetime.combine(t.date(), self.market_open, tzinfo=self.tz)
        session_close = datetime.datetime.combine(t.date(), self.market_close, tzinfo=self.tz)
        frac = (t - session_open).total_seconds() / (session_close - session_open).total_seconds()
        return 2.6 * frac**2 - 2.9 * frac + 1

    def next_market_open(self, t: datetime.datetime) -> datetime.datetime:
        t = t.astimezone(self.tz)
        day = t.date()

        while True:
            opening = datetime.datetime.combine(
                day, self.market_open, tzinfo=self.tz
            )

            if opening > t and day.weekday() < 5 and day not in self.market_holidays:
                return opening

            day += datetime.timedelta(days=1)

    def market_is_open(self, t: datetime.datetime) -> bool:
        if (
                t.weekday() >= 5
                or t.date() in self.market_holidays
                or t.time() < self.market_open
                or t.time() >= self.market_close
        ):
            return False
        return True

    @staticmethod
    def get_pressure(trades: int):
        p = 0
        opts = [-1, 1]
        for t in range(1, trades + 1):
            p += random.choice(opts)

        return p


if __name__ == "__main__":
    simulator = Simulation(
        ticker="SMLTR",
        start_dt=datetime.datetime(2026, 8, 1, 0, 0, 0),
        end_dt=datetime.datetime(2026, 8, 7, 0, 0, 0),
        starting_price=100,
        market_holidays=MARKET_HOLIDAYS,
        market_open=MARKET_OPEN,
        market_close=MARKET_CLOSE,
        impact=0.00005,
    )

    df = simulator.simulate()
    fig, ax = plt.subplots(figsize=(10, 5))

    # PRICE LINE GRAPH

    ax.plot(df["price"].to_numpy())
    dates = df.index.date
    # Display only unique days in DataFrame
    day_starts = [i for i in range(len(dates)) if i == 0 or dates[i] != dates[i - 1]]
    ax.set_xticks(day_starts)
    ax.set_xticklabels(
        [dates[i].strftime("%b %d") for i in day_starts],
        rotation=45,
        ha="right",
    )
    ax.set_xlabel("Trading day")
    ax.set_ylabel("Price")
    ax.set_title("SMLTR Stock Price")

    # 15-MIN CANDLES

    candles = df.resample("15min", closed="left", label="left").agg(
        Open=("price", "first"),
        High=("price", "max"),
        Low=("price", "min"),
        Close=("price", "last"),
        Volume=("volume", "sum"),
    ).dropna(subset=["Open"])

    mpf.plot(
        candles,
        type="candle",
        style="yahoo",
        volume=True,
        title="SMLTR 15-min candles",
        returnfig=True,
    )

    plt.tight_layout()
    plt.show()