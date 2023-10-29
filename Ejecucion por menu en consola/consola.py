# Listas y Diccionario vacio para almacenar la informacion
productos = {}
clientes = {}
ventas = []

# Funciones Basicas de productos listar, crear, actualizar y eliminar producto


def listar_productos():
    print("Lista de Productos:")
    for codigo, producto in productos.items():
        print(
            f"Código: {codigo}, Nombre: {producto['nombre']}, Precio: Q {producto['precio']}, Existencias: {producto['existencias']}")


def crear_producto():
    codigo = input("Ingrese el código del producto: ")
    nombre = input("Ingrese el nombre del producto: ")
    precio = float(input("Ingrese el precio del producto: "))
    existencias = int(input("Ingrese las existencias iniciales: "))
    productos[codigo] = {'nombre': nombre,
                         'precio': precio, 'existencias': existencias}
    print("Producto creado con éxito.")


def actualizar_producto():
    codigo = input("Ingrese el código del producto que desea actualizar: ")
    if codigo in productos:
        nombre = input("Ingrese el nuevo nombre del producto: ")
        precio = float(input("Ingrese el nuevo precio del producto: "))
        existencias = int(input("Ingrese las nuevas existencias: "))
        productos[codigo] = {'nombre': nombre,
                             'precio': precio, 'existencias': existencias}
        print("Producto actualizado con éxito.")
    else:
        print("El producto no existe.")


def eliminar_producto():
    codigo = input("Ingrese el código del producto que desea eliminar: ")
    if codigo in productos:
        del productos[codigo]
        print("Producto eliminado con éxito.")
    else:
        print("El producto no existe.")

# Funciones de clientes listar, crear, actualizar y eliminar cliente


def listar_clientes():
    print("Lista de Clientes:")
    for id_cliente, cliente in clientes.items():
        print(
            f"ID: {id_cliente}, Nombre: {cliente['nombre']}, Email: {cliente['email']}")


def crear_cliente():
    id_cliente = input("Ingrese el ID del cliente: ")
    nombre = input("Ingrese el nombre del cliente: ")
    email = input("Ingrese el email del cliente: ")
    clientes[id_cliente] = {'nombre': nombre, 'email': email}
    print("Cliente creado con éxito.")


def actualizar_cliente():
    id_cliente = input("Ingrese el ID del cliente que desea actualizar: ")
    if id_cliente in clientes:
        nombre = input("Ingrese el nuevo nombre del cliente: ")
        email = input("Ingrese el nuevo email del cliente: ")
        clientes[id_cliente] = {'nombre': nombre, 'email': email}
        print("Cliente actualizado con éxito.")
    else:
        print("El cliente no existe.")


def eliminar_cliente():
    id_cliente = input("Ingrese el ID del cliente que desea eliminar: ")
    if id_cliente in clientes:
        del clientes[id_cliente]
        print("Cliente eliminado con éxito.")
    else:
        print("El cliente no existe.")


# Funciones Basicas de ventas listar, crear y anular venta

def listar_ventas():
    print("Lista de Ventas:")
    for venta in ventas:
        print(
            f"ID de Venta: {venta['id_venta']}, Cliente: {venta['cliente_id']}, Total: Q {venta['total']}")


def crear_venta():
    id_venta = len(ventas) + 1
    cliente_id = input("Ingrese el ID del cliente: ")
    total = 0
    productos_vendidos = []

    while True:
        listar_productos()
        codigo = input(
            "Ingrese el código del producto que desea vender (presione 0 para salir): ")
        if codigo == '0':
            break
        if codigo in productos:
            cantidad = int(input("Ingrese la cantidad: "))
            if cantidad > productos[codigo]['existencias']:
                print("No hay suficientes existencias de este producto.")
            else:
                productos_vendidos.append(
                    {'codigo': codigo, 'cantidad': cantidad})
                total += productos[codigo]['precio'] * cantidad
                productos[codigo]['existencias'] -= cantidad
        else:
            print("El producto no existe.")

    ventas.append({'id_venta': id_venta, 'cliente_id': cliente_id,
                  'total': total, 'productos_vendidos': productos_vendidos})
    print("Venta registrada con éxito.")


def anular_venta():
    id_venta = input("Ingrese el ID de la venta que desea anular: ")
    for venta in ventas:
        if venta['id_venta'] == id_venta:
            for producto_vendido in venta['productos_vendidos']:
                codigo = producto_vendido['codigo']
                cantidad = producto_vendido['cantidad']
                productos[codigo]['existencias'] += cantidad
            ventas.remove(venta)
            print("Venta anulada con éxito.")
            return
    print("La venta no existe.")


# Reportes Basicos de ventas por clientes y productos

def reporte_venta_por_cliente():
    cliente_id = input("Ingrese el ID del cliente para el informe de ventas: ")
    print(f"Informe de Ventas para el Cliente ID {cliente_id}:")
    total_ventas_cliente = 0
    for venta in ventas:
        if venta['cliente_id'] == cliente_id:
            print(
                f"ID de Venta: {venta['id_venta']}, Total: Q {venta['total']}")
            total_ventas_cliente += venta['total']
    print(f"Total de Ventas para el Cliente: Q {total_ventas_cliente}")


def reporte_venta_por_producto():
    codigo_producto = input(
        "Ingrese el código del producto para el informe de ventas: ")
    print(f"Informe de Ventas para el Producto {codigo_producto}:")
    total_ventas_producto = 0
    for venta in ventas:
        for producto_vendido in venta['productos_vendidos']:
            if producto_vendido['codigo'] == codigo_producto:
                print(
                    f"ID de Venta: {venta['id_venta']}, Cantidad Vendida: {producto_vendido['cantidad']}")
                total_ventas_producto += producto_vendido['cantidad']
    print(
        f"Total de Ventas para el Producto: {total_ventas_producto} unidades")

# Menus de opciones


while True:
    print("\nOpciones:")
    print("1. Productos")
    print("2. Clientes")
    print("3. Ventas")
    print("4. Reportes")
    print("5. Salir")
    opcion = input("Seleccione una opción: ")

    if opcion == '1':
        print("\nGestión de Productos:")
        print("1. Lista de productos")
        print("2. Crear producto")
        print("3. Actualizar producto")
        print("4. Eliminar producto")
        subopcion = input("Seleccione una opción: ")

        if subopcion == '1':
            listar_productos()
        elif subopcion == '2':
            crear_producto()
        elif subopcion == '3':
            actualizar_producto()
        elif subopcion == '4':
            eliminar_producto()
        else:
            print("Seleccione una opcion valida.")

    elif opcion == '2':
        print("\nGestión de Clientes:")
        print("1. Lista de clientes")
        print("2. Crear cliente")
        print("3. Actualizar cliente")
        print("4. Eliminar cliente")
        subopcion = input("Seleccione una opción: ")

        if subopcion == '1':
            listar_clientes()
        elif subopcion == '2':
            crear_cliente()
        elif subopcion == '3':
            actualizar_cliente()
        elif subopcion == '4':
            eliminar_cliente()
        else:
            print("opción no válida. Por favor, seleccione una opción válida.")

    elif opcion == '3':
        print("\nGestión de Ventas:")
        print("1. Lista de ventas")
        print("2. Crear venta")
        print("3. Anular venta")
        subopcion = input("Seleccione una opción: ")

        if subopcion == '1':
            listar_ventas()
        elif subopcion == '2':
            crear_venta()
        elif subopcion == '3':
            anular_venta()
        else:
            print("opción no válida. Por favor, seleccione una opción válida.")

    elif opcion == '4':
        print("\nReportes:")
        print("1. Ventas de Clientes")
        print("2. Ventas de Productos")
        subopcion = input("Seleccione una opción: ")

        if subopcion == '1':
            reporte_venta_por_cliente()
        elif subopcion == '2':
            reporte_venta_por_producto()
        else:
            print("opción no válida. Por favor, seleccione una opción válida.")

    elif opcion == '5':
        break
    else:
        print("Opción no válida. Por favor, seleccione una opción válida.")
