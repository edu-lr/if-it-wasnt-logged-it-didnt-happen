import sqlite3

DB_PATH = "logs.db"

def get_connection():
    """Abre y devuelve una conexión a la base de datos SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Para acceder a columnas por nombre
    return conn

def init_db():
    
    # Crea la tabla de logs si no existe.
    # Se llama una sola vez al arrancar el servidor.
    
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
    """Inserta un log en la base de datos."""
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
    Todos los parámetros son opcionales.
    """
    conn = get_connection()
    
    query = "SELECT * FROM logs WHERE 1=1"  # 1=1 permite agregar filtros dinámicamente
    params = []

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

    query += " ORDER BY received_at DESC"  # Los más recientes primero

    rows = conn.execute(query, params).fetchall()
    conn.close()
    
    return [dict(row) for row in rows]  # Convierte cada fila a diccionario