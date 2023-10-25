import sqlite3
from sqlite3 import Error

class QueriesSQLite:
    def create_connection(path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

        return connection

    def execute_query(connection, query, data_tuple):
        cursor = connection.cursor()
        try:
            cursor.execute(query, data_tuple)
            connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    def execute_read_query(connection, query):
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")



if __name__=="__main__":
    connection = QueriesSQLite.create_connection("Sistema_Transaccional_de_Ventas_DB.sqlite")
    
    # crear_tabla_de_venta = """
    # CREATE TABLE IF NOT EXISTS ventas(
    #  Codigo_del_cliente TEXT PRIMARY KEY, 
    #  Codigo_del_producto TEXT NOT NULL, 
    #  Precio REAL NOT NULL, 
    #  Cantidad INTEGER NOT NULL,
    #  Total REAL NOT NULL
    # );
    # """
    # QueriesSQLite.execute_query(connection, crear_tabla_de_venta, tuple()) 

    # crear_tabla_de_producto = """
    # CREATE TABLE IF NOT EXISTS productos(
    #  Codigo TEXT PRIMARY KEY, 
    #  Nombre TEXT NOT NULL, 
    #  Precio REAL NOT NULL, 
    #  Cantidad INTEGER NOT NULL,
    #  Proveedor TEXT NOT NULL
    # );
    # """
    # QueriesSQLite.execute_query(connection, crear_tabla_de_producto, tuple()) 

    # crear_tabla_de_cliente = """
    # CREATE TABLE IF NOT EXISTS clientes(
    #  Codigo TEXT PRIMARY KEY, 
    #  Nombre TEXT NOT NULL, 
    #  Direccion TEXT NOT NULL,
    #  Tipo TEXT NOT NULL
    # );
    # """
    # QueriesSQLite.execute_query(connection, crear_tabla_de_cliente, tuple()) 

    # crear_tabla_de_venta = """
    # INSERT INTO
    #   ventas (Codigo_del_cliente, Codigo_del_producto, Precio, Cantidad, Total)
    # VALUES
    #     ('G11', '111', 20.0, 20, 400.00),
    #     ('D22', '222', 50.5, 15, 757.50), 
    #     ('S33', '333', 25.0, 10, 250.00),
    #     ('F44', '444', 80.0, 20, 1600.00),
    #     ('H55', '555', 750.0, 5, 3750.00),
    #     ('T66', '666', 100.0, 25, 2500.00),
    #     ('U77', '777', 35.5, 30, 1065.00),
    #     ('W88', '888', 65.0, 5, 325.00)
    # """
    # QueriesSQLite.execute_query(connection, crear_tabla_de_venta, tuple()) 

    # crear_tabla_de_producto = """
    # INSERT INTO
    #   productos (Codigo, Nombre, Precio, Cantidad, Proveedor)
    # VALUES
    #     ('111', 'leche 1l', 20.0, 20, 'S.A'),
    #     ('222', 'cereal 500g', 50.5, 15, 'S.E'), 
    #     ('333', 'yogurt 1L', 25.0, 10, 'S.C'),
    #     ('444', 'helado 2L', 80.0, 20, 'S.U'),
    #     ('555', 'alimento para perro 20kg', 750.0, 5, 'S.P'),
    #     ('666', 'shampoo', 100.0, 25, 'S.O'),
    #     ('777', 'papel higiénico 4 rollos', 35.5, 30, 'S.Y'),
    #     ('888', 'jabón para trastes', 65.0, 5, 'S.L')
    # """
    # QueriesSQLite.execute_query(connection, crear_tabla_de_producto, tuple()) 

    # seleccionar_ventas = "SELECT * from ventas"
    # ventas = QueriesSQLite.execute_read_query(connection, seleccionar_ventas)
    # for venta in ventas:
    #     print(venta)

    # seleccionar_productos = "SELECT * from productos"
    # productos = QueriesSQLite.execute_read_query(connection, seleccionar_productos)
    # for producto in productos:
    #     print(producto)

    # cliente_tuple=('G90', 'Marvin', 'Jalapa', 'Cliente')
    # crear_cliente = """
    # INSERT INTO
    #   clientes (Codigo, Nombre, Direccion, Tipo)
    # VALUES
    #     (?,?,?,?);
    # """
    # QueriesSQLite.execute_query(connection, crear_cliente, cliente_tuple)
    
    # seleccionar_clientes = "SELECT * from clientes"
    # clientes = QueriesSQLite.execute_read_query(connection, seleccionar_clientes)
    # for cliente in clientes:
    #     print("type:", type(cliente), "cliente:",cliente)    
    
    # nueva_data=('F10', 'Carlos', 'Jalapa', 'Cliente')
    # actualizar = """
    # UPDATE
    #   clientes
    # SET
    #   Codigo=?, Nombre=?, Direccion = ?
    # WHERE
    #   Tipo = ?
    # """
    # QueriesSQLite.execute_query(connection, actualizar, nueva_data)
    
    # seleccionar_clientes = "SELECT * from clientes"
    # clientes = QueriesSQLite.execute_read_query(connection, seleccionar_clientes)
    # for cliente in clientes:
    #     print("type:", type(cliente), "cliente:",cliente)

    # seleccionar_clientes = "SELECT * from clientes"
    # clientes = QueriesSQLite.execute_read_query(connection, seleccionar_clientes)
    # for cliente in clientes:
    #     print("type:", type(cliente), "cliente:",cliente)

    # venta_a_borrar=('G11',)
    # borrar_venta = """DELETE from ventas where Codigo_del_cliente = ?"""
    # QueriesSQLite.execute_query(connection, borrar_venta, venta_a_borrar)

    # producto_a_borrar=('888',)
    # borrar = """DELETE from productos where Codigo = ?"""
    # QueriesSQLite.execute_query(connection, borrar, producto_a_borrar)

    # seleccionar_ventas = "SELECT * from ventas"
    # ventas = QueriesSQLite.execute_read_query(connection, seleccionar_ventas)
    # for venta in ventas:
    #     print(venta)

    # seleccionar_productos = "SELECT * from productos"
    # productos = QueriesSQLite.execute_read_query(connection, seleccionar_productos)
    # for producto in productos:
    #     print(producto)