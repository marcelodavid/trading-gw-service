from fastapi import APIRouter, HTTPException, Depends, Path
from app.adapters.brokers.dtos import PriceContext
from app.adapters.brokers.base import AbstractBroker
from app.adapters.brokers.providers.fxcm import FXCMBroker
from app.entrypoints.fastapi.api.endpoints.schemas import HistoryRequest
from app.views import get_broker_status, get_price_history

router = APIRouter()


def get_broker_from_path(
    broker: str = Path(..., description="Broker name, e.g. 'fxcm'"),
) -> AbstractBroker:
    if broker.lower() == "fxcm":
        return FXCMBroker()
    raise HTTPException(status_code=400, detail=f"Unknown broker provider: {broker}")


@router.get("/{broker}/status")
def ping(broker: AbstractBroker = Depends(get_broker_from_path)):
    success = get_broker_status(broker)
    if not success:
        raise HTTPException(status_code=503, detail="Broker unreachable")
    return {"status": "ok", "broker": broker}


@router.post("/{broker}/history", response_model=PriceContext)
def get_history(
    request: HistoryRequest,
    broker: AbstractBroker = Depends(get_broker_from_path),
):
    try:
        return get_price_history(
            request.instrument,
            request.timeframe,
            request.date_from,
            request.date_to,
            request.quotes_count,
            broker,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
