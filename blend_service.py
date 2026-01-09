# blend_service.py

from database import run_query, fetch_all

class BlendService:

    def crear_blend(self, nombre, fecha):
        run_query(
            "INSERT INTO blends (nombre, fecha) VALUES (?, ?)",
            (nombre, fecha)
        )

    def agregar_componente(self, blend_id, varietal, volumen):
        run_query(
            "INSERT INTO blend_componentes (blend_id, varietal, volumen) VALUES (?, ?, ?)",
            (blend_id, varietal, volumen)
        )

    def listar_blends(self):
        return fetch_all("SELECT * FROM blends")

    def listar_componentes(self, blend_id):
        return fetch_all(
            "SELECT varietal, volumen FROM blend_componentes WHERE blend_id = ?",
            (blend_id,)
        )

    def composicion_porcentual(self, blend_id):
        componentes = self.listar_componentes(blend_id)
        total = sum([c[1] for c in componentes])

        if total == 0:
            return []

        resultado = []
        for varietal, volumen in componentes:
            porcentaje = (volumen / total) * 100
            resultado.append((varietal, volumen, porcentaje))

        return resultado