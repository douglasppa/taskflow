from datetime import datetime, timezone, timedelta
from fastapi import HTTPException
from http import HTTPStatus
from app.db.mongo import get_sync_mongo_db
from app.core.logger import log, LogLevel
from app.core.metrics import (
    frontend_lcp,
    frontend_ttfb,
    frontend_cls,
    frontend_inp,
    frontend_fcp,
)
from dateutil.parser import parse as parse_datetime


def save_metric(data: dict):
    try:
        if "timestamp" in data and isinstance(data["timestamp"], str):
            try:
                data["timestamp"] = parse_datetime(data["timestamp"])
            except Exception:
                log("Formato de timestamp inválido", level=LogLevel.WARNING)

        data["received_at"] = datetime.now(timezone.utc)

        db, client = get_sync_mongo_db()
        db.metrics.insert_one(data)

    except Exception as e:
        log(f"Erro ao inserir métrica no MongoDB: {e}", level=LogLevel.ERROR)
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Erro ao salvar métrica no banco de dados",
        )
    finally:
        try:
            client.close()
        except Exception:
            log("Erro ao fechar client MongoDB", level=LogLevel.WARNING)


METRIC_NAME_TO_GAUGE = {
    "LCP": frontend_lcp,
    "TTFB": frontend_ttfb,
    "CLS": frontend_cls,
    "INP": frontend_inp,
    "FCP": frontend_fcp,
}


def update_frontend_metrics():
    db, client = get_sync_mongo_db()

    try:
        one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
        metrics_cursor = db.metrics.find({"timestamp": {"$gte": one_hour_ago}})

        aggregate = {}

        for m in metrics_cursor:
            name = m.get("name")
            value = m.get("value")
            route = m.get("route", "unknown")
            browser = m.get("browser", "unknown")

            key = (name, route, browser)
            if key not in aggregate:
                aggregate[key] = []

            if isinstance(value, (int, float)):
                aggregate[key].append(value)

        for (name, route, browser), values in aggregate.items():
            if name in METRIC_NAME_TO_GAUGE and values:
                gauge = METRIC_NAME_TO_GAUGE[name]
                average = sum(values) / len(values)
                gauge.labels(route=route, browser=browser).set(average)

    except Exception as e:
        print(f"Erro ao atualizar métricas do frontend: {e}")
    finally:
        client.close()
