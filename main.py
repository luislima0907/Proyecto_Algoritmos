from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from sqlqueries import QueriesSQLite
from clientes.clientes import ClientesWindow
from administrador.administrador import AdministradorWindow
from ventas.ventas import VentasWindow

class MainWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Clientes_Widget = ClientesWindow()
        self.Ventas_Widget = VentasWindow()
        self.Administrador_Widget = AdministradorWindow()
        self.ids.Scrn_Clientes.add_Widget(self.Clientes_Widget)
        self.ids.Scrn_Ventas.add_Widget(self.Ventas_Widget)
        self.ids.Scrn_Administrador.add_Widget(self.Administrador_Widget)
        
class MainApp(App):
    def build(self):
        return MainWindow()
    
if __name__ == "__main__":
    MainApp().run()