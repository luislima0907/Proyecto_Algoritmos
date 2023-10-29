from .conexion_db import ConexionDB
from tkinter import messagebox


def crear_tabla():
    conexion = ConexionDB()

    sql = """
    CREATE TABLE inventarios (
        codigo_inventario INTEGER,
        nombre VARCHAR(100),
        existencia INTEGER,
        proveedor VARCHAR(100),
        precio INTEGER,
        PRIMARY KEY(codigo_inventario AUTOINCREMENT)
        )"""
    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()
        titulo = "Crear Registro"
        mensaje = "Se creo la tabla en la base de datos"
        messagebox.showinfo(titulo, mensaje)
    except:
        titulo = "Crear Registro"
        mensaje = "La tabla ya ha sido creada"
        messagebox.showwarning(titulo, mensaje)


def borrar_tabla():
    conexion = ConexionDB()

    sql = "DROP TABLE inventarios "
    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()
        titulo = "Borrar Registro"
        mensaje = "La tabla se elimino exitosamente"
        messagebox.showinfo(titulo, mensaje)
    except:
        titulo = "Borrar Registro"
        mensaje = "No existe tabla para borrar"
        messagebox.showerror(titulo, mensaje)


class Inventario:
    def __init__(self, nombre, existencia, proveedor, precio):
        self.codigo_inventario = None
        self.nombre = nombre
        self.existencia = existencia
        self.proveedor = proveedor
        self.precio = precio

    def __str__(self):
        return f"inventario[{self.nombre}, {self.existencia}, {self.proveedor}, {self.precio}]"


def listar():
    conexion = ConexionDB()

    lista_inventarios = []
    sql = "SELECT * FROM inventarios"

    try:
        conexion.cursor.execute(sql)
        lista_inventarios = conexion.cursor.fetchall()
        conexion.cerrar()
    except:
        titulo = "Aaaaaa"
        mensaje = "Eeeee"
        messagebox.showwarning(titulo, mensaje)
    return lista_inventarios


def guardar(inventario):
    conexion = ConexionDB()

    sql = f"""INSERT INTO inventarios (nombre, existencia, proveedor, precio)
    VALUES ('{inventario.nombre}', '{inventario.existencia}', '{inventario.proveedor}', '{inventario.precio}')"""

    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()
    except:
        titulo = "Conexion al registro"
        mensaje = "La tabla no esta creada en la base de datos"
        messagebox.showerror(titulo, mensaje)


def editar(inventario, codigo_inventario):
    conexion = ConexionDB()

    sql = f"""UPDATE inventarios SET
    nombre = '{inventario.nombre}', existencia = '{inventario.existencia}',
    proveedor = '{inventario.proveedor}', precio = '{inventario.precio}'
    WHERE codigo_inventario = {codigo_inventario}"""

    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()

    except:
        titulo = "AAAAAAA"
        mensaje = "EEEEEEE"
        messagebox.showerror(titulo, mensaje)


def eliminar(codigo_inventario):
    conexion = ConexionDB()
    sql = f'DELETE FROM inventarios WHERE codigo_inventario = {codigo_inventario}'

    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()
    except:
        titulo = 'Eliminar Datos'
        mensaje = 'No se pudo eliminar el registro'
        messagebox.showerror(titulo, mensaje)
