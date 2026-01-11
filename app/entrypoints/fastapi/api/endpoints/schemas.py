from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, validator


class Instrument(str, Enum):
    EURUSD = "EUR/USD"


class Timeframe(str, Enum):
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
    instrument: Instrument
    timeframe: Timeframe
    date_from: datetime
    date_to: datetime
    quotes_count: Optional[int] = 0

    class Config:
        use_enum_values = True

    @validator("quotes_count")
    def validate_quotes_count(cls, v):
        if v < 0:
            raise ValueError("quotes_count cannot be negative")
        return v

    @validator("date_from", "date_to")
    def validate_date_range(cls, v):
        if v > datetime.now():
            raise ValueError("date_from and date_to cannot be in the future")
        return v

    @validator("instrument")
    def validate_instrument(cls, v):
        if v not in Instrument:
            raise ValueError("instrument must be a valid Instrument")
        return v

    @validator("timeframe")
    def validate_timeframe(cls, v):
        if v not in Timeframe:
            raise ValueError("timeframe must be a valid Timeframe")
        return v
