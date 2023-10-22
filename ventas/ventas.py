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

inventario=[
	{'Codigo': '111', 'Nombre': 'leche 1L', 'Precio': 20.0, 'Cantidad': 20},
	{'Codigo': '222', 'Nombre': 'cereal 500g', 'Precio': 50.5, 'Cantidad': 15}, 
	{'Codigo': '333', 'Nombre': 'yogurt 1L', 'Precio': 25.0, 'Cantidad': 10},
	{'Codigo': '444', 'Nombre': 'helado 2L', 'Precio': 80.0, 'Cantidad': 20},
	{'Codigo': '555', 'Nombre': 'alimento para perro 20kg', 'Precio': 750.0, 'Cantidad': 5},
	{'Codigo': '666', 'Nombre': 'shampoo', 'Precio': 100.0, 'Cantidad': 25},
	{'Codigo': '777', 'Nombre': 'papel higiénico 4 rollos', 'Precio': 35.5, 'Cantidad': 30},
	{'Codigo': '888', 'Nombre': 'jabón para trastes', 'Precio': 65.0, 'Cantidad': 5},
	{'Codigo': '999', 'Nombre': 'refresco 600ml', 'Precio': 15.0, 'Cantidad': 10}
]

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
        self.ids['_Articulo'].text = data['Nombre'].capitalize()
        self.ids['_Cantidad'].text = str(data['cantidad_carrito'])
        self.ids['_Precio_por_Articulo'].text = str("{:.2f}".format(data['Precio']))
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
        self.ids['_Codigo'].text = data['Codigo']
        self.ids['_Articulo'].text = data['Nombre'].capitalize()
        self.ids['_Cantidad'].text = str(data['Cantidad'])
        self.ids['_Precio'].text = str("{:.2f}".format(data['Precio']))
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
        self.modificar_producto = None
    
    def agregar_articulo(self, articulo):
        articulo['Seleccionado']=False
        indice = -1
        if self.data:
            for i in range(len(self.data)):
                if articulo['Codigo'] == self.data[i]['Codigo']:
                    indice = i
            if indice >= 0:
                self.data[indice]['cantidad_carrito']+=1
                self.data[indice]['precio_total'] = self.data[indice]['Precio']*self.data[indice]['cantidad_carrito']
                self.refresh_from_data()
            else:
                self.data.append(articulo)
        else:
            self.data.append(articulo)
    
    def eliminar_articulo(self):
        indice = self.articulo_seleccionado()
        precio = 0
        if indice >= 0:
            self._layout_manager.deselect_node(self._layout_manager._last_selected_node)
            precio = self.data[indice]['precio_total']
            self.data.pop(indice)
            self.refresh_from_data()
        return precio
    
    def modificar_articulo(self):
        indice = self.articulo_seleccionado()
        if indice >= 0:
            popup = CambiarCantidadPopup(self.data[indice], self.actualizar_articulo)
            popup.open()
    
    def actualizar_articulo(self, valor):
        indice = self.articulo_seleccionado()
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
            self.modificar_producto(False, nuevo_total)
    
    def articulo_seleccionado(self):
        indice = -1
        for i in range(len(self.data)):
            if self.data[i]['Seleccionado']:
                indice = i
                break
        return indice

class ProductoPorNombrePopup(Popup):
    def __init__(self, input_nombre, agregar_producto_callback, **kwargs):
        super(ProductoPorNombrePopup, self).__init__(**kwargs)
        self.input_nombre = input_nombre
        self.agregar_producto = agregar_producto_callback
    
    def mostrar_articulos(self):
        self.open()
        for nombre in inventario:
            if nombre['Nombre'].lower().find(self.input_nombre) >= 0:
                producto = {'Codigo': nombre['Codigo'], 'Nombre': nombre['Nombre'], 'Precio': nombre['Precio'], 'Cantidad': nombre['Cantidad']}
                self.ids.RVS.agregar_articulo(producto)
    
    def seleccionar_articulo(self):
        indice = self.ids.RVS.articulo_seleccionado()
        if indice >= 0:
            _articulo = self.ids.RVS.data[indice]
            articulo = {}
            articulo['Codigo'] = _articulo['Codigo']
            articulo['Nombre'] = _articulo['Nombre']
            articulo['Precio'] = _articulo['Precio']
            articulo['cantidad_carrito'] = 1
            articulo['cantidad_inventario'] = _articulo['Cantidad']
            articulo['precio_total'] = _articulo['Precio']
            if callable(self.agregar_producto):
                self.agregar_producto(articulo)
            self.dismiss()

class CambiarCantidadPopup(Popup):
    def __init__(self, data, actualizar_articulo_callback, **kwargs):
        super(CambiarCantidadPopup, self).__init__(**kwargs)
        self.data = data
        self.actualizar_articulo = actualizar_articulo_callback
        self.ids.Informacion_Nueva_Cantidad_1.text = "Producto: " + self.data['Nombre'].capitalize()
        self.ids.Informacion_Nueva_Cantidad_2.text = "Cantidad: " + str(self.data['cantidad_carrito'])
        
    def validar_input(self, texto_input):
        try:
            nueva_cantidad = int(texto_input)
            self.ids.Notificacion_No_Valido.text = ''
            self.actualizar_articulo(nueva_cantidad)
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
    def __init__(self, **kwargs):
        super().__init__(*kwargs)
        self.Total = 0.0
        self.ids.RVS.modificar_producto = self.modificar_producto
        
        self.Ahora = datetime.now()
        self.ids.Fecha.text = self.Ahora.strftime("%d/%m/%y")
        Clock.schedule_interval(self.actualizar_hora, 1)
        self.ids.Hora.text = self.Ahora.strftime("%H:%M:%S")

        
    
    def agregar_producto_codigo(self, codigo):
        for producto in inventario:
            if codigo==producto['Codigo']:
                articulo = {}
                articulo['Codigo'] = producto['Codigo']
                articulo['Nombre'] = producto['Nombre']
                articulo['Precio'] = producto['Precio']
                articulo['cantidad_carrito'] = 1
                articulo['cantidad_inventario'] = producto['Cantidad']
                articulo['precio_total'] = producto['Precio']
                self.Total+=articulo['Precio']
                self.ids.Sub_Total.text = 'Q '+ "{:.2f}".format(self.Total)
                self.ids.RVS.agregar_articulo(articulo)
                self.agregar_producto(articulo)
                self.ids.Buscar_Codigo.text = ''
                break
    
    def agregar_producto_nombre(self, nombre):
        self.ids.Buscar_Nombre.text = ''
        popup = ProductoPorNombrePopup(nombre, self.agregar_producto)
        popup.mostrar_articulos()
        
    def agregar_producto(self, articulo):
        self.Total+=articulo['Precio']
        self.ids.Sub_Total.text = 'Q '+ "{:.2f}".format(self.Total)
        self.ids.RVS.agregar_articulo(articulo)    
    
    def eliminar_producto(self):
        menos_precio = self.ids.RVS.eliminar_articulo()
        self.Total-=menos_precio
        self.ids.Sub_Total.text = 'Q '+ "{:.2f}".format(self.Total)
        
    def modificar_producto(self, cambio = True, nuevo_total = None):
        if cambio:
            self.ids.RVS.modificar_articulo()
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
        self.ids.Buscar_Codigo.disabled = True
        self.ids.Buscar_Nombre.disabled = True
        nueva_cantidad = []
        for producto in self.ids.RVS.data:
            cantidad = producto['cantidad_inventario'] - producto['cantidad_carrito']
            if cantidad >= 0:
                nueva_cantidad.append({'Codigo': producto['Codigo'], 'Cantidad': cantidad})
            else:
                nueva_cantidad.append({'Codigo': producto['Codigo'], 'Cantidad': 0})
        for cantidad in nueva_cantidad:
            resultado = next((producto for producto in inventario if producto['Codigo'] == cantidad['Codigo']), None)
            resultado['Cantidad'] = cantidad['Cantidad']
                        
    def nueva_compra(self, desde_popup = False):
        if desde_popup:
            self.ids.RVS.data = []
            self.Total = 0.0
            self.ids.Sub_Total.text = '0.00'
            self.ids.Total.text = '0.00'
            self.ids.Notificacion_Exito.text = ''
            self.ids.Notificacion_Falla.text = ''
            self.ids.Buscar_Codigo.disabled = False
            self.ids.Buscar_Nombre.disabled = False
            self.ids.RVS.refresh_from_data()
        elif len(self.ids.RVS.data):
            popup = NuevaCompraPopup(self.nueva_compra)
            popup.open()
        
    def admin(self):
        print(f"Inventario: {inventario}")  

    def signout(self):
        print("Signout presionado")  

class VentasApp(App):
    def build(self):
        return VentasWindow()
    
if __name__ == "__main__":
    VentasApp().run()

