from typing import List
from datetime import datetime
from pydantic import BaseModel


class TickDTO(BaseModel):
    date: datetime
    bid: float
    ask: float


class CandleDTO(BaseModel):
    date: datetime
    bid_open: float
    bid_high: float
    bid_low: float
    bid_close: float
    volume: int


class PriceContext(BaseModel):
    instrument: str
    timeframe: str
    ticks: List[TickDTO] = []
    candles: List[CandleDTO] = []
