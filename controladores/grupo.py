import conexion
from datetime import datetime

def crear_grupo(nombre_grupo, id_cuestionario, id_lider):
    """Crea un nuevo grupo para un cuestionario
    id_lider ahora se refiere a id_jugador_cuestionario
    """
    connection = None
    try:
        connection = conexion.conectarbd()
        if not connection:
            return None, "Error al conectar con la base de datos"
        
        with connection.cursor() as cursor:
            # Verificar que el cuestionario sea grupal
            cursor.execute("""
                SELECT tipo_cuestionario FROM Cuestionario 
                WHERE id_cuestionario = %s
            """, (id_cuestionario,))
            cuestionario = cursor.fetchone()
            
            if not cuestionario:
                return None, "Cuestionario no encontrado"
            
            if cuestionario.get('tipo_cuestionario') != 'G':
                return None, "Este cuestionario no es grupal"
            
            # Verificar que el líder existe en Jugador_Cuestionario
            cursor.execute("""
                SELECT id_jugador_cuestionario FROM Jugador_Cuestionario
                WHERE id_jugador_cuestionario = %s AND id_cuestionario = %s
            """, (id_lider, id_cuestionario))
            jugador = cursor.fetchone()
            
            if not jugador:
                return None, "Debes estar registrado en el cuestionario primero"
            
            # Verificar que el líder no esté ya en otro grupo de este cuestionario
            cursor.execute("""
                SELECT gm.id_grupo FROM GrupoMiembro gm
                INNER JOIN Grupo g ON gm.id_grupo = g.id_grupo
                WHERE gm.id_jugador_cuestionario = %s AND g.id_cuestionario = %s
            """, (id_lider, id_cuestionario))
            grupo_existente = cursor.fetchone()
            
            if grupo_existente:
                return None, "Ya estás en un grupo para este cuestionario"
            
            # Crear el grupo
            cursor.execute("""
                INSERT INTO Grupo (nombre_grupo, id_cuestionario, id_lider, fecha_creacion, estado)
                VALUES (%s, %s, %s, NOW(), 'A')
            """, (nombre_grupo, id_cuestionario, id_lider))
            
            id_grupo = cursor.lastrowid
            
            # Agregar al líder como miembro
            cursor.execute("""
                INSERT INTO GrupoMiembro (id_grupo, id_jugador_cuestionario, fecha_union, es_lider)
                VALUES (%s, %s, NOW(), 1)
            """, (id_grupo, id_lider))
            
            connection.commit()
            return id_grupo, "Grupo creado exitosamente"
            
    except Exception as e:
        if connection:
            connection.rollback()
        print(f"Error en crear_grupo: {e}")
        import traceback
        traceback.print_exc()
        return None, f"Error al crear el grupo: {str(e)}"
    finally:
        if connection:
            connection.close()

def unirse_grupo(id_grupo, id_jugador_cuestionario):
    """Un estudiante se une a un grupo existente
    id_jugador_cuestionario ahora se refiere a Jugador_Cuestionario.id_jugador_cuestionario
    """
    connection = None
    try:
        connection = conexion.conectarbd()
        if not connection:
            return False, "Error al conectar con la base de datos"
        
        with connection.cursor() as cursor:
            # Verificar que el grupo existe y está activo
            cursor.execute("""
                SELECT g.id_grupo, g.id_cuestionario, g.estado, 
                       COUNT(gm.id_miembro) as num_miembros
                FROM Grupo g
                LEFT JOIN GrupoMiembro gm ON g.id_grupo = gm.id_grupo
                WHERE g.id_grupo = %s
                GROUP BY g.id_grupo
            """, (id_grupo,))
            grupo = cursor.fetchone()
            
            if not grupo:
                return False, "Grupo no encontrado"
            
            if grupo.get('estado') != 'A':
                return False, "El grupo no está activo"
            
            # Verificar límite de miembros (máximo 5 por defecto)
            if grupo.get('num_miembros', 0) >= 5:
                return False, "El grupo ya tiene el máximo de miembros permitidos"
            
            # Verificar que el jugador no esté ya en otro grupo del mismo cuestionario
            cursor.execute("""
                SELECT gm.id_grupo FROM GrupoMiembro gm
                INNER JOIN Grupo g ON gm.id_grupo = g.id_grupo
                WHERE gm.id_jugador_cuestionario = %s AND g.id_cuestionario = %s
            """, (id_jugador_cuestionario, grupo.get('id_cuestionario')))
            grupo_existente = cursor.fetchone()
            
            if grupo_existente:
                return False, "Ya estás en un grupo para este cuestionario"
            
            # Verificar que el jugador pertenezca al cuestionario
            cursor.execute("""
                SELECT id_jugador_cuestionario FROM Jugador_Cuestionario
                WHERE id_jugador_cuestionario = %s AND id_cuestionario = %s
            """, (id_jugador_cuestionario, grupo.get('id_cuestionario')))
            jugador = cursor.fetchone()
            
            if not jugador:
                return False, "Debes estar registrado en el cuestionario primero"
            
            # Agregar al grupo
            cursor.execute("""
                INSERT INTO GrupoMiembro (id_grupo, id_jugador_cuestionario, fecha_union, es_lider)
                VALUES (%s, %s, NOW(), 0)
            """, (id_grupo, id_jugador_cuestionario))
            
            connection.commit()
            return True, "Te has unido al grupo exitosamente"
            
    except Exception as e:
        if connection:
            connection.rollback()
        print(f"Error en unirse_grupo: {e}")
        import traceback
        traceback.print_exc()
        return False, f"Error al unirse al grupo: {str(e)}"
    finally:
        if connection:
            connection.close()

def obtener_todos_grupos(id_cuestionario):
    """Obtiene todos los grupos de un cuestionario (para docente)"""
    connection = None
    try:
        connection = conexion.conectarbd()
        if not connection:
            return []
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT g.id_grupo, g.nombre_grupo, g.id_lider, g.fecha_creacion,
                       g.metodo_evaluacion, g.puntaje, g.estado,
                       COUNT(gm.id_miembro) as num_miembros,
                       MAX(CASE WHEN gm.es_lider = 1 THEN jc.alias END) as lider_alias
                FROM Grupo g
                LEFT JOIN GrupoMiembro gm ON g.id_grupo = gm.id_grupo
                LEFT JOIN Jugador_Cuestionario jc ON gm.id_jugador_cuestionario = jc.id_jugador_cuestionario AND gm.es_lider = 1
                WHERE g.id_cuestionario = %s
                GROUP BY g.id_grupo, g.nombre_grupo, g.id_lider, g.fecha_creacion, 
                         g.metodo_evaluacion, g.puntaje, g.estado
                ORDER BY g.fecha_creacion DESC
            """, (id_cuestionario,))
            
            grupos = cursor.fetchall()
            return grupos
            
    except Exception as e:
        print(f"Error en obtener_todos_grupos: {e}")
        import traceback
        traceback.print_exc()
        return []
    finally:
        if connection:
            connection.close()

def obtener_grupos_disponibles(id_cuestionario):
    """Obtiene los grupos disponibles para unirse en un cuestionario"""
    connection = None
    try:
        connection = conexion.conectarbd()
        if not connection:
            return []
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT g.id_grupo, g.nombre_grupo, g.id_lider, g.fecha_creacion,
                       COUNT(gm.id_miembro) as num_miembros,
                       MAX(CASE WHEN gm.es_lider = 1 THEN jc.alias END) as lider_alias
                FROM Grupo g
                LEFT JOIN GrupoMiembro gm ON g.id_grupo = gm.id_grupo
                LEFT JOIN Jugador_Cuestionario jc ON gm.id_jugador_cuestionario = jc.id_jugador_cuestionario AND gm.es_lider = 1
                WHERE g.id_cuestionario = %s AND g.estado = 'A'
                GROUP BY g.id_grupo, g.nombre_grupo, g.id_lider, g.fecha_creacion
                HAVING num_miembros < 5
                ORDER BY g.fecha_creacion DESC
            """, (id_cuestionario,))
            
            grupos = cursor.fetchall()
            return grupos
            
    except Exception as e:
        print(f"Error en obtener_grupos_disponibles: {e}")
        import traceback
        traceback.print_exc()
        return []
    finally:
        if connection:
            connection.close()

def obtener_miembros_grupo(id_grupo):
    """Obtiene los miembros de un grupo"""
    connection = None
    try:
        connection = conexion.conectarbd()
        if not connection:
            return []
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT jc.id_jugador_cuestionario, jc.alias, gm.es_lider, gm.fecha_union
                FROM GrupoMiembro gm
                INNER JOIN Jugador_Cuestionario jc ON gm.id_jugador_cuestionario = jc.id_jugador_cuestionario
                WHERE gm.id_grupo = %s
                ORDER BY gm.es_lider DESC, gm.fecha_union ASC
            """, (id_grupo,))
            
            miembros = cursor.fetchall()
            return miembros
            
    except Exception as e:
        print(f"Error en obtener_miembros_grupo: {e}")
        import traceback
        traceback.print_exc()
        return []
    finally:
        if connection:
            connection.close()

def obtener_grupo_usuario(id_jugador_cuestionario, id_cuestionario):
    """Obtiene el grupo al que pertenece un jugador en un cuestionario
    id_jugador_cuestionario ahora se refiere a Jugador_Cuestionario.id_jugador_cuestionario
    """
    connection = None
    try:
        connection = conexion.conectarbd()
        if not connection:
            return None
        
        with connection.cursor() as cursor:
            if id_cuestionario:
                cursor.execute("""
                    SELECT g.id_grupo, g.nombre_grupo, g.id_lider, g.metodo_evaluacion, g.id_cuestionario
                    FROM Grupo g
                    INNER JOIN GrupoMiembro gm ON g.id_grupo = gm.id_grupo
                    WHERE gm.id_jugador_cuestionario = %s AND g.id_cuestionario = %s AND g.estado = 'A'
                """, (id_jugador_cuestionario, id_cuestionario))
            else:
                cursor.execute("""
                    SELECT g.id_grupo, g.nombre_grupo, g.id_lider, g.metodo_evaluacion, g.id_cuestionario
                    FROM Grupo g
                    INNER JOIN GrupoMiembro gm ON g.id_grupo = gm.id_grupo
                    WHERE gm.id_jugador_cuestionario = %s AND g.estado = 'A'
                    ORDER BY g.fecha_creacion DESC
                    LIMIT 1
                """, (id_jugador_cuestionario,))
            
            grupo = cursor.fetchone()
            return grupo
            
    except Exception as e:
        print(f"Error en obtener_grupo_usuario: {e}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        if connection:
            connection.close()

def establecer_metodo_evaluacion(id_grupo, metodo_evaluacion, id_jugador_cuestionario):
    """Establece el método de evaluación del grupo (solo el líder puede hacerlo)
    id_jugador_cuestionario ahora se refiere a Jugador_Cuestionario.id_jugador_cuestionario
    """
    connection = None
    try:
        connection = conexion.conectarbd()
        if not connection:
            return False, "Error al conectar con la base de datos"
        
        with connection.cursor() as cursor:
            # Verificar que el jugador sea el líder
            cursor.execute("""
                SELECT id_lider FROM Grupo
                WHERE id_grupo = %s
            """, (id_grupo,))
            grupo = cursor.fetchone()
            
            if not grupo:
                return False, "Grupo no encontrado"
            
            if grupo.get('id_lider') != id_jugador_cuestionario:
                return False, "Solo el líder del grupo puede establecer el método de evaluación"
            
            # Métodos válidos: 'votacion' (mayoría), 'consenso' (unanimidad), 'lider' (decide líder)
            metodos_validos = ['votacion', 'consenso', 'lider']
            if metodo_evaluacion not in metodos_validos:
                return False, "Método de evaluación no válido"
            
            # Actualizar método de evaluación
            cursor.execute("""
                UPDATE Grupo 
                SET metodo_evaluacion = %s
                WHERE id_grupo = %s
            """, (metodo_evaluacion, id_grupo))
            
            connection.commit()
            return True, "Método de evaluación establecido correctamente"
            
    except Exception as e:
        if connection:
            connection.rollback()
        print(f"Error en establecer_metodo_evaluacion: {e}")
        return False, f"Error al establecer método: {str(e)}"
    finally:
        if connection:
            connection.close()

def salir_grupo(id_grupo, id_jugador_cuestionario):
    """Un estudiante sale de un grupo
    id_jugador_cuestionario ahora se refiere a Jugador_Cuestionario.id_jugador_cuestionario
    """
    connection = None
    try:
        connection = conexion.conectarbd()
        if not connection:
            return False, "Error al conectar con la base de datos"
        
        with connection.cursor() as cursor:
            # Verificar que el jugador sea miembro
            cursor.execute("""
                SELECT es_lider FROM GrupoMiembro
                WHERE id_grupo = %s AND id_jugador_cuestionario = %s
            """, (id_grupo, id_jugador_cuestionario))
            miembro = cursor.fetchone()
            
            if not miembro:
                return False, "No eres miembro de este grupo"
            
            # Si es el líder, no puede salir (debe disolver el grupo primero)
            if miembro.get('es_lider'):
                return False, "El líder no puede salir del grupo. Debes disolver el grupo primero."
            
            # Eliminar del grupo
            cursor.execute("""
                DELETE FROM GrupoMiembro
                WHERE id_grupo = %s AND id_jugador_cuestionario = %s
            """, (id_grupo, id_jugador_cuestionario))
            
            connection.commit()
            return True, "Has salido del grupo exitosamente"
            
    except Exception as e:
        if connection:
            connection.rollback()
        print(f"Error en salir_grupo: {e}")
        import traceback
        traceback.print_exc()
        return False, f"Error al salir del grupo: {str(e)}"
    finally:
        if connection:
            connection.close()

def disolver_grupo(id_grupo, id_jugador_cuestionario):
    """El líder disuelve el grupo
    id_jugador_cuestionario ahora se refiere a Jugador_Cuestionario.id_jugador_cuestionario
    """
    connection = None
    try:
        connection = conexion.conectarbd()
        if not connection:
            return False, "Error al conectar con la base de datos"
        
        with connection.cursor() as cursor:
            # Verificar que el jugador sea el líder
            cursor.execute("""
                SELECT id_lider FROM Grupo
                WHERE id_grupo = %s AND estado = 'A'
            """, (id_grupo,))
            grupo = cursor.fetchone()
            
            if not grupo:
                return False, "Grupo no encontrado o ya disuelto"
            
            if grupo.get('id_lider') != id_jugador_cuestionario:
                return False, "Solo el líder puede disolver el grupo"
            
            # Cambiar estado del grupo a disuelto
            cursor.execute("""
                UPDATE Grupo 
                SET estado = 'D'
                WHERE id_grupo = %s
            """, (id_grupo,))
            
            # Nota: Los miembros se mantienen en la BD para historial, pero el grupo queda inactivo
            
            connection.commit()
            return True, "Grupo disuelto exitosamente"
            
    except Exception as e:
        if connection:
            connection.rollback()
        print(f"Error en disolver_grupo: {e}")
        return False, f"Error al disolver el grupo: {str(e)}"
    finally:
        if connection:
            connection.close()

