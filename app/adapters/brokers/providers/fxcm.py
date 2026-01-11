import logging
from datetime import datetime


from forexconnect import ForexConnect, fxcorepy
from forexconnect.errors import (
    LoginFailedError,
    RequestFailedError,
    TableManagerError,
    TimeFrameError,
)

from app.adapters.brokers.dtos import PriceContext, TickDTO, CandleDTO
from app.adapters.brokers.base import AbstractBroker
from app.adapters.brokers.providers.config import settings

logger = logging.getLogger(__name__)


class FXCMBroker(AbstractBroker):
    def __init__(self):
        self.user_id = settings.FXCM_USER_ID
        self.password = settings.FXCM_PASSWORD
        self.url = settings.FXCM_URL
        self.connection = settings.FXCM_CONNECTION

    def __str__(self):
        return "FXCM Broker"

    def ping(self) -> bool:
        with ForexConnect() as fx:
            try:
                fx.login(
                    user_id=self.user_id,
                    password=self.password,
                    url=self.url,
                    connection=self.connection,
                )
                logger.info("FXCM Broker ping successful.")
                return True
            except Exception as e:
                logger.error(f"FXCM Broker ping failed: {e}")
                return False

    def collect_price_history(
        self,
        instrument: str,
        timeframe: str,
        date_from: datetime,
        date_to: datetime,
        quotes_count: int,
    ) -> PriceContext:
        with ForexConnect() as fx:
            try:
                fx.login(
                    user_id=self.user_id,
                    password=self.password,
                    url=self.url,
                    connection=self.connection,
                )
                history_data = fx.get_history(
                    instrument,
                    timeframe,
                    date_from,
                    date_to,
                    quotes_count,
                )

                current_unit, _ = ForexConnect.parse_timeframe(timeframe)

                ctx = PriceContext(
                    instrument=instrument,
                    timeframe=timeframe,
                )

                if current_unit == fxcorepy.O2GTimeFrameUnit.TICK:
                    ticks = [
                        TickDTO(
                            date=row["Date"],
                            bid=row["Bid"],
                            ask=row["Ask"],
                        )
                        for row in history_data
                    ]
                    ctx.ticks = ticks
                else:
                    candles = [
                        CandleDTO(
                            date=row["Date"],
                            bid_open=row["BidOpen"],
                            bid_high=row["BidHigh"],
                            bid_low=row["BidLow"],
                            bid_close=row["BidClose"],
                            volume=row["Volume"],
                        )
                        for row in history_data
                    ]
                    ctx.candles = candles
                    logger.debug(
                        f"Collected {len(candles)} candles for {instrument} {timeframe}"
                    )

                return ctx

            except (
                LoginFailedError,
                RequestFailedError,
                TableManagerError,
                TimeFrameError,
            ) as e:
                logger.error(f"Error collecting price history: {e}")
                raise
            except Exception as e:
                logger.error(f"Unexpected error in collect_price_history: {e}")
                raise
