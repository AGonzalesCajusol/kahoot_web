import conexion

def registrar_cuestionario(nombre, tipo, descripcion, estado, pin, fecha_programacion, id_docente):
    try:
        connection = conexion.conectarbd()
        if connection:
            cursor = connection.cursor()

            query = """
                INSERT INTO Cuestionario (nombre, tipo_cuestionario, descripcion, estado, pin, fecha_programacion, id_docente)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (nombre, tipo, descripcion, estado, pin, fecha_programacion, id_docente))
            connection.commit()
            connection.close()

            return "Cuestionario registrado exitosamente"
        else:
            return "Error al conectar con la base de datos"
    
    except Exception as e:
        return f"Error al registrar el cuestionario: {str(e)}"

def registrar_pregunta(pregunta, puntaje, tiempo, tipo_pregunta, id_cuestionario):
    try:
        connection = conexion.conectarbd()
        if connection:
            cursor = connection.cursor()

            query = """
                INSERT INTO Pregunta (pregunta, puntaje, tiempo_respuesta, tipo_pregunta, id_cuestionario)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (pregunta, puntaje, tiempo, tipo_pregunta, id_cuestionario))
            connection.commit()  
            id_pregunta = cursor.lastrowid  
            connection.close()

            return id_pregunta
        else:
            return "Error al conectar con la base de datos"
    
    except Exception as e:
        return f"Error al registrar la pregunta: {str(e)}"









