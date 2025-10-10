from conexion import conectarbd

def validar_docente(correo, password):
    try:
        
        connection = conectarbd()
        if connection:
            cursor = connection.cursor()
            
            query = "SELECT * FROM Docente WHERE correo = %s AND password = %s"
            cursor.execute(query, (correo, password))
            result = cursor.fetchone()  

            connection.close()
            return result
        else:
            return None
    except Exception as e:
        return None
