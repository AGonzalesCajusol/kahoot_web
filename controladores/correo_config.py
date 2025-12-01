import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


EMAIL_ORIGEN = "kahootbamba@gmail.com"
CONTRASENA_APP = "bxvj ppif kgen rxlq"

def send_email(destinatario, codigo):
    try:
        # Crear mensaje
        mensaje = MIMEMultipart()
        mensaje["From"] = EMAIL_ORIGEN
        mensaje["To"] = destinatario
        mensaje["Subject"] = "Código de verificación - GoQuiz"

        cuerpo = f"""
        <html>
        <body>
            <h3>Hola 👋</h3>
            <p>Tu código de verificación es:</p>
            <h2 style="color:#007bff;">{codigo}</h2>
            <p>Este código expirará en 10 minutos.</p>
            <hr>
            <p>GoQuiz © 2025</p>
        </body>
        </html>
        """
        mensaje.attach(MIMEText(cuerpo, "html"))

        # Conectar al servidor SMTP de Gmail
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ORIGEN, CONTRASENA_APP)
            server.sendmail(EMAIL_ORIGEN, destinatario, mensaje.as_string())

        return True
    except Exception as e:
        print("Error enviando correo:", e)
        return False

def send_contact_email(nombre, correo, asunto, mensaje):
    try:
        # Crear mensaje
        mensaje_email = MIMEMultipart()
        mensaje_email["From"] = EMAIL_ORIGEN
        mensaje_email["To"] = "mixdjangel7@gmail.com"  # Correo de destino
        mensaje_email["Subject"] = f"Contacto GoQuiz: {asunto}"
        
        # Cuerpo del mensaje
        cuerpo = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #0072ff;">Nuevo mensaje de contacto - GoQuiz</h2>
            <hr style="border: 1px solid #e0e0e0; margin: 20px 0;">
            <p><strong>Nombre:</strong> {nombre}</p>
            <p><strong>Correo:</strong> {correo}</p>
            <p><strong>Asunto:</strong> {asunto}</p>
            <hr style="border: 1px solid #e0e0e0; margin: 20px 0;">
            <h3 style="color: #2c3e50;">Mensaje:</h3>
            <p style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; white-space: pre-wrap;">{mensaje}</p>
            <hr style="border: 1px solid #e0e0e0; margin: 20px 0;">
            <p style="color: #999; font-size: 0.9em;">GoQuiz © 2025</p>
        </body>
        </html>
        """
        mensaje_email.attach(MIMEText(cuerpo, "html"))
        
        # Conectar al servidor SMTP de Gmail
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ORIGEN, CONTRASENA_APP)
            server.sendmail(EMAIL_ORIGEN, "mixdjangel7@gmail.com", mensaje_email.as_string())
        
        return True
    except Exception as e:
        print("Error enviando correo de contacto:", e)
        return False