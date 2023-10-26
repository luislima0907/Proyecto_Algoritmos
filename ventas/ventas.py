from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.popup import Popup
from kivy.clock import Clock
from datetime import datetime, timedelta
import sqlite3
from kivy.lang import Builder

Builder.load_file('ventas/ventas.kv')

from datetime import datetime, timedelta
from sqlqueries import QueriesSQLite

con = sqlite3.connect("Sistema_Transaccional_de_Ventas_DB.sqlite")
cur = con.cursor()

for row in cur.execute('SELECT Codigo FROM clientes'):
    print(row)
    
con.close()

inventario = [
    {'Codigo_del_cliente': 'G11', 'Codigo_del_producto': '111', 'Precio': 20.0, 'Cantidad': 20, 'Total': 400.00},
    {'Codigo_del_cliente': 'D22', 'Codigo_del_producto': '222','Precio': 50.5, 'Cantidad': 15, 'Total': 757.50}, 
    {'Codigo_del_cliente': 'S33', 'Codigo_del_producto': '333','Precio': 25.0, 'Cantidad': 10, 'Total': 250.00},
    {'Codigo_del_cliente': 'F44', 'Codigo_del_producto': '444','Precio': 80.0, 'Cantidad': 20, 'Total': 1600.00},
    {'Codigo_del_cliente': 'H55', 'Codigo_del_producto': '555','Precio': 750.0, 'Cantidad': 5, 'Total': 3750.00},
    {'Codigo_del_cliente': 'T66', 'Codigo_del_producto': '666','Precio': 100.0, 'Cantidad': 25, 'Total': 2500.00},
    {'Codigo_del_cliente': 'U77', 'Codigo_del_producto': '777','Precio': 35.5, 'Cantidad': 30, 'Total': 1065.00},
    {'Codigo_del_cliente': 'W88', 'Codigo_del_producto': '888','Precio': 65.0, 'Cantidad': 5, 'Total': 325.00}
]

#print(inventario_sql.get(0))

# inventario=[
# 	{'Nombre_del_cliente': 'Luis', 'Codigo_del_cliente': 'G10', 'Codigo_del_producto': '111', 'Nombre_del_producto': 'leche 1L', 'Precio': 20.0, 'Cantidad': 20},
# 	{'Nombre_del_cliente': 'Marvin', 'Codigo_del_cliente': 'D30', 'Codigo_del_producto': '222', 'Nombre_del_producto': 'cereal 500g', 'Precio': 50.5, 'Cantidad': 15}, 
# 	{'Nombre_del_cliente': 'Jose', 'Codigo_del_cliente': 'P90', 'Codigo_del_producto': '333', 'Nombre_del_producto': 'yogurt 1L', 'Precio': 25.0, 'Cantidad': 10},
# 	{'Nombre_del_cliente': 'Danilo', 'Codigo_del_cliente': 'T80', 'Codigo_del_producto': '444', 'Nombre_del_producto': 'helado 2L', 'Precio': 80.0, 'Cantidad': 20},
# 	{'Nombre_del_cliente': 'Jaminton', 'Codigo_del_cliente': 'Y70', 'Codigo_del_producto': '555', 'Nombre_del_producto': 'alimento para perro 20kg', 'Precio': 750.0, 'Cantidad': 5},
# 	{'Nombre_del_cliente': 'Fabian', 'Codigo_del_cliente': 'U20', 'Codigo_del_producto': '666', 'Nombre_del_producto': 'shampoo', 'Precio': 100.0, 'Cantidad': 25},
# 	{'Nombre_del_cliente': 'Marco', 'Codigo_del_cliente': 'R40', 'Codigo_del_producto': '777', 'Nombre_del_producto': 'papel higiénico 4 rollos', 'Precio': 35.5, 'Cantidad': 30},
# 	{'Nombre_del_cliente': 'Yeferson', 'Codigo_del_cliente': 'H00', 'Codigo_del_producto': '888', 'Nombre_del_producto': 'jabón para trastes', 'Precio': 65.0, 'Cantidad': 5},
# 	{'Nombre_del_cliente': 'Kevin', 'Codigo_del_cliente': 'G60', 'Codigo_del_producto': '999', 'Nombre_del_producto': 'refresco 600ml', 'Precio': 15.0, 'Cantidad': 10}
# ]

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''
    touch_deselect_last = BooleanProperty(True)


class SelectableBoxLayout(RecycleDataViewBehavior, BoxLayout):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.ids['_Hashtag'].text = str(1+index)
        self.ids['_Codigo_Cliente'].text = data['Codigo_del_cliente']
        self.ids['_Codigo_Producto'].text = data['Codigo_del_producto']
        self.ids['_Cantidad'].text = str(data['cantidad_carrito'])
        self.ids['_Precio_por_Producto'].text = str("{:.2f}".format(data['Precio']))
        self.ids['_Precio'].text = str("{:.2f}".format(data['precio_total']))
        return super(SelectableBoxLayout, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableBoxLayout, self).on_touch_down(touch):
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


class SelectableBoxLayoutPopup(RecycleDataViewBehavior, BoxLayout):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.ids['_Codigo'].text = data['Codigo_del_producto']
        self.ids['_Producto'].text = data['Nombre_del_producto'].capitalize()
        self.ids['_Cantidad'].text = str(data['Cantidad'])
        self.ids['_Precio_por_Producto'].text = str("{:.2f}".format(data['Precio']))
        return super(SelectableBoxLayoutPopup, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableBoxLayoutPopup, self).on_touch_down(touch):
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


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = []
        self.modificar_cantidad_del_producto = None
    
    def agregar_venta(self, articulo):
        articulo['Seleccionado']=False
        indice = -1
        if self.data:
            for i in range(len(self.data)):
                if articulo['Codigo_del_cliente'] == self.data[i]['Codigo_del_cliente']:
                    indice = i
            if indice >= 0:
                self.data[indice]['cantidad_carrito']+=1
                self.data[indice]['precio_total'] = self.data[indice]['Precio']*self.data[indice]['cantidad_carrito']
                self.refresh_from_data()
            else:
                self.data.append(articulo)
        else:
            self.data.append(articulo)
    
    def anular_venta(self):
        indice = self.venta_seleccionada()
        precio = 0
        if indice >= 0:
            self._layout_manager.deselect_node(self._layout_manager._last_selected_node)
            precio = self.data[indice]['precio_total']
            self.data.pop(indice)
            self.refresh_from_data()
        return precio
    
    def modificar_venta(self):
        indice = self.venta_seleccionada()
        if indice >= 0:
            popup = CambiarCantidadPopup(self.data[indice], self.actualizar_venta)
            popup.open()
    
    def actualizar_venta(self, valor):
        indice = self.venta_seleccionada()
        if indice >= 0:
            if valor == 0:
                self.data.pop(indice)
                self._layout_manager.deselect_node(self._layout_manager._last_selected_node)
            else:
                self.data[indice]['cantidad_carrito'] = valor
                self.data[indice]['precio_total'] = self.data[indice]['Precio'] * valor
            self.refresh_from_data()
            nuevo_total = 0
            for data in self.data:
                nuevo_total += data['precio_total']
            self.modificar_cantidad_del_producto(False, nuevo_total)
    
    def venta_seleccionada(self):
        indice = -1
        for i in range(len(self.data)):
            if self.data[i]['Seleccionado']:
                indice = i
                break
        return indice
        
    def seleccionar_venta(self):
        indice = self.ids.RVS.venta_seleccionada()
        if indice >= 0:
            _venta = self.ids.RVS.data[indice]
            venta = {}
            venta['Codigo_del_cliente'] = _venta['Codigo_del_cliente']
            venta['Codigo_del_producto'] = _venta['Codigo_del_producto']
            venta['Cantidad'] = _venta['Cantidad']
            venta['Precio'] = _venta['Precio']
            venta['cantidad_carrito'] = 1
            venta['precio_total'] = _venta['Precio']
            if callable(self.agregar_venta):
                self.agregar_venta(venta)
            self.dismiss()

class CambiarCantidadPopup(Popup):
    def __init__(self, data, actualizar_venta_callback, **kwargs):
        super(CambiarCantidadPopup, self).__init__(**kwargs)
        self.data = data
        self.actualizar_venta = actualizar_venta_callback
        self.ids.Informacion_Nueva_Cantidad_1.text = "Codigo_del_cliente: " + self.data['Codigo_del_cliente']
        self.ids.Informacion_Nueva_Cantidad_2.text = "Codigo_del_producto: " + self.data['Codigo_del_producto']
        self.ids.Informacion_Nueva_Cantidad_3.text = "Cantidad: " + str(self.data['cantidad_carrito'])
        
    def validar_input(self, texto_input):
        try:
            nueva_cantidad = int(texto_input)
            self.ids.Notificacion_No_Valido.text = ''
            self.actualizar_venta(nueva_cantidad)
            self.dismiss()
        except:
            self.ids.Notificacion_No_Valido.text = 'Cantidad no valida'
            
class PagarPopup(Popup):
    def __init__(self, Total_A_Pagar, pagado_callback, **kwargs):
        super(PagarPopup, self).__init__(**kwargs)
        self.Total_A_Pagar = Total_A_Pagar
        self.pagado = pagado_callback
        self.ids.Total_A_Pagar.text = '{:.2f}'.format(self.Total_A_Pagar)
        self.ids.Boton_Pagar.bind(on_release = self.dismiss)
        
    def mostrar_cambio(self):
        recibido = self.ids.Recibido.text
        try:
            cambio = float(recibido) - float(self.Total_A_Pagar)
            if cambio >= 0:
                self.ids.Cambio.text = "{:.2f}".format(cambio)
                self.ids.Boton_Pagar.disabled = False
            else:
                self.ids.Cambio.text = 'Pago menor a cantidad a pagar'
        except:
            self.ids.Cambio.text = 'Pago no valido'
    
class NuevaCompraPopup(Popup):
    def __init__(self, nueva_compra_callback, **kwargs):
        super(NuevaCompraPopup, self).__init__(**kwargs)
        self.nueva_compra = nueva_compra_callback
        self.ids.Aceptar_Compra.bind(on_release = self.dismiss)


class VentasWindow(BoxLayout):
    Cliente= None
    def __init__(self, actualizar_productos_callback, **kwargs):
        super().__init__(*kwargs)
        self.Total = 0.0
        self.ids.RVS.modificar_cantidad_del_producto = self.modificar_cantidad_del_producto
        self.actualizar_productos = actualizar_productos_callback
        
        self.Ahora = datetime.now()
        self.ids.Fecha.text = self.Ahora.strftime("%d/%m/%y")
        Clock.schedule_interval(self.actualizar_hora, 1)
        self.ids.Hora.text = self.Ahora.strftime("%H:%M:%S")

    
    def agregar_venta_codigo_producto(self, codigo):
        connection = QueriesSQLite.create_connection('Sistema_Transaccional_de_Ventas_DB.sqlite')
        inventario_sql = QueriesSQLite.execute_read_query(connection, "SELECT * from ventas")
        for producto in inventario_sql:
            if codigo==producto[1]:
                articulo = {}
                articulo['Codigo_del_cliente'] = producto[0]
                articulo['Codigo_del_producto'] = producto[1]
                articulo['Precio'] = producto[2]
                articulo['cantidad_carrito'] = 1
                articulo['Cantidad'] = producto[3]
                articulo['Total'] = producto[2]
                self.Total+=articulo['Precio']
                self.ids.Sub_Total.text = 'Q '+ "{:.2f}".format(self.Total)
                self.ids.RVS.agregar_venta(articulo)
                self.agregar_venta(articulo)
                self.ids.Buscar_Codigo_Del_Cliente.text = ''
                break
              
    def agregar_venta_codigo_cliente(self, codigo):
        connection = QueriesSQLite.create_connection('Sistema_Transaccional_de_Ventas_DB.sqlite')
        inventario_sql = QueriesSQLite.execute_read_query(connection, "SELECT * from ventas")
        for cliente in inventario_sql:
            if codigo==cliente[0]:
                articulo = {}
                articulo['Codigo_del_cliente'] = cliente[0]
                articulo['Codigo_del_producto'] = cliente[1]
                articulo['Cantidad'] = cliente[3]
                articulo['Precio'] = cliente[2]
                articulo['cantidad_carrito'] = 1
                articulo['Total'] = cliente[2]
                self.Total+=articulo['Precio']
                self.ids.Sub_Total.text = 'Q '+ "{:.2f}".format(self.Total)
                self.ids.RVS.agregar_venta(articulo)
                self.agregar_venta(articulo)
                self.ids.Buscar_Codigo_Del_Cliente.text = ''
                break
        
    def agregar_venta(self, articulo):
        self.Total+=articulo['Precio']
        self.ids.Sub_Total.text = 'Q '+ "{:.2f}".format(self.Total)
        self.ids.RVS.agregar_venta(articulo)    
    
    def anular_venta(self):
        menos_precio = self.ids.RVS.anular_venta()
        self.Total-=menos_precio
        self.ids.Sub_Total.text = 'Q '+ "{:.2f}".format(self.Total)
        
    def modificar_cantidad_del_producto(self, cambio = True, nuevo_total = None):
        if cambio:
            self.ids.RVS.modificar_venta()
        else:
            self.Total = nuevo_total
            self.ids.Sub_Total.text = 'Q '+ "{:.2f}".format(self.Total)
    
    def actualizar_hora(self, *args):
        self.Ahora = self.Ahora+timedelta(seconds=1)
        self.ids.Hora.text = self.Ahora.strftime("%H:%M:%S") 
    
    def pagar(self):
        if self.ids.RVS.data:
            popup = PagarPopup(self.Total, self.pagado)
            popup.open()
        else:
            self.ids.Notificacion_Falla.text = 'No hay nada que pagar'
            
    def pagado(self):
        self.ids.Notificacion_Exito.text = 'Compra realizada con éxito'
        self.ids.Notificacion_Falla.text = ''
        self.ids.Total.text = 'Q ' + "{:.2f}".format(self.Total)
        self.ids.Buscar_Codigo_Del_Producto.disabled = True
        self.ids.Buscar_Codigo_Del_Cliente.disabled = True
        self.ids.Pagar.disabled = True
        connection = QueriesSQLite.create_connection("Sistema_Transaccional_de_Ventas_DB.sqlite")
        actualizar = """
        UPDATE
            ventas
        SET
            Cantidad=?, Total = ?
        WHERE
            Codigo_del_cliente=?
        """
        venta = """INSERT INTO Ventas (Codigo_del_cliente, Total, Fecha) VALUES (?, ?, ?)"""
        venta_tuple_2 = (self.Total, self.Ahora, self.Cliente['Codigo_del_cliente'])
        venta_id = QueriesSQLite.execute_query(connection, venta_tuple_2)
        venta_detalle = """INSERT INTO Ventas_Detalle(Codigo_del_producto, Precio, Producto, Cantidad) VALUES (?,?,?,?)"""
        #actualizar_inventario = []
        for venta in self.ids.RVS.data:
            nueva_cantidad = 0
            nuevo_total = 0
            if venta['Cantidad']-venta['cantidad_carrito']>0:
                nueva_cantidad = venta['Cantidad'] - venta['cantidad_carrito']
                nuevo_total = nueva_cantidad * venta['Precio']
            venta_tuple = (nueva_cantidad, nuevo_total, venta['Codigo_del_cliente'])
            ventas_detalle_tuple = (venta_id, venta['Precio'], venta['Codigo'], venta['cantidad_carrito'])
            QueriesSQLite.execute_query(connection, venta_detalle, ventas_detalle_tuple,)
            QueriesSQLite.execute_query(connection, actualizar, venta_tuple)

                        
    def nueva_compra(self, desde_popup = False):
        if desde_popup:
            self.ids.RVS.data = []
            self.Total = 0.0
            self.ids.Sub_Total.text = '0.00'
            self.ids.Total.text = '0.00'
            self.ids.Notificacion_Exito.text = ''
            self.ids.Notificacion_Falla.text = ''
            self.ids.Buscar_Codigo_Del_Producto.disabled = False
            self.ids.Buscar_Codigo_Del_Cliente.disabled = False
            self.ids.Pagar.disabled = False
            self.ids.RVS.refresh_from_data()
        elif len(self.ids.RVS.data):
            popup = NuevaCompraPopup(self.nueva_compra)
            popup.open()
        
    def inventarios_y_clientes(self):
        self.parent.parent.current = 'Scrn_Inventarios_Y_Clientes'
        connection = QueriesSQLite.create_connection("Sistema_Transaccional_de_Ventas_DB.sqlite")
        seleccionar_ventas = "SELECT * from ventas"
        ventas = QueriesSQLite.execute_read_query(connection, seleccionar_ventas)
        for venta in ventas:
            print(venta)

    def inicio(self):
        if self.ids.RVS.data:
            self.ids.Notificacion_Falla.text = 'Compra abierta'
        else:   
            self.parent.parent.current = 'Scrn_Inicio'        

class VentasApp(App):
    def build(self):
        return VentasWindow()
    
if __name__ == "__main__":
    VentasApp().run()

