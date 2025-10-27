from flask import request, jsonify, session
from controladores import cuestionario


def registrar_rutas(app):
    @app.route('/registrar_cuestionario', methods=['POST'])
    def registrar_cuestionario():
        datos = request.get_json()

        nombre = datos.get('nombre')
        tipo = datos.get('tipo')
        descripcion = datos.get('descripcion')
        estado = datos.get('estado')
        pin = datos.get('pin')
        fecha_programacion = datos.get('fecha_programacion')
        id_docente = datos.get('id_docente')

        response = cuestionario.registrar_cuestionario(nombre, tipo, descripcion, estado, pin, fecha_programacion, id_docente)

        if "exitosamente" in response:
            return jsonify({"message": response}), 201  
        else:
            return jsonify({"message": response}), 400

    # Ruta para registrar formulario
    @app.route('/registrar_pregunta', methods=['POST'])
    def registrar_pregunta():
        datos = request.get_json()
        id_docente = session['docente_id']
        response = cuestionario.registrar_cuestionario(datos, id_docente)
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
