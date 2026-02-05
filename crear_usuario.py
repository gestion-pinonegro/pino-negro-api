import hashlib
import sqlite3
from database import crear_tabla_usuarios, create_tables

# Crear tablas si no existen
create_tables()
crear_tabla_usuarios()

DB_NAME = "bodega.db"  # ajustá si tu base se llama distinto

# Lista de usuarios a crear
usuarios = [
    ("Franco.guillen", "Illescas2147", "admin"),
    ("Nicolas.molina", "Megustaelpene", "admin"),
    ("Julieta.martinez", "Laperita", "operador"),
    ("Juan.perez", "contraseñaSegura", "operador"),
]

# Abrir conexión una sola vez
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

for usuario, password, rol in usuarios:
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    try:
        cursor.execute(
            "INSERT INTO usuarios (usuario, password_hash, rol) VALUES (?, ?, ?)",
            (usuario, password_hash, rol)
        )
        print(f"Usuario '{usuario}' creado correctamente con rol '{rol}'.")
    except sqlite3.IntegrityError as e:
        print(f"No se pudo crear el usuario '{usuario}': {e}")

# Guardar y cerrar
conn.commit()
conn.close()