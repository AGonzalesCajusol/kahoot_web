from conexion import conectarbd

def obtener_resultados_por_cuestionario(id_cuestionario):
    
    connection = conectarbd()
    if not connection:
        return None

    try:
        with connection.cursor() as cursor:
            query_cuestionario = """
                SELECT id_cuestionario, nombre, pin, estado_juego, fecha_programacion
                FROM Cuestionario
                WHERE id_cuestionario = %s
            """
            cursor.execute(query_cuestionario, (id_cuestionario,))
            quiz = cursor.fetchone()

            if not quiz:
                return {"error": "Cuestionario no encontrado."}

            if quiz["estado_juego"] != "FN":
                return {"error": "El cuestionario aún no ha finalizado."}

            query_usuarios = """
                SELECT alias, puntaje
                FROM Usuario
                WHERE id_cuestionario = %s
                ORDER BY puntaje DESC, alias ASC
            """
            cursor.execute(query_usuarios, (id_cuestionario,))
            usuarios = cursor.fetchall()

            top3 = usuarios[:3]
            resto = usuarios[3:]

            return {
                "quiz": quiz,
                "top3": top3,
                "participantes": resto
            }

    except Exception as e:
        print("❌ Error al obtener resultados:", e)
        return {"error": "Error interno del servidor."}

    finally:
        connection.close()
