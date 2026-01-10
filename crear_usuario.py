import hashlib
from database import run_query, crear_tabla_usuarios, create_tables

# Crear tablas si no existen
create_tables()
crear_tabla_usuarios()

# Lista de usuarios a crear (usuario, contraseña, rol)
usuarios = [
    ("Franco.guillen", "Illescas2147", "admin"),
    ("Nicolas.molina", "Megustaelpene", "admin"),
    ("Maria.lopez", "clave123", "operador"),
    ("Juan.perez", "contraseñaSegura", "operador"),
]

# Recorrer la lista e insertar cada usuario
for usuario, password, rol in usuarios:
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    run_query("""
        INSERT INTO usuarios (usuario, password_hash, rol)
        VALUES (?, ?, ?)
    """, (usuario, password_hash, rol))
    print(f"Usuario '{usuario}' creado correctamente con rol '{rol}'.")