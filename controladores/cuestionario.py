import conexion

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


def registrar_cuestionario(datos,id_docente):
    detalle = datos.get('detalle', {})
    preguntas = datos.get('preguntas', [])
    connection = None
    try:
        connection = conexion.conectarbd()
        if connection:
            cursor = connection.cursor()

            query = """
                INSERT INTO Cuestionario (nombre, tipo_cuestionario, descripcion, estado, pin, fecha_programacion, id_docente)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                detalle.get('nombre_cuestionario'),
                detalle.get('tipo_formulario'),
                detalle.get('descripcion_formulario'),
                detalle.get('estado'),
                detalle.get('pin'),
                detalle.get('fecha_programacion'),
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
                respuesta = pregunta.get('respuesta')
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

def validar_pin(pin):
    connection = None
    try:
        connection = conexion.conectarbd()
        if connection:
            cursor = connection.cursor() 
            
            query = """
                SELECT id_cuestionario, tipo_cuestionario, estado_cuestionario
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









