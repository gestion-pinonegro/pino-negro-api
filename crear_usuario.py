import hashlib
from database import run_query, crear_tabla_usuarios, create_tables

# Crear tablas si no existen
create_tables()
crear_tabla_usuarios()

usuario = "Franco.guillen"
password = "Illescas2147"
rol = "admin"

# Crear hash SHA-256
password_hash = hashlib.sha256(password.encode()).hexdigest()

run_query("""
    INSERT INTO usuarios (usuario, password_hash, rol)
    VALUES (?, ?, ?)
""", (usuario, password_hash, rol))

print("Usuario creado correctamente.")