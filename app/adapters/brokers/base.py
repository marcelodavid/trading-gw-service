from datetime import datetime
import abc
from app.adapters.brokers.dtos import PriceContext


class AbstractBroker(abc.ABC):
    @abc.abstractmethod
    def ping(self) -> bool:
        """Ping the broker service/connection."""
        ...

    @abc.abstractmethod
    def collect_price_history(
        self,
        instrument: str,
        timeframe: str,
        date_from: datetime,
        date_to: datetime,
        quotes_count: int,
    ) -> PriceContext:
        """Collect historical price data."""
        ...
