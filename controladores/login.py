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


def verificar_correo_existente(email):
    try:
        connection = conectarbd()
        if connection:
            cursor = connection.cursor(dictionary=True)

            query_docente = "SELECT 1 FROM Docente WHERE correo = %s LIMIT 1"
            cursor.execute(query_docente, (email,))
            existe_docente = cursor.fetchone()

            query_jugador = "SELECT 1 FROM Jugador WHERE email = %s LIMIT 1"
            cursor.execute(query_jugador, (email,))
            existe_jugador = cursor.fetchone()

            connection.close()

            if existe_docente or existe_jugador:
                return True
            else:
                return False

    except Exception as e:
        print(f"Error al verificar correo: {e}")
        return False