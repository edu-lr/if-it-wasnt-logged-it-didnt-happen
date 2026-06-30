import httpx
import random
from datetime import datetime, timezone

SERVER_URL = "http://127.0.0.1:8000/logs"
TOKEN = "svc-meme-003"

MESSAGES = [
    "Meme rankeado con score 9.8/10",
    "Meme duplicado detectado, ignorando",
    "Error al cargar imagen del meme",
    "Cache de memes expirado, recargando",
    "Meme con contenido inapropiado bloqueado",
]

SEVERITIES = ["INFO", "DEBUG", "ERROR", "WARNING"]

def generate_log():
    return {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "service": "Meme Ranker",
        "severity": random.choice(SEVERITIES),
        "message": random.choice(MESSAGES),
    }

def send_logs(quantity=5):
    logs = [generate_log() for _ in range(quantity)]
    headers = {"Authorization": f"Token {TOKEN}"}
    response = httpx.post(SERVER_URL, json=logs, headers=headers)
    print(f"[Meme Ranker] Status: {response.status_code} | Respuesta: {response.json()}")

if __name__ == "__main__":
    send_logs(quantity=5)