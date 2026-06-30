# database.py
# Maneja toda la interacción con la base de datos SQLite.
# Responsabilidades: crear la tabla, insertar logs y consultar logs con filtros.

import sqlite3

# Nombre del archivo de base de datos que SQLite crea automáticamente
DB_PATH = "logs.db"

def get_connection():
    """
    Abre y devuelve una conexión a la base de datos SQLite.
    row_factory permite acceder a las columnas por nombre en vez de por índice.
    Ejemplo: row["service"] en vez de row[2]
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Crea la tabla de logs si no existe todavía.
    Se llama una sola vez cuando el servidor arranca.
    IF NOT EXISTS evita errores si la tabla ya fue creada antes.
    """
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp   TEXT NOT NULL,
            service     TEXT NOT NULL,
            severity    TEXT NOT NULL,
            message     TEXT NOT NULL,
            received_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def insert_log(timestamp, service, severity, message, received_at):
    """
    Inserta un log en la base de datos.
    Usa ? como placeholders para evitar inyección SQL.
    Los valores se pasan como tupla y SQLite los reemplaza en orden.
    """
    conn = get_connection()
    conn.execute("""
        INSERT INTO logs (timestamp, service, severity, message, received_at)
        VALUES (?, ?, ?, ?, ?)
    """, (timestamp, service, severity, message, received_at))
    conn.commit()
    conn.close()

def query_logs(timestamp_start=None, timestamp_end=None,
               received_at_start=None, received_at_end=None):
    """
    Consulta logs con filtros opcionales de fecha.
    Todos los parámetros son opcionales, si no llegan se devuelven todos los logs.

    timestamp    → cuándo ocurrió el evento en el servicio que lo generó
    received_at  → cuándo lo recibió el servidor central
    """
    conn = get_connection()

    # WHERE 1=1 permite agregar filtros con AND dinámicamente
    # sin preocuparse si es el primero o no
    query = "SELECT * FROM logs WHERE 1=1"
    params = []

    # Agrega cada filtro al query solo si fue enviado
    if timestamp_start:
        query += " AND timestamp >= ?"
        params.append(timestamp_start)
    if timestamp_end:
        query += " AND timestamp <= ?"
        params.append(timestamp_end)
    if received_at_start:
        query += " AND received_at >= ?"
        params.append(received_at_start)
    if received_at_end:
        query += " AND received_at <= ?"
        params.append(received_at_end)

    # Ordena del más reciente al más viejo
    query += " ORDER BY received_at DESC"

    # Ejecuta el query y trae todas las filas
    rows = conn.execute(query, params).fetchall()
    conn.close()

    # Convierte cada fila de SQLite a diccionario Python
    # para que FastAPI pueda transformarlo a JSON
    return [dict(row) for row in rows]