from fastapi import APIRouter, Request, HTTPException
from http import HTTPStatus
from app.services.metrics import save_metric
from app.core.logger import log, LogLevel

router = APIRouter()


@router.post("/metrics", summary="Receive metrics data", status_code=HTTPStatus.OK)
async def receive_metric(request: Request):
    try:
        data = await request.json()
        save_metric(data)
        return {"status": "ok"}
    except HTTPException as e:
        log("Erro conhecido ao salvar métrica", level=LogLevel.ERROR)
        raise e
    except Exception as e:
        log(f"Erro inesperado ao salvar métrica: {e}", level=LogLevel.ERROR)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Erro interno ao salvar métrica",
        )
