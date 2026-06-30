import httpx
import random
from datetime import datetime, timezone

# URL del servidor central
SERVER_URL = "http://127.0.0.1:8000/logs"

# Token único de este servicio
TOKEN = "svc-auth-001"

# Mensajes falsos pero convincentes
MESSAGES = [
    "Usuario autenticado correctamente",
    "Intento de login fallido para user@email.com",
    "Token JWT expirado, sesión cerrada",
    "Nuevo usuario registrado: user123",
    "Demasiados intentos fallidos, IP bloqueada",
]

SEVERITIES = ["INFO", "DEBUG", "ERROR", "WARNING"]

def generate_log():
    """Genera un log falso con datos aleatorios."""
    return {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "service": "Auth Service",
        "severity": random.choice(SEVERITIES),
        "message": random.choice(MESSAGES),
    }

def send_logs(quantity=5):
    """Genera y envía una cantidad de logs al servidor."""
    logs = [generate_log() for _ in range(quantity)]
    
    headers = {"Authorization": f"Token {TOKEN}"}
    
    response = httpx.post(SERVER_URL, json=logs, headers=headers)
    
    print(f"[Auth Service] Status: {response.status_code} | Respuesta: {response.json()}")

if __name__ == "__main__":
    send_logs(quantity=5)