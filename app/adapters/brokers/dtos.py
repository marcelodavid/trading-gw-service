from typing import List
from datetime import datetime
from pydantic import BaseModel, Field


class TickDTO(BaseModel):
    date: datetime = Field(..., description="Timestamp of the tick", example="2023-01-01T00:00:00Z")
    bid: float = Field(..., description="Bid price", example=1.0725)
    ask: float = Field(..., description="Ask price", example=1.0726)


class CandleDTO(BaseModel):
    date: datetime = Field(..., description="Timestamp of the candle (start of interval)", example="2023-01-01T00:00:00Z")
    bid_open: float = Field(..., description="Opening bid price", example=1.0720)
    bid_high: float = Field(..., description="Highest bid price in the interval", example=1.0730)
    bid_low: float = Field(..., description="Lowest bid price in the interval", example=1.0715)
    bid_close: float = Field(..., description="Closing bid price", example=1.0725)
    volume: int = Field(..., description="Trading volume during the interval", example=1500)


class PriceContext(BaseModel):
    instrument: str = Field(..., description="Trading instrument name", example="EUR/USD")
    timeframe: str = Field(..., description="Timeframe of the data", example="H1")
    ticks: List[TickDTO] = Field(default=[], description="List of price ticks (if timeframe is TICK)")
    candles: List[CandleDTO] = Field(default=[], description="List of price candles (for non-TICK timeframes)")

    class Config:
        json_schema_extra = {
            "example": {
                "instrument": "EUR/USD",
                "timeframe": "H1",
                "ticks": [],
                "candles": [
                    {
                        "date": "2023-01-01T00:00:00Z",
                        "bid_open": 1.0720,
                        "bid_high": 1.0730,
                        "bid_low": 1.0715,
                        "bid_close": 1.0725,
                        "volume": 1500
                    }
                ]
            }
        }
