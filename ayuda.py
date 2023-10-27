import sys

ayuda = sys.argv[1]
ayuda_interfaz = sys.argv[1]


if ayuda == "ayuda" or ayuda == "Ayuda" or ayuda == "help" or ayuda == "Help":
    print("Para ejecutar el programa y la interfaz gráfica, debemos hacer lo siguiente:\n")
    print("Debemos ubicarnos en la carpeta de 'SistemaTransaccionalDeVentas' en nuestro editor de codigo, podemos usar los comandos 'cd (nombre de la carpeta u archivo)' para movernos entre carpetas\n")
    print("Una vez ubicada la carpeta, debemos de escribir lo siguiente: py main.py\n")
    print("Con eso ya estaríamos accediendo al programa y su interfaz")
else:
    print("El comando para ayuda es: py ayuda.py ayuda")
    
if ayuda_interfaz == "Como uso la interfaz" or ayuda_interfaz == "como uso la interfaz":
    print("Para usar la interfaz gráfica, debemos hacer lo siguiente:\n")
    print("En la primera ventana podemos ver la Bienvenida al programa, nos pedirá ingresar un usuario y contraseña que hayamos guardado en nuestra base de datos, dependiendo el usuario que se ingrese tendrá permisos de trabajador o de administrador, el trabajador solo podrá acceder al apartado de las ventas y realizarlas para poder actualizar la base de datos, mientras que el administrador podrá agregar nuevos usuarios, productos y ventas a la base de datos, incluyendo la posibilidad de ver la información de cada una de las ventas realizadas en una ventana especial.\n")
    print("Si eres trabajador, te dirijirá al apartado de ventas donde se encontrarán todas las ventas que se hagan en nuestra tienda, podemos ingresar productos para la venta por su nombre o código en unos inputs abajo de la bienvenida.\n \nUna vez agregado el producto al carrito podemos seleccionarlo dando click encima de este y una vez hecho eso podemos hacer lo siguiente:\n 1. Podemos hacer un pago por esa venta dandole a 'Pagar'\n \n 1.1 Una vez le dimos a pagar, nos mostrará una ventana donde nos dará el total de la compra y un espacio para agregar el dinero necesaio para hacer la venta, si el dinero ingresado es menor al total, entonces no se hará la venta porque faltaría dinero para completarla, si tenemos el dinero suficiente nos mostrará el cambio que le devolvemos a la persona que hizo la compra, una vez hecho lo anterior, le damos a 'Aceptar' y con eso ya tendríamos la venta hecha, pero se nos desabilitarán los campos para ingresar los productos al carrito, esto para tener un mejor orden con cada venta a realizar y no tener conflicto con las bases de datos.\n \n 1.2 Si queremos realizar una nueva compra por parte de la persona, tendremos que darle al botón 'Nueva Compra' y se nos habilitarán los campos para ingresar productos al carrito nuevamente.\n 2. Anular la venta con el botón de 'Anular venta'\n \n 3. Modificar la cantidad del producto dandole en 'Cambiar Cantidad', luego nos va a mostrar una ventana para poder modificar la cantidad del producto que seleccionamos. ")
    print("Con eso ya estaríamos accediendo al programa y su interfaz")