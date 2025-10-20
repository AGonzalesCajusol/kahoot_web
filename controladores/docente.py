import hashlib
from conexion import conectarbd
from hashlib import sha256
import pymysql


def validar_docente(correo, password):
    try:
        connection = conectarbd()
        if not connection:
            return None

        with connection.cursor() as cursor:
            query = "SELECT * FROM Docente WHERE correo = %s AND password = %s"
            cursor.execute(query, (correo, password))
            result = cursor.fetchone()

        connection.close()
        return result

    except Exception as e:
        # opcional: print(e) para depuración
        return None
    

def registrar_docente(correo, password, nombres, apellidos):
    try:
        # Hash de la contraseña utilizando SHA-256
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        # Conectar a la base de datos y registrar el docente
        connection = conectarbd()
        if connection:
            cursor = connection.cursor()

            # Insertar los datos del docente en la base de datos
            query = "INSERT INTO Docente (correo, password, nombres, apellidos) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (correo, hashed_password, nombres, apellidos))
            connection.commit()  # Guardar los cambios
            connection.close()
            return "Docente registrado exitosamente"  # Mensaje de éxito
        else:
            return "Error al conectar con la base de datos"

    except Exception as e:
        return f"Error al registrar el docente: {str(e)}"
        