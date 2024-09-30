import sqlite3
import datetime

conn = sqlite3.connect("ferreteria.db")
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS Producto(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    codigo TEXT UNIQUE,
    cantidad INTEGER,
    precio_compra REAL,
    precio_venta REAL,
    proveedor TEXT
)
""")
conn.commit()

class Producto:
    def _init_(self, nombre, codigo, precio_compra, precio_venta, cantidad, proveedor):
        self.nombre = nombre
        self.codigo = codigo
        self.precio_compra = precio_compra
        self.precio_venta = precio_venta
        self.cantidad = cantidad
        self.proveedor = proveedor

class Ferreteria:
    def _init_(self):
        self.ventas = []

    def agregar_producto(self, producto):
        cursor.execute("""INSERT INTO Producto (nombre, codigo, cantidad, precio_compra, precio_venta, proveedor) VALUES (?, ?, ?, ?, ?, ?)""", (producto.nombre, producto.codigo, producto.cantidad, producto.precio_compra, producto.precio_venta, producto.proveedor))
        conn.commit()

    def buscar_producto(self, codigo):
        cursor.execute("SELECT * FROM Producto WHERE codigo = ?", (codigo,))
        row = cursor.fetchone()
        if row:
            return Producto(row[1], row[2], row[4], row[5], row[3], row[6])
        return None

    def vender_producto(self, codigo, cantidad):
        producto = self.buscar_producto(codigo)
        if producto and producto.cantidad >= cantidad:
            # Actualizar el stock en la base de datos
            nuevo_stock = producto.cantidad - cantidad
            cursor.execute(""" UPDATE Producto SET cantidad = ? WHERE codigo = ? """, (nuevo_stock, codigo))
            conn.commit()
            
            # Registrar la venta
            venta = {
                "producto": producto,
                "cantidad": cantidad,
                "fecha": datetime.datetime.now()
            }
            self.ventas.append(venta)
            print(f"Se vendieron {cantidad} unidades de {producto.nombre}")
        else:
            print("Producto no encontrado o stock insuficiente")

    def generar_reporte_ventas(self):
        if not self.ventas:
            print("No se han realizado ventas.")
            return
        
        for venta in self.ventas:
            print(f"Fecha: {venta['fecha']}")
            print(f"Producto: {venta['producto'].nombre}")
            print(f"Cantidad: {venta['cantidad']}")
            print(f"Precio unitario: ${venta['producto'].precio_venta}")
            print("-" * 20)

def menu():
    ferreteria = Ferreteria()

    while True:
        print("1. Añadir producto")
        print("2. Eliminar producto")
        print("3. Leer productos")
        print("4. Vender producto")
        print("5. Generar reporte de ventas")
        print("6. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            nombre = input("Nombre del producto: ")
            codigo = input("Código del producto: ")
            precio_compra = float(input("Precio de compra: "))
            precio_venta = float(input("Precio de venta: "))
            cantidad = int(input("Cantidad en stock: "))
            proveedor = input("Proveedor: ")
            producto = Producto(nombre, codigo, precio_compra, precio_venta, cantidad, proveedor)
            ferreteria.agregar_producto(producto)
            print(f"Producto {nombre} añadido.")

        elif opcion == "2":
            codigo = input("Código del producto a eliminar: ")
            cursor.execute("DELETE FROM Producto WHERE codigo = ?", (codigo,))
            conn.commit()
            print(f"Producto con código {codigo} eliminado.")

        elif opcion == "3":
            print("Productos en inventario:")
            cursor.execute("SELECT * FROM Producto")
            for row in cursor.fetchall():
                print(f"Código: {row[2]}, Nombre: {row[1]}, Cantidad: {row[3]}, Precio de compra: {row[4]}, Precio de venta: {row[5]}, Proveedor: {row[6]}")

        elif opcion == "4":
            codigo = input("Código del producto a vender: ")
            cantidad = int(input("Cantidad a vender: "))
            ferreteria.vender_producto(codigo, cantidad)

        elif opcion == "5":
            ferreteria.generar_reporte_ventas()

        elif opcion == "6":
            print("Saliendo...")
            break

        else:
            print("Opción no válida. Inténtalo de nuevo.")

menu()
conn.close()