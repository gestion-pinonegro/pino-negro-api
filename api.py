# api.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Crear app primero
app = FastAPI(
    title="API de Gestión de Bodega - Pino Negro",
    version="1.0.0"
)

# ---------------------------
# CORS (DEBE IR JUSTO DESPUÉS DE app = FastAPI)
# ---------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://pino-negro-app.onrender.com",
        "https://pino-negro-api.onrender.com",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# ---------------------------
# HANDLER PARA PRE-FLIGHT OPTIONS
# ---------------------------

@app.options("/{rest_of_path:path}")
def preflight_handler(rest_of_path: str):
    return {}

# ---------------------------
# IMPORTS QUE EJECUTAN CÓDIGO (DEBEN IR DESPUÉS DEL MIDDLEWARE)
# ---------------------------

from database import create_tables, crear_tabla_usuarios, fetch_all
from trazabilidad_service import TrazabilidadService
from inventario_service import InventarioService
from blend_service import BlendService
from finanzas_service import FinanzasService

# Crear tablas al iniciar la API
# ⚠️ IMPORTANTE: Comentado para evitar bloquear el preflight OPTIONS
# create_tables()
# crear_tabla_usuarios()

# Servicios
traz = TrazabilidadService()
inv = InventarioService()
blend = BlendService()
fin = FinanzasService()

# ---------------------------
# MODELOS Pydantic
# ---------------------------

class Trabajo(BaseModel):
    fecha: str
    lote: str
    tarea: str
    volumen: float
    notas: str | None = None

class ItemInventario(BaseModel):
    nombre: str
    unidad: str
    stock_inicial: float = 0

class MovimientoInventario(BaseModel):
    item_id: int
    tipo: str
    cantidad: float
    fecha: str

class Blend(BaseModel):
    nombre: str
    fecha: str

class Componente(BaseModel):
    blend_id: int
    varietal: str
    volumen: float

class MovimientoFinanzas(BaseModel):
    fecha: str
    concepto: str
    monto: float

# ---------------------------
# ENDPOINTS
# ---------------------------

@app.get("/")
def home():
    return {"mensaje": "API de Bodega funcionando"}

# LOGIN
import hashlib

class LoginData(BaseModel):
    usuario: str
    password: str

@app.post("/login")
def login(data: LoginData):
    rows = fetch_all(
        "SELECT password_hash, rol FROM usuarios WHERE usuario = ?",
        (data.usuario,)
    )

    if not rows:
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")

    password_hash_db, rol = rows[0]
    password_hash_input = hashlib.sha256(data.password.encode()).hexdigest()

    if password_hash_input != password_hash_db:
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")

    return {"mensaje": "ok", "rol": rol}

# TRAZABILIDAD
@app.post("/trabajos")
def crear_trabajo(data: Trabajo):
    traz.registrar_trabajo(data.fecha, data.lote, data.tarea, data.volumen, data.notas)
    return {"status": "ok", "mensaje": "Trabajo registrado"}

@app.get("/trabajos")
def listar_trabajos():
    return traz.listar_trabajos()

# INVENTARIO
@app.post("/inventario/items")
def crear_item(data: ItemInventario):
    inv.crear_item(data.nombre, data.unidad, data.stock_inicial)
    return {"status": "ok", "mensaje": "Item creado"}

@app.get("/inventario/items")
def listar_items():
    return inv.listar_items()

@app.post("/inventario/movimientos")
def registrar_movimiento(data: MovimientoInventario):
    inv.registrar_movimiento(data.item_id, data.tipo, data.cantidad, data.fecha)
    return {"status": "ok", "mensaje": "Movimiento registrado"}

# BLENDS
@app.post("/blends")
def crear_blend_api(data: Blend):
    blend.crear_blend(data.nombre, data.fecha)
    return {"status": "ok", "mensaje": "Blend creado"}

@app.post("/blends/componentes")
def agregar_componente_api(data: Componente):
    blend.agregar_componente(data.blend_id, data.varietal, data.volumen)
    return {"status": "ok", "mensaje": "Componente agregado"}

@app.get("/blends/{blend_id}/composicion")
def composicion(blend_id: int):
    return blend.composicion_porcentual(blend_id)

# FINANZAS
@app.post("/finanzas/ingresos")
def registrar_ingreso(data: MovimientoFinanzas):
    fin.registrar_ingreso(data.fecha, data.concepto, data.monto)
    return {"status": "ok", "mensaje": "Ingreso registrado"}

@app.post("/finanzas/egresos")
def registrar_egreso(data: MovimientoFinanzas):
    fin.registrar_egreso(data.fecha, data.concepto, data.monto)
    return {"status": "ok", "mensaje": "Egreso registrado"}

@app.get("/finanzas/balance")
def balance():
    return {"balance_total": fin.balance_total()}