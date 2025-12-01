import conexion
from conexion import conectarbd
import logging

logger = logging.getLogger(__name__)

def registrar_respuesta(id_jugador_cuestionario, id_pregunta, id_alternativa, tiempo_utilizado):
    # NOTA: id_jugador_cuestionario ahora se refiere a Jugador_Cuestionario.id_jugador_cuestionario
    # Validar que todos los parámetros sean válidos
    if not id_jugador_cuestionario or not id_pregunta or not id_alternativa:
        logger.error(f"Parámetros inválidos: id_jugador_cuestionario={id_jugador_cuestionario}, id_pregunta={id_pregunta}, id_alternativa={id_alternativa}")
        return 0
    
    # Asegurar que tiempo_utilizado sea un entero
    if tiempo_utilizado is None:
        tiempo_utilizado = 0
    try:
        tiempo_utilizado = int(tiempo_utilizado)
    except (ValueError, TypeError):
        tiempo_utilizado = 0
    
    conexion_db = conectarbd()
    if not conexion_db:
        logger.error("No se pudo conectar a la base de datos")
        return 0

    try:
        with conexion_db.cursor() as cursor:
            # Validar que la pregunta existe
            cursor.execute("""
                SELECT puntaje, tiempo_respuesta 
                FROM Pregunta 
                WHERE id_pregunta = %s
            """, (id_pregunta,))
            pregunta = cursor.fetchone()
            if not pregunta:
                logger.error(f"Pregunta {id_pregunta} no encontrada")
                return 0
            
            # Validar que la alternativa existe
            cursor.execute("""
                SELECT estado_alternativa 
                FROM Alternativa 
                WHERE id_alternativa = %s
            """, (id_alternativa,))
            alternativa = cursor.fetchone()
            if not alternativa:
                logger.error(f"Alternativa {id_alternativa} no encontrada")
                return 0

            base = float(pregunta['puntaje']) if pregunta['puntaje'] is not None else 0.0
            tiempo_maximo = int(pregunta['tiempo_respuesta']) if pregunta['tiempo_respuesta'] is not None else 30
            es_correcta = alternativa['estado_alternativa'] == 1
            
            # Calcular puntos con bonus por tiempo de respuesta
            if es_correcta:
                # Calcular tiempo restante
                tiempo_restante = max(0, tiempo_maximo - tiempo_utilizado)
                
                # Bonus por tiempo: cuanto más rápido responda, más bonus recibe
                # El bonus es un porcentaje del tiempo restante sobre el tiempo máximo
                # Máximo bonus: 50% del puntaje base (si responde instantáneamente)
                # Mínimo bonus: 0% (si usa todo el tiempo)
                porcentaje_tiempo_restante = tiempo_restante / tiempo_maximo if tiempo_maximo > 0 else 0
                bonus_por_tiempo = base * porcentaje_tiempo_restante * 0.5  # Máximo 50% de bonus
                
                # Puntos totales = puntos base + bonus por tiempo
                puntos = round(base + bonus_por_tiempo, 2)
            else:
                puntos = 0

            # Guardar la respuesta en la tabla Respuesta
            logger.info(f"Intentando guardar respuesta: jugador_cuestionario={id_jugador_cuestionario}, pregunta={id_pregunta}, alternativa={id_alternativa}, tiempo={tiempo_utilizado}")
            
            try:
                # Verificar si ya existe una respuesta para este jugador_cuestionario y pregunta
                cursor.execute("""
                    SELECT id_respuesta FROM Respuesta
                    WHERE id_jugador_cuestionario = %s AND id_pregunta = %s
                """, (id_jugador_cuestionario, id_pregunta))
                respuesta_existente = cursor.fetchone()
                
                if respuesta_existente:
                    # Actualizar respuesta existente
                    cursor.execute("""
                        UPDATE Respuesta 
                        SET id_alternativa = %s,
                            tiempo_utilizado = %s,
                            fecha_respuesta = CURRENT_TIMESTAMP
                        WHERE id_jugador_cuestionario = %s AND id_pregunta = %s
                    """, (id_alternativa, tiempo_utilizado, id_jugador_cuestionario, id_pregunta))
                    logger.info(f"UPDATE ejecutado para respuesta existente. Filas afectadas: {cursor.rowcount}")
                else:
                    # Insertar nueva respuesta
                    cursor.execute("""
                        INSERT INTO Respuesta (id_jugador_cuestionario, id_pregunta, id_alternativa, tiempo_utilizado)
                        VALUES (%s, %s, %s, %s)
                    """, (id_jugador_cuestionario, id_pregunta, id_alternativa, tiempo_utilizado))
                    logger.info(f"INSERT ejecutado. Filas afectadas: {cursor.rowcount}")
                
                # Hacer commit inmediatamente después del INSERT/UPDATE
                conexion_db.commit()
                logger.info("Commit realizado después de guardar respuesta")
                
                # Verificar que la respuesta se guardó correctamente
                cursor.execute("""
                    SELECT id_respuesta, id_jugador_cuestionario, id_pregunta, id_alternativa, tiempo_utilizado, fecha_respuesta
                    FROM Respuesta
                    WHERE id_jugador_cuestionario = %s AND id_pregunta = %s
                """, (id_jugador_cuestionario, id_pregunta))
                respuesta_guardada = cursor.fetchone()
                if respuesta_guardada:
                    logger.info(f"✅ Respuesta verificada en BD: id_respuesta={respuesta_guardada.get('id_respuesta')}, alternativa={respuesta_guardada.get('id_alternativa')}")
                else:
                    logger.error("❌ La respuesta NO se encontró después del INSERT/UPDATE y commit")
                    raise Exception("La respuesta no se guardó correctamente en la base de datos")
                    
            except Exception as insert_error:
                logger.error(f"Error al ejecutar INSERT/UPDATE: {insert_error}", exc_info=True)
                conexion_db.rollback()
                raise
            
            # Recalcular el puntaje total del usuario basado en todas sus respuestas con bonus por tiempo
            cursor.execute("""
                SELECT 
                    r.id_pregunta,
                    p.puntaje as puntaje_pregunta,
                    p.tiempo_respuesta as tiempo_maximo,
                    r.tiempo_utilizado,
                    a.estado_alternativa
                FROM Respuesta r
                INNER JOIN Alternativa a ON r.id_alternativa = a.id_alternativa
                INNER JOIN Pregunta p ON r.id_pregunta = p.id_pregunta
                WHERE r.id_jugador_cuestionario = %s
                ORDER BY r.id_pregunta
            """, (id_jugador_cuestionario,))
            todas_respuestas_jugador = cursor.fetchall()
            
            puntaje_total = 0.0
            for resp in todas_respuestas_jugador:
                if resp['estado_alternativa'] == 1:
                    puntaje_base = float(resp['puntaje_pregunta']) if resp['puntaje_pregunta'] is not None else 0.0
                    tiempo_max = int(resp['tiempo_maximo']) if resp['tiempo_maximo'] is not None else 30
                    tiempo_usado = int(resp['tiempo_utilizado']) if resp['tiempo_utilizado'] is not None else tiempo_max
                    
                    # Calcular bonus por tiempo
                    tiempo_restante = max(0, tiempo_max - tiempo_usado)
                    porcentaje_tiempo_restante = tiempo_restante / tiempo_max if tiempo_max > 0 else 0
                    bonus_por_tiempo = puntaje_base * porcentaje_tiempo_restante * 0.5  # Máximo 50% de bonus
                    
                    # Sumar puntos base + bonus
                    puntaje_total += puntaje_base + bonus_por_tiempo
            
            puntaje_total = min(round(puntaje_total, 2), 999.99)
            
            # Verificar que el jugador_cuestionario existe antes de actualizar
            cursor.execute("""
                SELECT id_jugador_cuestionario, alias, puntaje 
                FROM Jugador_Cuestionario 
                WHERE id_jugador_cuestionario = %s
            """, (id_jugador_cuestionario,))
            jugador_antes = cursor.fetchone()
            if not jugador_antes:
                logger.warning(f"Jugador_Cuestionario {id_jugador_cuestionario} no encontrado para actualizar puntaje")
                return puntos
            
            # Actualizar el puntaje total del jugador_cuestionario
            cursor.execute("""
                UPDATE Jugador_Cuestionario 
                SET puntaje = CAST(%s AS DECIMAL(5,2))
                WHERE id_jugador_cuestionario = %s
            """, (puntaje_total, id_jugador_cuestionario))
            
            logger.info(f"Puntaje actualizado: jugador_cuestionario={id_jugador_cuestionario}, puntaje={puntaje_total}")

            conexion_db.commit()
            logger.info(f"✅ Commit final realizado exitosamente. Puntos obtenidos: {puntos}")
            return puntos

    except Exception as e:
        logger.error(f"Error al registrar respuesta: {e}", exc_info=True)
        if conexion_db:
            try:
                conexion_db.rollback()
                logger.info("Rollback realizado")
            except Exception as rollback_error:
                logger.error(f"Error al hacer rollback: {rollback_error}")
        return 0

    finally:
        if conexion_db:
            try:
                conexion_db.close()
            except Exception as close_error:
                logger.error(f"Error al cerrar conexión: {close_error}")

def obtener_estadisticas_respuestas(id_pregunta, id_cuestionario):
    """
    Obtiene estadísticas de respuestas por alternativa para una pregunta.
    Retorna un diccionario con el porcentaje de respuestas por alternativa.
    """
    connection = None
    try:
        connection = conectarbd()
        if not connection:
            return {'estado': False, 'mensaje': 'Error al conectar con la base de datos'}
        
        cursor = connection.cursor()
        
        if isinstance(id_cuestionario, str):
            try:
                id_cuestionario = int(id_cuestionario)
            except ValueError:
                return {'estado': False, 'mensaje': 'ID de cuestionario inválido'}
        
        if isinstance(id_pregunta, str):
            try:
                id_pregunta = int(id_pregunta)
            except ValueError:
                return {'estado': False, 'mensaje': 'ID de pregunta inválido'}
        
        # Obtener total de participantes del cuestionario
        cursor.execute("""
            SELECT COUNT(*) as total_participantes
            FROM Jugador_Cuestionario
            WHERE id_cuestionario = %s
        """, (id_cuestionario,))
        total_result = cursor.fetchone()
        total_participantes = total_result['total_participantes'] if total_result else 0
        
        # Obtener todas las alternativas de la pregunta
        cursor.execute("""
            SELECT id_alternativa, respuesta, estado_alternativa
            FROM Alternativa
            WHERE id_pregunta = %s
            ORDER BY id_alternativa
        """, (id_pregunta,))
        alternativas = cursor.fetchall()
        
        # Obtener conteo de respuestas únicas por alternativa
        cursor.execute("""
            SELECT 
                a.id_alternativa,
                a.respuesta,
                a.estado_alternativa,
                COUNT(DISTINCT r.id_jugador_cuestionario) as cantidad_respuestas
            FROM Alternativa a
            LEFT JOIN Respuesta r ON a.id_alternativa = r.id_alternativa 
                AND r.id_pregunta = %s
            WHERE a.id_pregunta = %s
            GROUP BY a.id_alternativa, a.respuesta, a.estado_alternativa
            ORDER BY a.id_alternativa
        """, (id_pregunta, id_pregunta))
        estadisticas = cursor.fetchall()
        
        # Obtener total de respuestas únicas para esta pregunta
        cursor.execute("""
            SELECT COUNT(DISTINCT id_jugador_cuestionario) as total_respuestas_unicas
            FROM Respuesta
            WHERE id_pregunta = %s
        """, (id_pregunta,))
        total_respuestas_result = cursor.fetchone()
        total_respuestas = total_respuestas_result['total_respuestas_unicas'] if total_respuestas_result else 0
        
        # Calcular porcentajes
        resultados = []
        
        for stat in estadisticas:
            cantidad = int(stat['cantidad_respuestas']) if stat['cantidad_respuestas'] else 0
            porcentaje = (cantidad / total_participantes * 100) if total_participantes > 0 else 0
            
            resultados.append({
                'id_alternativa': stat['id_alternativa'],
                'respuesta': stat['respuesta'],
                'es_correcta': stat['estado_alternativa'] == 1,
                'cantidad': cantidad,
                'porcentaje': round(porcentaje, 1)
            })
        
        cursor.close()
        
        resultado_final = {
            'estado': True,
            'total_participantes': total_participantes,
            'total_respuestas': total_respuestas,
            'sin_respuesta': total_participantes - total_respuestas,
            'porcentaje_sin_respuesta': round(((total_participantes - total_respuestas) / total_participantes * 100) if total_participantes > 0 else 0, 1),
            'alternativas': resultados
        }
        
        return resultado_final
        
    except Exception as e:
        return {'estado': False, 'mensaje': f'Error al obtener estadísticas: {str(e)}'}
    finally:
        if connection:
            try:
                connection.close()
            except Exception:
                pass
