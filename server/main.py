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

# Inicializa la base de datos al arrancar
@app.on_event("startup")
def startup():
    init_db()

# --- Modelo del log entrante ---
class LogEntry(BaseModel):
    timestamp: str
    service: str
    severity: str
    message: str

# --- POST /logs → recibe uno o varios logs ---
@app.post("/logs")
def receive_logs(
    logs: list[LogEntry],
    authorization: Optional[str] = Header(default=None)
):
    # Valida el token
    service_name = validate_token(authorization)
    if not service_name:
        raise HTTPException(status_code=401, detail="Quién so, vo?")

    # Guarda cada log en la base de datos
    received_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    for log in logs:
        insert_log(
            timestamp=log.timestamp,
            service=log.service,
            severity=log.severity,
            message=log.message,
            received_at=received_at
        )

    return {"status": "ok", "received": len(logs)}

# --- GET /logs → consulta con filtros opcionales ---
@app.get("/logs")
def get_logs(
    authorization: Optional[str] = Header(default=None),
    timestamp_start: Optional[str] = None,
    timestamp_end: Optional[str] = None,
    received_at_start: Optional[str] = None,
    received_at_end: Optional[str] = None,
):
    # Valida el token
    service_name = validate_token(authorization)
    if not service_name:
        raise HTTPException(status_code=401, detail="Quién so, vo?")

    results = query_logs(
        timestamp_start=timestamp_start,
        timestamp_end=timestamp_end,
        received_at_start=received_at_start,
        received_at_end=received_at_end,
    )

    return {"total": len(results), "logs": results}