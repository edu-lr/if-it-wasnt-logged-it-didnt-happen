import httpx
import random
from datetime import datetime, timezone

SERVER_URL = "http://127.0.0.1:8000/logs"
TOKEN = "svc-pay-002"

MESSAGES = [
    "Pago procesado exitosamente por $1500",
    "Tarjeta rechazada para orden #4521",
    "Reembolso iniciado para transacción #9981",
    "Timeout al conectar con pasarela de pago",
    "Transacción sospechosa detectada, orden pausada",
]

SEVERITIES = ["INFO", "DEBUG", "ERROR", "WARNING"]

def generate_log():
    return {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "service": "Payment Service",
        "severity": random.choice(SEVERITIES),
        "message": random.choice(MESSAGES),
    }

def send_logs(quantity=5):
    logs = [generate_log() for _ in range(quantity)]
    headers = {"Authorization": f"Token {TOKEN}"}
    response = httpx.post(SERVER_URL, json=logs, headers=headers)
    print(f"[Payment Service] Status: {response.status_code} | Respuesta: {response.json()}")

if __name__ == "__main__":
    send_logs(quantity=5)