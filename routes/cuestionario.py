from flask import request, jsonify
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

    @app.route('/registrar_pregunta', methods=['POST'])
    def registrar_pregunta_route():
        datos = request.get_json()
        pregunta_texto = datos.get('pregunta')
        puntaje = datos.get('puntaje')
        tiempo = datos.get('tiempo')
        tipo_pregunta = datos.get('tipo_pregunta')
        id_cuestionario = 6  

        id_pregunta = cuestionario.registrar_pregunta(pregunta_texto, puntaje, tiempo, tipo_pregunta, id_cuestionario)

        if isinstance(id_pregunta, int):
            return jsonify({"message": "Pregunta registrada exitosamente", "id_pregunta": id_pregunta}), 201
        else:
            return jsonify({"message": id_pregunta}), 400
        



