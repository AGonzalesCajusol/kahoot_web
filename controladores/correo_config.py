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
