from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.lang import Builder
from sqlqueries import QueriesSQLite

Builder.load_file('inventarios_y_clientes/inventarios_y_clientes.kv')

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''
    touch_deselect_last = BooleanProperty(True)

class SelectableProductoLabel(RecycleDataViewBehavior, BoxLayout):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    
    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.ids['_Hashtag'].text = str(1+index)
        self.ids['_Codigo'].text = data['Codigo']
        self.ids['_Nombre'].text = data['Nombre'].title()
        self.ids['_Proveedor'].text = data['Proveedor']
        self.ids['_Cantidad'].text = str(data['Cantidad'])
        self.ids['_Precio'].text = str("{:.2f}".format(data['Precio']))
        return super(SelectableProductoLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableProductoLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            rv.data[index]['Seleccionado'] = True
        else:
            rv.data[index]['Seleccionado'] = False

class SelectableClienteLabel(RecycleDataViewBehavior, BoxLayout):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    
    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.ids['_Hashtag'].text = str(1+index)
        self.ids['_Codigo'].text = data['Codigo']
        self.ids['_Nombre'].text = data['Nombre'].title()
        self.ids['_Direccion'].text = data['Direccion']
        self.ids['_Tipo'].text = data['Tipo']
        return super(SelectableClienteLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableClienteLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            rv.data[index]['Seleccionado'] = True
        else:
            rv.data[index]['Seleccionado'] = False

class InventariosYClientesRV(RecycleView):
    def __init__(self, **kwargs):
        super(InventariosYClientesRV, self).__init__(**kwargs)
        self.data = []
    
    def agregar_datos(self, datos):
        for dato in datos:
            dato['Seleccionado'] = False
            self.data.append(dato)
        self.refresh_from_data()
        
    def dato_seleccionado(self):
        indice = -1
        for i in range(len(self.data)):
            if self.data[i]['Seleccionado']:
                indice = i
                break
        return indice

class ProductoPopup(Popup):
    def __init__(self, agregar_callback, **kwargs):
        super(ProductoPopup, self).__init__(**kwargs)
        self.agregar_callback = agregar_callback
    
    def abrir(self, agregar, producto = None):
        if agregar:
            self.ids.Producto_Info_1.text = 'Agregar producto nuevo'
            self.ids.Producto_Codigo.disabled = False
        else:
            self.ids.Producto_Info_1.text = 'Agregar producto nuevo'
            self.ids.Producto_Codigo.text = producto['Codigo']
            self.ids.Producto_Codigo.text = True
            self.ids.Producto_Nombre.text = producto['Nombre']
            self.ids.Producto_Proveedor.text = producto['Proveedor']
            self.ids.Producto_Cantidad.text = str(producto['Cantidad'])
            self.ids.Producto_Precio.text = str(producto['Precio'])
        self.open()
        
    def verificar(self, Producto_Codigo, Producto_Nombre, Producto_Proveedor, Producto_Cantidad, Producto_Precio):
        alerta_1 = 'Falta: '
        alerta_2 = ''
        validado = {}
        if not Producto_Codigo:
            alerta_1 += 'Codigo '
            validado['Codigo'] = False
        else:
            try:
                numeric = str(Producto_Codigo)
                validado['Codigo'] = Producto_Codigo
            except:
                alerta_2 += 'Codigo no valido'
                validado['Codigo'] = False
                
        if not Producto_Nombre:
            alerta_1 += 'Nombre '
            validado['Nombre'] = False
        else:
            validado['Nombre'] = Producto_Nombre.title()
        
        if not Producto_Proveedor:
            alerta_1 += 'Proveedor '
            validado['Proveedor'] = False
        else:
            validado['Proveedor'] = Producto_Proveedor.title()
        
        if not Producto_Cantidad:
            alerta_1 += 'Cantidad '
            validado['Cantidad'] = False
        else:
            try:
                numeric = int(Producto_Cantidad)
                validado['Cantidad'] = Producto_Cantidad
            except:
                alerta_2 += 'Cantidad no valida'
                validado['Cantidad'] = False
                
        if not Producto_Precio:
            alerta_1 += 'Precio '
            validado['Precio'] = False
        else:
            try:
                numeric = float(Producto_Precio)
                validado['Precio'] = Producto_Precio
            except:
                alerta_2 += ' Precio no valido'
                validado['Precio'] = False
                
        valores = list(validado.values())
        
        if False in valores:
            self.ids.No_Valido_Notificacion.text = alerta_1 + alerta_2
        else:
            self.ids.No_Valido_Notificacion.text = 'Validado'
            validado['Cantidad'] = int(validado['Cantidad'])
            validado['Precio'] = float(validado['Precio'])
            print(type(validado['Precio']))
            self.agregar_callback(True, validado)
            self.dismiss()
        
class VistaProductos(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.cargar_productos, 1)
        
    def cargar_productos(self, *args):
        _productos = []
        connection = QueriesSQLite.create_connection("Sistema_Transaccional_de_Ventas_DB.sqlite")
        inventario_sql = QueriesSQLite.execute_read_query(connection, "SELECT * from productos")
        for producto in inventario_sql:
            _productos.append({'Codigo': producto[0], 'Nombre': producto[1], 'Precio': producto[2], 'Cantidad': producto[3], 'Proveedor': producto[4]})
        self.ids.RV_Productos.agregar_datos(_productos)
    
    def agregar_producto(self, agregar = False, validado = None):
        if agregar:
            producto_tuple = tuple(validado.values())
            connection = QueriesSQLite.create_connection("Sistema_Transaccional_de_Ventas_DB.sqlite")
            crear_producto = """
            INSERT INTO
                productos (Codigo, Nombre, Precio, Cantidad, Proveedor)
            VALUES
                (?, ?, ?, ?, ?);
            """
            QueriesSQLite.execute_query(connection, crear_producto, producto_tuple)
            self.ids.RV_Productos.data.append(validado)
            self.ids.RV_Productos.refresh_from_data()
        else:
            popup = ProductoPopup(self.agregar_producto)
            popup.abrir(True)
        
    def modificar_producto(self):
        print("Modificar producto")

    def eliminar_producto(self):
        print("Eliminar producto")

class VistaClientes(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.cargar_clientes, 1)
        
    def cargar_clientes(self, *args):
        _clientes = []
        connection = QueriesSQLite.create_connection("Sistema_Transaccional_de_Ventas_DB.sqlite")
        clientes_sql = QueriesSQLite.execute_read_query(connection, "SELECT * from clientes")
        for cliente in clientes_sql:
            _clientes.append({'Codigo': cliente[0], 'Nombre': cliente[1], 'Direccion': cliente[2], 'Tipo': cliente[3]})
        self.ids.RV_Clientes.agregar_datos(_clientes)

    def agregar_cliente(self):
        print("Agregar cliente")

    def modificar_cliente(self):
        print("Modificar cliente")

    def eliminar_cliente(self):
        print("Eliminar cliente")

class InventariosYClientesWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(*kwargs)
        self.vista_actual = "Productos"
        self.Vista_Manager = self.ids.Vista_Manager
        
    def cambiar_vista(self):
        if self.vista_actual == "Productos":
            self.vista_actual = "Clientes"
        else:
            self.vista_actual = "Productos"
        self.Vista_Manager.current = self.vista_actual

    def inventarios_y_clientes(self):
        self.parent.parent.current = 'Scrn_Inventarios_Y_Clientes'

    def ventas(self):
        self.parent.parent.current = 'Scrn_Ventas'

        
class InventariosYClientesApp(App):
    def build(self):
        return InventariosYClientesWindow()
    
if __name__ == "__main__":
    InventariosYClientesApp().run()