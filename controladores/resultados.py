from conexion import conectarbd

def obtener_resultados_por_cuestionario(id_cuestionario, id_jugador_cuestionario=None, id_docente=None):
    # NOTA: id_jugador_cuestionario ahora se refiere a Jugador_Cuestionario.id_jugador_cuestionario
    
    connection = conectarbd()
    if not connection:
        return {"error": "Error al conectar con la base de datos"}

    try:
        with connection.cursor() as cursor:
            # Obtener información del cuestionario (sin fecha_programacion que no existe)
            query_cuestionario = """
                SELECT id_cuestionario, nombre, pin, estado_juego, tipo_cuestionario
                FROM Cuestionario
                WHERE id_cuestionario = %s
            """
            cursor.execute(query_cuestionario, (id_cuestionario,))
            quiz = cursor.fetchone()

            if not quiz:
                print(f"❌ Cuestionario {id_cuestionario} no encontrado")
                return {"error": "Cuestionario no encontrado."}

            print(f"✅ Cuestionario encontrado: {quiz['nombre']}, estado_juego: {quiz['estado_juego']}")

            # Permitir mostrar resultados si el juego está finalizado o si está en curso (para debugging)
            # Si el juego está en curso pero queremos ver resultados, los mostramos igual
            if quiz["estado_juego"] not in ["FN", "IN"]:
                print(f"⚠️ El cuestionario aún no ha iniciado o finalizado. Estado: {quiz['estado_juego']}")
                # No bloqueamos, permitimos ver resultados aunque el juego esté en curso

            # Obtener participantes ordenados por puntaje (tipo Kahoot)
            # Si hay empates en puntaje, se ordenan por tiempo total (menor tiempo = mejor posición)
            query_usuarios = """
                SELECT 
                    jc.id_jugador_cuestionario, 
                    jc.alias, 
                    COALESCE(jc.puntaje, 0) as puntaje, 
                    jc.id_jugador,
                    COALESCE(SUM(r.tiempo_utilizado), 0) as tiempo_total
                FROM Jugador_Cuestionario jc
                LEFT JOIN Respuesta r ON jc.id_jugador_cuestionario = r.id_jugador_cuestionario
                WHERE jc.id_cuestionario = %s
                GROUP BY jc.id_jugador_cuestionario, jc.alias, jc.puntaje, jc.id_jugador
                ORDER BY COALESCE(jc.puntaje, 0) DESC, tiempo_total ASC, jc.alias ASC
            """
            cursor.execute(query_usuarios, (id_cuestionario,))
            usuarios = cursor.fetchall()
            
            print(f"[DEBUG] Jugadores encontrados: {len(usuarios) if usuarios else 0}")
            for u in usuarios:
                puntaje_valor = u.get('puntaje') or 0
                print(f"  - Jugador {u['id_jugador_cuestionario']} ({u['alias']}): {puntaje_valor} puntos")
                # Asegurar que el puntaje sea un número
                u['puntaje'] = float(puntaje_valor) if puntaje_valor is not None else 0.0
            
            # Obtener información del jugador actual si está en la sesión
            usuario_actual = None
            if id_jugador_cuestionario:
                for usuario in usuarios:
                    if usuario['id_jugador_cuestionario'] == id_jugador_cuestionario:
                        usuario_actual = usuario
                        break

            print(f"📊 Participantes encontrados: {len(usuarios) if usuarios else 0}")

            # Calcular estadísticas tipo Kahoot
            total_participantes = len(usuarios) if usuarios else 0
            # Asegurar que todos los puntajes sean números válidos
            for u in usuarios:
                if u.get('puntaje') is None:
                    u['puntaje'] = 0.0
                else:
                    try:
                        u['puntaje'] = float(u['puntaje'])
                    except (ValueError, TypeError):
                        u['puntaje'] = 0.0
            
            puntaje_maximo = float(usuarios[0]["puntaje"]) if usuarios and len(usuarios) > 0 else 0.0
            puntaje_promedio = sum(u.get("puntaje", 0) for u in usuarios) / total_participantes if total_participantes > 0 else 0.0
            
            print(f"[DEBUG] Puntaje máximo: {puntaje_maximo}, Promedio: {puntaje_promedio}")

            top3 = usuarios[:3] if usuarios else []
            resto = usuarios[3:] if usuarios else []

            print(f"🏆 Top 3: {[(u.get('alias'), u.get('puntaje')) for u in top3]}")
            print(f"📋 Resto: {len(resto)} participantes")

            # Obtener total de puntos de recompensa del cuestionario (para docente)
            total_puntos_recompensa = 0
            if id_docente:
                from controladores import recompensa
                total_puntos_recompensa = recompensa.obtener_total_puntos_recompensa_cuestionario(id_cuestionario)
            
            # Agregar estadísticas al objeto quiz
            quiz["total_participantes"] = total_participantes
            quiz["puntaje_maximo"] = round(puntaje_maximo, 2)
            quiz["puntaje_promedio"] = round(puntaje_promedio, 2)
            quiz["total_puntos_recompensa"] = total_puntos_recompensa

            # Verificar si el docente es el dueño del cuestionario
            es_docente_dueño = False
            if id_docente:
                cursor.execute("""
                    SELECT id_docente FROM Cuestionario
                    WHERE id_cuestionario = %s
                """, (id_cuestionario,))
                cuestionario_docente = cursor.fetchone()
                if cuestionario_docente and cuestionario_docente.get('id_docente') == id_docente:
                    es_docente_dueño = True

            resultado = {
                "quiz": quiz,
                "top3": top3,
                "participantes": resto,
                "usuario_actual": usuario_actual,
                "es_docente_dueño": es_docente_dueño
            }

            print(f"✅ Resultados preparados correctamente")
            return resultado

    except Exception as e:
        print(f"❌ Error al obtener resultados: {e}")
        import traceback
        traceback.print_exc()
        return {"error": f"Error interno del servidor: {str(e)}"}

    finally:
        if connection:
            connection.close()
