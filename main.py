from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from sqlqueries import QueriesSQLite

#Esto nos sirvió para insertar los productos por medio de sql lite
# if __name__=="__main__":
#     connection = QueriesSQLite.create_connection("Sistema_Transaccional_de_Ventas_DB.sqlite")

# 	select_products = "SELECT * from productos"
# 	productos = QueriesSQLite.execute_read_query(connection, select_products)
# 	for producto in productos:
# 		print(producto)
    
# 	producto_dict = {'codigo': '999', 'nombre': 'refresco 600ml', 'precio': 15.0, 'cantidad': 10}
# 	producto_tuple = tuple(producto_dict.values())
# 	crear_producto = """
# 	INSERT INTO
# 		productos (codigo, nombre, precio, cantidad)
# 	VALUES
# 		(?,?,?,?);
# 	"""
# 	QueriesSQLite.execute_query(connection, crear_producto, producto_tuple)

# 	select_products = "SELECT * from productos"
# 	productos = QueriesSQLite.execute_read_query(connection, select_products)
# 	for producto in productos:
# 		print(producto)

from signin.signin import SigninWindow
from admin.admin import AdminWindow
from ventas.ventas import VentasWindow

class MainWindow(BoxLayout):
	QueriesSQLite.create_tables()
	def __init__(self, **kwargs):
		super().__init__(*kwargs)
		self.admin_widget=AdminWindow()
		self.ventas_widget=VentasWindow(self.admin_widget.actualizar_productos)
		self.signin_widget=SigninWindow(self.ventas_widget.poner_usuario)
		self.ids.scrn_signin.add_widget(self.signin_widget)
		self.ids.scrn_ventas.add_widget(self.ventas_widget)
		self.ids.scrn_admin.add_widget(self.admin_widget)

class MainApp(App):
	def build(self):
		return MainWindow()

if __name__=="__main__":
	MainApp().run()