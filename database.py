# database.py
# Sistema de gestión de bodega – conexión y creación de tablas SQLite

import sqlite3

DB_NAME = "bodega.db"

# ---------------------------------------
# Conexión a la base de datos
# ---------------------------------------
def get_connection():
    return sqlite3.connect(DB_NAME)

# ---------------------------------------
# Crear todas las tablas del sistema
# ---------------------------------------
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # TRABAJOS (Trazabilidad)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trabajos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            lote TEXT NOT NULL,
            tarea TEXT NOT NULL,
            volumen REAL,
            notas TEXT
        );
    """)

    # MOVIMIENTOS DE VOLUMEN
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimientos_volumen (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            origen TEXT,
            destino TEXT,
            volumen REAL NOT NULL,
            lote TEXT,
            trabajo_id INTEGER,
            FOREIGN KEY (trabajo_id) REFERENCES trabajos(id)
        );
    """)

    # FINANZAS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS finanzas_ingresos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            concepto TEXT NOT NULL,
            monto REAL NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS finanzas_egresos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            concepto TEXT NOT NULL,
            monto REAL NOT NULL
        );
    """)

    # INVENTARIO
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventario_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            unidad TEXT NOT NULL,
            stock REAL NOT NULL DEFAULT 0
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventario_movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            item_id INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            cantidad REAL NOT NULL,
            FOREIGN KEY (item_id) REFERENCES inventario_items(id)
        );
    """)

    # BLENDS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blends (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            fecha TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blend_componentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            blend_id INTEGER NOT NULL,
            varietal TEXT NOT NULL,
            volumen REAL NOT NULL,
            FOREIGN KEY (blend_id) REFERENCES blends(id)
        );
    """)

    conn.commit()
    conn.close()
    print("Tablas principales creadas correctamente.")

# ---------------------------------------
# Crear tabla de usuarios
# ---------------------------------------
def crear_tabla_usuarios():
    run_query("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            rol TEXT NOT NULL
        )
    """)

# ---------------------------------------
# Función genérica para ejecutar queries
# ---------------------------------------
def run_query(query, params=()):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

# ---------------------------------------
# Función genérica para obtener datos
# ---------------------------------------
def fetch_all(query, params=()):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows

# ---------------------------------------
# Ejecutar creación de tablas si se corre este archivo directamente
# ---------------------------------------
if __name__ == "__main__":
    create_tables()
    crear_tabla_usuarios()
    print("Todas las tablas creadas correctamente.")