import os
from datetime import datetime, timedelta

import pandas as pd
from forexconnect import ForexConnect, fxcorepy

USER_ID = os.getenv("BROKER_USER_ID")
PASSWORD = os.getenv("BROKER_PASSWORD")
URL = os.getenv("BROKER_URL")
CONNECTION = os.getenv("BROKER_CONNECTION")


def print_history(
    fx, instrument: str, timeframe: str, date_from: datetime, date_to, quotes_count=100
):
    history = fx.get_history(instrument, timeframe, date_from, date_to, quotes_count)
    current_unit, _ = ForexConnect.parse_timeframe(timeframe)

    date_format = "%m.%d.%Y %H:%M:%S"
    if current_unit == fxcorepy.O2GTimeFrameUnit.TICK:
        print("Date, Bid, Ask")
        print(history.dtype.names)
        for row in history:
            print(
                "{0:s}, {1:,.5f}, {2:,.5f}".format(
                    pd.to_datetime(str(row["Date"])).strftime(date_format),
                    row["Bid"],
                    row["Ask"],
                )
            )
    else:
        print("Date, BidOpen, BidHigh, BidLow, BidClose, Volume")
        for row in history:
            print(
                "{0:s}, {1:,.5f}, {2:,.5f}, {3:,.5f}, {4:,.5f}, {5:d}".format(
                    pd.to_datetime(str(row["Date"])).strftime(date_format),
                    row["BidOpen"],
                    row["BidHigh"],
                    row["BidLow"],
                    row["BidClose"],
                    row["Volume"],
                )
            )


def main():
    with ForexConnect() as fx:
        try:
            fx.login(user_id=USER_ID, password=PASSWORD, url=URL, connection=CONNECTION)
            print_history(
                fx,
                instrument="EUR/USD",
                timeframe="H1",
                date_from=datetime.now() - timedelta(weeks=1),
                date_to=datetime.now(),
                quotes_count=1000,
            )
        except Exception as e:
            print(e)
        try:
            fx.logout()
        except Exception as e:
            print(e)


main()
