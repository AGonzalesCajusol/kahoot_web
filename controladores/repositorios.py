from conexion import conectarbd

def obtener_cuestionarios_publicos():
    try:        
        connection = conectarbd()
        if connection:
            cursor = connection.cursor()

            query = "SELECT  c.id_cuestionario, c.nombre, c.tipo_cuestionario, c.descripcion, c.pin, c.imagen_url, " \
            "CONCAT(d.nombres, ' ', d.apellidos) AS docente_completo FROM  Cuestionario c LEFT JOIN " \
            "Docente d ON c.id_docente = d.id_docente WHERE c.estado = 'P'"
            
            cursor.execute(query)

            cuestionarios = cursor.fetchall()

            connection.close()

            return cuestionarios  
        
    except Exception as e:
        print(f"Error al obtener los cuestionarios: {e}")
        return None
