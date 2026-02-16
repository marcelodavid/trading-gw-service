from enum import Enum
from typing import Optional
from datetime import datetime, timezone
from pydantic import BaseModel, validator, Field


class Instrument(str, Enum):
    """Supported trading instruments."""
    EURUSD = "EUR/USD"
    GBPUSD = "GBP/USD"
    USDJPY = "USD/JPY"
    AUDUSD = "AUD/USD"
    USDCAD = "USD/CAD"


class Timeframe(str, Enum):
    """Supported timeframes for historical data."""
    m1 = "m1"
    m5 = "m5"
    m15 = "m15"
    m30 = "m30"
    H1 = "H1"
    H4 = "H4"
    D1 = "D1"
    W1 = "W1"
    M1 = "M1"


class HistoryRequest(BaseModel):
    """Schema for historical data requests."""
    instrument: Instrument = Field(
        ..., 
        description="The trading pair to fetch data for",
        example="EUR/USD"
    )
    timeframe: Timeframe = Field(
        ..., 
        description="The granularity of the data",
        example="H1"
    )
    date_from: datetime = Field(
        ..., 
        description="Start date for the data range (ISO 8601)",
        example="2023-01-01T00:00:00Z"
    )
    date_to: datetime = Field(
        ..., 
        description="End date for the data range (ISO 8601)",
        example="2023-01-02T00:00:00Z"
    )
    quotes_count: Optional[int] = Field(
        0, 
        description="Maximum number of quotes to return. Use 0 for no limit.",
        example=500,
        ge=0
    )

    class Config:
        use_enum_values = True
        json_schema_extra = {
            "example": {
                "instrument": "EUR/USD",
                "timeframe": "H1",
                "date_from": "2023-01-01T00:00:00Z",
                "date_to": "2023-01-02T00:00:00Z",
                "quotes_count": 500
            }
        }

    @validator("date_from", "date_to")
    def validate_date_range(cls, v):
        """Ensure date is not in the future, handling timezone-aware datetimes."""
        now = datetime.now(v.tzinfo) if v.tzinfo else datetime.now()
        if v > now:
            raise ValueError("date_from and date_to cannot be in the future")
        return v

class StatusResponse(BaseModel):
    """Schema for broker status response."""
    status: str = Field(..., description="Connection status", example="ok")
    broker: str = Field(..., description="Broker name identifier", example="fxcm")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "ok",
                "broker": "fxcm"
            }
        }

