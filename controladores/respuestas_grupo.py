import conexion
from conexion import conectarbd
import logging

logger = logging.getLogger(__name__)

def registrar_respuesta_grupo(id_grupo, id_pregunta, id_alternativa, tiempo_utilizado):
    """
    Registra la respuesta final del grupo para una pregunta
    Esta respuesta se determina según el método de evaluación del grupo
    """
    if not id_grupo or not id_pregunta or not id_alternativa:
        logger.error(f"Parámetros inválidos: id_grupo={id_grupo}, id_pregunta={id_pregunta}, id_alternativa={id_alternativa}")
        return 0
    
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
            tiempo_maximo = int(pregunta['tiempo_respuesta']) if pregunta['tiempo_respuesta'] else 0
            es_correcta = alternativa['estado_alternativa'] == 1
            
            # Calcular puntos con bonus por tiempo de respuesta (igual que respuestas individuales)
            if es_correcta:
                tiempo_restante = max(0, tiempo_maximo - tiempo_utilizado)
                porcentaje_tiempo_restante = tiempo_restante / tiempo_maximo if tiempo_maximo > 0 else 0
                bonus_por_tiempo = base * porcentaje_tiempo_restante * 0.5
                puntos = round(base + bonus_por_tiempo, 2)
            else:
                puntos = 0

            # Guardar o actualizar la respuesta del grupo
            cursor.execute("""
                INSERT INTO RespuestaGrupo (id_grupo, id_pregunta, id_alternativa, tiempo_utilizado, fecha_respuesta)
                VALUES (%s, %s, %s, %s, NOW())
                ON DUPLICATE KEY UPDATE
                    id_alternativa = VALUES(id_alternativa),
                    tiempo_utilizado = VALUES(tiempo_utilizado),
                    fecha_respuesta = NOW()
            """, (id_grupo, id_pregunta, id_alternativa, tiempo_utilizado))
            
            # Actualizar el puntaje del grupo (suma de todas las respuestas correctas con bonus por tiempo)
            cursor.execute("""
                UPDATE Grupo 
                SET puntaje = (
                    SELECT COALESCE(SUM(
                        CASE 
                            WHEN a.estado_alternativa = 1 THEN
                                p.puntaje + (p.puntaje * GREATEST(0, p.tiempo_respuesta - rg.tiempo_utilizado) / p.tiempo_respuesta * 0.5)
                            ELSE 0
                        END
                    ), 0)
                    FROM RespuestaGrupo rg
                    INNER JOIN Pregunta p ON rg.id_pregunta = p.id_pregunta
                    INNER JOIN Alternativa a ON rg.id_alternativa = a.id_alternativa
                    WHERE rg.id_grupo = %s
                )
                WHERE id_grupo = %s
            """, (id_grupo, id_grupo))
            
            conexion_db.commit()
            logger.info(f"Respuesta del grupo {id_grupo} registrada: {puntos} puntos")
            return puntos
            
    except Exception as e:
        if conexion_db:
            conexion_db.rollback()
        logger.error(f"Error al registrar respuesta del grupo: {e}")
        import traceback
        traceback.print_exc()
        return 0
    finally:
        if conexion_db:
            conexion_db.close()

def obtener_votaciones_grupo(id_grupo, id_pregunta):
    """
    Obtiene todas las votaciones de los miembros del grupo para una pregunta
    Retorna un diccionario con id_alternativa como clave y cantidad de votos como valor
    """
    conexion_db = conectarbd()
    if not conexion_db:
        return {}
    
    try:
        with conexion_db.cursor() as cursor:
            cursor.execute("""
                SELECT id_alternativa, COUNT(*) as votos
                FROM VotacionGrupo
                WHERE id_grupo = %s AND id_pregunta = %s
                GROUP BY id_alternativa
            """, (id_grupo, id_pregunta))
            
            resultados = cursor.fetchall()
            votaciones = {}
            for row in resultados:
                votaciones[row['id_alternativa']] = row['votos']
            
            return votaciones
    except Exception as e:
        logger.error(f"Error al obtener votaciones del grupo: {e}")
        return {}
    finally:
        if conexion_db:
            conexion_db.close()

def registrar_votacion_miembro(id_grupo, id_pregunta, id_jugador_cuestionario, id_alternativa):
    """
    Registra la votación de un miembro del grupo para una pregunta
    """
    conexion_db = conectarbd()
    if not conexion_db:
        return False
    
    try:
        with conexion_db.cursor() as cursor:
            # Verificar que el jugador es miembro del grupo
            cursor.execute("""
                SELECT id_miembro FROM GrupoMiembro
                WHERE id_grupo = %s AND id_jugador_cuestionario = %s
            """, (id_grupo, id_jugador_cuestionario))
            
            if not cursor.fetchone():
                logger.warning(f"Jugador {id_jugador_cuestionario} no es miembro del grupo {id_grupo}")
                return False
            
            # Registrar o actualizar la votación
            cursor.execute("""
                INSERT INTO VotacionGrupo (id_grupo, id_pregunta, id_jugador_cuestionario, id_alternativa, fecha_votacion)
                VALUES (%s, %s, %s, %s, NOW())
                ON DUPLICATE KEY UPDATE
                    id_alternativa = VALUES(id_alternativa),
                    fecha_votacion = NOW()
            """, (id_grupo, id_pregunta, id_jugador_cuestionario, id_alternativa))
            
            conexion_db.commit()
            return True
    except Exception as e:
        if conexion_db:
            conexion_db.rollback()
        logger.error(f"Error al registrar votación: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if conexion_db:
            conexion_db.close()

def determinar_respuesta_grupo(id_grupo, id_pregunta, metodo_evaluacion):
    """
    Determina la respuesta final del grupo según el método de evaluación
    Retorna el id_alternativa seleccionado o None si no se puede determinar
    """
    conexion_db = conectarbd()
    if not conexion_db:
        return None
    
    try:
        with conexion_db.cursor() as cursor:
            # Obtener todas las votaciones
            votaciones = obtener_votaciones_grupo(id_grupo, id_pregunta)
            
            if not votaciones:
                return None
            
            # Obtener número total de miembros del grupo
            cursor.execute("""
                SELECT COUNT(*) as total_miembros
                FROM GrupoMiembro
                WHERE id_grupo = %s
            """, (id_grupo,))
            resultado = cursor.fetchone()
            total_miembros = resultado['total_miembros'] if resultado else 0
            
            if total_miembros == 0:
                return None
            
            if metodo_evaluacion == 'votacion':
                # Mayoría simple: la alternativa con más votos
                if votaciones:
                    alternativa_ganadora = max(votaciones.items(), key=lambda x: x[1])
                    return alternativa_ganadora[0]
            
            elif metodo_evaluacion == 'consenso':
                # Unanimidad: todos deben votar por la misma alternativa
                if len(votaciones) == 1:
                    alternativa, votos = list(votaciones.items())[0]
                    if votos == total_miembros:
                        return alternativa
                return None
            
            elif metodo_evaluacion == 'lider':
                # Decisión del líder
                cursor.execute("""
                    SELECT id_lider FROM Grupo WHERE id_grupo = %s
                """, (id_grupo,))
                grupo = cursor.fetchone()
                if grupo:
                    id_lider = grupo['id_lider']
                    cursor.execute("""
                        SELECT id_alternativa FROM VotacionGrupo
                        WHERE id_grupo = %s AND id_pregunta = %s AND id_jugador_cuestionario = %s
                    """, (id_grupo, id_pregunta, id_lider))
                    voto_lider = cursor.fetchone()
                    if voto_lider:
                        return voto_lider['id_alternativa']
            
            return None
    except Exception as e:
        logger.error(f"Error al determinar respuesta del grupo: {e}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        if conexion_db:
            conexion_db.close()

