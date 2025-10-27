import hashlib

from flask import jsonify
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
        

def modificar_docente(correo, nuevo_nombre, nuevo_apellido, nuevo_correo=None, nueva_contrasena=None):
    try:
        connection = conectarbd()
        if not connection:
            return jsonify({"code": 0, "message": "Error al conectar con la base de datos."}), 500
        
        cursor = connection.cursor()
            
        if nuevo_correo:
            cursor.execute("SELECT * FROM Docente WHERE correo = %s", (nuevo_correo,))
            if cursor.fetchone():
                return jsonify({"code": 0, "message": "El nuevo correo ya está registrado."}), 400
        
        update_query = "UPDATE Docente SET nombres = %s, apellidos = %s"
        params = [nuevo_nombre, nuevo_apellido]
        
        if nuevo_correo:
            update_query += ", correo = %s"
            params.append(nuevo_correo)
        
        if nueva_contrasena:
            # Hash de la nueva contraseña
            hashed_password = hashlib.sha256(nueva_contrasena.encode('utf-8')).hexdigest()
            update_query += ", password = %s"
            params.append(hashed_password)
        
        update_query += " WHERE correo = %s"
        params.append(correo)
        
        cursor.execute(update_query, tuple(params))
        connection.commit()
        
        connection.close()
        
        return jsonify({"code": 1, "message": "Datos actualizados exitosamente."}), 200
        
    except Exception as e:
        print(f"Error al actualizar docente: {e}")
        return jsonify({"code": 0, "message": "Error al actualizar los datos."}), 500
