# trazabilidad_service.py

from database import run_query, fetch_all

class TrazabilidadService:

    def registrar_trabajo(self, fecha, lote, tarea, volumen, notas=None):
        run_query(
            "INSERT INTO trabajos (fecha, lote, tarea, volumen, notas) VALUES (?, ?, ?, ?, ?)",
            (fecha, lote, tarea, volumen, notas)
        )

    def listar_trabajos(self):
        return fetch_all("SELECT * FROM trabajos")

    def buscar_por_lote(self, lote):
        return fetch_all(
            "SELECT * FROM trabajos WHERE lote = ?",
            (lote,)
        )