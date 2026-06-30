# main.py
# Servidor central de logging.
# Define los endpoints POST /logs (recibir) y GET /logs (consultar).
# Valida tokens de autenticación en cada request.

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
from typing import Optional
import sys
import os

# Permite importar auth y database desde la misma carpeta
sys.path.append(os.path.dirname(__file__))

from auth import validate_token
from database import init_db, insert_log, query_logs

app = FastAPI(title="Logging Service")

# --- Inicialización ---

@app.on_event("startup")
def startup():
    """Crea la tabla en SQLite al arrancar el servidor, si no existe."""
    init_db()

# --- Modelo del log entrante ---

class LogEntry(BaseModel):
    """
    Define la estructura que debe tener cada log en el JSON entrante.
    Si falta algún campo, FastAPI rechaza el request automáticamente.
    """
    timestamp: str
    service: str
    severity: str
    message: str

# --- Endpoints ---

@app.post("/logs")
def receive_logs(
    logs: list[LogEntry],
    authorization: Optional[str] = Header(default=None)
):
    """
    Recibe una lista de logs en formato JSON y los guarda en la base de datos.
    Requiere un token válido en el header Authorization.
    Ejemplo: Authorization: Token svc-auth-001
    """

    # Valida el token antes de procesar cualquier log
    service_name = validate_token(authorization)
    if not service_name:
        raise HTTPException(status_code=401, detail="Quién sos, bro?")

    # Genera el timestamp de recepción una sola vez para todo el batch
    received_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    # Guarda cada log individualmente en la base de datos
    for log in logs:
        insert_log(
            timestamp=log.timestamp,
            service=log.service,
            severity=log.severity,
            message=log.message,
            received_at=received_at
        )

    # Devuelve cuántos logs se guardaron exitosamente
    return {"status": "ok", "received": len(logs)}

@app.get("/logs")
def get_logs(
    authorization: Optional[str] = Header(default=None),
    timestamp_start: Optional[str] = None,
    timestamp_end: Optional[str] = None,
    received_at_start: Optional[str] = None,
    received_at_end: Optional[str] = None,
):
    """
    Consulta logs guardados en la base de datos.
    Requiere token válido en el header Authorization.
    Acepta filtros opcionales por fecha en la URL.
    Ejemplo: GET /logs?timestamp_start=2026-06-23 23:00:00
    """

    # Valida el token antes de devolver cualquier dato
    service_name = validate_token(authorization)
    if not service_name:
        raise HTTPException(status_code=401, detail="Quién sos, bro?")

    # Consulta la base de datos con los filtros que hayan llegado
    results = query_logs(
        timestamp_start=timestamp_start,
        timestamp_end=timestamp_end,
        received_at_start=received_at_start,
        received_at_end=received_at_end,
    )

    # Devuelve el total de logs encontrados y la lista completa
    return {"total": len(results), "logs": results}