import hashlib
from conexion import conectarbd

def validar_jugador(email, password):
    try:
        connection = conectarbd()
        if not connection:
            return None

        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        with connection.cursor() as cursor:
            query = "SELECT * FROM Jugador WHERE email = %s AND contraseña = %s"
            cursor.execute(query, (email, hashed_password))
            print("Email recibido:", email)
            print("Password hasheado:", hashed_password)

            result = cursor.fetchone()
            print("Resultado consulta:", result)


        connection.close()
        return result

    except Exception as e:
        print("Error en validar_jugador:", e)
        return None
