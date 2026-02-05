# finanzas_service.py

from database import run_query, fetch_all

class FinanzasService:

    def registrar_ingreso(self, fecha, concepto, monto):
        run_query(
            "INSERT INTO finanzas_ingresos (fecha, concepto, monto) VALUES (?, ?, ?)",
            (fecha, concepto, monto)
        )

    def registrar_egreso(self, fecha, concepto, monto):
        run_query(
            "INSERT INTO finanzas_egresos (fecha, concepto, monto) VALUES (?, ?, ?)",
            (fecha, concepto, monto)
        )

    def listar_ingresos(self):
        return fetch_all("SELECT * FROM finanzas_ingresos")

    def listar_egresos(self):
        return fetch_all("SELECT * FROM finanzas_egresos")

    def balance_total(self):
        ingresos = fetch_all("SELECT SUM(monto) FROM finanzas_ingresos")[0][0] or 0
        egresos = fetch_all("SELECT SUM(monto) FROM finanzas_egresos")[0][0] or 0
        return ingresos - egresos

    def movimientos_por_fecha(self, fecha):
        ingresos = fetch_all(
            "SELECT fecha, concepto, monto FROM finanzas_ingresos WHERE fecha = ?",
            (fecha,)
        )
        egresos = fetch_all(
            "SELECT fecha, concepto, monto FROM finanzas_egresos WHERE fecha = ?",
            (fecha,)
        )
        return ingresos, egresos