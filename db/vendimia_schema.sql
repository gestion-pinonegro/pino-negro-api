CREATE TABLE IF NOT EXISTS vendimia_ingresos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_ingreso TEXT NOT NULL,
    productor TEXT NOT NULL,
    finca TEXT,
    cuartel TEXT,
    variedad TEXT NOT NULL,
    peso_bruto REAL NOT NULL,
    tara REAL NOT NULL,
    peso_neto REAL GENERATED ALWAYS AS (peso_bruto - tara) STORED,
    estado TEXT DEFAULT 'pendiente',
    observaciones TEXT,
    usuario_registro TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS vendimia_muestras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ingreso_id INTEGER NOT NULL,
    brix REAL,
    ph REAL,
    acidez_total REAL,
    temperatura REAL,
    peso_racimo REAL,
    fecha_muestra TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ingreso_id) REFERENCES vendimia_ingresos(id)
);

CREATE TABLE IF NOT EXISTS vendimia_destinos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ingreso_id INTEGER NOT NULL,
    tipo_destino TEXT NOT NULL,
    destino TEXT NOT NULL,
    fecha_asignacion TEXT DEFAULT CURRENT_TIMESTAMP,
    usuario_asigna TEXT NOT NULL,
    FOREIGN KEY (ingreso_id) REFERENCES vendimia_ingresos(id)
);