from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from sqlqueries import QueriesSQLite
from clientes.clientes import ClientesWindow
from administrador.administrador import AdministradorWindow
from ventas.ventas import VentasWindow

class MainWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.clientes_widget = ClientesWindow()
        self.ventas_widget = VentasWindow()
        self.administrador_widget = AdministradorWindow()
        self.ids.Scrn_Clientes.add_widget(self.clientes_widget)
        self.ids.Scrn_Ventas.add_widget(self.ventas_widget)
        self.ids.Scrn_Administrador.add_widget(self.administrador_widget)
        
class MainApp(App):
    def build(self):
        return MainWindow()
    
if __name__ == "__main__":
    MainApp().run()