import numpy as np
from decimal import Decimal
from datetime import datetime
from app.adapters.brokers.dtos import TickDTO, CandleDTO


def test_tick_dto_decimal_precision():
    """Standard float input is coerced to Decimal."""
    tick = TickDTO(date=datetime.now(), bid=1.07255, ask=1.07256)

    assert isinstance(tick.bid, Decimal)
    assert isinstance(tick.ask, Decimal)
    assert tick.bid == Decimal("1.07255")
    assert tick.ask == Decimal("1.07256")


def test_tick_dto_numpy_float_precision():
    """numpy.float64 inputs (from forexconnect) are correctly converted to Decimal."""
    tick = TickDTO(date=datetime.now(), bid=np.float64(1.07255), ask=np.float64(1.07256))

    assert isinstance(tick.bid, Decimal)
    assert isinstance(tick.ask, Decimal)
    assert tick.bid == Decimal("1.07255")
    assert tick.ask == Decimal("1.07256")


def test_candle_dto_decimal_precision():
    """All CandleDTO price fields become Decimal instances."""
    candle = CandleDTO(
        date=datetime.now(),
        bid_open=1.07201,
        bid_high=1.07302,
        bid_low=1.07153,
        bid_close=1.07254,
        volume=100,
    )

    assert isinstance(candle.bid_open, Decimal)
    assert candle.bid_open == Decimal("1.07201")
    assert candle.bid_high == Decimal("1.07302")
    assert candle.bid_low == Decimal("1.07153")
    assert candle.bid_close == Decimal("1.07254")


def test_high_precision_validation():
    """Full precision is preserved for values with many decimal places."""
    val = Decimal("1.072554321")
    tick = TickDTO(date=datetime.now(), bid=val, ask=val)

    assert tick.bid == val
    assert tick.ask == val
