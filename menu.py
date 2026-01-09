# menu.py

from trazabilidad_service import TrazabilidadService
from inventario_service import InventarioService
from blend_service import BlendService
from finanzas_service import FinanzasService

class MenuApp:

    def __init__(self):
        self.traz = TrazabilidadService()
        self.inv = InventarioService()
        self.blend = BlendService()
        self.fin = FinanzasService()

    def mostrar_menu(self):
        print("\n=== SISTEMA DE GESTIÓN DE BODEGA ===")
        print("1. Trazabilidad")
        print("2. Inventario")
        print("3. Blends")
        print("4. Finanzas")
        print("5. Salir\n")

    def ejecutar(self):
        while True:
            self.mostrar_menu()
            opcion = input("Elegí una opción: ")

            if opcion == "1":
                self.menu_trazabilidad()
            elif opcion == "2":
                self.menu_inventario()
            elif opcion == "3":
                self.menu_blend()
            elif opcion == "4":
                self.menu_finanzas()
            elif opcion == "5":
                print("Saliendo del sistema...")
                break
            else:
                print("Opción inválida.\n")

    # -------------------------
    # SUBMENÚS
    # -------------------------

    def menu_trazabilidad(self):
        print("\n--- TRAZABILIDAD ---")
        fecha = input("Fecha (YYYY-MM-DD): ")
        lote = input("Lote: ")
        tarea = input("Tarea: ")
        volumen = float(input("Volumen: "))
        notas = input("Notas: ")

        self.traz.registrar_trabajo(fecha, lote, tarea, volumen, notas)
        print("Trabajo registrado!\n")

    def menu_inventario(self):
        print("\n--- INVENTARIO ---")
        print("1. Crear item")
        print("2. Registrar movimiento")
        print("3. Ver items")
        print("4. Volver\n")

        op = input("Elegí una opción: ")

        if op == "1":
            nombre = input("Nombre del item: ")
            unidad = input("Unidad: ")
            stock = float(input("Stock inicial: "))
            self.inv.crear_item(nombre, unidad, stock)
            print("Item creado!\n")

        elif op == "2":
            item_id = int(input("ID del item: "))
            tipo = input("Tipo (ingreso/egreso): ")
            cantidad = float(input("Cantidad: "))
            fecha = input("Fecha: ")
            self.inv.registrar_movimiento(item_id, tipo, cantidad, fecha)
            print("Movimiento registrado!\n")

        elif op == "3":
            print("\nItems:")
            for item in self.inv.listar_items():
                print(item)
            print()

    def menu_blend(self):
        print("\n--- BLENDS ---")
        print("1. Crear blend")
        print("2. Agregar componente")
        print("3. Ver blends")
        print("4. Volver\n")

        op = input("Elegí una opción: ")

        if op == "1":
            nombre = input("Nombre del blend: ")
            fecha = input("Fecha: ")
            self.blend.crear_blend(nombre, fecha)
            print("Blend creado!\n")

        elif op == "2":
            blend_id = int(input("ID del blend: "))
            varietal = input("Varietal: ")
            volumen = float(input("Volumen: "))
            self.blend.agregar_componente(blend_id, varietal, volumen)
            print("Componente agregado!\n")

        elif op == "3":
            print("\nBlends:")
            for b in self.blend.listar_blends():
                print(b)
            print()

    def menu_finanzas(self):
        print("\n--- FINANZAS ---")
        print("1. Registrar ingreso")
        print("2. Registrar egreso")
        print("3. Ver ingresos")
        print("4. Ver egresos")
        print("5. Ver balance")
        print("6. Volver\n")

        op = input("Elegí una opción: ")

        if op == "1":
            fecha = input("Fecha: ")
            concepto = input("Concepto: ")
            monto = float(input("Monto: "))
            self.fin.registrar_ingreso(fecha, concepto, monto)
            print("Ingreso registrado!\n")

        elif op == "2":
            fecha = input("Fecha: ")
            concepto = input("Concepto: ")
            monto = float(input("Monto: "))
            self.fin.registrar_egreso(fecha, concepto, monto)
            print("Egreso registrado!\n")

        elif op == "3":
            print("\nIngresos:")
            for i in self.fin.listar_ingresos():
                print(i)
            print()

        elif op == "4":
            print("\nEgresos:")
            for e in self.fin.listar_egresos():
                print(e)
            print()

        elif op == "5":
            print("\nBalance total:", self.fin.balance_total(), "\n")