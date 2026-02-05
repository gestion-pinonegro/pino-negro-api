import sqlite3

DB_PATH = "bodega.db"

class VendimiaService:

    # -------------------------
    # CREAR INGRESO DE UVA
    # -------------------------
    def crear_ingreso(self, fecha_ingreso, productor, finca, cuartel, variedad,
                      peso_bruto, tara, observaciones, usuario_registro):

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        query = """
            INSERT INTO vendimia_ingresos
            (fecha_ingreso, productor, finca, cuartel, variedad,
             peso_bruto, tara, estado, observaciones, usuario_registro)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'pendiente', ?, ?)
        """

        cursor.execute(query, (
            fecha_ingreso,
            productor,
            finca,
            cuartel,
            variedad,
            peso_bruto,
            tara,
            observaciones,
            usuario_registro
        ))

        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    # -------------------------
    # LISTAR INGRESOS
    # -------------------------
    def listar_ingresos(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM vendimia_ingresos ORDER BY fecha_ingreso DESC")
        rows = cursor.fetchall()

        conn.close()
        return rows

    # -------------------------
    # OBTENER INGRESO POR ID
    # -------------------------
    def obtener_ingreso(self, ingreso_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM vendimia_ingresos WHERE id = ?", (ingreso_id,))
        row = cursor.fetchone()

        conn.close()
        return row

    # -------------------------
    # REGISTRAR MUESTRA
    # -------------------------
    def registrar_muestra(self, ingreso_id, brix, ph, acidez_total, temperatura, peso_racimo):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        query = """
            INSERT INTO vendimia_muestras
            (ingreso_id, brix, ph, acidez_total, temperatura, peso_racimo)
            VALUES (?, ?, ?, ?, ?, ?)
        """

        cursor.execute(query, (
            ingreso_id,
            brix,
            ph,
            acidez_total,
            temperatura,
            peso_racimo
        ))

        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id
        # -------------------------
    # ASIGNAR DESTINO
    # -------------------------
    def asignar_destino(self, ingreso_id, tipo_destino, destino, usuario_asigna):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        query = """
            INSERT INTO vendimia_destinos
            (ingreso_id, tipo_destino, destino, usuario_asigna)
            VALUES (?, ?, ?, ?)
        """

        cursor.execute(query, (
            ingreso_id,
            tipo_destino,
            destino,
            usuario_asigna
        ))

        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id
        # -------------------------
    # LISTAR MUESTRAS POR INGRESO
    # -------------------------
    def listar_muestras_por_ingreso(self, ingreso_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        query = """
            SELECT id, ingreso_id, brix, ph, acidez_total, temperatura, peso_racimo, fecha_muestra
            FROM vendimia_muestras
            WHERE ingreso_id = ?
            ORDER BY fecha_muestra DESC
        """

        cursor.execute(query, (ingreso_id,))
        rows = cursor.fetchall()

        conn.close()
        return rows
    
     # -------------------------
    # EDITAR MUESTRA
    # -------------------------
    def editar_muestra(self, muestra_id, brix, ph, acidez_total, temperatura, peso_racimo):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        query = """
            UPDATE vendimia_muestras
            SET brix = ?, ph = ?, acidez_total = ?, temperatura = ?, peso_racimo = ?
            WHERE id = ?
        """

        cursor.execute(query, (
            brix,
            ph,
            acidez_total,
            temperatura,
            peso_racimo,
            muestra_id
        ))

        conn.commit()
        updated = cursor.rowcount
        conn.close()
        return updated > 0
    
        # -------------------------
    # BORRAR MUESTRA
    # -------------------------
    def borrar_muestra(self, muestra_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        query = "DELETE FROM vendimia_muestras WHERE id = ?"

        cursor.execute(query, (muestra_id,))

        conn.commit()
        deleted = cursor.rowcount
        conn.close()
        return deleted > 0
    
    # -------------------------
    # DASHBOARD VENDIMIA
    # -------------------------
    def kilos_totales(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT SUM(peso_neto) FROM vendimia_ingresos")
        total = cursor.fetchone()[0]

        conn.close()
        return total or 0
    
    def kilos_por_variedad(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT variedad, SUM(peso_neto)
            FROM vendimia_ingresos
            GROUP BY variedad
            ORDER BY SUM(peso_neto) DESC
        """)

        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def kilos_por_productor(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT productor, SUM(peso_neto)
            FROM vendimia_ingresos
            GROUP BY productor
            ORDER BY SUM(peso_neto) DESC
        """)

        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def ingresos_por_dia(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT DATE(fecha_ingreso), SUM(peso_neto)
            FROM vendimia_ingresos
            GROUP BY DATE(fecha_ingreso)
            ORDER BY DATE(fecha_ingreso)
        """)

        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def cantidad_muestras(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM vendimia_muestras")
        total = cursor.fetchone()[0]

        conn.close()
        return total
    
    def destinos_resumen(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT tipo_destino, COUNT(*)
            FROM vendimia_destinos
            GROUP BY tipo_destino
        """)

        rows = cursor.fetchall()
        conn.close()
        return rows