# if-it-wasnt-logged-it-didnt-happen

> "Los sistemas caen. Los logs sobreviven." — proverbio DevOps

Sistema de logging distribuido construido con FastAPI y SQLite. Múltiples servicios simulados envían logs a un servidor central que los valida, guarda y expone para consulta. Porque si no está logueado, técnicamente no pasó.

---

## Tecnologías

- Python 3.10+
- FastAPI
- Uvicorn
- SQLite
- httpx

---

## Estructura del proyecto

```
logging-system/
├── server/
│   ├── main.py        # Servidor FastAPI, endpoints POST y GET /logs
│   ├── database.py    # Conexión a SQLite, inserción y consulta de logs
│   ├── auth.py        # Validación de tokens
│   └── tokens.py      # Lista de tokens válidos por servicio
├── clients/
│   ├── auth_service.py      # Servicio simulado: autenticación
│   ├── payment_service.py   # Servicio simulado: pagos
│   ├── meme_ranker.py       # Servicio simulado: ranking de memes
│   └── stress_test.py       # Prueba de carga: 1000 logs seguidos
├── requirements.txt
└── README.md
```

---

## Instalación

```bash
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## Correr el servidor

```bash
uvicorn server.main:app --reload
```

El servidor arranca en `http://127.0.0.1:8000`

---

## Correr los servicios simulados

```bash
python clients/auth_service.py
python clients/payment_service.py
python clients/meme_ranker.py
```

---

## Prueba de carga

```bash
python clients/stress_test.py
```

Envía 1000 logs en tandas de 50 sin que el servidor explote.

---

## Endpoints

### POST /logs
Recibe uno o varios logs en formato JSON.

**Header requerido:**
```
Authorization: Token TU_TOKEN_AQUI
```

**Body:**
```json
[
    {
        "timestamp": "2026-06-23 23:00:00",
        "service": "Auth Service",
        "severity": "ERROR",
        "message": "Algo falló"
    }
]
```

**Respuesta exitosa:**
```json
{
    "status": "ok",
    "received": 1
}
```

**Token inválido:**
```json
{
    "error": "Quién sos, bro?"
}
```

---

### GET /logs
Devuelve todos los logs. Acepta filtros opcionales por fecha.

**Filtros disponibles:**
| Filtro | Descripción |
|--------|-------------|
| `timestamp_start` | Logs ocurridos desde esta fecha |
| `timestamp_end` | Logs ocurridos hasta esta fecha |
| `received_at_start` | Logs recibidos por el servidor desde esta fecha |
| `received_at_end` | Logs recibidos por el servidor hasta esta fecha |

**Ejemplo:**
```
GET /logs?timestamp_start=2026-06-23 23:15:00&timestamp_end=2026-06-23 23:30:00
```

**Respuesta:**
```json
{
    "total": 10,
    "logs": [
        {
            "id": 1,
            "timestamp": "2026-06-23 23:16:00",
            "service": "Auth Service",
            "severity": "ERROR",
            "message": "IP bloqueada",
            "received_at": "2026-06-23 23:16:01"
        }
    ]
}
```

---

## Tokens válidos

| Token | Servicio |
|-------|----------|
| `svc-auth-001` | Auth Service |
| `svc-pay-002` | Payment Service |
| `svc-meme-003` | Meme Ranker |

---

## Documentación interactiva

Con el servidor corriendo, abrí en el navegador:
```
http://127.0.0.1:8000/docs
```
