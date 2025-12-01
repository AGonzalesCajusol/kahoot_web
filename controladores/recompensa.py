from conexion import conectarbd

def verificar_recompensa_recibida(id_cuestionario, id_jugador_cuestionario):
    """Verifica si un jugador ya recibió recompensa en un cuestionario"""
    connection = conectarbd()
    if not connection:
        return False
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id_recompensa FROM Recompensa
                WHERE id_cuestionario = %s AND id_jugador_cuestionario = %s
            """, (id_cuestionario, id_jugador_cuestionario))
            resultado = cursor.fetchone()
            return resultado is not None
    except Exception as e:
        print(f"❌ Error al verificar recompensa: {e}")
        return False
    finally:
        if connection:
            connection.close()

def obtener_info_jugador_cuestionario(id_jugador_cuestionario, id_cuestionario):
    """Obtiene la información del jugador y su puntaje en el cuestionario"""
    connection = conectarbd()
    if not connection:
        return None
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT jc.id_jugador_cuestionario, jc.alias, jc.puntaje, jc.id_jugador, jc.id_cuestionario
                FROM Jugador_Cuestionario jc
                WHERE jc.id_jugador_cuestionario = %s AND jc.id_cuestionario = %s
            """, (id_jugador_cuestionario, id_cuestionario))
            return cursor.fetchone()
    except Exception as e:
        print(f"❌ Error al obtener info jugador: {e}")
        return None
    finally:
        if connection:
            connection.close()

def calcular_recompensa(puntaje, total_participantes):
    """Calcula la recompensa basada en el puntaje y posición"""
    # Sistema de recompensas:
    # - Top 1: 100 puntos
    # - Top 2: 75 puntos
    # - Top 3: 50 puntos
    # - Top 10%: 25 puntos
    # - Resto: 10 puntos
    
    # Esta función se puede ajustar según necesidades
    # Por ahora, retornamos puntos base según posición
    if total_participantes == 0:
        return 0
    
    # La posición se calcula después de obtener todos los participantes
    return 10  # Puntos base

def obtener_posicion_jugador(id_jugador_cuestionario, id_cuestionario):
    """Obtiene la posición del jugador en el ranking del cuestionario"""
    connection = conectarbd()
    if not connection:
        return None
    
    try:
        with connection.cursor() as cursor:
            # Obtener todos los jugadores ordenados por puntaje
            # Si hay empates en puntaje, se ordenan por tiempo total (menor tiempo = mejor posición)
            cursor.execute("""
                SELECT 
                    jc.id_jugador_cuestionario, 
                    jc.alias, 
                    COALESCE(jc.puntaje, 0) as puntaje,
                    COALESCE(SUM(r.tiempo_utilizado), 0) as tiempo_total
                FROM Jugador_Cuestionario jc
                LEFT JOIN Respuesta r ON jc.id_jugador_cuestionario = r.id_jugador_cuestionario
                WHERE jc.id_cuestionario = %s
                GROUP BY jc.id_jugador_cuestionario, jc.alias, jc.puntaje
                ORDER BY COALESCE(jc.puntaje, 0) DESC, tiempo_total ASC, jc.alias ASC
            """, (id_cuestionario,))
            jugadores = cursor.fetchall()
            
            # Calcular posición manualmente
            posicion = 0
            total_participantes = len(jugadores)
            jugador_encontrado = None
            
            for idx, jugador in enumerate(jugadores, 1):
                if jugador['id_jugador_cuestionario'] == id_jugador_cuestionario:
                    posicion = idx
                    jugador_encontrado = jugador
                    break
            
            if jugador_encontrado:
                return {
                    'posicion': posicion,
                    'total_participantes': total_participantes,
                    'puntaje': jugador_encontrado['puntaje']
                }
            return None
    except Exception as e:
        print(f"❌ Error al obtener posición: {e}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        if connection:
            connection.close()

def calcular_puntos_recompensa(posicion, total_participantes):
    """Calcula los puntos de recompensa según la posición"""
    if posicion == 1:
        return 100
    elif posicion == 2:
        return 75
    elif posicion == 3:
        return 50
    elif posicion <= max(1, int(total_participantes * 0.1)):  # Top 10%
        return 25
    else:
        return 10

def otorgar_recompensas_automaticas(id_cuestionario):
    """Otorga recompensas automáticamente a todos los jugadores según su posición"""
    connection = conectarbd()
    if not connection:
        print("❌ Error: No se pudo conectar a la base de datos para otorgar recompensas")
        return False
    
    try:
        with connection.cursor() as cursor:
            # Obtener todos los jugadores ordenados por puntaje
            # Si hay empates en puntaje, se ordenan por tiempo total (menor tiempo = mejor posición)
            cursor.execute("""
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
            """, (id_cuestionario,))
            jugadores = cursor.fetchall()
            
            if not jugadores or len(jugadores) == 0:
                print(f"⚠️ No hay jugadores en el cuestionario {id_cuestionario}")
                return False
            
            total_participantes = len(jugadores)
            recompensas_otorgadas = 0
            
            # Otorgar recompensas a cada jugador según su posición
            for idx, jugador in enumerate(jugadores, 1):
                id_jugador_cuestionario = jugador['id_jugador_cuestionario']
                id_jugador = jugador.get('id_jugador')
                puntaje_jugador = float(jugador.get('puntaje', 0) or 0)
                
                # Verificar si ya recibió recompensa
                cursor.execute("""
                    SELECT id_recompensa FROM Recompensa
                    WHERE id_cuestionario = %s AND id_jugador_cuestionario = %s
                """, (id_cuestionario, id_jugador_cuestionario))
                ya_tiene_recompensa = cursor.fetchone()
                
                if ya_tiene_recompensa:
                    print(f"⏭️ Jugador {jugador['alias']} ya tiene recompensa, se omite")
                    continue
                
                # Si el jugador tiene 0 puntos, recibe 0 puntos de recompensa
                if puntaje_jugador <= 0:
                    puntos_recompensa = 0
                    print(f"⚠️ Jugador {jugador['alias']} tiene 0 puntos, recibe 0 puntos de recompensa")
                else:
                    # Calcular puntos de recompensa según posición solo si tiene puntos
                    puntos_recompensa = calcular_puntos_recompensa(idx, total_participantes)
                
                # Registrar recompensa
                try:
                    cursor.execute("""
                        INSERT INTO Recompensa (id_cuestionario, id_jugador_cuestionario, id_jugador, puntos, tipo_recompensa, fecha_recompensa)
                        VALUES (%s, %s, %s, %s, %s, NOW())
                    """, (id_cuestionario, id_jugador_cuestionario, id_jugador, puntos_recompensa, 'puntos'))
                    recompensas_otorgadas += 1
                    print(f"✅ Recompensa otorgada: {jugador['alias']} - Posición {idx} - Puntaje: {puntaje_jugador} - Recompensa: {puntos_recompensa} puntos")
                except Exception as e:
                    print(f"❌ Error al otorgar recompensa a {jugador['alias']}: {e}")
                    continue
            
            connection.commit()
            print(f"🎉 Recompensas otorgadas automáticamente: {recompensas_otorgadas} de {total_participantes} jugadores")
            return True
            
    except Exception as e:
        print(f"❌ Error al otorgar recompensas automáticas: {e}")
        import traceback
        traceback.print_exc()
        connection.rollback()
        return False
    finally:
        if connection:
            connection.close()

def registrar_recompensa(id_cuestionario, id_jugador_cuestionario, id_jugador, puntos, tipo_recompensa='puntos'):
    """Registra una recompensa para un jugador"""
    connection = conectarbd()
    if not connection:
        return False
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Recompensa (id_cuestionario, id_jugador_cuestionario, id_jugador, puntos, tipo_recompensa, fecha_recompensa)
                VALUES (%s, %s, %s, %s, %s, NOW())
                ON DUPLICATE KEY UPDATE
                    puntos = VALUES(puntos),
                    tipo_recompensa = VALUES(tipo_recompensa),
                    fecha_recompensa = NOW()
            """, (id_cuestionario, id_jugador_cuestionario, id_jugador, puntos, tipo_recompensa))
            connection.commit()
            return True
    except Exception as e:
        print(f"❌ Error al registrar recompensa: {e}")
        import traceback
        traceback.print_exc()
        connection.rollback()
        return False
    finally:
        if connection:
            connection.close()

def obtener_recompensas_por_cuestionario(id_cuestionario):
    """Obtiene todas las recompensas otorgadas en un cuestionario (para docente)"""
    connection = conectarbd()
    if not connection:
        return []
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    r.id_recompensa,
                    r.puntos,
                    r.tipo_recompensa,
                    r.fecha_recompensa,
                    jc.alias,
                    jc.puntaje,
                    j.email as email_jugador,
                    c.nombre as nombre_cuestionario
                FROM Recompensa r
                INNER JOIN Jugador_Cuestionario jc ON r.id_jugador_cuestionario = jc.id_jugador_cuestionario
                LEFT JOIN Jugador j ON r.id_jugador = j.id_jugador
                INNER JOIN Cuestionario c ON r.id_cuestionario = c.id_cuestionario
                WHERE r.id_cuestionario = %s
                ORDER BY r.fecha_recompensa DESC
            """, (id_cuestionario,))
            return cursor.fetchall()
    except Exception as e:
        print(f"❌ Error al obtener recompensas: {e}")
        import traceback
        traceback.print_exc()
        return []
    finally:
        if connection:
            connection.close()

def obtener_recompensas_por_docente(id_docente):
    """Obtiene todas las recompensas otorgadas en los cuestionarios de un docente"""
    connection = conectarbd()
    if not connection:
        return []
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    r.id_recompensa,
                    r.puntos,
                    r.tipo_recompensa,
                    r.fecha_recompensa,
                    jc.alias,
                    jc.puntaje,
                    j.email as email_jugador,
                    c.nombre as nombre_cuestionario,
                    c.id_cuestionario
                FROM Recompensa r
                INNER JOIN Jugador_Cuestionario jc ON r.id_jugador_cuestionario = jc.id_jugador_cuestionario
                LEFT JOIN Jugador j ON r.id_jugador = j.id_jugador
                INNER JOIN Cuestionario c ON r.id_cuestionario = c.id_cuestionario
                WHERE c.id_docente = %s
                ORDER BY r.fecha_recompensa DESC
            """, (id_docente,))
            return cursor.fetchall()
    except Exception as e:
        print(f"❌ Error al obtener recompensas por docente: {e}")
        import traceback
        traceback.print_exc()
        return []
    finally:
        if connection:
            connection.close()

def obtener_total_puntos_jugador(id_jugador):
    """Obtiene el total de puntos de recompensa de un jugador (máximo 1000)"""
    connection = conectarbd()
    if not connection:
        return 0
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT COALESCE(SUM(r.puntos), 0) as total_puntos
                FROM Recompensa r
                WHERE r.id_jugador = %s
            """, (id_jugador,))
            resultado = cursor.fetchone()
            total = resultado.get('total_puntos', 0) if resultado else 0
            # El máximo es 1000 puntos
            return min(total, 1000)
    except Exception as e:
        print(f"❌ Error al obtener total puntos jugador: {e}")
        import traceback
        traceback.print_exc()
        return 0
    finally:
        if connection:
            connection.close()

def obtener_recompensas_por_jugador(id_jugador):
    """Obtiene todas las recompensas recibidas por un jugador"""
    connection = conectarbd()
    if not connection:
        return []
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    r.id_recompensa,
                    r.puntos,
                    r.tipo_recompensa,
                    r.fecha_recompensa,
                    c.nombre as nombre_cuestionario,
                    c.id_cuestionario
                FROM Recompensa r
                INNER JOIN Cuestionario c ON r.id_cuestionario = c.id_cuestionario
                WHERE r.id_jugador = %s
                ORDER BY r.fecha_recompensa DESC
            """, (id_jugador,))
            return cursor.fetchall()
    except Exception as e:
        print(f"❌ Error al obtener recompensas por jugador: {e}")
        import traceback
        traceback.print_exc()
        return []
    finally:
        if connection:
            connection.close()

def obtener_puntos_recompensa_jugador_cuestionario(id_jugador_cuestionario, id_cuestionario):
    """Obtiene los puntos de recompensa de un jugador en un cuestionario específico"""
    connection = conectarbd()
    if not connection:
        return 0
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT COALESCE(SUM(r.puntos), 0) as puntos_recompensa
                FROM Recompensa r
                WHERE r.id_cuestionario = %s AND r.id_jugador_cuestionario = %s
            """, (id_cuestionario, id_jugador_cuestionario))
            resultado = cursor.fetchone()
            return resultado.get('puntos_recompensa', 0) if resultado else 0
    except Exception as e:
        print(f"❌ Error al obtener puntos de recompensa: {e}")
        import traceback
        traceback.print_exc()
        return 0
    finally:
        if connection:
            connection.close()

def obtener_total_puntos_recompensa_cuestionario(id_cuestionario):
    """Obtiene la sumatoria total de todos los puntos de recompensa otorgados en un cuestionario"""
    connection = conectarbd()
    if not connection:
        return 0
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT COALESCE(SUM(r.puntos), 0) as total_puntos_recompensa
                FROM Recompensa r
                WHERE r.id_cuestionario = %s
            """, (id_cuestionario,))
            resultado = cursor.fetchone()
            return resultado.get('total_puntos_recompensa', 0) if resultado else 0
    except Exception as e:
        print(f"❌ Error al obtener total puntos de recompensa: {e}")
        import traceback
        traceback.print_exc()
        return 0
    finally:
        if connection:
            connection.close()

def verificar_jugador_registrado(id_jugador_cuestionario, id_cuestionario):
    """Verifica si el jugador tiene un jugador registrado asociado"""
    connection = conectarbd()
    if not connection:
        return False
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id_jugador FROM Jugador_Cuestionario
                WHERE id_jugador_cuestionario = %s AND id_cuestionario = %s
            """, (id_jugador_cuestionario, id_cuestionario))
            resultado = cursor.fetchone()
            return resultado and resultado.get('id_jugador') is not None
    except Exception as e:
        print(f"❌ Error al verificar jugador: {e}")
        return False
    finally:
        if connection:
            connection.close()

def asociar_jugador_a_jugador_cuestionario(id_jugador_cuestionario, id_jugador, id_cuestionario):
    """Asocia un jugador registrado a un jugador_cuestionario"""
    connection = conectarbd()
    if not connection:
        return False
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE Jugador_Cuestionario
                SET id_jugador = %s
                WHERE id_jugador_cuestionario = %s AND id_cuestionario = %s
            """, (id_jugador, id_jugador_cuestionario, id_cuestionario))
            connection.commit()
            return True
    except Exception as e:
        print(f"❌ Error al asociar jugador: {e}")
        connection.rollback()
        return False
    finally:
        if connection:
            connection.close()
