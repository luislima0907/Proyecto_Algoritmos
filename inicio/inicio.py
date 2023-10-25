from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from sqlqueries import QueriesSQLite

Builder.load_file('inicio/inicio.kv')

class InicioWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(*kwargs)

    def verificar_cliente(self, codigo, nombre):
        connection = QueriesSQLite.create_connection("Sistema_Transaccional_de_Ventas_DB.sqlite")
        users = QueriesSQLite.execute_read_query(connection, "SELECT * from clientes")
        if codigo == '' or nombre == '':
            self.ids.Inicio_Notificacion.text='Falta tipo de cliente y/o nombre'
        else:
            usuario = {}
            for user in users:
                if user[0] == codigo:
                    usuario['Nombre']=user[1]
                    usuario['Codigo']=user[0]
                    usuario['Direccion']=user[2]
                    usuario['Tipo'] = user[3]
                    break
            if usuario:
                if usuario['Nombre'] == nombre:
                    self.ids.Codigo.text = ''
                    self.ids.Nombre.text = ''
                    self.ids.Inicio_Notificacion.text=''
                    self.parent.parent.current='Scrn_Ventas'
                    #self.poner_cliente(usuario)
                else:
                    self.ids.Inicio_Notificacion.text='Tipo o nombre incorrecto'
            else:
                self.ids.Inicio_Notificacion.text='Tipo o nombre incorrecto'

        
    # def inventarios_y_clientes(self):
    #     self.parent.parent.current = 'Scrn_Inventarios_Y_Clientes'

    # def ventas(self):
    #     self.parent.parent.current = 'Scrn_Ventas'

        
class InicioApp(App):
    def build(self):
        return InicioWindow()
    
if __name__ == "__main__":
    InicioApp().run()