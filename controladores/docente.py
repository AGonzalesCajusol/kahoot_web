import hashlib
import os
import base64
from datetime import datetime
from flask import jsonify
from conexion import conectarbd
from hashlib import sha256
import pymysql


def validar_docente(correo, password):
    try:
        connection = conectarbd()
        if not connection:
            return None

        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()  
        with connection.cursor() as cursor:
            query = "SELECT * FROM Docente WHERE correo = %s AND password = %s"
            cursor.execute(query, (correo, hashed_password))
            result = cursor.fetchone()

        connection.close()
        return result

    except Exception as e:
        print("Error en validar_docente:", e)
        return None

    

def correo_disponible(correo):
    try:
        connection = conectarbd()
        if not connection:
            return False
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_docente FROM Docente WHERE correo = %s", (correo,))
            if cursor.fetchone():
                return False
            cursor.execute("SELECT id_jugador FROM Jugador WHERE email = %s", (correo,))
            if cursor.fetchone():
                return False
        
        connection.close()
        return True
    except Exception as e:
        print("Error en correo_disponible:", e)
        return False
    
def guardar_rostro_archivo(rostro_base64, correo, tipo_usuario='docente'):
    """
    Guarda una imagen de rostro como archivo en lugar de base64 en la BD
    Args:
        rostro_base64: Imagen en formato base64 (data:image/jpeg;base64,...)
        correo: Correo del usuario para generar nombre único
        tipo_usuario: 'docente' o 'jugador'
    Returns:
        Ruta relativa del archivo guardado o None si hay error
    """
    try:
        if not rostro_base64:
            return None

        # Extraer datos base64
        if ',' in rostro_base64:
            header, data = rostro_base64.split(',', 1)
        else:
            data = rostro_base64
            header = 'data:image/jpeg;base64'

        # Crear directorio si no existe
        upload_dir = 'static/uploads/reconocimiento_facial'
        os.makedirs(upload_dir, exist_ok=True)

        # Generar nombre único para el archivo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_correo = correo.replace('@', '_at_').replace('.', '_')[:30]
        filename = f"{tipo_usuario}_{safe_correo}_{timestamp}.jpg"
        filepath = os.path.join(upload_dir, filename)

        # Decodificar y guardar
        image_data = base64.b64decode(data)
        with open(filepath, 'wb') as f:
            f.write(image_data)

        return f"uploads/reconocimiento_facial/{filename}"
    except Exception as e:
        return None

def registrar_docente(correo, password, nombres, apellidos, rostro=None):
    """
    Registra un nuevo docente
    Args:
        correo: Correo electrónico del docente
        password: Contraseña en texto plano
        nombres: Nombres del docente
        apellidos: Apellidos del docente
        rostro: Datos faciales en base64 (opcional). Si se proporciona, se guarda como archivo.
    """
    try:
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        connection = conectarbd()
        if connection:
            cursor = connection.cursor()

            if rostro:
                rostro_path = guardar_rostro_archivo(rostro, correo, 'docente')
                if rostro_path:
                    query = "INSERT INTO Docente (correo, password, nombres, apellidos, rostro) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(query, (correo, hashed_password, nombres, apellidos, rostro_path))
                else:
                    query = "INSERT INTO Docente (correo, password, nombres, apellidos, rostro) VALUES (%s, %s, %s, %s, NULL)"
                    cursor.execute(query, (correo, hashed_password, nombres, apellidos))
            else:
                query = "INSERT INTO Docente (correo, password, nombres, apellidos, rostro) VALUES (%s, %s, %s, %s, NULL)"
                cursor.execute(query, (correo, hashed_password, nombres, apellidos))
            
            connection.commit()
            connection.close()
            return "Docente registrado exitosamente"  
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

def registrar_jugador(email, password, rostro=None):
    """
    Registra un nuevo jugador
    Args:
        email: Correo electrónico del jugador
        password: Contraseña en texto plano
        rostro: Datos faciales en base64 (opcional). Si se proporciona, se guarda como archivo.
    """
    try:
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        connection = conectarbd()
        if connection:
            cursor = connection.cursor()
            
            if rostro:
                rostro_path = guardar_rostro_archivo(rostro, email, 'jugador')
                if rostro_path:
                    query = "INSERT INTO Jugador (email, contraseña, rostro) VALUES (%s, %s, %s)"
                    cursor.execute(query, (email, hashed_password, rostro_path))
                else:
                    query = "INSERT INTO Jugador (email, contraseña) VALUES (%s, %s)"
                    cursor.execute(query, (email, hashed_password))
            else:
                query = "INSERT INTO Jugador (email, contraseña) VALUES (%s, %s)"
                cursor.execute(query, (email, hashed_password))
            
            connection.commit()
            connection.close()
            return "Jugador registrado exitosamente"
        else:
            return "Error al conectar con la base de datos"
    except Exception as e:
        return f"Error al registrar jugador: {str(e)}"

def obtener_docentes():
    """
    Obtiene todos los docentes de la base de datos
    Retorna una lista de tuplas con los datos de los docentes
    """
    try:
        connection = conectarbd()
        if not connection:
            return []
        
        with connection.cursor() as cursor:
            query = "SELECT id_docente, correo, password, nombres, apellidos, rostro FROM Docente ORDER BY id_docente"
            cursor.execute(query)
            resultados = cursor.fetchall()
        
        connection.close()
        return resultados
    except Exception as e:
        print(f"Error en obtener_docentes: {e}")
        return []

def obtener_docente_por_id(id_docente):
    """
    Obtiene un docente por su ID
    Retorna una tupla con los datos del docente o None si no existe
    """
    try:
        connection = conectarbd()
        if not connection:
            return None
        
        with connection.cursor() as cursor:
            query = "SELECT id_docente, correo, password, nombres, apellidos, rostro FROM Docente WHERE id_docente = %s"
            cursor.execute(query, (id_docente,))
            resultado = cursor.fetchone()
        
        connection.close()
        return resultado
    except Exception as e:
        print(f"Error en obtener_docente_por_id: {e}")
        return None

def obtener_docente_por_email(correo):
    """
    Obtiene un docente por su correo
    Retorna una tupla con los datos del docente o None si no existe
    """
    try:
        connection = conectarbd()
        if not connection:
            return None
        
        with connection.cursor() as cursor:
            query = "SELECT id_docente, correo, password, nombres, apellidos FROM Docente WHERE correo = %s"
            cursor.execute(query, (correo,))
            resultado = cursor.fetchone()
        
        connection.close()
        return resultado
    except Exception as e:
        print(f"Error en obtener_docente_por_email: {e}")
        return None

def insertar_docente(correo, password, nombres, apellidos):
    """
    Inserta un nuevo docente en la base de datos
    Retorna True si se insertó correctamente, False en caso contrario
    """
    try:
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        connection = conectarbd()
        if not connection:
            return False
        
        cursor = connection.cursor()
        query = "INSERT INTO Docente (correo, password, nombres, apellidos) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (correo, hashed_password, nombres, apellidos))
        connection.commit()
        connection.close()
        return True
    except Exception as e:
        print(f"Error en insertar_docente: {e}")
        return False

def actualizar_docente(id_docente, correo=None, password=None, nombres=None, apellidos=None, rostro=None):
    """
    Actualiza los datos de un docente
    El parámetro rostro se mantiene por compatibilidad pero ya no se usa (reconocimiento facial deshabilitado)
    Retorna True si se actualizó correctamente, False en caso contrario
    """
    try:
        connection = conectarbd()
        if not connection:
            return False
        
        cursor = connection.cursor()
        
        # Construir la query dinámicamente según los campos proporcionados
        # Nota: rostro ya no se actualiza, se ignora si se proporciona
        update_fields = []
        params = []
        
        if correo is not None:
            update_fields.append("correo = %s")
            params.append(correo)
        
        if password is not None:
            hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            update_fields.append("password = %s")
            params.append(hashed_password)
        
        if nombres is not None:
            update_fields.append("nombres = %s")
            params.append(nombres)
        
        if apellidos is not None:
            update_fields.append("apellidos = %s")
            params.append(apellidos)
        
        # rostro ya no se actualiza (reconocimiento facial deshabilitado)
        
        if not update_fields:
            connection.close()
            return False
        
        query = "UPDATE Docente SET " + ", ".join(update_fields) + " WHERE id_docente = %s"
        params.append(id_docente)
        
        cursor.execute(query, tuple(params))
        connection.commit()
        connection.close()
        return True
    except Exception as e:
        print(f"Error en actualizar_docente: {e}")
        return False

def eliminar_docente(id_docente):
    """
    Elimina un docente de la base de datos
    Retorna True si se eliminó correctamente, False en caso contrario
    """
    try:
        connection = conectarbd()
        if not connection:
            return False
        
        cursor = connection.cursor()
        query = "DELETE FROM Docente WHERE id_docente = %s"
        cursor.execute(query, (id_docente,))
        connection.commit()
        connection.close()
        return True
    except Exception as e:
        print(f"Error en eliminar_docente: {e}")
        return False
