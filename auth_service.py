import sqlite3
from fastapi import HTTPException
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "CAMBIA_ESTE_SECRETO"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def crear_usuario(nombre, email, password, rol):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    password_hash = pwd_context.hash(password)

    try:
        cursor.execute("""
            INSERT INTO usuarios (nombre, email, password_hash, rol)
            VALUES (?, ?, ?, ?)
        """, (nombre, email, password_hash, rol))
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    return {"mensaje": "Usuario creado correctamente"}


def login_usuario(email, password):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, password_hash, rol FROM usuarios WHERE email = ?", (email,))
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=400, detail="Credenciales inválidas")

    user_id, password_hash, rol = user

    if not pwd_context.verify(password, password_hash):
        raise HTTPException(status_code=400, detail="Credenciales inválidas")

    token = jwt.encode(
        {"sub": user_id, "rol": rol, "exp": datetime.utcnow() + timedelta(hours=12)},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {"token": token, "rol": rol}