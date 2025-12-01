import conexion
import random

def fnmodificardetalleformulario(data):
    print("[DEBUG] Datos recibidos en fnmodificardetalleformulario:", data)
    try:
        conn = conexion.conectarbd()
        with conn.cursor() as cursor:
            imagen_url = data.get('imagen_url')
            print(f"[DEBUG] imagen_url recibida: {imagen_url}")
            print(f"[DEBUG] tipo de imagen_url: {type(imagen_url)}")
            
            consulta = '''
                UPDATE Cuestionario 
                SET nombre = %s,
                    estado = %s,
                    tipo_cuestionario = %s,
                    descripcion = %s,
                    imagen_url = %s
                WHERE id_cuestionario = %s;
            ''' 
            valores = (
                data.get('nombre_formulario'),
                data.get('estado'),
                data.get('tipo_formulario'),
                data.get('descripcion_formulario'),
                imagen_url,  # Puede ser None/null para eliminar la imagen
                data.get('id_formulario')
            )
            print(f"[DEBUG] Valores a ejecutar: {valores}")
            
            cursor.execute(consulta, valores)
            filas_afectadas = cursor.rowcount
            print(f"[DEBUG] Filas afectadas: {filas_afectadas}")
            
            conn.commit()
            print("[DEBUG] Commit realizado exitosamente")
            
            # Verificar que se actualizó correctamente
            cursor.execute("SELECT imagen_url FROM Cuestionario WHERE id_cuestionario = %s", (data.get('id_formulario'),))
            verificacion = cursor.fetchone()
            print(f"[DEBUG] imagen_url después del UPDATE: {verificacion.get('imagen_url') if verificacion else 'No encontrado'}")
            
        return {'estado': True, 'mensaje': 'Se modificó correctamente'}
    except Exception as e:
        print("Error en fnmodificardetalleformulario:", e)
        import traceback
        traceback.print_exc()
        return {'estado': False, 'mensaje': 'No se pudo modificar'}


def datos_cuestionario1(id_for):
    conn = conexion.conectarbd()
    with conn.cursor() as cursor:
        sql = '''
            SELECT 
                pr.id_pregunta,
                pr.pregunta,
                pr.puntaje,
                pr.tiempo_respuesta,
                JSON_ARRAYAGG(JSON_OBJECT(
                    'id_alternativa', al.id_alternativa,
                    'respuesta', al.respuesta,
                    'estado_alternativa', al.estado_alternativa
                )) AS alternativas
            FROM Pregunta pr
            INNER JOIN Alternativa al ON pr.id_pregunta = al.id_pregunta
            WHERE pr.id_cuestionario = %s
            GROUP BY pr.id_pregunta, pr.pregunta, pr.puntaje;
        '''
        cursor.execute(sql,(id_for))
        respuestas = cursor.fetchall()
        sql2 = '''
            select id_cuestionario, nombre, estado, tipo_cuestionario, descripcion, imagen_url from  Cuestionario where id_cuestionario = %s;

        '''
        cursor.execute(sql2,(id_for))
        detalle = cursor.fetchone()
    return {
        "detalle": detalle,
        "respuestas": respuestas
    }

def datos_cuestionario(id_for):
    conn = conexion.conectarbd()
    with conn.cursor() as cursor:
        sql = '''
            SELECT 
                pr.id_pregunta,
                pr.pregunta,
                pr.puntaje,
                pr.tiempo_respuesta,
                JSON_ARRAYAGG(JSON_OBJECT(
                    'id_alternativa', al.id_alternativa,
                    'respuesta', al.respuesta,
                    'estado_alternativa', al.estado_alternativa
                )) AS alternativas
            FROM Pregunta pr
            INNER JOIN Alternativa al ON pr.id_pregunta = al.id_pregunta
            WHERE pr.id_cuestionario = %s
            GROUP BY pr.id_pregunta, pr.pregunta, pr.puntaje;
        '''
        cursor.execute(sql,(id_for))
        datos_frm = cursor.fetchall()
    return datos_frm

def retornar_dartosformuario(id_formulario):
    conn = conexion.conectarbd()
    with conn.cursor() as cursor:
        sql = "select id_cuestionario, c.nombre, c.pin from Cuestionario  as c where c.id_cuestionario = %s"
        cursor.execute(sql,(id_formulario))
        datos_frm = cursor.fetchone()
    return datos_frm

def obtener_cuestionarios_activos(id_docente):
    connection = None
    try:
        connection = conexion.conectarbd()
        if connection:
            cursor = connection.cursor()

            query = """
                SELECT id_cuestionario, nombre, tipo_cuestionario, pin, estado, imagen_url, estado_juego
                FROM Cuestionario
                WHERE estado = 'P' AND id_docente = %s
            """
            cursor.execute(query, (id_docente,))            
            
            return cursor.fetchall()

    except Exception as e:
        print(e)
        return []  
    finally:
        if connection:
            connection.close()

def obtener_cuestionarios_archivados(id_docente):
    connection = None
    try:
        connection = conexion.conectarbd()
        if connection:
            cursor = connection.cursor()

            query = """
                SELECT id_cuestionario, nombre, tipo_cuestionario, pin, estado, imagen_url, estado_juego
                FROM Cuestionario
                WHERE estado = 'R' AND id_docente = %s
            """
            cursor.execute(query, (id_docente,))

            return cursor.fetchall()
    except Exception as e:
        print(e)
        return []  
    finally:
        if connection:
            connection.close()

def actualizar_puntaje_usuario(id_usuario, nuevo_puntaje):
    # NOTA: id_usuario ahora se refiere a id_jugador_cuestionario
    connection = None
    try:
        connection = conexion.conectarbd()
        if connection:
            cursor = connection.cursor()

            query = """
                UPDATE Jugador_Cuestionario
                SET puntaje = %s
                WHERE id_jugador_cuestionario = %s
            """
            cursor.execute(query, (nuevo_puntaje, id_usuario))
            connection.commit()

            filas_afectadas = cursor.rowcount
            connection.close()

            if filas_afectadas > 0:
                print("✅ Puntaje actualizado correctamente.")
                return True
            else:
                print("⚠ No se encontró el usuario con ese ID.")
                return False
    except Exception as e:
        return False
    
def validar_pin(pin):
    connection = None
    try:
        connection = conexion.conectarbd()
        if connection:
            cursor = connection.cursor() 
            
            query = """
                SELECT id_cuestionario, tipo_cuestionario, estado_cuestionario, estado_juego, estado
                FROM Cuestionario
                WHERE pin = %s AND estado = 'P'
            """
            cursor.execute(query, (pin,))
            resultado = cursor.fetchone()
            cursor.close()
            connection.close()
            
            return resultado 
        else:
            print("No se pudo conectar a la base de datos")
            return None
    except Exception as e:
        print(f"Error en validar_pin: {e}")
        return None

def actualizar_estado_juego(id_cuestionario, nuevo_estado):
    connection = None
    try:
        connection = conexion.conectarbd()
        if connection:
            cursor = connection.cursor()

            estados_validos = ['SL', 'IN', 'FN']
            if nuevo_estado not in estados_validos:
                print(f"Estado inválido: {nuevo_estado}")
                return False

            query = """
                UPDATE Cuestionario
                SET estado_juego = %s
                WHERE id_cuestionario = %s
            """
            cursor.execute(query, (nuevo_estado, id_cuestionario))
            connection.commit()

            filas_afectadas = cursor.rowcount
            cursor.close()
            connection.close()

            if filas_afectadas > 0:
                print(f"Estado del juego actualizado a '{nuevo_estado}' para id_cuestionario {id_cuestionario}")
                return True
            else:
                print(f"No se encontró el cuestionario con id {id_cuestionario}")
                return False

        else:
            print("No se pudo conectar a la base de datos")
            return False
    except Exception as e:
        print(f"Error en actualizar_estado_juego: {e}")
        return False

def resetear_cuestionario(id_cuestionario):
    """
    Resetea el cuestionario para que pueda reutilizarse desde cero
    Esto incluye:
    - Resetear el estado_juego a 'SL' (sin iniciar)
    - Generar un nuevo PIN
    - Eliminar todos los participantes (Usuario)
    - Eliminar grupos y respuestas de grupos si existen
    """
    connection = None
    try:
        connection = conexion.conectarbd()
        if not connection:
            return {'estado': False, 'mensaje': 'Error al conectar con la base de datos'}
        
        cursor = connection.cursor()
        
        # Verificar que el cuestionario exista
        cursor.execute("SELECT id_cuestionario FROM Cuestionario WHERE id_cuestionario = %s", (id_cuestionario,))
        if not cursor.fetchone():
            return {'estado': False, 'mensaje': 'El cuestionario no existe'}
        
        # 1. Eliminar todos los participantes del cuestionario
        cursor.execute("DELETE FROM Jugador_Cuestionario WHERE id_cuestionario = %s", (id_cuestionario,))
        participantes_eliminados = cursor.rowcount
        print(f"Participantes eliminados: {participantes_eliminados}")
        
        # 2. Eliminar grupos y sus respuestas (si existen)
        # Primero obtener los IDs de los grupos
        cursor.execute("SELECT id_grupo FROM Grupo WHERE id_cuestionario = %s", (id_cuestionario,))
        grupos = cursor.fetchall()
        grupos_ids = [g['id_grupo'] for g in grupos] if grupos else []
        
        if grupos_ids:
            # Eliminar respuestas de grupos
            placeholders = ','.join(['%s'] * len(grupos_ids))
            query_respuestas = f"DELETE FROM RespuestaGrupo WHERE id_grupo IN ({placeholders})"
            cursor.execute(query_respuestas, grupos_ids)
            
            # Eliminar miembros de grupos
            query_miembros = f"DELETE FROM GrupoMiembro WHERE id_grupo IN ({placeholders})"
            cursor.execute(query_miembros, grupos_ids)
            
            # Finalmente eliminar los grupos
            cursor.execute("DELETE FROM Grupo WHERE id_cuestionario = %s", (id_cuestionario,))
            grupos_eliminados = cursor.rowcount
            print(f"Grupos eliminados: {grupos_eliminados}")
        else:
            print("No hay grupos para eliminar")
        
        # 3. Generar un nuevo PIN
        nuevo_pin = crear_pin()
        
        # 4. Resetear el estado del juego a 'SL' (sin iniciar) y actualizar el PIN
        query = """
            UPDATE Cuestionario
            SET estado_juego = 'SL', pin = %s
            WHERE id_cuestionario = %s
        """
        cursor.execute(query, (nuevo_pin, id_cuestionario))
        connection.commit()
        
        cursor.close()
        
        return {
            'estado': True, 
            'mensaje': f'Cuestionario reseteado correctamente. Nuevo PIN: {nuevo_pin}',
            'nuevo_pin': nuevo_pin
        }
        
    except Exception as e:
        if connection:
            connection.rollback()
        print(f"Error en resetear_cuestionario: {e}")
        import traceback
        traceback.print_exc()
        return {'estado': False, 'mensaje': f'Error al resetear el cuestionario: {str(e)}'}
    finally:
        if connection:
            try:
                connection.close()
            except Exception as e:
                # La conexión ya estaba cerrada, ignorar el error
                pass

def eliminar_cuestionario_completo(id_cuestionario):
    """
    Elimina completamente un cuestionario y todo lo relacionado:
    - Participantes (Usuario)
    - Respuestas de grupos (RespuestaGrupo)
    - Miembros de grupos (GrupoMiembro)
    - Grupos (Grupo)
    - Recompensas (Recompensa)
    - Alternativas (Alternativa)
    - Preguntas (Pregunta)
    - El cuestionario mismo (Cuestionario)
    """
    connection = None
    try:
        connection = conexion.conectarbd()
        if not connection:
            return {'estado': False, 'mensaje': 'Error al conectar con la base de datos'}
        
        cursor = connection.cursor()
        
        # Verificar que el cuestionario exista
        cursor.execute("SELECT id_cuestionario, nombre FROM Cuestionario WHERE id_cuestionario = %s", (id_cuestionario,))
        cuestionario_data = cursor.fetchone()
        if not cuestionario_data:
            return {'estado': False, 'mensaje': 'El cuestionario no existe'}
        
        nombre_cuestionario = cuestionario_data.get('nombre', 'Cuestionario')
        
        # 1. Obtener IDs de preguntas para eliminar alternativas
        cursor.execute("SELECT id_pregunta FROM Pregunta WHERE id_cuestionario = %s", (id_cuestionario,))
        preguntas = cursor.fetchall()
        preguntas_ids = [p['id_pregunta'] for p in preguntas] if preguntas else []
        
        # 2. Obtener IDs de grupos para eliminar relaciones
        cursor.execute("SELECT id_grupo FROM Grupo WHERE id_cuestionario = %s", (id_cuestionario,))
        grupos = cursor.fetchall()
        grupos_ids = [g['id_grupo'] for g in grupos] if grupos else []
        
        # 3. Eliminar en orden (respetando foreign keys)
        # 3.1 Eliminar respuestas de grupos
        if grupos_ids:
            placeholders = ','.join(['%s'] * len(grupos_ids))
            query_respuestas_grupo = f"DELETE FROM RespuestaGrupo WHERE id_grupo IN ({placeholders})"
            cursor.execute(query_respuestas_grupo, grupos_ids)
        
        # 3.2 Eliminar miembros de grupos
        if grupos_ids:
            placeholders = ','.join(['%s'] * len(grupos_ids))
            query_miembros = f"DELETE FROM GrupoMiembro WHERE id_grupo IN ({placeholders})"
            cursor.execute(query_miembros, grupos_ids)
        
        # 3.3 Eliminar grupos
        if grupos_ids:
            cursor.execute("DELETE FROM Grupo WHERE id_cuestionario = %s", (id_cuestionario,))
        
        # 3.4 Eliminar recompensas
        cursor.execute("DELETE FROM Recompensa WHERE id_cuestionario = %s", (id_cuestionario,))
        
        # 3.5 Eliminar alternativas de preguntas
        if preguntas_ids:
            placeholders = ','.join(['%s'] * len(preguntas_ids))
            query_alternativas = f"DELETE FROM Alternativa WHERE id_pregunta IN ({placeholders})"
            cursor.execute(query_alternativas, preguntas_ids)
        
        # 3.6 Eliminar preguntas
        if preguntas_ids:
            cursor.execute("DELETE FROM Pregunta WHERE id_cuestionario = %s", (id_cuestionario,))
        
        # 3.7 Eliminar participantes
        cursor.execute("DELETE FROM Jugador_Cuestionario WHERE id_cuestionario = %s", (id_cuestionario,))
        
        # 3.8 Finalmente eliminar el cuestionario
        cursor.execute("DELETE FROM Cuestionario WHERE id_cuestionario = %s", (id_cuestionario,))
        
        connection.commit()
        cursor.close()
        
        return {
            'estado': True,
            'mensaje': f'Cuestionario "{nombre_cuestionario}" eliminado correctamente'
        }
        
    except Exception as e:
        if connection:
            connection.rollback()
        print(f"Error en eliminar_cuestionario_completo: {e}")
        import traceback
        traceback.print_exc()
        return {'estado': False, 'mensaje': f'Error al eliminar el cuestionario: {str(e)}'}
    finally:
        if connection:
            try:
                connection.close()
            except Exception as e:
                pass

def obtener_participantes(id_cuestionario):
    """
    Obtiene la lista de participantes de un cuestionario con sus puntajes actualizados.
    IMPORTANTE: Usa una nueva conexión cada vez para leer los datos más recientes.
    """
    conexion_db = None
    try:
        # Usar una nueva conexión para asegurar que leemos los datos más recientes
        conexion_db = conexion.conectarbd()
        if not conexion_db:
            print(f"[ERROR] No se pudo establecer conexión a la base de datos para cuestionario {id_cuestionario}")
            return []
        
        with conexion_db.cursor() as cursor:
            # Ordenar por puntaje descendente para mostrar el marcador correctamente
            # Usar CAST para asegurar que el puntaje se lea correctamente
            consulta = """
                SELECT 
                    jc.alias, 
                    CAST(COALESCE(jc.puntaje, 0) AS DECIMAL(5,2)) as puntaje,
                    COALESCE(SUM(r.tiempo_utilizado), 0) as tiempo_total
                FROM Jugador_Cuestionario jc
                LEFT JOIN Respuesta r ON jc.id_jugador_cuestionario = r.id_jugador_cuestionario
                WHERE jc.id_cuestionario = %s
                GROUP BY jc.alias, jc.puntaje
                ORDER BY CAST(COALESCE(jc.puntaje, 0) AS DECIMAL(5,2)) DESC, tiempo_total ASC, jc.alias ASC
            """
            cursor.execute(consulta, (id_cuestionario,))
            
            resultados = cursor.fetchall()
            
            participantes = []
            if resultados:
                for fila in resultados:
                    alias_valor = fila.get("alias") if fila else None
                    puntaje_valor = fila.get("puntaje") if fila else None
                    
                    alias_cadena = str(alias_valor) if alias_valor else ""
                    
                    try:
                        # Convertir a float asegurándonos de manejar decimales correctamente
                        if puntaje_valor is None:
                            puntaje_float = 0.0
                        elif isinstance(puntaje_valor, (int, float)):
                            puntaje_float = float(puntaje_valor)
                        else:
                            puntaje_float = float(str(puntaje_valor))
                    except (ValueError, TypeError) as e:
                        print(f"[WARNING] Error al convertir puntaje '{puntaje_valor}' para {alias_cadena}: {e}")
                        puntaje_float = 0.0
                    
                    print(f"[DEBUG] Participante: {alias_cadena}, puntaje en BD: {puntaje_valor}, puntaje procesado: {puntaje_float}")
                    
                    participantes.append({
                        "alias": alias_cadena,
                        "puntaje": puntaje_float
                    })
        
        print(f"[OK] ✅ Participantes obtenidos para cuestionario {id_cuestionario}: {len(participantes)} participantes")
        if participantes:
            print(f"[OK] 📋 Participantes: {[(p['alias'], p['puntaje']) for p in participantes]}")
        return participantes
        
    except Exception as e:
        error_msg = str(e)
        error_type = type(e).__name__
        print(f"[ERROR] Error al obtener participantes para cuestionario {id_cuestionario}: {error_type} - {error_msg}")
        
        if "Already closed" not in error_msg and "already closed" not in error_msg.lower():
            import traceback
            traceback.print_exc()
        
        return []
        
    finally:
        # Asegurar que la conexión se cierre correctamente
        try:
            if conexion_db:
                conexion_db.close()
                print(f"[DEBUG] Conexión cerrada para obtener_participantes")
        except Exception as error_cierre:
            print(f"[WARNING] Error al cerrar conexión: {error_cierre}")
            pass

def crear_pin():
    pin = str(random.randint(10000, 99999))
    return pin

def reutilizar_cuestionario(id_cuestionario_origen, id_docente_destino):
    """
    Copia un cuestionario completo (preguntas y alternativas) para un nuevo docente.
    Retorna el id del nuevo cuestionario creado o None si hay error.
    """
    connection = None
    try:
        connection = conexion.conectarbd()
        if not connection:
            return None, "Error al conectar con la base de datos"
        
        cursor = connection.cursor()
        
        # 1. Obtener datos del cuestionario original
        cursor.execute("""
            SELECT nombre, tipo_cuestionario, descripcion, estado
            FROM Cuestionario
            WHERE id_cuestionario = %s
        """, (id_cuestionario_origen,))
        cuestionario_original = cursor.fetchone()
        
        if not cuestionario_original:
            return None, "El cuestionario no existe"
        
        # 2. Crear nuevo cuestionario con nombre modificado
        nombre_original = cuestionario_original.get('nombre', '')
        nuevo_nombre = f"{nombre_original} (Copia)"
        
        cursor.execute("""
            INSERT INTO Cuestionario (nombre, tipo_cuestionario, descripcion, pin, estado, id_docente)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            nuevo_nombre,
            cuestionario_original.get('tipo_cuestionario'),
            cuestionario_original.get('descripcion'),
            crear_pin(),
            'R',  # Siempre privado por defecto
            id_docente_destino
        ))
        
        id_cuestionario_nuevo = cursor.lastrowid
        
        # 3. Copiar todas las preguntas
        cursor.execute("""
            SELECT id_pregunta, pregunta, puntaje, tiempo_respuesta, tipo_pregunta
            FROM Pregunta
            WHERE id_cuestionario = %s
        """, (id_cuestionario_origen,))
        preguntas = cursor.fetchall()
        
        for pregunta in preguntas:
            # Insertar nueva pregunta
            cursor.execute("""
                INSERT INTO Pregunta (pregunta, puntaje, tiempo_respuesta, tipo_pregunta, id_cuestionario)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                pregunta.get('pregunta'),
                pregunta.get('puntaje'),
                pregunta.get('tiempo_respuesta'),
                pregunta.get('tipo_pregunta'),
                id_cuestionario_nuevo
            ))
            
            id_pregunta_nuevo = cursor.lastrowid
            id_pregunta_original = pregunta.get('id_pregunta')
            
            # 4. Copiar todas las alternativas de la pregunta
            cursor.execute("""
                SELECT respuesta, estado_alternativa
                FROM Alternativa
                WHERE id_pregunta = %s
            """, (id_pregunta_original,))
            alternativas = cursor.fetchall()
            
            for alternativa in alternativas:
                cursor.execute("""
                    INSERT INTO Alternativa (respuesta, estado_alternativa, id_pregunta)
                    VALUES (%s, %s, %s)
                """, (
                    alternativa.get('respuesta'),
                    alternativa.get('estado_alternativa'),
                    id_pregunta_nuevo
                ))
        
        connection.commit()
        return id_cuestionario_nuevo, "Cuestionario reutilizado exitosamente"
        
    except Exception as e:
        if connection:
            connection.rollback()
        print(f"Error al reutilizar cuestionario: {e}")
        import traceback
        traceback.print_exc()
        return None, f"Error al reutilizar el cuestionario: {str(e)}"
    finally:
        if connection:
            connection.close()
def registrar_cuestionarioSPDF(datos, id_docente):
    detalle = datos.get('detalle', {})
    preguntas = datos.get('preguntas', [])

    nombre = detalle.get('nombre_formulario', '').strip()
    if not nombre or len(nombre) < 3:
        return False, "El nombre del cuestionario debe tener al menos 3 caracteres"
    if len(nombre) > 200:
        return False, "El nombre del cuestionario no puede exceder 200 caracteres"
    
    tipo_formulario = detalle.get('tipo_formulario')
    if not tipo_formulario or tipo_formulario not in ['I', 'G']:
        return False, "Debe seleccionar un tipo de cuestionario válido"
    
    descripcion = detalle.get('descripcion_formulario', '').strip()
    if descripcion and len(descripcion) > 1000:
        return False, "La descripción no puede exceder 1000 caracteres"
    
    if not preguntas or len(preguntas) == 0:
        return False, "Debe agregar al menos una pregunta"
    
    if len(preguntas) > 50:
        return False, "No se pueden tener más de 50 preguntas"
    
    for index, pregunta in enumerate(preguntas, 1):
        nombre_pregunta = pregunta.get('nombre_pregunta', '').strip()
        if not nombre_pregunta or len(nombre_pregunta) < 5:
            return False, f"La pregunta {index} debe tener al menos 5 caracteres"
        if len(nombre_pregunta) > 500:
            return False, f"La pregunta {index} no puede exceder 500 caracteres"
        
        tipo_pregunta = pregunta.get('tipo_pregunta')
        if tipo_pregunta not in ['VF', 'ALT']:
            return False, f"La pregunta {index} debe tener un tipo válido (VF o ALT)"
        
        puntos = pregunta.get('puntos')
        try:
            puntos = int(puntos) if puntos else 0
        except (ValueError, TypeError):
            puntos = 0
        if not puntos or puntos <= 0 or puntos > 1000:
            return False, f"La pregunta {index} debe tener puntos entre 1 y 1000"
        
        tiempo = pregunta.get('tiempo')
        try:
            tiempo = int(tiempo) if tiempo else 0
        except (ValueError, TypeError):
            tiempo = 0
        if not tiempo or tiempo < 2 or tiempo > 300:
            return False, f"La pregunta {index} debe tener tiempo entre 2 y 300 segundos"
        
        respuesta = pregunta.get('respuesta', '').strip()
        if not respuesta:
            return False, f"La pregunta {index} debe tener una respuesta correcta"
        
        if tipo_pregunta == 'ALT':
            alternativas = pregunta.get('alternativas', [])
            if len(alternativas) < 2:
                return False, f"La pregunta {index} debe tener al menos 2 alternativas"
            if len(alternativas) > 6:
                return False, f"La pregunta {index} no puede tener más de 6 alternativas"
            
            if respuesta not in alternativas:
                return False, f"La respuesta correcta de la pregunta {index} debe estar en las alternativas"
            
            if len(alternativas) != len(set(alt.strip().lower() for alt in alternativas)):
                return False, f"La pregunta {index} no puede tener alternativas duplicadas"
        elif tipo_pregunta == 'VF':
            if respuesta not in ['Verdadero', 'Falso']:
                return False, f"La pregunta {index} debe tener respuesta 'Verdadero' o 'Falso'"
            
            alternativas = pregunta.get('alternativas', [])
            if len(alternativas) != 2 or set(alternativas) != {'Verdadero', 'Falso'}:
                pregunta['alternativas'] = ['Verdadero', 'Falso']

    connection = None
    try:
        connection = conexion.conectarbd()
        if connection:
            cursor = connection.cursor()

            query = """
                INSERT INTO Cuestionario (nombre, tipo_cuestionario, descripcion, pin, estado, id_docente, imagen_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            estado = detalle.get('estado')
            if estado == 'Público' or estado == 'P':
                estado = 'P'
            elif estado == 'Privado' or estado == 'R':
                estado = 'R'
            else:
                estado = 'P'

            imagen_url = detalle.get('imagen_url') or None

            cursor.execute(query, (
                nombre,
                tipo_formulario,
                descripcion if descripcion else None,
                crear_pin(),
                estado,
                id_docente,
                imagen_url
            ))

            id_cuestionario = cursor.lastrowid

            for pregunta_data in preguntas:
                nombre_pregunta_val = pregunta_data.get('nombre_pregunta', '').strip()
                puntos_val = pregunta_data.get('puntos')
                tiempo_val = pregunta_data.get('tiempo')
                tipo_pregunta_val = pregunta_data.get('tipo_pregunta')
                
                try:
                    puntos_val = int(puntos_val) if puntos_val else 0
                    tiempo_val = int(tiempo_val) if tiempo_val else 0
                except (ValueError, TypeError):
                    return False, f"Error al procesar puntos o tiempo de una pregunta"

                query = """
                    INSERT INTO Pregunta (pregunta, puntaje, tiempo_respuesta, tipo_pregunta, id_cuestionario)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    nombre_pregunta_val,
                    puntos_val,
                    tiempo_val,
                    tipo_pregunta_val,
                    id_cuestionario
                ))

                id_pregunta = cursor.lastrowid

                respuestas = pregunta_data.get('alternativas', [])
                respuesta = pregunta_data.get('respuesta', '').strip()

                for rpt in respuestas:
                    query = """
                        INSERT INTO Alternativa (respuesta, estado_alternativa, id_pregunta)
                        VALUES (%s, %s, %s)
                    """
                    estado_alt = 1 if str(rpt).strip() == str(respuesta).strip() else 0
                    cursor.execute(query, (rpt, estado_alt, id_pregunta))

            connection.commit()
            return True, "Cuestionario registrado exitosamente"
        else:
            return False, "Error al conectar con la base de datos"

    except Exception as e:
        if connection:
            connection.rollback()
        error_msg = f"Error al registrar el cuestionario: {str(e)}"
        print(f"Error en registrar_cuestionarioSPDF: {e}")
        print(f"Datos recibidos - Detalle: {detalle}, Preguntas: {len(preguntas) if preguntas else 0}")
        import traceback
        traceback.print_exc()
        return False, error_msg

    finally:
        if connection:
            connection.close()

def registrar_cuestionario(datos,id_docente):
    detalle = datos.get('detalle', {})
    preguntas = datos.get('preguntas', [])
    print("detalle" , detalle)
    print("pregfunta" , preguntas)
    connection = None
    try:
        connection = conexion.conectarbd()
        if connection:
            cursor = connection.cursor()

            query = """
                INSERT INTO Cuestionario (nombre, tipo_cuestionario, descripcion, pin, estado, id_docente, imagen_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            estado = detalle.get('estado')
            if (estado == 'Público'):
                estado = "P"
            elif (estado == 'Privado'):
                estado = 'R'
        
            imagen_url = detalle.get('imagen_url') or None

            cursor.execute(query, (
                detalle.get('nombre_formulario'),
                str(detalle.get('tipo_formulario', 'I'))[0],
                detalle.get('descripcion_formulario'),
                crear_pin(),
                estado,
                id_docente,
                imagen_url
            ))

            id_cuestionario = cursor.lastrowid
            for pregunta in preguntas:
                query = """
                    INSERT INTO Pregunta (pregunta, puntaje, tiempo_respuesta, tipo_pregunta, id_cuestionario)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    pregunta.get('nombre_pregunta'),
                    pregunta.get('puntos'),
                    pregunta.get('tiempo'),
                    str(pregunta.get('tipo_pregunta', 'ALT'))[:3],
                    id_cuestionario
                ))
                id_pregunta = cursor.lastrowid 

                respuestas = pregunta.get('alternativas')
                respuesta = pregunta.get('respuesta_correcta')
                
                if not respuestas:
                    print(f"⚠️ Error: La pregunta '{pregunta.get('nombre_pregunta')}' no tiene alternativas")
                    continue
                
                if not isinstance(respuestas, list):
                    if isinstance(respuestas, str):
                        respuestas = [x.strip() for x in respuestas.split(',') if x.strip()]
                    else:
                        respuestas = []
                
                if pregunta.get('tipo_pregunta') == 'VF' and not respuestas:
                    respuestas = ['Verdadero', 'Falso']
                    if not respuesta:
                        respuesta = 'Verdadero'
                
                for indice, rpt in enumerate(respuestas):
                    texto_alternativa = str(rpt).strip()
                    estado = 0
                    
                    if respuesta:
                        respuesta_str = str(respuesta).strip()
                        if texto_alternativa == respuesta_str:
                            estado = 1
                        elif respuesta_str.isdigit():
                            indice_correcto = int(respuesta_str) - 1
                            if indice == indice_correcto:
                                estado = 1
                    
                    query = """
                            INSERT INTO Alternativa (respuesta, estado_alternativa, id_pregunta)
                            VALUES (%s, %s, %s)
                        """
                    cursor.execute(query, (texto_alternativa, estado, id_pregunta))
            connection.commit()  
            return True
        else:
            return 3
    except Exception as e:
        connection.rollback()
        print(e)
        return False
    finally:
        if connection:
            connection.close()

def modificar_pregunta(id_pregunta, datos):
    """
    Modifica una pregunta existente y sus alternativas
    """
    connection = None
    try:
        connection = conexion.conectarbd()
        if not connection:
            return {'estado': False, 'mensaje': 'Error al conectar con la base de datos'}
        
        cursor = connection.cursor()
        
        # Validar que la pregunta exista
        cursor.execute("SELECT id_pregunta, id_cuestionario FROM Pregunta WHERE id_pregunta = %s", (id_pregunta,))
        pregunta_existente = cursor.fetchone()
        if not pregunta_existente:
            return {'estado': False, 'mensaje': 'La pregunta no existe'}
        
        # Validar datos
        nombre_pregunta = datos.get('nombre_pregunta', '').strip()
        if not nombre_pregunta or len(nombre_pregunta) < 5:
            return {'estado': False, 'mensaje': 'La pregunta debe tener al menos 5 caracteres'}
        if len(nombre_pregunta) > 500:
            return {'estado': False, 'mensaje': 'La pregunta no puede exceder 500 caracteres'}
        
        puntos = datos.get('puntos')
        try:
            puntos = int(puntos) if puntos else 0
        except (ValueError, TypeError):
            puntos = 0
        if not puntos or puntos <= 0 or puntos > 1000:
            return {'estado': False, 'mensaje': 'Los puntos deben estar entre 1 y 1000'}
        
        tiempo = datos.get('tiempo')
        try:
            tiempo = int(tiempo) if tiempo else 0
        except (ValueError, TypeError):
            tiempo = 0
        if not tiempo or tiempo < 2 or tiempo > 300:
            return {'estado': False, 'mensaje': 'El tiempo debe estar entre 2 y 300 segundos'}
        
        tipo_pregunta = datos.get('tipo_pregunta')
        if tipo_pregunta not in ['VF', 'ALT']:
            return {'estado': False, 'mensaje': 'Tipo de pregunta inválido'}
        
        alternativas = datos.get('alternativas', [])
        respuesta = datos.get('respuesta', '').strip()
        
        if not respuesta:
            return {'estado': False, 'mensaje': 'Debe especificar una respuesta correcta'}
        
        if tipo_pregunta == 'ALT':
            if len(alternativas) < 2:
                return {'estado': False, 'mensaje': 'Debe tener al menos 2 alternativas'}
            if len(alternativas) > 6:
                return {'estado': False, 'mensaje': 'No puede tener más de 6 alternativas'}
            if respuesta not in alternativas:
                return {'estado': False, 'mensaje': 'La respuesta correcta debe estar en las alternativas'}
        elif tipo_pregunta == 'VF':
            if respuesta not in ['Verdadero', 'Falso']:
                return {'estado': False, 'mensaje': 'La respuesta debe ser Verdadero o Falso'}
            alternativas = ['Verdadero', 'Falso']
        
        # Actualizar la pregunta
        query = """
            UPDATE Pregunta 
            SET pregunta = %s, puntaje = %s, tiempo_respuesta = %s, tipo_pregunta = %s
            WHERE id_pregunta = %s
        """
        cursor.execute(query, (nombre_pregunta, puntos, tiempo, tipo_pregunta, id_pregunta))
        
        # Eliminar alternativas existentes
        cursor.execute("DELETE FROM Alternativa WHERE id_pregunta = %s", (id_pregunta,))
        
        # Insertar nuevas alternativas
        for alt in alternativas:
            estado_alt = 1 if str(alt).strip() == str(respuesta).strip() else 0
            cursor.execute(
                "INSERT INTO Alternativa (respuesta, estado_alternativa, id_pregunta) VALUES (%s, %s, %s)",
                (alt, estado_alt, id_pregunta)
            )
        
        connection.commit()
        return {'estado': True, 'mensaje': 'Pregunta modificada correctamente'}
        
    except Exception as e:
        if connection:
            connection.rollback()
        print(f"Error en modificar_pregunta: {e}")
        import traceback
        traceback.print_exc()
        return {'estado': False, 'mensaje': f'Error al modificar la pregunta: {str(e)}'}
    finally:
        if connection:
            connection.close()

def eliminar_pregunta(id_pregunta):
    """
    Elimina una pregunta y sus alternativas
    """
    connection = None
    try:
        connection = conexion.conectarbd()
        if not connection:
            return {'estado': False, 'mensaje': 'Error al conectar con la base de datos'}
        
        cursor = connection.cursor()
        
        # Verificar que la pregunta exista
        cursor.execute("SELECT id_pregunta FROM Pregunta WHERE id_pregunta = %s", (id_pregunta,))
        if not cursor.fetchone():
            return {'estado': False, 'mensaje': 'La pregunta no existe'}
        
        # Eliminar alternativas primero (por foreign key)
        cursor.execute("DELETE FROM Alternativa WHERE id_pregunta = %s", (id_pregunta,))
        
        # Eliminar la pregunta
        cursor.execute("DELETE FROM Pregunta WHERE id_pregunta = %s", (id_pregunta,))
        
        connection.commit()
        return {'estado': True, 'mensaje': 'Pregunta eliminada correctamente'}
        
    except Exception as e:
        if connection:
            connection.rollback()
        print(f"Error en eliminar_pregunta: {e}")
        import traceback
        traceback.print_exc()
        return {'estado': False, 'mensaje': f'Error al eliminar la pregunta: {str(e)}'}
    finally:
        if connection:
            connection.close()

def agregar_pregunta_a_cuestionario(id_cuestionario, datos_pregunta):
    """
    Agrega una nueva pregunta a un cuestionario existente
    """
    connection = None
    try:
        connection = conexion.conectarbd()
        if not connection:
            return {'estado': False, 'mensaje': 'Error al conectar con la base de datos', 'id_pregunta': None}
        
        cursor = connection.cursor()
        
        # Verificar que el cuestionario exista
        cursor.execute("SELECT id_cuestionario FROM Cuestionario WHERE id_cuestionario = %s", (id_cuestionario,))
        if not cursor.fetchone():
            return {'estado': False, 'mensaje': 'El cuestionario no existe', 'id_pregunta': None}
        
        # Validar datos
        nombre_pregunta = datos_pregunta.get('nombre_pregunta', '').strip()
        if not nombre_pregunta or len(nombre_pregunta) < 5:
            return {'estado': False, 'mensaje': 'La pregunta debe tener al menos 5 caracteres', 'id_pregunta': None}
        if len(nombre_pregunta) > 500:
            return {'estado': False, 'mensaje': 'La pregunta no puede exceder 500 caracteres', 'id_pregunta': None}
        
        puntos = datos_pregunta.get('puntos')
        try:
            puntos = int(puntos) if puntos else 0
        except (ValueError, TypeError):
            puntos = 0
        if not puntos or puntos <= 0 or puntos > 1000:
            return {'estado': False, 'mensaje': 'Los puntos deben estar entre 1 y 1000', 'id_pregunta': None}
        
        tiempo = datos_pregunta.get('tiempo')
        try:
            tiempo = int(tiempo) if tiempo else 0
        except (ValueError, TypeError):
            tiempo = 0
        if not tiempo or tiempo < 2 or tiempo > 300:
            return {'estado': False, 'mensaje': 'El tiempo debe estar entre 2 y 300 segundos', 'id_pregunta': None}
        
        tipo_pregunta = datos_pregunta.get('tipo_pregunta')
        if tipo_pregunta not in ['VF', 'ALT']:
            return {'estado': False, 'mensaje': 'Tipo de pregunta inválido', 'id_pregunta': None}
        
        alternativas = datos_pregunta.get('alternativas', [])
        respuesta = datos_pregunta.get('respuesta', '').strip()
        
        if not respuesta:
            return {'estado': False, 'mensaje': 'Debe especificar una respuesta correcta', 'id_pregunta': None}
        
        if tipo_pregunta == 'ALT':
            if len(alternativas) < 2:
                return {'estado': False, 'mensaje': 'Debe tener al menos 2 alternativas', 'id_pregunta': None}
            if len(alternativas) > 6:
                return {'estado': False, 'mensaje': 'No puede tener más de 6 alternativas', 'id_pregunta': None}
            if respuesta not in alternativas:
                return {'estado': False, 'mensaje': 'La respuesta correcta debe estar en las alternativas', 'id_pregunta': None}
        elif tipo_pregunta == 'VF':
            if respuesta not in ['Verdadero', 'Falso']:
                return {'estado': False, 'mensaje': 'La respuesta debe ser Verdadero o Falso', 'id_pregunta': None}
            alternativas = ['Verdadero', 'Falso']
        
        # Insertar la pregunta
        query = """
            INSERT INTO Pregunta (pregunta, puntaje, tiempo_respuesta, tipo_pregunta, id_cuestionario)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (nombre_pregunta, puntos, tiempo, tipo_pregunta, id_cuestionario))
        id_pregunta = cursor.lastrowid
        
        # Insertar alternativas
        for alt in alternativas:
            estado_alt = 1 if str(alt).strip() == str(respuesta).strip() else 0
            cursor.execute(
                "INSERT INTO Alternativa (respuesta, estado_alternativa, id_pregunta) VALUES (%s, %s, %s)",
                (alt, estado_alt, id_pregunta)
            )
        
        connection.commit()
        return {'estado': True, 'mensaje': 'Pregunta agregada correctamente', 'id_pregunta': id_pregunta}
        
    except Exception as e:
        if connection:
            connection.rollback()
        print(f"Error en agregar_pregunta_a_cuestionario: {e}")
        import traceback
        traceback.print_exc()
        return {'estado': False, 'mensaje': f'Error al agregar la pregunta: {str(e)}', 'id_pregunta': None}
    finally:
        if connection:
            connection.close()


