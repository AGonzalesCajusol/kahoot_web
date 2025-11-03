import conexion
import random

def datos_cuestionario(id_for):
    conn = conexion.conectarbd()
    print(id_for)
    with conn.cursor() as cursor:
        sql = '''
            SELECT 
                pr.id_pregunta,
                pr.pregunta,        -- texto de la pregunta
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
                SELECT id_cuestionario, nombre, tipo_cuestionario, pin
                FROM Cuestionario
                WHERE estado_cuestionario = 'A' AND id_docente = %s
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
                SELECT id_cuestionario, nombre, tipo_cuestionario, pin
                FROM Cuestionario
                WHERE estado_cuestionario = 'I' AND id_docente = %s
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
    connection = None
    try:
        connection = conexion.conectarbd()
        if connection:
            cursor = connection.cursor()

            query = """
                UPDATE Usuario
                SET puntaje = %s
                WHERE id_usuario = %s
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
                SELECT id_cuestionario, tipo_cuestionario, estado_cuestionario, estado_juego
                FROM Cuestionario
                WHERE pin = %s AND estado_cuestionario = 'A'
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

            # Validar que el estado sea permitido
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

def crear_pin():
    pin = str(random.randint(10000, 99999))
    return pin
def registrar_cuestionarioSPDF(datos, id_docente):
    detalle = datos.get('detalle', {})
    preguntas = datos.get('preguntas', [])
    print("📘 Detalle:", detalle)
    print("❓ Preguntas:", preguntas)

    connection = None
    try:
        connection = conexion.conectarbd()
        if connection:
            cursor = connection.cursor()

            query = """
                INSERT INTO Cuestionario (nombre, tipo_cuestionario, descripcion, pin, estado, id_docente)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            estado = detalle.get('estado')
            if estado == 'Público':
                estado = 'P'
            elif estado == 'Privado':
                estado = 'R'

            cursor.execute(query, (
                detalle.get('nombre_cuestionario'),  # ✅ corregido
                detalle.get('tipo_formulario'),      # ✅ sin [0]
                detalle.get('descripcion_formulario'),
                crear_pin(),
                estado,
                id_docente
            ))

            id_cuestionario = cursor.lastrowid
            print(f"✅ Cuestionario creado con ID: {id_cuestionario}")

            for pregunta in preguntas:
                print("🟢 Insertando pregunta:", pregunta.get('nombre_pregunta'))

                query = """
                    INSERT INTO Pregunta (pregunta, puntaje, tiempo_respuesta, tipo_pregunta, id_cuestionario)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    pregunta.get('nombre_pregunta'),
                    pregunta.get('puntos'),
                    pregunta.get('tiempo'),
                    pregunta.get('tipo_pregunta'),
                    id_cuestionario
                ))

                id_pregunta = cursor.lastrowid
                print(f"   ↳ ID pregunta: {id_pregunta}")

                respuestas = pregunta.get('alternativas', [])
                respuesta = pregunta.get('respuesta')  # ✅ corregido

                for rpt in respuestas:
                    query = """
                        INSERT INTO Alternativa (respuesta, estado_alternativa, id_pregunta)
                        VALUES (%s, %s, %s)
                    """
                    estado_alt = 1 if str(rpt).strip() == str(respuesta).strip() else 0
                    cursor.execute(query, (rpt, estado_alt, id_pregunta))
                    print(f"      ↳ Alternativa: {rpt} ({'Correcta' if estado_alt else 'Incorrecta'})")

            connection.commit()
            print("✅ Todo insertado correctamente.")
            return True
        else:
            print("⚠️ No se pudo conectar a la base de datos.")
            return 3

    except Exception as e:
        if connection:
            connection.rollback()
        print("❌ Error:", e)
        return False

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
                INSERT INTO Cuestionario (nombre, tipo_cuestionario, descripcion, pin, estado, id_docente)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            estado = detalle.get('estado')
            if (estado == 'Público'):
                estado = "P"
            elif (estado == 'Privado'):
                estado = 'R'
        

            cursor.execute(query, (
                detalle.get('nombre_formulario'),
                detalle.get('tipo_formulario')[0],
                detalle.get('descripcion_formulario'),
                crear_pin(),
                estado,
                id_docente
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
                    pregunta.get('tipo_pregunta'),
                    id_cuestionario
                ))
                id_pregunta = cursor.lastrowid 

                respuestas = pregunta.get('alternativas')
                respuesta = pregunta.get('respuesta_correcta')
                for rpt in respuestas:
                    query = """
                            INSERT INTO Alternativa (respuesta, estado_alternativa, id_pregunta)
                            VALUES (%s, %s, %s)
                        """
                    estado = 1 if str(rpt).strip() == respuesta  else 0
                    cursor.execute(query, (rpt, estado ,id_pregunta))
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





