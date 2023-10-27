import smtplib
import email.mime.multipart
import email.mime.base
import os
from email.mime.text import MIMEText

#IMPORTANTE: Para ejecutar este envio debes ubicarte en la carpeta de "SistemaTransaccionalDeVentas" y todo esto con el entorno virtual activo para que no hayan problemas.

# # Crea la conexión SMTP
# server = smtplib.SMTP('smtp.gmail.com', 587)

# Ingresa el correo que quieres que sea el remitente para enviar el correo con el archivo a otra persona
# Tambien debes ingresar la contraseña que te dan al momento de tener la verificación de dos pasos activa y conexión hacia una app que tu quieras
# correo = 'perezlc440@gmail.com'
# pas ='zvbvkoboaippqhlf'
# # Inicia sesión en tu cuenta de Gmail
# server.starttls()

# server.login(correo, pas)

# # Definir el remitente y destinatario del correo electrónico
# remitente = "perezlc440@gmail.com"
# destinatario = "llimap5@miumg.edu.gt"

# # Crear el mensaje del correo electrónico
# mensaje = email.mime.multipart.MIMEMultipart()
# mensaje['From'] = remitente
# mensaje['To'] = destinatario
# mensaje['Subject'] = "Correo electrónico con archivo adjunto"

# # Añadir el cuerpo del mensaje
# cuerpo = "Hola,\n\nAqui encontraras las ventas que se realizaron ese día en nuestra tienda enviado desde Python con un archivo adjunto.\n\nSaludos,\n Luis y Marvin"
# mensaje.attach(email.mime.text.MIMEText(cuerpo, 'plain'))

# # Añadir el archivo Excel como adjunto y definir la ruta del archivo                                                                    aqui debes pegar el archivo que copiaste en la consola
# ruta_archivo = 'C:/Users/Dell Inspiron 5000/Desktop/Proyecto Final de Algoritmos/kivy_env/SistemaTransaccionalDeVentas/admin/ventas_csv/26-10-23.csv'
# archivo = open(ruta_archivo, 'rb')
# adjunto = email.mime.base.MIMEBase('application', 'octet-stream')
# adjunto.set_payload((archivo).read())
# email.encoders.encode_base64(adjunto)
# adjunto.add_header('Content-Disposition', "attachment; filename= %s" % ruta_archivo)
# mensaje.attach(adjunto)

# # Convertir el mensaje a texto plano
# texto = mensaje.as_string()

# # Enviar el correo electrónico
# server.sendmail(remitente, destinatario, texto)

# # Cerrar la conexión SMTP
# server.quit()



# # smpt_objeto = smtplib.SMTP("smtp.gmail.com", 587)
# # contrasenia = os.getenv('GOOGLE_APP_PASS')
# # usuario = os.getenv('GOOGLE_APP_EMAIL')

# # def enviar_correo(asunto, mensaje, destinatario):
# #     smpt_objeto.starttls()
# #     smpt_objeto.login(usuario, contrasenia)
# #     smpt_objeto.sendmail("Notificaciones Algoritmos", destinatario, f"Subject: {asunto} \n{mensaje}" )
# # enviar_correo("Te saludo desde python", "Hola como estas", "llimap5@miumg.edu.gt")
