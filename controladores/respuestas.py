import conexion
from conexion import conectarbd

def registrar_respuesta(id_usuario, id_pregunta, id_alternativa, tiempo_utilizado):
    conexion = conectarbd()
    if not conexion:
        print("Error de conexión a la base de datos")
        return 0

    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
                SELECT puntaje, tiempo_respuesta 
                FROM Pregunta 
                WHERE id_pregunta = %s
            """, (id_pregunta,))
            pregunta = cursor.fetchone()
            if not pregunta:
                return 0
            
            cursor.execute("""
                SELECT estado_alternativa 
                FROM Alternativa 
                WHERE id_alternativa = %s
            """, (id_alternativa,))
            alternativa = cursor.fetchone()
            if not alternativa:
                return 0

            base = pregunta['puntaje']
            tiempo_respuesta = pregunta['tiempo_respuesta']
            es_correcta = alternativa['estado_alternativa'] == 1

            if es_correcta:
                bonus = max(0, ((tiempo_respuesta - tiempo_utilizado) / tiempo_respuesta) * 0.5)
                puntos = round(base * (1 + bonus), 2)
            else:
                puntos = round(-base / 2, 2)

            cursor.execute("""
                UPDATE Usuario 
                SET puntaje = puntaje + %s 
                WHERE id_usuario = %s
            """, (puntos, id_usuario))

            conexion.commit()
            return puntos

    except Exception as e:
        print("Error al registrar respuesta:", e)
        return 0

    finally:
        conexion.close()
