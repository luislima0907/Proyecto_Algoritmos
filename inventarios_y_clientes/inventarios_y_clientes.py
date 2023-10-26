from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview import RecycleView
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.lang import Builder
from sqlqueries import QueriesSQLite
from datetime import datetime, timedelta

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
        self.ids['_Precio'].text = str(f"{data['Precio']}")
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

class ItemVentaLabel(RecycleDataViewBehavior, BoxLayout):
	index = None

	def refresh_view_attrs(self, rv, index, data):
		self.index = index
		self.ids['_hashtag'].text = str(1+index)
		self.ids['_codigo'].text = data['codigo']
		self.ids['_articulo'].text = data['producto'].capitalize()
		self.ids['_cantidad'].text = str(data['cantidad'])
		self.ids['_precio_por_articulo'].text = str("{:.2f}".format(data['precio']))+" /artículo"
		self.ids['_total'].text= str("{:.2f}".format(data['total']))
		return super(ItemVentaLabel, self).refresh_view_attrs(
            rv, index, data)

# esto es nuevo tambien en kv
class SelectableVentaLabel(RecycleDataViewBehavior, BoxLayout):
        index = None
        selected = BooleanProperty(False)
        selectable = BooleanProperty(True)

        def refresh_view_attrs(self, rv, index, data):
            self.index = index
            self.ids['_hashtag'].text = str(1+index)
            self.ids['_username'].text = data['username']
            self.ids['_cantidad'].text = str(data['Productos'])
            self.ids['_articulo'].text = data['Nombre'].capitalize()
            self.ids['_total'].text = 'Q '+ str("{:.2f}".format(data['Total']))
            self.ids['_time'].text = str(data['Fecha'].strftime("%H:%M:%S"))
            self.ids['_date'].text = str(data['Fecha'].strftime("%d/%m/%Y"))
            return super(SelectableVentaLabel, self).refresh_view_attrs(
                rv, index, data)

        def on_touch_down(self, touch):
            if super(SelectableVentaLabel, self).on_touch_down(touch):
                return True
            if self.collide_point(*touch.pos) and self.selectable:
                return self.parent.select_with_touch(self.index, touch)

        def apply_selection(self, rv, index, is_selected):
            self.selected = is_selected
            if is_selected:
                rv.data[index]['seleccionado']=True
            else:
                rv.data[index]['seleccionado']=False

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
            self.ids.Producto_Codigo.disabled = True
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
            try:
                numeric = str(Producto_Nombre)
                validado['Nombre'] = Producto_Nombre.title()
            except:
                alerta_2 += 'Nombre no valido'
                validado['Nombre'] = False
        
        if not Producto_Proveedor:
            alerta_1 += 'Proveedor '
            validado['Proveedor'] = False
        else:
            try:
                numeric = str(Producto_Proveedor)
                validado['Proveedor'] = Producto_Proveedor.title()
            except:
                alerta_2 += 'Proveedor no valido'
                validado['Proveedor'] = False
        
        if not Producto_Cantidad:
            alerta_1 += 'Cantidad '
            validado['Cantidad'] = False
        else:
            try:
                cantidad_string = int(Producto_Cantidad)
                validado['Cantidad'] = Producto_Cantidad
            except:
                alerta_2 += 'Cantidad no valida'
                validado['Cantidad'] = False
                
        if not Producto_Precio:
            alerta_1 += 'Precio '
            validado['Precio'] = False
        else:
            try:
                precio_string = float(Producto_Precio)
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
        if inventario_sql:
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
        
    def modificar_producto(self, modificar =  False, validado = None):
        indice = self.ids.RV_Productos.dato_seleccionado()
        if modificar:
            producto_tuple = (validado['Nombre'], validado['Precio'], validado['Cantidad'], validado['Proveedor'], validado['Codigo'])
            connection = QueriesSQLite.create_connection("Sistema_Transaccional_de_Ventas_DB.sqlite")
            actualizar = """
            UPDATE
                productos
            SET
                Nombre = ?, Precio = ?, Cantidad = ?, Proveedor = ?
            WHERE
                Codigo = ?
            """
            QueriesSQLite.execute_query(connection, actualizar, producto_tuple)
            self.ids.RV_Productos.data[indice]['Nombre'] = validado['Nombre']
            self.ids.RV_Productos.data[indice]['Precio'] = validado['Precio']
            self.ids.RV_Productos.data[indice]['Cantidad'] = validado['Cantidad']
            self.ids.RV_Productos.data[indice]['Proveedor'] = validado['Proveedor']
            self.ids.RV_Productos.refresh_from_data()
            seleccionar_productos = "SELECT * from productos"
            productos = QueriesSQLite.execute_read_query(connection, seleccionar_productos)
            for producto in productos:
                print(producto)
                        
        else:
            if indice >=0:
                producto = self.ids.RV_Productos.data[indice]
                popup = ProductoPopup(self.modificar_producto)
                popup.abrir(False, producto)
        
    def eliminar_producto(self):
        indice = self.ids.RV_Productos.dato_seleccionado()
        if indice >=0:
            producto_tuple = (self.ids.RV_Productos.data[indice]['Codigo'],)
            connection = QueriesSQLite.create_connection("Sistema_Transaccional_de_Ventas_DB.sqlite")
            borrar = """DELETE from productos WHERE Codigo = ?"""
            QueriesSQLite.execute_query(connection, borrar, producto_tuple)
            self.ids.RV_Productos.data.pop(indice)
            self.ids.RV_Productos.refresh_from_data()

    def actualizar_productos(self, producto_actualizado):
        for producto_nuevo in producto_actualizado:
            for producto_viejo in self.ids.RV_Productos.data:
                if producto_nuevo['Codigo'] == producto_viejo['Codigo']:
                    producto_viejo['Cantidad']= producto_nuevo['Cantidad']
                    #producto_viejo['Total'] = producto_nuevo['Total']
                    break
        self.ids.RV_Productos.refresh_from_data()
        
class ClientePopup(Popup):
    def __init__(self, _agregar_callback, **kwargs):
        super(ClientePopup, self).__init__(**kwargs)
        self.agregar_cliente = _agregar_callback
    
    def abrir(self, agregar, cliente = None):
        if agregar:
            self.ids.Cliente_Info_1.text = 'Agregar cliente nuevo'
            self.ids.Cliente_Codigo.disabled = False
        else:
            self.ids.Cliente_Info_1.text = 'Modificar cliente'
            self.ids.Cliente_Codigo.text = cliente['Codigo']
            self.ids.Cliente_Codigo.disabled = True
            self.ids.Cliente_Nombre.text = cliente['Nombre']
            self.ids.Cliente_Direccion.text = cliente['Direccion']
            self.ids.Cliente_Tipo.text = cliente['Tipo']
        self.open()

    def verificar(self, Cliente_Codigo, Cliente_Nombre, Cliente_Direccion, Cliente_Tipo):
        alerta_1 = 'Falta: '
        alerta_2 = ''
        validado = {}
        if not Cliente_Codigo:
            alerta_1 += 'Codigo '
            validado['Codigo'] = False
        else:
            try:
                codigo = str(Cliente_Codigo)
                validado['Codigo'] = Cliente_Codigo
            except:
                alerta_2 += 'Codigo no valido'
                validado['Codigo'] = False
                
        if not Cliente_Nombre:
            alerta_1 += 'Nombre '
            validado['Nombre'] = False
        else:
            try:
                nombre = str(Cliente_Nombre)
                validado['Nombre'] = Cliente_Nombre.title()
            except:
                alerta_2 += 'Nombre no valido'
                validado['Nombre'] = False
        
        if not Cliente_Direccion:
            alerta_1 += 'Direccion '
            validado['Direccion'] = False
        else:
            try:
                direccion = str(Cliente_Direccion)
                validado['Direccion'] = Cliente_Direccion.title()
            except:
                alerta_2 += 'Direccion no valida'
                validado['Direccion'] = False
        
        if not Cliente_Tipo:
            alerta_1 += 'Tipo '
            validado['Tipo'] = False
        else:
            try:
                tipo = str(Cliente_Tipo)
                validado['Tipo'] = Cliente_Tipo
            except:
                alerta_2 += 'Tipo no valida'
                validado['Tipo'] = False
                
        valores = list(validado.values())
        
        if False in valores:
            self.ids.No_Valido_Notificacion_2.text = alerta_1 + alerta_2
        else:
            self.ids.No_Valido_Notificacion_2.text = 'Validado'
            self.agregar_cliente(True, validado)
            self.dismiss()     
   
class VistaClientes(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.cargar_clientes, 1)
        
    def cargar_clientes(self, *args):
        _clientes = []
        connection = QueriesSQLite.create_connection("Sistema_Transaccional_de_Ventas_DB.sqlite")
        clientes_sql = QueriesSQLite.execute_read_query(connection, "SELECT * from clientes")
        if clientes_sql:
            for cliente in clientes_sql:
                _clientes.append({'Codigo': cliente[0], 'Nombre': cliente[1], 'Direccion': cliente[2], 'Tipo': cliente[3]})
            self.ids.RV_Clientes.agregar_datos(_clientes)
        self.ids.RV_Clientes.agregar_datos(_clientes)

    def agregar_cliente(self, agregar = False, validado = None):
        if agregar:
            cliente_tuple = tuple(validado.values())
            connection = QueriesSQLite.create_connection("Sistema_Transaccional_de_Ventas_DB.sqlite")
            crear_cliente = """
            INSERT INTO
                clientes (Codigo, Nombre, Direccion, Tipo)
            VALUES
                (?,?,?,?);
            """
            QueriesSQLite.execute_query(connection, crear_cliente, cliente_tuple)
            self.ids.RV_Clientes.data.append(validado)
            self.ids.RV_Clientes.refresh_from_data()
            seleccionar_clientes = "SELECT * from clientes"
            clientes = QueriesSQLite.execute_read_query(connection, seleccionar_clientes)
            for cliente in clientes:
                print("type:", type(cliente), "cliente:",cliente)    
        else:
            popup = ClientePopup(self.agregar_cliente)
            popup.abrir(True)
            
            
    def modificar_cliente(self, modificar = False, validado = None):
        indice = self.ids.RV_Clientes.dato_seleccionado()
        if modificar:
            cliente_tuple = (validado['Nombre'], validado['Direccion'], validado['Tipo'], validado['Codigo'])
            connection = QueriesSQLite.create_connection("Sistema_Transaccional_de_Ventas_DB.sqlite")
            actualizar = """
            UPDATE
                clientes
            SET
                Nombre=?, Direccion=?, Tipo=?
            WHERE
                Codigo=?
            """
            QueriesSQLite.execute_query(connection, actualizar, cliente_tuple)
            self.ids.RV_Clientes.data[indice]['Nombre'] = validado['Nombre']
            self.ids.RV_Clientes.data[indice]['Direccion'] = validado['Direccion']
            self.ids.RV_Clientes.data[indice]['Tipo'] = validado['Tipo']
            self.ids.RV_Clientes.refresh_from_data()
        else:
            if indice >=0:
                cliente = self.ids.RV_Clientes.data[indice]
                popup = ClientePopup(self.modificar_cliente)
                popup.abrir(False,cliente)        
        
    def eliminar_cliente(self):
        indice = self.ids.RV_Clientes.dato_seleccionado()
        if indice >=0:
            cliente_tuple = (self.ids.RV_Clientes.data[indice]['Codigo'],)
            connection = QueriesSQLite.create_connection("Sistema_Transaccional_de_Ventas_DB.sqlite")
            borrar = """DELETE from clientes WHERE Codigo = ?"""
            QueriesSQLite.execute_query(connection, borrar, cliente_tuple)
            self.ids.RV_Clientes.data.pop(indice)
            self.ids.RV_Clientes.refresh_from_data()
  
# igual esto es nuevo tambien en kv
class InfoVentaPopup(Popup):
        connection = QueriesSQLite.create_connection("Sistema_Transaccional_de_Ventas_DB.sqlite")
        select_item_query = """SELECT Nombre FROM Productos WHERE Codigo = ?"""
        def __init__(self, venta, **kwargs):
            super(InfoVentaPopup, self).__init__(**kwargs)
            self.venta = [{"Codigo_del_producto": producto[3], "Producto": QueriesSQLite.execute_read_query(self.connection, self.select_item_query, (producto[3],))[0][0], "Cantidad": producto[4], "Precio": producto[2], "Total": producto[4] * producto[2]} for producto in venta]
            print(self.venta)
            # print(QueriesSQLite.execute_read_query(self.connection, self.select_item_query, (producto[3],)))
            # print(type(QueriesSQLite.execute_read_query(self.connection, self.select_item_query, (producto[3],))))

        def mostrar(self):
            self.open()
            total_item = 0
            total_dinero = 0.0
            for articulo in self.venta:
                total_item+=articulo['Cantidad']
                total_dinero += articulo['Total']
            self.ids.total_items.text = str(total_item)
            self.ids.total_dinero.text ='Q ' + str("{:.2f}".format(total_dinero))
            self.ids.info_rv.agregar_datos(self.venta)

# nueva clase creada y tabien en kv
class VistaVentas(Screen):
            productos_actuales=[]
            def __init__(self, **kwargs):
                    super().__init__(**kwargs)

            def crear_csv(self):
                pass

            def mas_info(self):
                    indice = self.ids.Ventas_RV.dato_seleccionado()
                    if indice >= 0:
                        venta = self.productos_actuales[indice]
                        p = InfoVentaPopup(venta)
                        p.mostrar()


            def cargar_venta(self, choice='Default'):
                connection = QueriesSQLite.create_connection("Sistema_Transaccional_de_Ventas_DB.sqlite")
                validar_input = True
                final_suma = 0
                fecha_inicio = datetime.strptime('01/01/00', '%d/%m/%y')
                fecha_fin = datetime.strptime('31/12/2099', '%d/%m/%Y')
                
                _ventas = []
                _total_productos =[]
                
                seleccionar_ventas_query = """ SELECT * FROM Ventas WHERE Fecha BETWEEN ? AND ? """
                seleccionar_productos_query = """ SELECT * FROM Ventas_Detalle WHERE Codigo_del_cliente """
                
                self.ids.Ventas_RV.data = []
                if choice == 'Default':
                    fecha_inicio = datetime.today().date()
                    fecha_fin = fecha_inicio + timedelta(days=1)
                    self.ids.Fecha.text = str(fecha_inicio.strftime("%d-%m-%y"))
                elif choice == 'Date':
                    date = self.ids.single_date.text
                    try:
                        fecha_elegida = datetime.strptime(date, '%d/%m/%y')
                    except:
                        validar_input = False
                    if validar_input:
                        fecha_inicio =fecha_elegida
                        fecha_fin = fecha_elegida+timedelta(days=1)
                        self.ids.Fecha.text = fecha_elegida.strftime('%d/%m/%y')
                else:
                    if self.ids.initial_date.text:
                        initial_date = self.ids.initial_date.text
                        try:
                            fecha_inicio = datetime.strptime(initial_date, "%d/%m/%y")
                        except:
                            validar_input = False
                    if self.ids.last_date.text:
                        last_date = self.ids.last_date.text
                        try:
                            fecha_inicio = datetime.strptime(last_date, "%d/%m/%y")
                        except:
                            validar_input = False
                    if validar_input:
                        self.ids.Fecha.text = fecha_inicio.strftime("%d-%m-%y") + " - " + fecha_fin.strftime("%d-%m-%y")
                                        
                if validar_input:
                    inicio_fin = (fecha_inicio, fecha_fin)
                    ventas_sql = QueriesSQLite.execute_read_query(connection, seleccionar_ventas_query, inicio_fin)
                    if ventas_sql:
                        for venta in ventas_sql:
                            final_suma+=venta[4]
                            ventas_detalle_sql = QueriesSQLite.execute_read_query(connection, seleccionar_productos_query, (venta[0],))
                            _total_productos.append(ventas_detalle_sql)
                            count = 0
                            for producto in ventas_detalle_sql:
                                count += producto[4]
                            _ventas.append({"Codigo_del_producto": venta['1'], "Productos": count, "Total": venta[4], "Fecha": datetime.strptime(venta[5], '%Y-%m-%d %H:%M:%S.%f')})
                    self.ids.Ventas_RV.agregar_datos(_ventas)
                    self.productos_actuales = _total_productos
                self.ids.final_suma.text ='Q ' + str("{:.2f}".format(final_suma))
                self.ids.initial_date.text = ""
                self.ids.last_date.text = ""
                self.ids.single_date.text = ''


#import dropdown tambien!!!
#agregado customdropdown y tambien en kv y selectablesale label
class CustomDropDown(DropDown):
        def __init__(self, cambiar_callback, **kwargs):
            self._succ_cb = cambiar_callback
            super(CustomDropDown, self).__init__(**kwargs)

        def vista(self, vista):
            if callable(self._succ_cb):
                self._succ_cb(True, vista)

          
class InventariosYClientesWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vista_actual = "Productos"
        self.Vista_Manager = self.ids.Vista_Manager
        self.dropdown = CustomDropDown(self.cambiar_vista)				# nuevo
        self.ids.Cambiar_Vista.bind(on_release=self.dropdown.open)		# nuevo
        
    def cambiar_vista(self, cambio = False, vista = None):
        if cambio:
            self.vista_actual=vista
            self.Vista_Manager.current=self.vista_actual
            self.dropdown.dismiss()

    def inventarios_y_clientes(self):
        self.parent.parent.current = 'Scrn_Inventarios_Y_Clientes'

    def ventas(self):
        self.parent.parent.current = 'Scrn_Ventas'

    def inicio(self):
        self.parent.parent.current = 'Scrn_Inicio'
    
    def actualizar_productos(self, productos):
        self.ids.Vista_Productos.actualizar_productos(productos)
        
class InventariosYClientesApp(App):
    def build(self):
        return InventariosYClientesWindow()
    
if __name__ == "__main__":
    InventariosYClientesApp().run()