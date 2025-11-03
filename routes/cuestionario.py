from flask import redirect, render_template, request, jsonify, session, url_for
import conexion
from controladores import cuestionario
from controladores import docente


def registrar_rutas(app):
    @app.route('/registrar_respuestasform', methods=['POST'])
    def registrar_respuestasform():
        id_participante = session['id_usuario']
        datos = request.get_json()
        cuestionario.actualizar_puntaje_usuario(id_participante, datos.get('puntaje'))
        return {'puntaje': 12}


    @app.route('/registrar_cuestionario', methods=['POST'])
    def registrar_cuestionario():
        datos = request.get_json()

        nombre = datos.get('nombre')
        tipo = datos.get('tipo')
        descripcion = datos.get('descripcion')
        estado = datos.get('estado')
        fecha_programacion = datos.get('fecha_programacion')
        id_docente = datos.get('id_docente')

        response = cuestionario.registrar_cuestionario(nombre, tipo, descripcion, estado, fecha_programacion, id_docente)

        if "exitosamente" in response:
            return jsonify({"message": response}), 201  
        else:
            return jsonify({"message": response}), 400

    # Ruta para registrar formulario
    @app.route('/registrar_pregunta', methods=['POST'])
    def registrar_pregunta():
        datos = request.get_json()
        print("estos son los datos", datos)
        id_docente = session['docente_id']
        response = cuestionario.registrar_cuestionarioSPDF(datos, id_docente)
        if response:
            return jsonify({'estado': True})
        
        return jsonify({'estado': False})

    @app.route('/registrar_alternativa', methods=['POST'])
    def registrar_alternativa_route():
        datos = request.get_json()  
        respuesta = datos.get('respuesta')
        estado = datos.get('estado')
        id_pregunta = datos.get('id_pregunta')

        response = cuestionario.registrar_alternativa(respuesta, estado, id_pregunta)

        if "registrada exitosamente" in response:
            return jsonify({"message": response}), 201
        else:
            return jsonify({"message": response}), 400

    
    @app.route('/cuestionarios_activos', methods=['GET'], endpoint='cuestionarios_activos_endpoint')
    def cuestionarios_activos():
        id_docente = request.args.get('id_docente') 
        print("ID Docente recibido:", id_docente)
        if not id_docente:
            return jsonify({'error': 'Falta id_docente'}), 400 
        
        
        cuestionarios = cuestionario.obtener_cuestionarios_activos(id_docente)
        print(cuestionarios)
        return jsonify(cuestionarios)

    @app.route('/cuestionarios_archivados', methods=['GET'], endpoint='cuestionarios_archivados_endpoint')
    def cuestionarios_archivados():
        id_docente = request.args.get('id_docente')  
        print("ID Docente recibido:", id_docente)
        if not id_docente:
            return jsonify({'error': 'Falta id_docente'}), 400
        
        cuestionarios = cuestionario.obtener_cuestionarios_archivados(id_docente)
        print(cuestionarios)
        return jsonify(cuestionarios)

    @app.route('/validar_pin', methods=['POST'])
    def validar_pin_route():
        try:
            datos = request.get_json()
            pin = datos.get('pin')

            if not pin:
                return jsonify({"error": "PIN es requerido"}), 400

            resultado = cuestionario.validar_pin(pin)

            if not resultado:
                return jsonify({"error": "PIN inválido o cuestionario inactivo"}), 400

            id_cuestionario = resultado['id_cuestionario']
            tipo_cuestionario = resultado['tipo_cuestionario']
            estado_cuestionario = resultado['estado_cuestionario']
            estado_juego = resultado['estado_juego']

            print(f"id_cuestionario: {id_cuestionario}, tipo_cuestionario: {tipo_cuestionario}, estado_cuestionario: {estado_cuestionario}, estado_juego: {estado_juego}")

            if estado_juego == 'IN':
                return jsonify({"error":"El juego ya inicio"}), 400
            elif estado_juego == 'FN':
                return jsonify({"error": "el juego ya finalizo"}), 400

            session['id_cuestionario'] = id_cuestionario
            session['tipo_cuestionario'] = tipo_cuestionario

            return jsonify({
                "id_cuestionario": id_cuestionario,
                "tipo_cuestionario": tipo_cuestionario,
                "estado_cuestionario": estado_cuestionario,
                "estado_juego" : estado_juego
            }), 200

        except Exception as e:
            print(f"Error en /validar_pin: {e}")
            return jsonify({"error": "Error interno del servidor"}), 500

    @app.route('/registrar_alias')
    def registrar_alias():
        id_cuestionario = session['id_cuestionario']
        print(id_cuestionario)
        return render_template('alias.html', id_cuestionario=id_cuestionario)

    @app.route('/verificar_alias', methods=['POST'])
    def verificar_alias():
        data = request.get_json()
        alias = data.get('alias')
        id_cuestionario = data.get('id_cuestionario')

        connection = conexion.conectarbd()
        if not connection:
            return jsonify({'error': 'Error al conectar con la base de datos'}), 500

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id_usuario FROM Usuario
                    WHERE alias = %s AND id_cuestionario = %s
                """, (alias, id_cuestionario))
                existente = cursor.fetchone()

                if existente:
                    return jsonify({'error': 'Alias ya en uso, elige otro nombre'}), 400

                cursor.execute("""
                    INSERT INTO Usuario (alias, id_cuestionario, puntaje)
                    VALUES (%s, %s, 0)
                """, (alias, id_cuestionario))
                session['id_usuario'] = cursor.lastrowid
                connection.commit()
                return jsonify({'success': True}), 200

        except Exception as e:
            print("Error en verificar_alias:", e)
            return jsonify({'error': 'Error interno del servidor'}), 500

        finally:
            connection.close()

    @app.route('/sala_espera/<int:id_cuestionario>')
    def sala_espera(id_cuestionario):
        connection = conexion.conectarbd()
        cursor = connection.cursor()

        query_cuestionario = """
            SELECT 
                c.nombre AS nombre_cuestionario,
                c.pin,
                CONCAT(d.nombres, ' ', d.apellidos) AS nombre_docente
            FROM Cuestionario c
            INNER JOIN Docente d ON c.id_docente = d.id_docente
            WHERE c.id_cuestionario = %s
        """
        cursor.execute(query_cuestionario, (id_cuestionario,))
        cuestionario = cursor.fetchone()

        if not cuestionario:
            cursor.close()
            connection.close()
            return "Cuestionario no encontrado", 404

        query_usuarios = """
            SELECT alias, puntaje
            FROM Usuario
            WHERE id_cuestionario = %s
            ORDER BY id_usuario ASC
        """
        cursor.execute(query_usuarios, (id_cuestionario,))
        resultados = cursor.fetchall()

        usuarios = [{"alias": row["alias"], "puntaje": row["puntaje"]} for row in resultados]

        cursor.close()
        connection.close()

        return render_template(
            'sala_espera.html',
            cuestionario=cuestionario,
            usuarios=usuarios
        )
    import pandas as pd
    @app.route('/subirformulario_excel', methods=['POST'])
    def subirformulario_excel():
        excel = request.files['excel_archivo']
        df = pd.read_excel(excel)

        # Dividir por columnas
        formulario_cols = df.columns[0:4]   # A–D
        pregunta_cols = df.columns[4:10]     # E–I

        # Crear JSON del formulario (usamos la primera fila)
        formulario = df[formulario_cols].iloc[0].to_dict()

        # Crear JSON de preguntas (todas las filas)
        preguntas = df[pregunta_cols].to_dict(orient='records')

        # Limpiar respuestas (separar por comas)
        for p in preguntas:
            if isinstance(p.get('respuestas'), str):
                p['respuestas'] = [x.strip() for x in p['respuestas'].split(',')]

        resultado = {
            "detalle": formulario,
            "preguntas": preguntas
        }
        print(resultado)

        id_docente = session['docente_id']
        response = cuestionario.registrar_cuestionario(resultado, id_docente)
        if(response):
            return jsonify({'estado': True, 'mensaje': 'se registro con éxito!!, la página se actualizara..'})
        elif(response== False):
            return jsonify({'estado': False, 'mensaje': 'No cumple con el formato el excel revise el formato de guía'})
        #error de bd
        return 'asdnas'
    
    