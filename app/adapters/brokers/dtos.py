from typing import List
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class TickDTO(BaseModel):
    date: datetime = Field(..., description="Timestamp of the tick", json_schema_extra={"example": "2023-01-01T00:00:00Z"})
    bid: Decimal = Field(..., description="Bid price", json_schema_extra={"example": "1.0725"})
    ask: Decimal = Field(..., description="Ask price", json_schema_extra={"example": "1.0726"})


class CandleDTO(BaseModel):
    date: datetime = Field(..., description="Timestamp of the candle (start of interval)", json_schema_extra={"example": "2023-01-01T00:00:00Z"})
    bid_open: Decimal = Field(..., description="Opening bid price", json_schema_extra={"example": "1.0720"})
    bid_high: Decimal = Field(..., description="Highest bid price in the interval", json_schema_extra={"example": "1.0730"})
    bid_low: Decimal = Field(..., description="Lowest bid price in the interval", json_schema_extra={"example": "1.0715"})
    bid_close: Decimal = Field(..., description="Closing bid price", json_schema_extra={"example": "1.0725"})
    volume: int = Field(..., description="Trading volume during the interval", json_schema_extra={"example": 1500})


class PriceContext(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "instrument": "EUR/USD",
                "timeframe": "H1",
                "ticks": [],
                "candles": [
                    {
                        "date": "2023-01-01T00:00:00Z",
                        "bid_open": "1.0720",
                        "bid_high": "1.0730",
                        "bid_low": "1.0715",
                        "bid_close": "1.0725",
                        "volume": 1500
                    }
                ]
            }
        }
    )

    instrument: str = Field(..., description="Trading instrument name", json_schema_extra={"example": "EUR/USD"})
    timeframe: str = Field(..., description="Timeframe of the data", json_schema_extra={"example": "H1"})
    ticks: List[TickDTO] = Field(default=[], description="List of price ticks (if timeframe is TICK)")
    candles: List[CandleDTO] = Field(default=[], description="List of price candles (for non-TICK timeframes)")
