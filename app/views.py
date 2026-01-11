from datetime import datetime
from app.adapters.brokers.dtos import PriceContext
from app.adapters.brokers.base import AbstractBroker


def get_broker_status(broker_provider: AbstractBroker) -> bool:
    return broker_provider.ping()


def get_price_history(
    instrument: str,
    timeframe: str,
    date_from: datetime,
    date_to: datetime,
    quotes_count: int,
    broker_provider: AbstractBroker,
) -> PriceContext:
    return broker_provider.collect_price_history(
        instrument, timeframe, date_from, date_to, quotes_count
    )
