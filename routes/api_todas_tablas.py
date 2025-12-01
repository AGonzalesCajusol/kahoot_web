from flask import request, jsonify
from flask_jwt import jwt_required
from controladores import docente as controlador_docente
from controladores import jugador as controlador_jugador
from controladores import cuestionario as controlador_cuestionario
from controladores import grupo as controlador_grupo
from controladores import recompensa as controlador_recompensa
from controladores import respuestas as controlador_respuestas
from conexion import conectarbd
import hashlib

def registrar_rutas_api(app):
    """
    Registra las rutas de API REST para todas las tablas
    Todas las rutas requieren autenticación JWT
    5 APIs por cada tabla: registrar, actualizar, obtener por ID, obtener todos, eliminar
    """
    
    # ========== DOCENTE (ya existe, pero lo incluimos para completitud) ==========
    @app.route("/api_registrar_docente", methods=["POST"])
    @jwt_required()
    def api_registrar_docente():
        try:
            data = request.json
            correo = data.get("correo")
            password = data.get("password")
            nombres = data.get("nombres")
            apellidos = data.get("apellidos")
            
            if not correo or not password or not nombres or not apellidos:
                return jsonify({"data": [], "message": "Faltan campos obligatorios", "status": 0}), 400
            
            docente_existente = controlador_docente.obtener_docente_por_email(correo)
            if docente_existente:
                return jsonify({"data": [], "message": "El correo ya está registrado", "status": 0}), 400
            
            resultado = controlador_docente.insertar_docente(correo, password, nombres, apellidos)
            if resultado:
                return jsonify({"data": [], "message": "Docente registrado correctamente", "status": 1}), 201
            else:
                return jsonify({"data": [], "message": "Error al registrar el docente", "status": 0}), 500
        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_actualizar_docente", methods=["POST"])
    @jwt_required()
    def api_actualizar_docente():
        try:
            data = request.json
            id_docente = data.get("id_docente")
            if not id_docente:
                return jsonify({"data": [], "message": "El campo id_docente es obligatorio", "status": 0}), 400
            
            docente_existente = controlador_docente.obtener_docente_por_id(id_docente)
            if not docente_existente:
                return jsonify({"data": [], "message": "El docente no existe", "status": 0}), 404
            
            resultado = controlador_docente.actualizar_docente(
                id_docente, data.get("correo"), data.get("password"), 
                data.get("nombres"), data.get("apellidos")
            )
            if resultado:
                return jsonify({"data": [], "message": "Docente actualizado correctamente", "status": 1}), 200
            else:
                return jsonify({"data": [], "message": "Error al actualizar el docente", "status": 0}), 500
        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_obtener_docente_id", methods=["GET"])
    @jwt_required()
    def api_obtener_docente_id():
        try:
            data = request.json if request.is_json else {}
            id_docente = data.get("id_docente") or request.args.get("id_docente")
            if not id_docente:
                return jsonify({"data": [], "message": "El campo id_docente es obligatorio", "status": 0}), 400
            
            try:
                id_docente = int(id_docente)
            except ValueError:
                return jsonify({"data": [], "message": "El id_docente debe ser un número", "status": 0}), 400
            
            docente = controlador_docente.obtener_docente_por_id(id_docente)
            if not docente:
                return jsonify({"data": [], "message": "Docente no encontrado", "status": 0}), 404
            
            docente_dict = {
                "ID docente": docente[0],
                "Correo": docente[1],
                "Nombres": docente[3],
                "Apellidos": docente[4]
            }
            return jsonify({"data": [docente_dict], "message": "Docente obtenido correctamente", "status": 1}), 200
        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_obtener_docentes", methods=["GET"])
    @jwt_required()
    def api_obtener_docentes():
        try:
            docentes = controlador_docente.obtener_docentes()
            data_list = []
            for docente in docentes:
                docente_dict = {
                    "ID docente": docente[0],
                    "Correo": docente[1],
                    "Nombres": docente[3],
                    "Apellidos": docente[4]
                }
                data_list.append(docente_dict)
            return jsonify({"data": data_list, "message": "Listado correcto de docentes", "status": 1}), 200
        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_eliminar_docente", methods=["DELETE"])
    @jwt_required()
    def api_eliminar_docente():
        try:
            data = request.json if request.is_json else {}
            id_docente = data.get("id_docente")
            if not id_docente:
                return jsonify({"data": [], "message": "El campo id_docente es obligatorio", "status": 0}), 400
            
            try:
                id_docente = int(id_docente)
            except ValueError:
                return jsonify({"data": [], "message": "El id_docente debe ser un número", "status": 0}), 400
            
            docente_existente = controlador_docente.obtener_docente_por_id(id_docente)
            if not docente_existente:
                return jsonify({"data": [], "message": "El docente no existe", "status": 0}), 404
            
            resultado = controlador_docente.eliminar_docente(id_docente)
            if resultado:
                return jsonify({"data": [], "message": "Docente eliminado correctamente", "status": 1}), 200
            else:
                return jsonify({"data": [], "message": "Error al eliminar el docente", "status": 0}), 500
        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    # ========== JUGADOR ==========
    @app.route("/api_registrar_jugador", methods=["POST"])
    @jwt_required()
    def api_registrar_jugador():
        try:
            data = request.json
            email = data.get("email")
            password = data.get("password")
            
            if not email or not password:
                return jsonify({"data": [], "message": "Faltan campos obligatorios: email, password", "status": 0}), 400
            
            jugador_existente = controlador_jugador.obtener_jugador_por_email(email)
            if jugador_existente:
                return jsonify({"data": [], "message": "El email ya está registrado", "status": 0}), 400
            
            resultado = controlador_jugador.insertar_jugador(email, password)
            if resultado:
                return jsonify({"data": [], "message": "Jugador registrado correctamente", "status": 1}), 201
            else:
                return jsonify({"data": [], "message": "Error al registrar el jugador", "status": 0}), 500
        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_actualizar_jugador", methods=["POST"])
    @jwt_required()
    def api_actualizar_jugador():
        try:
            data = request.json
            id_jugador = data.get("id_jugador")
            if not id_jugador:
                return jsonify({"data": [], "message": "El campo id_jugador es obligatorio", "status": 0}), 400
            
            jugador_existente = controlador_jugador.obtener_jugador_por_id(id_jugador)
            if not jugador_existente:
                return jsonify({"data": [], "message": "El jugador no existe", "status": 0}), 404
            
            resultado = controlador_jugador.actualizar_jugador(
                id_jugador, data.get("email"), data.get("password")
            )
            if resultado:
                return jsonify({"data": [], "message": "Jugador actualizado correctamente", "status": 1}), 200
            else:
                return jsonify({"data": [], "message": "Error al actualizar el jugador", "status": 0}), 500
        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_obtener_jugador_id", methods=["GET"])
    @jwt_required()
    def api_obtener_jugador_id():
        try:
            data = request.json if request.is_json else {}
            id_jugador = data.get("id_jugador") or request.args.get("id_jugador")
            if not id_jugador:
                return jsonify({"data": [], "message": "El campo id_jugador es obligatorio", "status": 0}), 400
            
            try:
                id_jugador = int(id_jugador)
            except ValueError:
                return jsonify({"data": [], "message": "El id_jugador debe ser un número", "status": 0}), 400
            
            jugador = controlador_jugador.obtener_jugador_por_id(id_jugador)
            if not jugador:
                return jsonify({"data": [], "message": "Jugador no encontrado", "status": 0}), 404
            
            jugador_dict = {
                "ID jugador": jugador[0],
                "Email": jugador[1]
            }
            return jsonify({"data": [jugador_dict], "message": "Jugador obtenido correctamente", "status": 1}), 200
        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_obtener_jugadores", methods=["GET"])
    @jwt_required()
    def api_obtener_jugadores():
        try:
            jugadores = controlador_jugador.obtener_jugadores()
            data_list = []
            for jugador in jugadores:
                jugador_dict = {
                    "ID jugador": jugador[0],
                    "Email": jugador[1]
                }
                data_list.append(jugador_dict)
            return jsonify({"data": data_list, "message": "Listado correcto de jugadores", "status": 1}), 200
        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_eliminar_jugador", methods=["DELETE"])
    @jwt_required()
    def api_eliminar_jugador():
        try:
            data = request.json if request.is_json else {}
            id_jugador = data.get("id_jugador")
            if not id_jugador:
                return jsonify({"data": [], "message": "El campo id_jugador es obligatorio", "status": 0}), 400
            
            try:
                id_jugador = int(id_jugador)
            except ValueError:
                return jsonify({"data": [], "message": "El id_jugador debe ser un número", "status": 0}), 400
            
            jugador_existente = controlador_jugador.obtener_jugador_por_id(id_jugador)
            if not jugador_existente:
                return jsonify({"data": [], "message": "El jugador no existe", "status": 0}), 404
            
            resultado = controlador_jugador.eliminar_jugador(id_jugador)
            if resultado:
                return jsonify({"data": [], "message": "Jugador eliminado correctamente", "status": 1}), 200
            else:
                return jsonify({"data": [], "message": "Error al eliminar el jugador", "status": 0}), 500
        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

