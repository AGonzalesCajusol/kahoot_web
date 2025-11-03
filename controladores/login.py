import hashlib
from conexion import conectarbd
from flask import session
from controladores.reconocimiento_facial import verificar_rostro

def validar_docente(correo, password):
    try:
        connection = conectarbd()
        if connection:
            cursor = connection.cursor()
        
            query = "SELECT * FROM Docente WHERE correo = %s"
            cursor.execute(query, (correo,))
            result = cursor.fetchone()  

            if result:
                hashed_password = result['password']
                input_hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

                if input_hashed_password == hashed_password:
                    session['docente_id'] = result['id_docente']
                    session['correo'] = result['correo']
                    session['nombres'] = result['nombres']
                    session['apellidos'] = result['apellidos']
                    return result  
                else:
                    return None  

            connection.close()
            return None  
        
    except Exception as e:
        return None  
def login_facial(imagen_base64):
    try:
        connection = conectarbd()
        if connection:
            cursor = connection.cursor()
            query = "SELECT id_docente, correo, nombres, apellidos, rostro FROM Docente WHERE rostro IS NOT NULL"
            cursor.execute(query)
            docentes = cursor.fetchall()
            connection.close()

            for docente in docentes:
                embedding_almacenado = docente['rostro']
                
                if verificar_rostro(imagen_base64, embedding_almacenado):
                    session['docente_id'] = docente['id_docente']
                    session['correo'] = docente['correo']
                    session['nombres'] = docente['nombres']
                    session['apellidos'] = docente['apellidos']
                    return {"success": True, "message": "Inicio de sesión exitoso"}

            return {"success": False, "message": "Rostro no reconocido"}
        else:
            return {"success": False, "message": "Error al conectar con la base de datos"}

    except Exception as e:
        return {"success": False, "message": f"Ocurrió un error en el inicio de sesión facial."}
