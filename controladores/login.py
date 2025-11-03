import hashlib
from conexion import conectarbd
from flask import session

def validar_docente(correo, password):
    try:
        connection = conectarbd()
        if connection:
            cursor = connection.cursor()
        
            query = "SELECT * FROM Docente WHERE correo = %s"
            cursor.execute(query, (correo,))
            result = cursor.fetchone()  # Obtener el primer resultado

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
