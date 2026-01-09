# inventario_service.py

from database import run_query, fetch_all

class InventarioService:

    def crear_item(self, nombre, unidad, stock_inicial=0):
        run_query(
            "INSERT INTO inventario_items (nombre, unidad, stock) VALUES (?, ?, ?)",
            (nombre, unidad, stock_inicial)
        )

    def listar_items(self):
        return fetch_all("SELECT * FROM inventario_items")

    def registrar_movimiento(self, item_id, tipo, cantidad, fecha):
        # Registrar movimiento
        run_query(
            "INSERT INTO inventario_movimientos (fecha, item_id, tipo, cantidad) VALUES (?, ?, ?, ?)",
            (fecha, item_id, tipo, cantidad)
        )

        # Actualizar stock
        if tipo == "ingreso":
            run_query(
                "UPDATE inventario_items SET stock = stock + ? WHERE id = ?",
                (cantidad, item_id)
            )
        elif tipo == "egreso":
            run_query(
                "UPDATE inventario_items SET stock = stock - ? WHERE id = ?",
                (cantidad, item_id)
            )

    def movimientos_de_item(self, item_id):
        return fetch_all(
            "SELECT fecha, tipo, cantidad FROM inventario_movimientos WHERE item_id = ?",
            (item_id,)
        )

    def stock_de_item(self, item_id):
        result = fetch_all(
            "SELECT nombre, stock, unidad FROM inventario_items WHERE id = ?",
            (item_id,)
        )
        return result[0] if result else None