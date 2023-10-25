from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from sqlqueries import QueriesSQLite

# if __name__ == "__main__":
#     connection = QueriesSQLite.create_connection("Sistema_Transaccional_de_Ventas_DB.sqlite")
    
#     seleccionar_ventas = "SELECT * from ventas"
#     ventas = QueriesSQLite.execute_read_query(connection, seleccionar_ventas)
#     for venta in ventas:
#         print(venta)
        
#     venta_dict = {'Codigo_del_cliente': 'R99','Codigo_del_producto': '999','Precio': 60.0,'Cantidad': 10,'Total': 600.00}
#     venta_tuple = tuple(venta_dict.values())
#     crear_venta = """
#     INSERT INTO
#         ventas (Codigo_del_cliente, Codigo_del_producto, Precio, Cantidad, Total)
#     VALUES
#         (?,?,?,?,?);
#     """
#     QueriesSQLite.execute_query(connection, crear_venta, venta_tuple)
    
#     seleccionar_ventas = "SELECT * from ventas"
#     ventas = QueriesSQLite.execute_read_query(connection, seleccionar_ventas)
#     for venta in ventas:
#         print(venta)

from inicio.inicio import InicioWindow
from inventarios_y_clientes.inventarios_y_clientes import InventariosYClientesWindow
from ventas.ventas import VentasWindow

class MainWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(*kwargs)
        self.ventas_widget = VentasWindow()
        self.inicio_widget = InicioWindow()
        self.inventarios_y_clientes_widget = InventariosYClientesWindow()
        self.ids.Scrn_Inicio.add_widget(self.inicio_widget)
        self.ids.Scrn_Ventas.add_widget(self.ventas_widget)
        self.ids.Scrn_Inventarios_Y_Clientes.add_widget(self.inventarios_y_clientes_widget)
        
class MainApp(App):
    def build(self):
        return MainWindow()
    
if __name__ == "__main__":
    MainApp().run()