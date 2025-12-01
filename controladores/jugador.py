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


def obtener_jugador_por_email(email):
    """
    Obtiene un jugador por su email
    Retorna una tupla con los datos del jugador o None si no existe
    Formato: (id_jugador, email, contraseña, ...)
    """
    try:
        connection = conectarbd()
        if not connection:
            return None
        
        with connection.cursor() as cursor:
            query = "SELECT id_jugador, email, contraseña FROM Jugador WHERE email = %s"
            cursor.execute(query, (email,))
            resultado = cursor.fetchone()
        
        connection.close()
        return resultado
    except Exception as e:
        print(f"Error en obtener_jugador_por_email: {e}")
        return None

def obtener_jugador_por_id(id_jugador):
    """
    Obtiene un jugador por su ID
    Retorna una tupla con los datos del jugador o None si no existe
    Formato: (id_jugador, email, contraseña, ...)
    """
    try:
        connection = conectarbd()
        if not connection:
            return None
        
        with connection.cursor() as cursor:
            query = "SELECT id_jugador, email, contraseña FROM Jugador WHERE id_jugador = %s"
            cursor.execute(query, (id_jugador,))
            resultado = cursor.fetchone()
        
        connection.close()
        return resultado
    except Exception as e:
        print(f"Error en obtener_jugador_por_id: {e}")
        return None

def obtener_cuestionarios_jugador(id_jugador):
    """
    Retorna la lista de cuestionarios que un jugador ha jugado,
    incluyendo puntaje y fecha de participación.
    Busca por id_jugador en la tabla Jugador_Cuestionario.
    """
    connection = conectarbd()
    if not connection:
        return []

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    jc.id_cuestionario,
                    jc.alias,
                    jc.puntaje,
                    jc.fecha_participacion AS fecha_registro,
                    c.nombre AS nombre_cuestionario,
                    c.pin,
                    c.tipo_cuestionario
                FROM Jugador_Cuestionario jc
                INNER JOIN Cuestionario c ON jc.id_cuestionario = c.id_cuestionario
                WHERE jc.id_jugador = %s
                ORDER BY jc.fecha_participacion DESC
            """, (id_jugador,))
            resultados = cursor.fetchall()
            return resultados
    except Exception as e:
        print("Error al obtener cuestionarios del jugador:", e)
        import traceback
        traceback.print_exc()
        return []
    finally:
        if connection:
            connection.close()

def obtener_jugadores():
    """Obtiene todos los jugadores"""
    try:
        connection = conectarbd()
        if not connection:
            return []
        
        with connection.cursor() as cursor:
            query = "SELECT id_jugador, email, contraseña FROM Jugador ORDER BY id_jugador"
            cursor.execute(query)
            resultados = cursor.fetchall()
        
        connection.close()
        return resultados
    except Exception as e:
        print(f"Error en obtener_jugadores: {e}")
        return []

def insertar_jugador(email, password):
    """Inserta un nuevo jugador"""
    try:
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        connection = conectarbd()
        if not connection:
            return False
        
        cursor = connection.cursor()
        query = "INSERT INTO Jugador (email, contraseña) VALUES (%s, %s)"
        cursor.execute(query, (email, hashed_password))
        connection.commit()
        connection.close()
        return True
    except Exception as e:
        print(f"Error en insertar_jugador: {e}")
        return False

def actualizar_jugador(id_jugador, email=None, password=None):
    """Actualiza un jugador"""
    try:
        connection = conectarbd()
        if not connection:
            return False
        
        cursor = connection.cursor()
        update_fields = []
        params = []
        
        if email is not None:
            update_fields.append("email = %s")
            params.append(email)
        
        if password is not None:
            hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            update_fields.append("contraseña = %s")
            params.append(hashed_password)
        
        if not update_fields:
            connection.close()
            return False
        
        query = "UPDATE Jugador SET " + ", ".join(update_fields) + " WHERE id_jugador = %s"
        params.append(id_jugador)
        
        cursor.execute(query, tuple(params))
        connection.commit()
        connection.close()
        return True
    except Exception as e:
        print(f"Error en actualizar_jugador: {e}")
        return False

def eliminar_jugador(id_jugador):
    """Elimina un jugador"""
    try:
        connection = conectarbd()
        if not connection:
            return False
        
        cursor = connection.cursor()
        query = "DELETE FROM Jugador WHERE id_jugador = %s"
        cursor.execute(query, (id_jugador,))
        connection.commit()
        connection.close()
        return True
    except Exception as e:
        print(f"Error en eliminar_jugador: {e}")
        return False
