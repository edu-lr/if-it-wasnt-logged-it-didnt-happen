import httpx
import random
from datetime import datetime, timezone

SERVER_URL = "http://127.0.0.1:8000/logs"
TOKEN = "svc-auth-001"

MESSAGES = [
    "Usuario autenticado correctamente",
    "Intento de login fallido",
    "Token JWT expirado",
    "Nuevo usuario registrado",
    "IP bloqueada por intentos fallidos",
]

SEVERITIES = ["INFO", "DEBUG", "ERROR", "WARNING"]

def generate_log():
    return {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "service": "Auth Service",
        "severity": random.choice(SEVERITIES),
        "message": random.choice(MESSAGES),
    }

def stress_test(total_logs=1000, batch_size=50):
    """
    Envía total_logs logs en tandas de batch_size.
    En vez de mandar 1000 de golpe, los manda de a 50
    para simular varios servicios enviando al mismo tiempo.
    """
    headers = {"Authorization": f"Token {TOKEN}"}
    enviados = 0
    errores = 0

    print(f"Iniciando stress test: {total_logs} logs en tandas de {batch_size}...")

    while enviados < total_logs:
        logs = [generate_log() for _ in range(batch_size)]
        
        try:
            response = httpx.post(SERVER_URL, json=logs, headers=headers, timeout=10)
            if response.status_code == 200:
                enviados += batch_size
                print(f"Enviados: {enviados}/{total_logs}")
            else:
                errores += 1
                print(f"Error en tanda: {response.status_code}")
        except Exception as e:
            errores += 1
            print(f"Excepción: {e}")

    print(f"\nResultado: {enviados} logs enviados, {errores} errores")

if __name__ == "__main__":
    stress_test(total_logs=1000, batch_size=1000)