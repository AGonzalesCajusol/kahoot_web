from flask import request, jsonify
from flask_jwt import jwt_required
import random
from controladores import docente as controlador_docente
from controladores import jugador as controlador_jugador
from controladores import cuestionario as controlador_cuestionario
from controladores import grupo as controlador_grupo
from controladores import recompensa as controlador_recompensa
from conexion import conectarbd

# Importar controlador de respuestas si está disponible
try:
    from controladores import respuestas as controlador_respuestas
except ImportError:
    controlador_respuestas = None

def registrar_rutas_api(app):
    """
    Registra todas las rutas de API REST para todas las tablas.
    La mayoría de las rutas requieren autenticación JWT.
    Algunas rutas de lectura (GET) no requieren autenticación.
    """
    
    # ============================================
    # APIs PARA TABLA DOCENTE
    # ============================================
    
    @app.route("/api_registrar_docente", methods=["POST"])
    @jwt_required()
    def api_registrar_docente():
        """API para registrar un nuevo docente"""
        try:
            data = request.json
            correo = data.get("correo")
            password = data.get("password")
            nombres = data.get("nombres")
            apellidos = data.get("apellidos")
            
            if not correo or not password or not nombres or not apellidos:
                return jsonify({
                    "data": [],
                    "message": "Faltan campos obligatorios: correo, password, nombres, apellidos",
                    "status": 0
                }), 400
            
            docente_existente = controlador_docente.obtener_docente_por_email(correo)
            if docente_existente:
                return jsonify({
                    "data": [],
                    "message": "El correo ya está registrado",
                    "status": 0
                }), 400
            
            resultado = controlador_docente.insertar_docente(correo, password, nombres, apellidos)
            
            if resultado:
                return jsonify({
                    "data": [],
                    "message": "Docente registrado correctamente",
                    "status": 1
                }), 201
            else:
                return jsonify({
                    "data": [],
                    "message": "Error al registrar el docente",
                    "status": 0
                }), 500

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_actualizar_docente", methods=["POST"])
    @jwt_required()
    def api_actualizar_docente():
        """API para actualizar un docente existente"""
        try:
            data = request.json
            id_docente = data.get("id_docente")
            
            if not id_docente:
                return jsonify({
                    "data": [],
                    "message": "El campo id_docente es obligatorio",
                    "status": 0
                }), 400
            
            docente_existente = controlador_docente.obtener_docente_por_id(id_docente)
            if not docente_existente:
                return jsonify({
                    "data": [],
                    "message": "El docente no existe",
                    "status": 0
                }), 404
            
            correo = data.get("correo")
            password = data.get("password")
            nombres = data.get("nombres")
            apellidos = data.get("apellidos")
            
            resultado = controlador_docente.actualizar_docente(
                id_docente, correo, password, nombres, apellidos
            )
            
            if resultado:
                return jsonify({
                    "data": [],
                    "message": "Docente actualizado correctamente",
                    "status": 1
                }), 200
            else:
                return jsonify({
                    "data": [],
                    "message": "Error al actualizar el docente",
                    "status": 0
                }), 500

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_obtener_docente_id", methods=["GET"])
    def api_obtener_docente_id():
        """API para obtener un docente por su ID (sin autenticación JWT requerida)"""
        """API para obtener un docente por su ID"""
        try:
            data = request.json if request.is_json else {}
            id_docente = data.get("id_docente") or request.args.get("id_docente")
            
            if not id_docente:
                return jsonify({
                    "data": [],
                    "message": "El campo id_docente es obligatorio",
                    "status": 0
                }), 400
            
            try:
                id_docente = int(id_docente)
            except ValueError:
                return jsonify({
                    "data": [],
                    "message": "El id_docente debe ser un número",
                    "status": 0
                }), 400
            
            docente = controlador_docente.obtener_docente_por_id(id_docente)
            if not docente:
                return jsonify({
                    "data": [],
                    "message": "Docente no encontrado",
                    "status": 0
                }), 404
            
            if isinstance(docente, dict):
                docente_dict = {
                    "ID docente": docente.get('id_docente'),
                    "Correo": docente.get('correo'),
                    "Nombres": docente.get('nombres'),
                    "Apellidos": docente.get('apellidos')
                }
            else:
                docente_dict = {
                    "ID docente": docente[0],
                    "Correo": docente[1],
                    "Nombres": docente[3],
                    "Apellidos": docente[4]
                }
            
            return jsonify({
                "data": [docente_dict],
                "message": "Docente obtenido correctamente",
                "status": 1
            }), 200

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_obtener_docentes", methods=["GET"])
    def api_obtener_docentes():
        """API para obtener todos los docentes (sin autenticación JWT requerida)"""
        try:
            docentes = controlador_docente.obtener_docentes()
            data_list = []
            
            for docente in docentes:
                if isinstance(docente, dict):
                    docente_dict = {
                        "ID docente": docente.get('id_docente'),
                        "Correo": docente.get('correo'),
                        "Nombres": docente.get('nombres'),
                        "Apellidos": docente.get('apellidos')
                    }
                else:
                    docente_dict = {
                        "ID docente": docente[0],
                        "Correo": docente[1],
                        "Nombres": docente[3],
                        "Apellidos": docente[4]
                    }
                data_list.append(docente_dict)
            
            return jsonify({
                "data": data_list,
                "message": "Listado correcto de docentes",
                "status": 1
            }), 200

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_eliminar_docente", methods=["DELETE"])
    @jwt_required()
    def api_eliminar_docente():
        """API para eliminar un docente"""
        try:
            data = request.json if request.is_json else {}
            id_docente = data.get("id_docente")
            
            if not id_docente:
                return jsonify({
                    "data": [],
                    "message": "El campo id_docente es obligatorio",
                    "status": 0
                }), 400
            
            try:
                id_docente = int(id_docente)
            except ValueError:
                return jsonify({
                    "data": [],
                    "message": "El id_docente debe ser un número",
                    "status": 0
                }), 400
            
            docente_existente = controlador_docente.obtener_docente_por_id(id_docente)
            if not docente_existente:
                return jsonify({
                    "data": [],
                    "message": "El docente no existe",
                    "status": 0
                }), 404
            
            resultado = controlador_docente.eliminar_docente(id_docente)
            
            if resultado:
                return jsonify({
                    "data": [],
                    "message": "Docente eliminado correctamente",
                    "status": 1
                }), 200
            else:
                return jsonify({
                    "data": [],
                    "message": "Error al eliminar el docente",
                    "status": 0
                }), 500

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    # ============================================
    # APIs PARA TABLA JUGADOR
    # ============================================
    
    @app.route("/api_registrar_jugador", methods=["POST"])
    @jwt_required()
    def api_registrar_jugador():
        """API para registrar un nuevo jugador"""
        try:
            data = request.json
            email = data.get("email")
            password = data.get("password")
            
            if not email or not password:
                return jsonify({
                    "data": [],
                    "message": "Faltan campos obligatorios: email, password",
                    "status": 0
                }), 400
            
            jugador_existente = controlador_jugador.obtener_jugador_por_email(email)
            if jugador_existente:
                return jsonify({
                    "data": [],
                    "message": "El email ya está registrado",
                    "status": 0
                }), 400
            
            resultado = controlador_jugador.insertar_jugador(email, password)
            
            if resultado:
                return jsonify({
                    "data": [],
                    "message": "Jugador registrado correctamente",
                    "status": 1
                }), 201
            else:
                return jsonify({
                    "data": [],
                    "message": "Error al registrar el jugador",
                    "status": 0
                }), 500

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_actualizar_jugador", methods=["POST"])
    @jwt_required()
    def api_actualizar_jugador():
        """API para actualizar un jugador existente"""
        try:
            data = request.json
            id_jugador = data.get("id_jugador")
            
            if not id_jugador:
                return jsonify({
                    "data": [],
                    "message": "El campo id_jugador es obligatorio",
                    "status": 0
                }), 400
            
            jugador_existente = controlador_jugador.obtener_jugador_por_id(id_jugador)
            if not jugador_existente:
                return jsonify({
                    "data": [],
                    "message": "El jugador no existe",
                    "status": 0
                }), 404
            
            email = data.get("email")
            password = data.get("password")
            
            resultado = controlador_jugador.actualizar_jugador(id_jugador, email, password)
            
            if resultado:
                return jsonify({
                    "data": [],
                    "message": "Jugador actualizado correctamente",
                    "status": 1
                }), 200
            else:
                return jsonify({
                    "data": [],
                    "message": "Error al actualizar el jugador",
                    "status": 0
                }), 500

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_obtener_jugador_id", methods=["GET"])
    def api_obtener_jugador_id():
        """API para obtener un jugador por su ID (sin autenticación JWT requerida)"""
        try:
            data = request.json if request.is_json else {}
            id_jugador = data.get("id_jugador") or request.args.get("id_jugador")
            
            if not id_jugador:
                return jsonify({
                    "data": [],
                    "message": "El campo id_jugador es obligatorio",
                    "status": 0
                }), 400
            
            try:
                id_jugador = int(id_jugador)
            except ValueError:
                return jsonify({
                    "data": [],
                    "message": "El id_jugador debe ser un número",
                    "status": 0
                }), 400
            
            jugador = controlador_jugador.obtener_jugador_por_id(id_jugador)
            if not jugador:
                return jsonify({
                    "data": [],
                    "message": "Jugador no encontrado",
                    "status": 0
                }), 404
            
            if isinstance(jugador, dict):
                jugador_dict = {
                    "ID jugador": jugador.get('id_jugador'),
                    "Email": jugador.get('email')
                }
            else:
                jugador_dict = {
                    "ID jugador": jugador[0],
                    "Email": jugador[1]
                }
            
            return jsonify({
                "data": [jugador_dict],
                "message": "Jugador obtenido correctamente",
                "status": 1
            }), 200

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_obtener_jugadores", methods=["GET"])
    def api_obtener_jugadores():
        """API para obtener todos los jugadores (sin autenticación JWT requerida)"""
        try:
            jugadores = controlador_jugador.obtener_jugadores()
            data_list = []
            
            for jugador in jugadores:
                if isinstance(jugador, dict):
                    jugador_dict = {
                        "ID jugador": jugador.get('id_jugador'),
                        "Email": jugador.get('email')
                    }
                else:
                    jugador_dict = {
                        "ID jugador": jugador[0],
                        "Email": jugador[1]
                    }
                data_list.append(jugador_dict)
            
            return jsonify({
                "data": data_list,
                "message": "Listado correcto de jugadores",
                "status": 1
            }), 200

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_eliminar_jugador", methods=["DELETE"])
    @jwt_required()
    def api_eliminar_jugador():
        """API para eliminar un jugador"""
        try:
            data = request.json if request.is_json else {}
            id_jugador = data.get("id_jugador")
            
            if not id_jugador:
                return jsonify({
                    "data": [],
                    "message": "El campo id_jugador es obligatorio",
                    "status": 0
                }), 400
            
            try:
                id_jugador = int(id_jugador)
            except ValueError:
                return jsonify({
                    "data": [],
                    "message": "El id_jugador debe ser un número",
                    "status": 0
                }), 400
            
            jugador_existente = controlador_jugador.obtener_jugador_por_id(id_jugador)
            if not jugador_existente:
                return jsonify({
                    "data": [],
                    "message": "El jugador no existe",
                    "status": 0
                }), 404
            
            resultado = controlador_jugador.eliminar_jugador(id_jugador)
            
            if resultado:
                return jsonify({
                    "data": [],
                    "message": "Jugador eliminado correctamente",
                    "status": 1
                }), 200
            else:
                return jsonify({
                    "data": [],
                    "message": "Error al eliminar el jugador",
                    "status": 0
                }), 500

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    # ============================================
    # APIs PARA TABLA CUESTIONARIO
    # ============================================
    
    @app.route("/api_registrar_cuestionario", methods=["POST"])
    @jwt_required()
    def api_registrar_cuestionario():
        """API para registrar un nuevo cuestionario (solo cuestionario, sin preguntas ni alternativas)"""
        try:
            data = request.json
            nombre = data.get("nombre")
            id_docente = data.get("id_docente")
            estado = data.get("estado", "P")
            tipo_cuestionario = data.get("tipo_cuestionario", "I")
            descripcion = data.get("descripcion", "")
            
            if not nombre or not id_docente:
                return jsonify({
                    "data": [],
                    "message": "Faltan campos obligatorios: nombre, id_docente",
                    "status": 0
                }), 400
            
            # Validar nombre
            nombre = nombre.strip()
            if len(nombre) < 3:
                return jsonify({
                    "data": [],
                    "message": "El nombre del cuestionario debe tener al menos 3 caracteres",
                    "status": 0
                }), 400
            
            if len(nombre) > 200:
                return jsonify({
                    "data": [],
                    "message": "El nombre del cuestionario no puede exceder 200 caracteres",
                    "status": 0
                }), 400
            
            # Validar tipo_cuestionario
            if tipo_cuestionario not in ['I', 'G']:
                tipo_cuestionario = 'I'
            
            # Validar estado
            if estado not in ['P', 'R']:
                if estado == 'Público':
                    estado = 'P'
                elif estado == 'Privado':
                    estado = 'R'
                else:
                    estado = 'P'
            
            # Generar PIN aleatorio
            pin = str(random.randint(10000, 99999))
            
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            try:
                with connection.cursor() as cursor:
                    query = """
                        INSERT INTO Cuestionario (nombre, tipo_cuestionario, descripcion, pin, estado, id_docente)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(query, (
                        nombre,
                        tipo_cuestionario,
                        descripcion if descripcion else None,
                        pin,
                        estado,
                        id_docente
                    ))
                    
                    id_cuestionario = cursor.lastrowid
                    connection.commit()
                
                return jsonify({
                    "data": [{"id_cuestionario": id_cuestionario, "pin": pin}],
                    "message": "Cuestionario registrado correctamente",
                    "status": 1
                }), 201
                
            finally:
                connection.close()
                
        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_actualizar_cuestionario", methods=["POST"])
    @jwt_required()
    def api_actualizar_cuestionario():
        """API para actualizar un cuestionario existente"""
        try:
            data = request.json
            id_cuestionario = data.get("id_cuestionario")
            
            if not id_cuestionario:
                return jsonify({
                    "data": [],
                    "message": "El campo id_cuestionario es obligatorio",
                    "status": 0
                }), 400
            
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            try:
                with connection.cursor() as cursor:
                    # Verificar existencia del cuestionario
                    cursor.execute("""
                        SELECT nombre, estado, tipo_cuestionario, descripcion
                        FROM Cuestionario
                        WHERE id_cuestionario = %s
                    """, (id_cuestionario,))
                    cuestionario_db = cursor.fetchone()
                    
                    if not cuestionario_db:
                        return jsonify({
                            "data": [],
                            "message": "El cuestionario no existe",
                            "status": 0
                        }), 404
                    
                    # Tomar valores actuales si no se envían nuevos
                    nombre = data.get("nombre") or cuestionario_db.get("nombre") or cuestionario_db[0]
                    estado = data.get("estado") or cuestionario_db.get("estado") or cuestionario_db[1]
                    tipo_cuestionario = data.get("tipo_cuestionario") or cuestionario_db.get("tipo_cuestionario") or cuestionario_db[2]
                    descripcion = data.get("descripcion") if data.get("descripcion") is not None else (cuestionario_db.get("descripcion") if isinstance(cuestionario_db, dict) else cuestionario_db[3])
                    
                    # Validaciones
                    nombre = nombre.strip()
                    if len(nombre) < 3:
                        return jsonify({
                            "data": [],
                            "message": "El nombre del cuestionario debe tener al menos 3 caracteres",
                            "status": 0
                        }), 400
                    if len(nombre) > 200:
                        return jsonify({
                            "data": [],
                            "message": "El nombre del cuestionario no puede exceder 200 caracteres",
                            "status": 0
                        }), 400
                    
                    if estado not in ['P', 'R']:
                        if estado == 'Público':
                            estado = 'P'
                        elif estado == 'Privado':
                            estado = 'R'
                        else:
                            estado = 'P'
                    
                    if tipo_cuestionario not in ['I', 'G']:
                        tipo_cuestionario = 'I'
                    
                    cursor.execute("""
                        UPDATE Cuestionario
                        SET nombre = %s,
                            estado = %s,
                            tipo_cuestionario = %s,
                            descripcion = %s
                        WHERE id_cuestionario = %s
                    """, (
                        nombre,
                        estado,
                        tipo_cuestionario,
                        descripcion if descripcion else None,
                        id_cuestionario
                    ))
                    
                    connection.commit()
                
                return jsonify({
                    "data": [],
                    "message": "Cuestionario actualizado correctamente",
                    "status": 1
                }), 200
            
            finally:
                connection.close()
                
        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_obtener_cuestionario_id", methods=["GET"])
    def api_obtener_cuestionario_id():
        """API para obtener un cuestionario por su ID con sus preguntas (sin autenticación JWT requerida)"""
        try:
            data = request.json if request.is_json else {}
            id_cuestionario = data.get("id_cuestionario") or request.args.get("id_cuestionario")
            
            if not id_cuestionario:
                return jsonify({
                    "data": [],
                    "message": "El campo id_cuestionario es obligatorio",
                    "status": 0
                }), 400
            
            try:
                id_cuestionario = int(id_cuestionario)
            except ValueError:
                return jsonify({
                    "data": [],
                    "message": "El id_cuestionario debe ser un número",
                    "status": 0
                }), 400
            
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            try:
                with connection.cursor() as cursor:
                    # Obtener información básica del cuestionario
                    query_cuestionario = """
                        SELECT id_cuestionario, nombre, estado, tipo_cuestionario, descripcion, pin
                        FROM Cuestionario
                        WHERE id_cuestionario = %s
                    """
                    cursor.execute(query_cuestionario, (id_cuestionario,))
                    cuestionario_info = cursor.fetchone()
                    
                    if not cuestionario_info:
                        return jsonify({
                            "data": [],
                            "message": "Cuestionario no encontrado",
                            "status": 0
                        }), 404
                    
                    # Obtener preguntas del cuestionario
                    preguntas = controlador_cuestionario.datos_cuestionario(id_cuestionario)
                    
                    # Procesar preguntas
                    preguntas_procesadas = []
                    if preguntas:
                        for pregunta in preguntas:
                            pregunta_dict = {}
                            if isinstance(pregunta, dict):
                                pregunta_dict = {
                                    "id_pregunta": pregunta.get('id_pregunta'),
                                    "pregunta": pregunta.get('pregunta'),
                                    "puntaje": pregunta.get('puntaje'),
                                    "tiempo_respuesta": pregunta.get('tiempo_respuesta'),
                                    "alternativas": pregunta.get('alternativas')
                                }
                            else:
                                # Manejar tuplas
                                pregunta_dict = {
                                    "id_pregunta": pregunta[0] if len(pregunta) > 0 else None,
                                    "pregunta": pregunta[1] if len(pregunta) > 1 else None,
                                    "puntaje": pregunta[2] if len(pregunta) > 2 else None,
                                    "tiempo_respuesta": pregunta[3] if len(pregunta) > 3 else None,
                                    "alternativas": pregunta[4] if len(pregunta) > 4 else None
                                }
                            
                            # Procesar alternativas si es string JSON
                            if pregunta_dict.get('alternativas') and isinstance(pregunta_dict['alternativas'], str):
                                try:
                                    pregunta_dict['alternativas'] = json.loads(pregunta_dict['alternativas'])
                                except:
                                    pass
                            
                            preguntas_procesadas.append(pregunta_dict)
                    
                    # Construir respuesta
                    if isinstance(cuestionario_info, dict):
                        cuestionario_dict = {
                            "ID cuestionario": cuestionario_info.get('id_cuestionario'),
                            "Nombre": cuestionario_info.get('nombre'),
                            "Estado": cuestionario_info.get('estado'),
                            "Tipo": cuestionario_info.get('tipo_cuestionario'),
                            "Descripcion": cuestionario_info.get('descripcion'),
                            "PIN": cuestionario_info.get('pin'),
                            "Preguntas": preguntas_procesadas
                        }
                    else:
                        cuestionario_dict = {
                            "ID cuestionario": cuestionario_info[0] if len(cuestionario_info) > 0 else None,
                            "Nombre": cuestionario_info[1] if len(cuestionario_info) > 1 else None,
                            "Estado": cuestionario_info[2] if len(cuestionario_info) > 2 else None,
                            "Tipo": cuestionario_info[3] if len(cuestionario_info) > 3 else None,
                            "Descripcion": cuestionario_info[4] if len(cuestionario_info) > 4 else None,
                            "PIN": cuestionario_info[5] if len(cuestionario_info) > 5 else None,
                            "Preguntas": preguntas_procesadas
                        }
                
                return jsonify({
                    "data": [cuestionario_dict],
                    "message": "Cuestionario obtenido correctamente",
                    "status": 1
                }), 200
                
            finally:
                connection.close()
                
        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_obtener_cuestionarios", methods=["GET"])
    def api_obtener_cuestionarios():
        """API para obtener todos los cuestionarios (opcionalmente filtrados por id_docente) (sin autenticación JWT requerida)"""
        try:
            data = request.json if request.is_json else {}
            id_docente = data.get("id_docente") or request.args.get("id_docente")
            
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            try:
                with connection.cursor() as cursor:
                    # Si se proporciona id_docente, filtrar por docente
                    if id_docente:
                        try:
                            id_docente = int(id_docente)
                        except ValueError:
                            return jsonify({
                                "data": [],
                                "message": "El id_docente debe ser un número",
                                "status": 0
                            }), 400
                        
                        # Obtener cuestionarios activos y archivados del docente
                        query_activos = """
                            SELECT id_cuestionario, nombre, tipo_cuestionario, pin, estado, descripcion
                            FROM Cuestionario
                            WHERE estado = 'P' AND id_docente = %s
                        """
                        cursor.execute(query_activos, (id_docente,))
                        cuestionarios_activos = list(cursor.fetchall())
                        
                        query_archivados = """
                            SELECT id_cuestionario, nombre, tipo_cuestionario, pin, estado, descripcion
                            FROM Cuestionario
                            WHERE estado = 'R' AND id_docente = %s
                        """
                        cursor.execute(query_archivados, (id_docente,))
                        cuestionarios_archivados = list(cursor.fetchall())
                    else:
                        # Si no se proporciona id_docente, obtener todos los cuestionarios
                        query_todos = """
                            SELECT id_cuestionario, nombre, tipo_cuestionario, pin, estado, descripcion
                            FROM Cuestionario
                            ORDER BY id_cuestionario DESC
                        """
                        cursor.execute(query_todos)
                        cuestionarios_activos = list(cursor.fetchall())
                        cuestionarios_archivados = []
                    
                    # Combinar listas (ahora ambas son listas)
                    todos_cuestionarios = cuestionarios_activos + cuestionarios_archivados
                    
                    data_list = []
                    for cuestionario in todos_cuestionarios:
                        # Extraer id_cuestionario
                        if isinstance(cuestionario, dict):
                            id_cuestionario = cuestionario.get('id_cuestionario')
                            cuestionario_dict = {
                                "ID cuestionario": id_cuestionario,
                                "Nombre": cuestionario.get('nombre'),
                                "Estado": cuestionario.get('estado'),
                                "Tipo": cuestionario.get('tipo_cuestionario'),
                                "Descripcion": cuestionario.get('descripcion'),
                                "PIN": cuestionario.get('pin')
                            }
                        else:
                            # Manejar tuplas de la base de datos
                            id_cuestionario = cuestionario[0] if len(cuestionario) > 0 else None
                            cuestionario_dict = {
                                "ID cuestionario": id_cuestionario,
                                "Nombre": cuestionario[1] if len(cuestionario) > 1 else None,
                                "Tipo": cuestionario[2] if len(cuestionario) > 2 else None,
                                "PIN": cuestionario[3] if len(cuestionario) > 3 else None,
                                "Estado": cuestionario[4] if len(cuestionario) > 4 else None,
                                "Descripcion": cuestionario[5] if len(cuestionario) > 5 else None
                            }
                        
                        # Obtener preguntas y alternativas del cuestionario
                        preguntas_procesadas = []
                        if id_cuestionario:
                            try:
                                preguntas = controlador_cuestionario.datos_cuestionario(id_cuestionario)
                                if preguntas:
                                    for pregunta in preguntas:
                                        pregunta_dict = {}
                                        if isinstance(pregunta, dict):
                                            pregunta_dict = {
                                                "id_pregunta": pregunta.get('id_pregunta'),
                                                "pregunta": pregunta.get('pregunta'),
                                                "puntaje": pregunta.get('puntaje'),
                                                "tiempo_respuesta": pregunta.get('tiempo_respuesta'),
                                                "alternativas": pregunta.get('alternativas')
                                            }
                                        else:
                                            # Manejar tuplas
                                            pregunta_dict = {
                                                "id_pregunta": pregunta[0] if len(pregunta) > 0 else None,
                                                "pregunta": pregunta[1] if len(pregunta) > 1 else None,
                                                "puntaje": pregunta[2] if len(pregunta) > 2 else None,
                                                "tiempo_respuesta": pregunta[3] if len(pregunta) > 3 else None,
                                                "alternativas": pregunta[4] if len(pregunta) > 4 else None
                                            }
                                        
                                        # Procesar alternativas si es string JSON
                                        if pregunta_dict.get('alternativas') and isinstance(pregunta_dict['alternativas'], str):
                                            try:
                                                pregunta_dict['alternativas'] = json.loads(pregunta_dict['alternativas'])
                                            except:
                                                pass
                                        
                                        preguntas_procesadas.append(pregunta_dict)
                            except Exception as e:
                                # Si hay error al obtener preguntas, continuar sin ellas
                                print(f"Error al obtener preguntas del cuestionario {id_cuestionario}: {e}")
                                preguntas_procesadas = []
                        
                        # Agregar preguntas al cuestionario
                        cuestionario_dict["Preguntas"] = preguntas_procesadas
                        data_list.append(cuestionario_dict)
                
                return jsonify({
                    "data": data_list,
                    "message": "Listado correcto de cuestionarios",
                    "status": 1
                }), 200
                
            finally:
                connection.close()
                
        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_eliminar_cuestionario", methods=["DELETE"])
    @jwt_required()
    def api_eliminar_cuestionario():
        """API para eliminar un cuestionario"""
        try:
            data = request.json if request.is_json else {}
            id_cuestionario = data.get("id_cuestionario")
            
            if not id_cuestionario:
                return jsonify({
                    "data": [],
                    "message": "El campo id_cuestionario es obligatorio",
                    "status": 0
                }), 400
            
            try:
                id_cuestionario = int(id_cuestionario)
            except ValueError:
                return jsonify({
                    "data": [],
                    "message": "El id_cuestionario debe ser un número",
                    "status": 0
                }), 400
            
            cuestionario = controlador_cuestionario.datos_cuestionario(id_cuestionario)
            if not cuestionario:
                return jsonify({
                    "data": [],
                    "message": "El cuestionario no existe",
                    "status": 0
                }), 404
            
            resultado = controlador_cuestionario.eliminar_cuestionario_completo(id_cuestionario)
            
            if resultado and resultado.get('estado'):
                return jsonify({
                    "data": [],
                    "message": "Cuestionario eliminado correctamente",
                    "status": 1
                }), 200
            else:
                return jsonify({
                    "data": [],
                    "message": resultado.get('mensaje', "Error al eliminar el cuestionario") if resultado else "Error al eliminar el cuestionario",
                    "status": 0
                }), 500

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    # ============================================
    # APIs PARA TABLA GRUPO
    # ============================================
    
    @app.route("/api_registrar_grupo", methods=["POST"])
    @jwt_required()
    def api_registrar_grupo():
        """API para registrar un nuevo grupo"""
        try:
            data = request.json
            nombre_grupo = data.get("nombre_grupo")
            id_cuestionario = data.get("id_cuestionario")
            id_lider = data.get("id_lider")
            
            if not nombre_grupo or not id_cuestionario or not id_lider:
                return jsonify({
                    "data": [],
                    "message": "Faltan campos obligatorios: nombre_grupo, id_cuestionario, id_lider",
                    "status": 0
                }), 400
            
            resultado = controlador_grupo.crear_grupo(nombre_grupo, id_cuestionario, id_lider)
            
            if resultado and resultado.get('exito'):
                return jsonify({
                    "data": [{"id_grupo": resultado.get('id_grupo')}],
                    "message": "Grupo registrado correctamente",
                    "status": 1
                }), 201
            else:
                return jsonify({
                    "data": [],
                    "message": resultado.get('mensaje', "Error al registrar el grupo") if resultado else "Error al registrar el grupo",
                    "status": 0
                }), 500

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_actualizar_grupo", methods=["POST"])
    @jwt_required()
    def api_actualizar_grupo():
        """API para actualizar un grupo existente (cambiar método de evaluación)"""
        try:
            data = request.json
            id_grupo = data.get("id_grupo")
            metodo_evaluacion = data.get("metodo_evaluacion")
            id_jugador_cuestionario = data.get("id_jugador_cuestionario")
            
            if not id_grupo or not metodo_evaluacion or not id_jugador_cuestionario:
                return jsonify({
                    "data": [],
                    "message": "Faltan campos obligatorios: id_grupo, metodo_evaluacion, id_jugador_cuestionario",
                    "status": 0
                }), 400
            
            resultado = controlador_grupo.establecer_metodo_evaluacion(id_grupo, metodo_evaluacion, id_jugador_cuestionario)
            
            if resultado and resultado.get('exito'):
                return jsonify({
                    "data": [],
                    "message": "Grupo actualizado correctamente",
                    "status": 1
                }), 200
            else:
                return jsonify({
                    "data": [],
                    "message": resultado.get('mensaje', "Error al actualizar el grupo") if resultado else "Error al actualizar el grupo",
                    "status": 0
                }), 500

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_obtener_grupo_id", methods=["GET"])
    def api_obtener_grupo_id():
        """API para obtener un grupo por su ID (sin autenticación JWT requerida)"""
        try:
            data = request.json if request.is_json else {}
            id_grupo = data.get("id_grupo") or request.args.get("id_grupo")
            
            if not id_grupo:
                return jsonify({
                    "data": [],
                    "message": "El campo id_grupo es obligatorio",
                    "status": 0
                }), 400
            
            try:
                id_grupo = int(id_grupo)
            except ValueError:
                return jsonify({
                    "data": [],
                    "message": "El id_grupo debe ser un número",
                    "status": 0
                }), 400
            
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            with connection.cursor() as cursor:
                query = "SELECT id_grupo, nombre_grupo, id_cuestionario, id_lider, metodo_evaluacion FROM Grupo WHERE id_grupo = %s"
                cursor.execute(query, (id_grupo,))
                grupo = cursor.fetchone()
            
            connection.close()
            
            if not grupo:
                return jsonify({
                    "data": [],
                    "message": "Grupo no encontrado",
                    "status": 0
                }), 404
            
            if isinstance(grupo, dict):
                grupo_dict = {
                    "ID grupo": grupo.get('id_grupo'),
                    "Nombre grupo": grupo.get('nombre_grupo'),
                    "ID cuestionario": grupo.get('id_cuestionario'),
                    "ID lider": grupo.get('id_lider'),
                    "Metodo evaluacion": grupo.get('metodo_evaluacion')
                }
            else:
                grupo_dict = {
                    "ID grupo": grupo[0],
                    "Nombre grupo": grupo[1],
                    "ID cuestionario": grupo[2],
                    "ID lider": grupo[3],
                    "Metodo evaluacion": grupo[4] if len(grupo) > 4 else None
                }
            
            return jsonify({
                "data": [grupo_dict],
                "message": "Grupo obtenido correctamente",
                "status": 1
            }), 200

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_obtener_grupos", methods=["GET"])
    def api_obtener_grupos():
        """API para obtener todos los grupos de un cuestionario (sin autenticación JWT requerida)"""
        try:
            data = request.json if request.is_json else {}
            id_cuestionario = data.get("id_cuestionario") or request.args.get("id_cuestionario")
            
            id_cuestionario_int = None
            if id_cuestionario:
                try:
                    id_cuestionario_int = int(id_cuestionario)
                except ValueError:
                    return jsonify({
                        "data": [],
                        "message": "El id_cuestionario debe ser un número",
                        "status": 0
                    }), 400
            
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            try:
                with connection.cursor() as cursor:
                    if id_cuestionario_int:
                        query = """
                            SELECT id_grupo, nombre_grupo, id_cuestionario, id_lider, metodo_evaluacion
                            FROM Grupo
                            WHERE id_cuestionario = %s
                            ORDER BY id_grupo
                        """
                        cursor.execute(query, (id_cuestionario_int,))
                    else:
                        query = """
                            SELECT id_grupo, nombre_grupo, id_cuestionario, id_lider, metodo_evaluacion
                            FROM Grupo
                            ORDER BY id_cuestionario, id_grupo
                        """
                        cursor.execute(query)
                    grupos = cursor.fetchall()
            finally:
                connection.close()
            
            data_list = []
            
            for grupo in grupos:
                if isinstance(grupo, dict):
                    grupo_dict = {
                        "ID grupo": grupo.get('id_grupo'),
                        "Nombre grupo": grupo.get('nombre_grupo'),
                        "ID cuestionario": grupo.get('id_cuestionario'),
                        "ID lider": grupo.get('id_lider'),
                        "Metodo evaluacion": grupo.get('metodo_evaluacion')
                    }
                else:
                    grupo_dict = {
                        "ID grupo": grupo[0] if len(grupo) > 0 else None,
                        "Nombre grupo": grupo[1] if len(grupo) > 1 else None,
                        "ID cuestionario": grupo[2] if len(grupo) > 2 else None,
                        "ID lider": grupo[3] if len(grupo) > 3 else None,
                        "Metodo evaluacion": grupo[4] if len(grupo) > 4 else None
                    }
                data_list.append(grupo_dict)
            
            return jsonify({
                "data": data_list,
                "message": "Listado correcto de grupos",
                "status": 1
            }), 200

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_eliminar_grupo", methods=["DELETE"])
    @jwt_required()
    def api_eliminar_grupo():
        """API para eliminar (disolver) un grupo"""
        try:
            data = request.json if request.is_json else {}
            id_grupo = data.get("id_grupo")
            id_jugador_cuestionario = data.get("id_jugador_cuestionario")
            
            if not id_grupo or not id_jugador_cuestionario:
                return jsonify({
                    "data": [],
                    "message": "Faltan campos obligatorios: id_grupo, id_jugador_cuestionario",
                    "status": 0
                }), 400
            
            try:
                id_grupo = int(id_grupo)
                id_jugador_cuestionario = int(id_jugador_cuestionario)
            except ValueError:
                return jsonify({
                    "data": [],
                    "message": "Los IDs deben ser números",
                    "status": 0
                }), 400
            
            resultado = controlador_grupo.disolver_grupo(id_grupo, id_jugador_cuestionario)
            
            if resultado and resultado.get('exito'):
                return jsonify({
                    "data": [],
                    "message": "Grupo eliminado correctamente",
                    "status": 1
                }), 200
            else:
                return jsonify({
                    "data": [],
                    "message": resultado.get('mensaje', "Error al eliminar el grupo") if resultado else "Error al eliminar el grupo",
                    "status": 0
                }), 500

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    # ============================================
    # APIs PARA TABLA RECOMPENSA
    # ============================================
    
    @app.route("/api_registrar_recompensa", methods=["POST"])
    @jwt_required()
    def api_registrar_recompensa():
        """API para registrar una nueva recompensa"""
        try:
            data = request.json
            id_cuestionario = data.get("id_cuestionario")
            id_jugador_cuestionario = data.get("id_jugador_cuestionario")
            id_jugador = data.get("id_jugador")
            puntos = data.get("puntos")
            tipo_recompensa = data.get("tipo_recompensa", "puntos")
            
            if not id_cuestionario or not id_jugador_cuestionario or not id_jugador or puntos is None:
                return jsonify({
                    "data": [],
                    "message": "Faltan campos obligatorios: id_cuestionario, id_jugador_cuestionario, id_jugador, puntos",
                    "status": 0
                }), 400
            
            resultado = controlador_recompensa.registrar_recompensa(
                id_cuestionario, id_jugador_cuestionario, id_jugador, puntos, tipo_recompensa
            )
            
            if resultado:
                return jsonify({
                    "data": [],
                    "message": "Recompensa registrada correctamente",
                    "status": 1
                }), 201
            else:
                return jsonify({
                    "data": [],
                    "message": "Error al registrar la recompensa",
                    "status": 0
                }), 500

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_actualizar_recompensa", methods=["POST"])
    @jwt_required()
    def api_actualizar_recompensa():
        """API para actualizar una recompensa existente"""
        try:
            data = request.json
            id_recompensa = data.get("id_recompensa")
            puntos = data.get("puntos")
            tipo_recompensa = data.get("tipo_recompensa")
            
            if not id_recompensa:
                return jsonify({
                    "data": [],
                    "message": "El campo id_recompensa es obligatorio",
                    "status": 0
                }), 400
            
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            try:
                # Verificar que existe
                with connection.cursor() as cursor:
                    query = "SELECT id_recompensa FROM Recompensa WHERE id_recompensa = %s"
                    cursor.execute(query, (id_recompensa,))
                    recompensa = cursor.fetchone()
                
                if not recompensa:
                    return jsonify({
                        "data": [],
                        "message": "La recompensa no existe",
                        "status": 0
                    }), 404
                
                # Actualizar
                update_fields = []
                params = []
                
                if puntos is not None:
                    update_fields.append("puntos = %s")
                    params.append(puntos)
                
                if tipo_recompensa is not None:
                    update_fields.append("tipo_recompensa = %s")
                    params.append(tipo_recompensa)
                
                if not update_fields:
                    return jsonify({
                        "data": [],
                        "message": "No hay campos para actualizar",
                        "status": 0
                    }), 400
                
                with connection.cursor() as cursor:
                    query = "UPDATE Recompensa SET " + ", ".join(update_fields) + " WHERE id_recompensa = %s"
                    params.append(id_recompensa)
                    cursor.execute(query, tuple(params))
                    connection.commit()
                
                return jsonify({
                    "data": [],
                    "message": "Recompensa actualizada correctamente",
                    "status": 1
                }), 200
            finally:
                connection.close()

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_obtener_recompensa_id", methods=["GET"])
    def api_obtener_recompensa_id():
        """API para obtener una recompensa por su ID (sin autenticación JWT requerida)"""
        try:
            data = request.json if request.is_json else {}
            id_recompensa = data.get("id_recompensa") or request.args.get("id_recompensa")
            
            if not id_recompensa:
                return jsonify({
                    "data": [],
                    "message": "El campo id_recompensa es obligatorio",
                    "status": 0
                }), 400
            
            try:
                id_recompensa = int(id_recompensa)
            except ValueError:
                return jsonify({
                    "data": [],
                    "message": "El id_recompensa debe ser un número",
                    "status": 0
                }), 400
            
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            with connection.cursor() as cursor:
                query = "SELECT id_recompensa, id_cuestionario, id_jugador_cuestionario, id_jugador, puntos, tipo_recompensa, fecha_recompensa FROM Recompensa WHERE id_recompensa = %s"
                cursor.execute(query, (id_recompensa,))
                recompensa = cursor.fetchone()
            
            connection.close()
            
            if not recompensa:
                return jsonify({
                    "data": [],
                    "message": "Recompensa no encontrada",
                    "status": 0
                }), 404
            
            if isinstance(recompensa, dict):
                recompensa_dict = {
                    "ID recompensa": recompensa.get('id_recompensa'),
                    "ID cuestionario": recompensa.get('id_cuestionario'),
                    "ID jugador cuestionario": recompensa.get('id_jugador_cuestionario'),
                    "ID jugador": recompensa.get('id_jugador'),
                    "Puntos": recompensa.get('puntos'),
                    "Tipo recompensa": recompensa.get('tipo_recompensa'),
                    "Fecha recompensa": str(recompensa.get('fecha_recompensa')) if recompensa.get('fecha_recompensa') else None
                }
            else:
                recompensa_dict = {
                    "ID recompensa": recompensa[0],
                    "ID cuestionario": recompensa[1],
                    "ID jugador cuestionario": recompensa[2],
                    "ID jugador": recompensa[3],
                    "Puntos": recompensa[4],
                    "Tipo recompensa": recompensa[5],
                    "Fecha recompensa": str(recompensa[6]) if len(recompensa) > 6 and recompensa[6] else None
                }
            
            return jsonify({
                "data": [recompensa_dict],
                "message": "Recompensa obtenida correctamente",
                "status": 1
            }), 200

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_obtener_recompensas", methods=["GET"])
    def api_obtener_recompensas():
        """API para obtener todas las recompensas de un cuestionario (sin autenticación JWT requerida)"""
        try:
            data = request.json if request.is_json else {}
            id_cuestionario = data.get("id_cuestionario") or request.args.get("id_cuestionario")
            
            id_cuestionario_int = None
            if id_cuestionario:
                try:
                    id_cuestionario_int = int(id_cuestionario)
                except ValueError:
                    return jsonify({
                        "data": [],
                        "message": "El id_cuestionario debe ser un número",
                        "status": 0
                    }), 400
            
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            try:
                with connection.cursor() as cursor:
                    if id_cuestionario_int:
                        query = """
                            SELECT id_recompensa, id_cuestionario, id_jugador_cuestionario, id_jugador,
                                   puntos, tipo_recompensa, fecha_recompensa
                            FROM Recompensa
                            WHERE id_cuestionario = %s
                            ORDER BY id_recompensa
                        """
                        cursor.execute(query, (id_cuestionario_int,))
                    else:
                        query = """
                            SELECT id_recompensa, id_cuestionario, id_jugador_cuestionario, id_jugador,
                                   puntos, tipo_recompensa, fecha_recompensa
                            FROM Recompensa
                            ORDER BY id_cuestionario, id_recompensa
                        """
                        cursor.execute(query)
                    recompensas = cursor.fetchall()
            finally:
                connection.close()
            
            data_list = []
            
            for recompensa in recompensas:
                if isinstance(recompensa, dict):
                    recompensa_dict = {
                        "ID recompensa": recompensa.get('id_recompensa'),
                        "ID cuestionario": recompensa.get('id_cuestionario'),
                        "ID jugador cuestionario": recompensa.get('id_jugador_cuestionario'),
                        "ID jugador": recompensa.get('id_jugador'),
                        "Puntos": recompensa.get('puntos'),
                        "Tipo recompensa": recompensa.get('tipo_recompensa'),
                        "Fecha recompensa": str(recompensa.get('fecha_recompensa')) if recompensa.get('fecha_recompensa') else None
                    }
                else:
                    recompensa_dict = {
                        "ID recompensa": recompensa[0] if len(recompensa) > 0 else None,
                        "ID cuestionario": recompensa[1] if len(recompensa) > 1 else None,
                        "ID jugador cuestionario": recompensa[2] if len(recompensa) > 2 else None,
                        "ID jugador": recompensa[3] if len(recompensa) > 3 else None,
                        "Puntos": recompensa[4] if len(recompensa) > 4 else None,
                        "Tipo recompensa": recompensa[5] if len(recompensa) > 5 else None,
                        "Fecha recompensa": str(recompensa[6]) if len(recompensa) > 6 and recompensa[6] else None
                    }
                data_list.append(recompensa_dict)
            
            return jsonify({
                "data": data_list,
                "message": "Listado correcto de recompensas",
                "status": 1
            }), 200

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_eliminar_recompensa", methods=["DELETE"])
    @jwt_required()
    def api_eliminar_recompensa():
        """API para eliminar una recompensa"""
        try:
            data = request.json if request.is_json else {}
            id_recompensa = data.get("id_recompensa")
            
            if not id_recompensa:
                return jsonify({
                    "data": [],
                    "message": "El campo id_recompensa es obligatorio",
                    "status": 0
                }), 400
            
            try:
                id_recompensa = int(id_recompensa)
            except ValueError:
                return jsonify({
                    "data": [],
                    "message": "El id_recompensa debe ser un número",
                    "status": 0
                }), 400
            
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            # Verificar que existe
            with connection.cursor() as cursor:
                query = "SELECT id_recompensa FROM Recompensa WHERE id_recompensa = %s"
                cursor.execute(query, (id_recompensa,))
                recompensa = cursor.fetchone()
            
            try:
                if not recompensa:
                    return jsonify({
                        "data": [],
                        "message": "La recompensa no existe",
                        "status": 0
                    }), 404
                
                # Eliminar
                with connection.cursor() as cursor:
                    query = "DELETE FROM Recompensa WHERE id_recompensa = %s"
                    cursor.execute(query, (id_recompensa,))
                    connection.commit()
                
                return jsonify({
                    "data": [],
                    "message": "Recompensa eliminada correctamente",
                    "status": 1
                }), 200
            finally:
                connection.close()

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    # ============================================
    # APIs PARA TABLA PREGUNTA
    # ============================================
    
    @app.route("/api_registrar_pregunta", methods=["POST"])
    @jwt_required()
    def api_registrar_pregunta():
        """API para registrar una nueva pregunta (solo pregunta, sin alternativas)"""
        try:
            data = request.json
            id_cuestionario = data.get("id_cuestionario")
            nombre_pregunta = data.get("nombre_pregunta")
            puntos = data.get("puntos")
            tiempo = data.get("tiempo")
            tipo_pregunta = data.get("tipo_pregunta")
            
            if not id_cuestionario or not nombre_pregunta or not puntos or not tiempo or not tipo_pregunta:
                return jsonify({
                    "data": [],
                    "message": "Faltan campos obligatorios: id_cuestionario, nombre_pregunta, puntos, tiempo, tipo_pregunta",
                    "status": 0
                }), 400
            
            # Validar nombre_pregunta
            nombre_pregunta = nombre_pregunta.strip()
            if len(nombre_pregunta) < 5:
                return jsonify({
                    "data": [],
                    "message": "La pregunta debe tener al menos 5 caracteres",
                    "status": 0
                }), 400
            
            if len(nombre_pregunta) > 500:
                return jsonify({
                    "data": [],
                    "message": "La pregunta no puede exceder 500 caracteres",
                    "status": 0
                }), 400
            
            # Validar tipo_pregunta
            if tipo_pregunta not in ['VF', 'ALT']:
                return jsonify({
                    "data": [],
                    "message": "El tipo_pregunta debe ser 'VF' (Verdadero/Falso) o 'ALT' (Alternativas)",
                    "status": 0
                }), 400
            
            # Validar puntos
            try:
                puntos = int(puntos)
                if puntos <= 0 or puntos > 1000:
                    return jsonify({
                        "data": [],
                        "message": "Los puntos deben estar entre 1 y 1000",
                        "status": 0
                    }), 400
            except (ValueError, TypeError):
                return jsonify({
                    "data": [],
                    "message": "Los puntos deben ser un número válido",
                    "status": 0
                }), 400
            
            # Validar tiempo
            try:
                tiempo = int(tiempo)
                if tiempo < 2 or tiempo > 300:
                    return jsonify({
                        "data": [],
                        "message": "El tiempo debe estar entre 2 y 300 segundos",
                        "status": 0
                    }), 400
            except (ValueError, TypeError):
                return jsonify({
                    "data": [],
                    "message": "El tiempo debe ser un número válido",
                    "status": 0
                }), 400
            
            # Validar que el cuestionario existe
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            try:
                with connection.cursor() as cursor:
                    # Verificar que el cuestionario existe
                    query_check = "SELECT id_cuestionario FROM Cuestionario WHERE id_cuestionario = %s"
                    cursor.execute(query_check, (id_cuestionario,))
                    cuestionario = cursor.fetchone()
                    
                    if not cuestionario:
                        return jsonify({
                            "data": [],
                            "message": "El cuestionario no existe",
                            "status": 0
                        }), 404
                    
                    # Insertar la pregunta
                    query = """
                        INSERT INTO Pregunta (pregunta, puntaje, tiempo_respuesta, tipo_pregunta, id_cuestionario)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(query, (
                        nombre_pregunta,
                        puntos,
                        tiempo,
                        tipo_pregunta,
                        id_cuestionario
                    ))
                    
                    id_pregunta = cursor.lastrowid
                    connection.commit()
                
                return jsonify({
                    "data": [{"id_pregunta": id_pregunta}],
                    "message": "Pregunta registrada correctamente",
                    "status": 1
                }), 201
                
            finally:
                connection.close()
                
        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_actualizar_pregunta", methods=["POST"])
    @jwt_required()
    def api_actualizar_pregunta():
        """API para actualizar una pregunta existente (solo pregunta, sin alternativas)"""
        try:
            data = request.json
            id_pregunta = data.get("id_pregunta")
            
            if not id_pregunta:
                return jsonify({
                    "data": [],
                    "message": "El campo id_pregunta es obligatorio",
                    "status": 0
                }), 400
            
            try:
                id_pregunta = int(id_pregunta)
            except ValueError:
                return jsonify({
                    "data": [],
                    "message": "El id_pregunta debe ser un número",
                    "status": 0
                }), 400
            
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            try:
                with connection.cursor() as cursor:
                    # Verificar que la pregunta existe
                    query_check = "SELECT id_pregunta FROM Pregunta WHERE id_pregunta = %s"
                    cursor.execute(query_check, (id_pregunta,))
                    pregunta = cursor.fetchone()
                    
                    if not pregunta:
                        return jsonify({
                            "data": [],
                            "message": "La pregunta no existe",
                            "status": 0
                        }), 404
                    
                    # Construir query de actualización solo con los campos proporcionados
                    campos_actualizar = []
                    valores = []
                    
                    if "nombre_pregunta" in data:
                        nombre_pregunta = data.get("nombre_pregunta", "").strip()
                        if len(nombre_pregunta) < 5:
                            return jsonify({
                                "data": [],
                                "message": "La pregunta debe tener al menos 5 caracteres",
                                "status": 0
                            }), 400
                        if len(nombre_pregunta) > 500:
                            return jsonify({
                                "data": [],
                                "message": "La pregunta no puede exceder 500 caracteres",
                                "status": 0
                            }), 400
                        campos_actualizar.append("pregunta = %s")
                        valores.append(nombre_pregunta)
                    
                    if "puntos" in data:
                        try:
                            puntos = int(data.get("puntos"))
                            if puntos <= 0 or puntos > 1000:
                                return jsonify({
                                    "data": [],
                                    "message": "Los puntos deben estar entre 1 y 1000",
                                    "status": 0
                                }), 400
                            campos_actualizar.append("puntaje = %s")
                            valores.append(puntos)
                        except (ValueError, TypeError):
                            return jsonify({
                                "data": [],
                                "message": "Los puntos deben ser un número válido",
                                "status": 0
                            }), 400
                    
                    if "tiempo" in data:
                        try:
                            tiempo = int(data.get("tiempo"))
                            if tiempo < 2 or tiempo > 300:
                                return jsonify({
                                    "data": [],
                                    "message": "El tiempo debe estar entre 2 y 300 segundos",
                                    "status": 0
                                }), 400
                            campos_actualizar.append("tiempo_respuesta = %s")
                            valores.append(tiempo)
                        except (ValueError, TypeError):
                            return jsonify({
                                "data": [],
                                "message": "El tiempo debe ser un número válido",
                                "status": 0
                            }), 400
                    
                    if "tipo_pregunta" in data:
                        tipo_pregunta = data.get("tipo_pregunta")
                        if tipo_pregunta not in ['VF', 'ALT']:
                            return jsonify({
                                "data": [],
                                "message": "El tipo_pregunta debe ser 'VF' (Verdadero/Falso) o 'ALT' (Alternativas)",
                                "status": 0
                            }), 400
                        campos_actualizar.append("tipo_pregunta = %s")
                        valores.append(tipo_pregunta)
                    
                    # Si no hay campos para actualizar
                    if not campos_actualizar:
                        return jsonify({
                            "data": [],
                            "message": "No se proporcionaron campos para actualizar",
                            "status": 0
                        }), 400
                    
                    # Agregar id_pregunta al final para el WHERE
                    valores.append(id_pregunta)
                    
                    # Ejecutar UPDATE
                    query = f"UPDATE Pregunta SET {', '.join(campos_actualizar)} WHERE id_pregunta = %s"
                    cursor.execute(query, valores)
                    connection.commit()
                    
                    filas_afectadas = cursor.rowcount
                    
                    if filas_afectadas == 0:
                        return jsonify({
                            "data": [],
                            "message": "No se pudo actualizar la pregunta",
                            "status": 0
                        }), 500
                
                return jsonify({
                    "data": [],
                    "message": "Pregunta actualizada correctamente",
                    "status": 1
                }), 200
                
            finally:
                connection.close()
                
        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_obtener_pregunta_id", methods=["GET"])
    def api_obtener_pregunta_id():
        """API para obtener una pregunta por su ID (sin autenticación JWT requerida)"""
        try:
            data = request.json if request.is_json else {}
            id_pregunta = data.get("id_pregunta") or request.args.get("id_pregunta")
            
            if not id_pregunta:
                return jsonify({
                    "data": [],
                    "message": "El campo id_pregunta es obligatorio",
                    "status": 0
                }), 400
            
            try:
                id_pregunta = int(id_pregunta)
            except ValueError:
                return jsonify({
                    "data": [],
                    "message": "El id_pregunta debe ser un número",
                    "status": 0
                }), 400
            
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            with connection.cursor() as cursor:
                query = """
                    SELECT p.id_pregunta, p.pregunta, p.puntaje, p.tiempo_respuesta, 
                           p.tipo_pregunta, p.id_cuestionario
                    FROM Pregunta p
                    WHERE p.id_pregunta = %s
                """
                cursor.execute(query, (id_pregunta,))
                pregunta = cursor.fetchone()
            
            if not pregunta:
                connection.close()
                return jsonify({
                    "data": [],
                    "message": "Pregunta no encontrada",
                    "status": 0
                }), 404
            
            # Obtener alternativas
            with connection.cursor() as cursor:
                query_alt = """
                    SELECT id_alternativa, respuesta, estado_alternativa
                    FROM Alternativa
                    WHERE id_pregunta = %s
                """
                cursor.execute(query_alt, (id_pregunta,))
                alternativas = cursor.fetchall()
            
            connection.close()
            
            if isinstance(pregunta, dict):
                pregunta_dict = {
                    "ID pregunta": pregunta.get('id_pregunta'),
                    "Pregunta": pregunta.get('pregunta'),
                    "Puntaje": pregunta.get('puntaje'),
                    "Tiempo respuesta": pregunta.get('tiempo_respuesta'),
                    "Tipo pregunta": pregunta.get('tipo_pregunta'),
                    "ID cuestionario": pregunta.get('id_cuestionario'),
                    "Alternativas": []
                }
            else:
                pregunta_dict = {
                    "ID pregunta": pregunta[0],
                    "Pregunta": pregunta[1],
                    "Puntaje": pregunta[2],
                    "Tiempo respuesta": pregunta[3],
                    "Tipo pregunta": pregunta[4] if len(pregunta) > 4 else None,
                    "ID cuestionario": pregunta[5] if len(pregunta) > 5 else None,
                    "Alternativas": []
                }
            
            # Agregar alternativas
            for alt in alternativas:
                if isinstance(alt, dict):
                    alt_dict = {
                        "ID alternativa": alt.get('id_alternativa'),
                        "Respuesta": alt.get('respuesta'),
                        "Estado alternativa": alt.get('estado_alternativa')
                    }
                else:
                    alt_dict = {
                        "ID alternativa": alt[0],
                        "Respuesta": alt[1],
                        "Estado alternativa": alt[2] if len(alt) > 2 else None
                    }
                pregunta_dict["Alternativas"].append(alt_dict)
            
            return jsonify({
                "data": [pregunta_dict],
                "message": "Pregunta obtenida correctamente",
                "status": 1
            }), 200

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_obtener_preguntas", methods=["GET"])
    def api_obtener_preguntas():
        """API para obtener todas las preguntas de un cuestionario (sin autenticación JWT requerida)"""
        try:
            data = request.json if request.is_json else {}
            id_cuestionario = data.get("id_cuestionario") or request.args.get("id_cuestionario")
            
            id_cuestionario_int = None
            if id_cuestionario:
                try:
                    id_cuestionario_int = int(id_cuestionario)
                except ValueError:
                    return jsonify({
                        "data": [],
                        "message": "El id_cuestionario debe ser un número",
                        "status": 0
                    }), 400
            
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            with connection.cursor() as cursor:
                if id_cuestionario_int:
                    query = """
                        SELECT p.id_pregunta, p.pregunta, p.puntaje, p.tiempo_respuesta, 
                               p.tipo_pregunta, p.id_cuestionario
                        FROM Pregunta p
                        WHERE p.id_cuestionario = %s
                        ORDER BY p.id_pregunta
                    """
                    cursor.execute(query, (id_cuestionario_int,))
                else:
                    query = """
                        SELECT p.id_pregunta, p.pregunta, p.puntaje, p.tiempo_respuesta, 
                               p.tipo_pregunta, p.id_cuestionario
                        FROM Pregunta p
                        ORDER BY p.id_cuestionario, p.id_pregunta
                    """
                    cursor.execute(query)
                preguntas = cursor.fetchall()
            
            data_list = []
            
            for pregunta in preguntas:
                if isinstance(pregunta, dict):
                    pregunta_dict = {
                        "ID pregunta": pregunta.get('id_pregunta'),
                        "Pregunta": pregunta.get('pregunta'),
                        "Puntaje": pregunta.get('puntaje'),
                        "Tiempo respuesta": pregunta.get('tiempo_respuesta'),
                        "Tipo pregunta": pregunta.get('tipo_pregunta'),
                        "ID cuestionario": pregunta.get('id_cuestionario')
                    }
                    id_pregunta = pregunta.get('id_pregunta')
                else:
                    pregunta_dict = {
                        "ID pregunta": pregunta[0],
                        "Pregunta": pregunta[1],
                        "Puntaje": pregunta[2],
                        "Tiempo respuesta": pregunta[3],
                        "Tipo pregunta": pregunta[4] if len(pregunta) > 4 else None,
                        "ID cuestionario": pregunta[5] if len(pregunta) > 5 else None
                    }
                    id_pregunta = pregunta[0]
                
                # Obtener alternativas para esta pregunta
                with connection.cursor() as cursor_alt:
                    query_alt = """
                        SELECT id_alternativa, respuesta, estado_alternativa
                        FROM Alternativa
                        WHERE id_pregunta = %s
                    """
                    cursor_alt.execute(query_alt, (id_pregunta,))
                    alternativas = cursor_alt.fetchall()
                    
                    pregunta_dict["Alternativas"] = []
                    for alt in alternativas:
                        if isinstance(alt, dict):
                            alt_dict = {
                                "ID alternativa": alt.get('id_alternativa'),
                                "Respuesta": alt.get('respuesta'),
                                "Estado alternativa": alt.get('estado_alternativa')
                            }
                        else:
                            alt_dict = {
                                "ID alternativa": alt[0],
                                "Respuesta": alt[1],
                                "Estado alternativa": alt[2] if len(alt) > 2 else None
                            }
                        pregunta_dict["Alternativas"].append(alt_dict)
                
                data_list.append(pregunta_dict)
            
            connection.close()
            
            return jsonify({
                "data": data_list,
                "message": "Listado correcto de preguntas",
                "status": 1
            }), 200

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_eliminar_pregunta", methods=["DELETE"])
    @jwt_required()
    def api_eliminar_pregunta():
        """API para eliminar una pregunta"""
        try:
            data = request.json if request.is_json else {}
            id_pregunta = data.get("id_pregunta")
            
            if not id_pregunta:
                return jsonify({
                    "data": [],
                    "message": "El campo id_pregunta es obligatorio",
                    "status": 0
                }), 400
            
            try:
                id_pregunta = int(id_pregunta)
            except ValueError:
                return jsonify({
                    "data": [],
                    "message": "El id_pregunta debe ser un número",
                    "status": 0
                }), 400
            
            resultado = controlador_cuestionario.eliminar_pregunta(id_pregunta)
            
            if resultado and resultado.get('estado'):
                return jsonify({
                    "data": [],
                    "message": "Pregunta eliminada correctamente",
                    "status": 1
                }), 200
            else:
                return jsonify({
                    "data": [],
                    "message": resultado.get('mensaje', "Error al eliminar la pregunta") if resultado else "Error al eliminar la pregunta",
                    "status": 0
                }), 500

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    # ============================================
    # APIs PARA TABLA ALTERNATIVA
    # ============================================
    
    @app.route("/api_registrar_alternativa", methods=["POST"])
    @jwt_required()
    def api_registrar_alternativa():
        """API para registrar una nueva alternativa"""
        try:
            data = request.json
            id_pregunta = data.get("id_pregunta")
            respuesta = data.get("respuesta")
            estado_alternativa = data.get("estado_alternativa", 0)
            
            if not id_pregunta or not respuesta:
                return jsonify({
                    "data": [],
                    "message": "Faltan campos obligatorios: id_pregunta, respuesta",
                    "status": 0
                }), 400
            
            # Verificar que la pregunta existe
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            with connection.cursor() as cursor:
                query = "SELECT id_pregunta FROM Pregunta WHERE id_pregunta = %s"
                cursor.execute(query, (id_pregunta,))
                pregunta = cursor.fetchone()
            
            try:
                if not pregunta:
                    return jsonify({
                        "data": [],
                        "message": "La pregunta no existe",
                        "status": 0
                    }), 404
                
                # Insertar alternativa
                with connection.cursor() as cursor:
                    query = "INSERT INTO Alternativa (respuesta, estado_alternativa, id_pregunta) VALUES (%s, %s, %s)"
                    cursor.execute(query, (respuesta, estado_alternativa, id_pregunta))
                    id_alternativa = cursor.lastrowid
                    connection.commit()
                
                return jsonify({
                    "data": [{"id_alternativa": id_alternativa}],
                    "message": "Alternativa registrada correctamente",
                    "status": 1
                }), 201
            finally:
                connection.close()
                
        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_actualizar_alternativa", methods=["POST"])
    @jwt_required()
    def api_actualizar_alternativa():
        """API para actualizar una alternativa existente"""
        try:
            data = request.json
            id_alternativa = data.get("id_alternativa")
            respuesta = data.get("respuesta")
            estado_alternativa = data.get("estado_alternativa")
            
            if not id_alternativa:
                return jsonify({
                    "data": [],
                    "message": "El campo id_alternativa es obligatorio",
                    "status": 0
                }), 400
            
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            # Verificar que existe
            with connection.cursor() as cursor:
                query = "SELECT id_alternativa FROM Alternativa WHERE id_alternativa = %s"
                cursor.execute(query, (id_alternativa,))
                alternativa = cursor.fetchone()
            
            if not alternativa:
                connection.close()
                return jsonify({
                    "data": [],
                    "message": "La alternativa no existe",
                    "status": 0
                }), 404
            
            # Actualizar
            update_fields = []
            params = []
            
            if respuesta is not None:
                update_fields.append("respuesta = %s")
                params.append(respuesta)
            
            if estado_alternativa is not None:
                update_fields.append("estado_alternativa = %s")
                params.append(estado_alternativa)
            
            if not update_fields:
                connection.close()
                return jsonify({
                    "data": [],
                    "message": "No hay campos para actualizar",
                    "status": 0
                }), 400
            
            with connection.cursor() as cursor:
                query = "UPDATE Alternativa SET " + ", ".join(update_fields) + " WHERE id_alternativa = %s"
                params.append(id_alternativa)
                cursor.execute(query, tuple(params))
                connection.commit()
            
            connection.close()
            
            return jsonify({
                "data": [],
                "message": "Alternativa actualizada correctamente",
                "status": 1
            }), 200

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_obtener_alternativa_id", methods=["GET"])
    def api_obtener_alternativa_id():
        """API para obtener una alternativa por su ID (sin autenticación JWT requerida)"""
        try:
            data = request.json if request.is_json else {}
            id_alternativa = data.get("id_alternativa") or request.args.get("id_alternativa")
            
            if not id_alternativa:
                return jsonify({
                    "data": [],
                    "message": "El campo id_alternativa es obligatorio",
                    "status": 0
                }), 400
            
            try:
                id_alternativa = int(id_alternativa)
            except ValueError:
                return jsonify({
                    "data": [],
                    "message": "El id_alternativa debe ser un número",
                    "status": 0
                }), 400
            
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            with connection.cursor() as cursor:
                query = "SELECT id_alternativa, respuesta, estado_alternativa, id_pregunta FROM Alternativa WHERE id_alternativa = %s"
                cursor.execute(query, (id_alternativa,))
                alternativa = cursor.fetchone()
            
            connection.close()
            
            if not alternativa:
                return jsonify({
                    "data": [],
                    "message": "Alternativa no encontrada",
                    "status": 0
                }), 404
            
            if isinstance(alternativa, dict):
                alternativa_dict = {
                    "ID alternativa": alternativa.get('id_alternativa'),
                    "Respuesta": alternativa.get('respuesta'),
                    "Estado alternativa": alternativa.get('estado_alternativa'),
                    "ID pregunta": alternativa.get('id_pregunta')
                }
            else:
                alternativa_dict = {
                    "ID alternativa": alternativa[0],
                    "Respuesta": alternativa[1],
                    "Estado alternativa": alternativa[2],
                    "ID pregunta": alternativa[3] if len(alternativa) > 3 else None
                }
            
            return jsonify({
                "data": [alternativa_dict],
                "message": "Alternativa obtenida correctamente",
                "status": 1
            }), 200

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_obtener_alternativas", methods=["GET"])
    def api_obtener_alternativas():
        """API para obtener todas las alternativas de una pregunta (sin autenticación JWT requerida)"""
        try:
            data = request.json if request.is_json else {}
            id_pregunta = data.get("id_pregunta") or request.args.get("id_pregunta")
            
            id_pregunta_int = None
            if id_pregunta:
                try:
                    id_pregunta_int = int(id_pregunta)
                except ValueError:
                    return jsonify({
                        "data": [],
                        "message": "El id_pregunta debe ser un número",
                        "status": 0
                    }), 400
            
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            try:
                with connection.cursor() as cursor:
                    if id_pregunta_int:
                        query = """
                            SELECT id_alternativa, respuesta, estado_alternativa, id_pregunta
                            FROM Alternativa
                            WHERE id_pregunta = %s
                            ORDER BY id_alternativa
                        """
                        cursor.execute(query, (id_pregunta_int,))
                    else:
                        query = """
                            SELECT id_alternativa, respuesta, estado_alternativa, id_pregunta
                            FROM Alternativa
                            ORDER BY id_pregunta, id_alternativa
                        """
                        cursor.execute(query)
                    alternativas = cursor.fetchall()
            finally:
                connection.close()
            
            data_list = []
            
            for alternativa in alternativas:
                if isinstance(alternativa, dict):
                    alternativa_dict = {
                        "ID alternativa": alternativa.get('id_alternativa'),
                        "Respuesta": alternativa.get('respuesta'),
                        "Estado alternativa": alternativa.get('estado_alternativa'),
                        "ID pregunta": alternativa.get('id_pregunta')
                    }
                else:
                    alternativa_dict = {
                        "ID alternativa": alternativa[0],
                        "Respuesta": alternativa[1],
                        "Estado alternativa": alternativa[2],
                        "ID pregunta": alternativa[3] if len(alternativa) > 3 else None
                    }
                data_list.append(alternativa_dict)
            
            return jsonify({
                "data": data_list,
                "message": "Listado correcto de alternativas",
                "status": 1
            }), 200

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_eliminar_alternativa", methods=["DELETE"])
    @jwt_required()
    def api_eliminar_alternativa():
        """API para eliminar una alternativa"""
        try:
            data = request.json if request.is_json else {}
            id_alternativa = data.get("id_alternativa")
            
            if not id_alternativa:
                return jsonify({
                    "data": [],
                    "message": "El campo id_alternativa es obligatorio",
                    "status": 0
                }), 400
            
            try:
                id_alternativa = int(id_alternativa)
            except ValueError:
                return jsonify({
                    "data": [],
                    "message": "El id_alternativa debe ser un número",
                    "status": 0
                }), 400
            
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            # Verificar que existe
            with connection.cursor() as cursor:
                query = "SELECT id_alternativa FROM Alternativa WHERE id_alternativa = %s"
                cursor.execute(query, (id_alternativa,))
                alternativa = cursor.fetchone()
            
            if not alternativa:
                connection.close()
                return jsonify({
                    "data": [],
                    "message": "La alternativa no existe",
                    "status": 0
                }), 404
            
            # Eliminar
            with connection.cursor() as cursor:
                query = "DELETE FROM Alternativa WHERE id_alternativa = %s"
                cursor.execute(query, (id_alternativa,))
                connection.commit()
            
            connection.close()
            
            return jsonify({
                "data": [],
                "message": "Alternativa eliminada correctamente",
                "status": 1
            }), 200

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    # ============================================
    # APIs PARA TABLA JUGADOR_CUESTIONARIO
    # ============================================
    
    @app.route("/api_registrar_jugador_cuestionario", methods=["POST"])
    @jwt_required()
    def api_registrar_jugador_cuestionario():
        """API para registrar un nuevo jugador en cuestionario"""
        try:
            data = request.json
            id_jugador = data.get("id_jugador")
            alias = data.get("alias")
            id_cuestionario = data.get("id_cuestionario")
            puntaje = data.get("puntaje", 0.00)
            
            if not alias or not id_cuestionario:
                return jsonify({
                    "data": [],
                    "message": "Faltan campos obligatorios: alias, id_cuestionario",
                    "status": 0
                }), 400
            
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            try:
                # Verificar que el alias no esté duplicado para el cuestionario
                with connection.cursor() as cursor:
                    query = "SELECT id_jugador_cuestionario FROM Jugador_Cuestionario WHERE id_cuestionario = %s AND alias = %s"
                    cursor.execute(query, (id_cuestionario, alias))
                    existe = cursor.fetchone()
                    
                    if existe:
                        return jsonify({
                            "data": [],
                            "message": "El alias ya está en uso para este cuestionario",
                            "status": 0
                        }), 400
                
                # Insertar jugador_cuestionario
                with connection.cursor() as cursor:
                    query = "INSERT INTO Jugador_Cuestionario (id_jugador, alias, id_cuestionario, puntaje) VALUES (%s, %s, %s, %s)"
                    cursor.execute(query, (id_jugador, alias, id_cuestionario, puntaje))
                    id_jugador_cuestionario = cursor.lastrowid
                    connection.commit()
                
                return jsonify({
                    "data": [{"id_jugador_cuestionario": id_jugador_cuestionario}],
                    "message": "Jugador registrado en cuestionario correctamente",
                    "status": 1
                }), 201
            finally:
                connection.close()
                
        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_actualizar_jugador_cuestionario", methods=["POST"])
    @jwt_required()
    def api_actualizar_jugador_cuestionario():
        """API para actualizar un jugador_cuestionario existente"""
        try:
            data = request.json
            id_jugador_cuestionario = data.get("id_jugador_cuestionario")
            
            if not id_jugador_cuestionario:
                return jsonify({
                    "data": [],
                    "message": "El campo id_jugador_cuestionario es obligatorio",
                    "status": 0
                }), 400
            
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            # Verificar que existe
            with connection.cursor() as cursor:
                query = "SELECT id_jugador_cuestionario FROM Jugador_Cuestionario WHERE id_jugador_cuestionario = %s"
                cursor.execute(query, (id_jugador_cuestionario,))
                jugador_cuestionario = cursor.fetchone()
            
            if not usuario:
                connection.close()
                return jsonify({
                    "data": [],
                    "message": "El usuario no existe",
                    "status": 0
                }), 404
            
            # Actualizar
            update_fields = []
            params = []
            
            if data.get("alias") is not None:
                update_fields.append("alias = %s")
                params.append(data.get("alias"))
            
            if data.get("puntaje") is not None:
                update_fields.append("puntaje = %s")
                params.append(data.get("puntaje"))
            
            if data.get("id_jugador") is not None:
                update_fields.append("id_jugador = %s")
                params.append(data.get("id_jugador"))
            
            if not update_fields:
                connection.close()
                return jsonify({
                    "data": [],
                    "message": "No hay campos para actualizar",
                    "status": 0
                }), 400
            
            with connection.cursor() as cursor:
                query = "UPDATE Jugador_Cuestionario SET " + ", ".join(update_fields) + " WHERE id_jugador_cuestionario = %s"
                params.append(id_jugador_cuestionario)
                cursor.execute(query, tuple(params))
                connection.commit()
            
            connection.close()
            
            return jsonify({
                "data": [],
                "message": "Jugador_Cuestionario actualizado correctamente",
                "status": 1
            }), 200

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_obtener_jugador_cuestionario_id", methods=["GET"])
    def api_obtener_jugador_cuestionario_id():
        """API para obtener un jugador_cuestionario por su ID (sin autenticación JWT requerida)"""
        try:
            data = request.json if request.is_json else {}
            id_jugador_cuestionario = data.get("id_jugador_cuestionario") or request.args.get("id_jugador_cuestionario")
            
            if not id_jugador_cuestionario:
                return jsonify({
                    "data": [],
                    "message": "El campo id_jugador_cuestionario es obligatorio",
                    "status": 0
                }), 400
            
            try:
                id_jugador_cuestionario = int(id_jugador_cuestionario)
            except ValueError:
                return jsonify({
                    "data": [],
                    "message": "El id_jugador_cuestionario debe ser un número",
                    "status": 0
                }), 400
            
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            with connection.cursor() as cursor:
                query = "SELECT id_jugador_cuestionario, id_jugador, alias, id_cuestionario, puntaje, fecha_participacion FROM Jugador_Cuestionario WHERE id_jugador_cuestionario = %s"
                cursor.execute(query, (id_jugador_cuestionario,))
                jugador_cuestionario = cursor.fetchone()
            
            connection.close()
            
            if not jugador_cuestionario:
                return jsonify({
                    "data": [],
                    "message": "Jugador_Cuestionario no encontrado",
                    "status": 0
                }), 404
            
            if isinstance(jugador_cuestionario, dict):
                jugador_cuestionario_dict = {
                    "ID jugador cuestionario": jugador_cuestionario.get('id_jugador_cuestionario'),
                    "ID jugador": jugador_cuestionario.get('id_jugador'),
                    "Alias": jugador_cuestionario.get('alias'),
                    "ID cuestionario": jugador_cuestionario.get('id_cuestionario'),
                    "Puntaje": float(jugador_cuestionario.get('puntaje')) if jugador_cuestionario.get('puntaje') else 0.00,
                    "Fecha participacion": str(jugador_cuestionario.get('fecha_participacion')) if jugador_cuestionario.get('fecha_participacion') else None
                }
            else:
                jugador_cuestionario_dict = {
                    "ID jugador cuestionario": jugador_cuestionario[0],
                    "ID jugador": jugador_cuestionario[1],
                    "Alias": jugador_cuestionario[2],
                    "ID cuestionario": jugador_cuestionario[3],
                    "Puntaje": float(jugador_cuestionario[4]) if len(jugador_cuestionario) > 4 and jugador_cuestionario[4] else 0.00,
                    "Fecha participacion": str(jugador_cuestionario[5]) if len(jugador_cuestionario) > 5 and jugador_cuestionario[5] else None
                }
            
            return jsonify({
                "data": [jugador_cuestionario_dict],
                "message": "Jugador_Cuestionario obtenido correctamente",
                "status": 1
            }), 200

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_obtener_jugadores_cuestionario", methods=["GET"])
    def api_obtener_jugadores_cuestionario():
        """API para obtener todos los jugadores de un cuestionario (sin autenticación JWT requerida)"""
        try:
            data = request.json if request.is_json else {}
            id_cuestionario = data.get("id_cuestionario") or request.args.get("id_cuestionario")
            
            id_cuestionario_int = None
            if id_cuestionario:
                try:
                    id_cuestionario_int = int(id_cuestionario)
                except ValueError:
                    return jsonify({
                        "data": [],
                        "message": "El id_cuestionario debe ser un número",
                        "status": 0
                    }), 400
            
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            try:
                with connection.cursor() as cursor:
                    if id_cuestionario_int:
                        query = """
                            SELECT id_jugador_cuestionario, id_jugador, alias, id_cuestionario, puntaje, fecha_participacion
                            FROM Jugador_Cuestionario
                            WHERE id_cuestionario = %s
                            ORDER BY puntaje DESC, alias ASC
                        """
                        cursor.execute(query, (id_cuestionario_int,))
                    else:
                        query = """
                            SELECT id_jugador_cuestionario, id_jugador, alias, id_cuestionario, puntaje, fecha_participacion
                            FROM Jugador_Cuestionario
                            ORDER BY id_cuestionario, puntaje DESC, alias ASC
                        """
                        cursor.execute(query)
                    jugadores_cuestionario = cursor.fetchall()
            finally:
                connection.close()
            
            data_list = []
            
            for jugador_cuestionario in jugadores_cuestionario:
                if isinstance(jugador_cuestionario, dict):
                    jugador_cuestionario_dict = {
                        "ID jugador cuestionario": jugador_cuestionario.get('id_jugador_cuestionario'),
                        "ID jugador": jugador_cuestionario.get('id_jugador'),
                        "Alias": jugador_cuestionario.get('alias'),
                        "ID cuestionario": jugador_cuestionario.get('id_cuestionario'),
                        "Puntaje": float(jugador_cuestionario.get('puntaje')) if jugador_cuestionario.get('puntaje') else 0.00,
                        "Fecha participacion": str(jugador_cuestionario.get('fecha_participacion')) if jugador_cuestionario.get('fecha_participacion') else None
                    }
                else:
                    jugador_cuestionario_dict = {
                        "ID jugador cuestionario": jugador_cuestionario[0],
                        "ID jugador": jugador_cuestionario[1],
                        "Alias": jugador_cuestionario[2],
                        "ID cuestionario": jugador_cuestionario[3],
                        "Puntaje": float(jugador_cuestionario[4]) if len(jugador_cuestionario) > 4 and jugador_cuestionario[4] else 0.00,
                        "Fecha participacion": str(jugador_cuestionario[5]) if len(jugador_cuestionario) > 5 and jugador_cuestionario[5] else None
                    }
                data_list.append(jugador_cuestionario_dict)
            
            return jsonify({
                "data": data_list,
                "message": "Listado correcto de jugadores_cuestionario",
                "status": 1
            }), 200

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_eliminar_jugador_cuestionario", methods=["DELETE"])
    @jwt_required()
    def api_eliminar_jugador_cuestionario():
        """API para eliminar un jugador_cuestionario"""
        try:
            data = request.json if request.is_json else {}
            id_jugador_cuestionario = data.get("id_jugador_cuestionario")
            
            if not id_jugador_cuestionario:
                return jsonify({
                    "data": [],
                    "message": "El campo id_jugador_cuestionario es obligatorio",
                    "status": 0
                }), 400
            
            try:
                id_jugador_cuestionario = int(id_jugador_cuestionario)
            except ValueError:
                return jsonify({
                    "data": [],
                    "message": "El id_jugador_cuestionario debe ser un número",
                    "status": 0
                }), 400
            
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            # Verificar que existe
            with connection.cursor() as cursor:
                query = "SELECT id_jugador_cuestionario FROM Jugador_Cuestionario WHERE id_jugador_cuestionario = %s"
                cursor.execute(query, (id_jugador_cuestionario,))
                jugador_cuestionario = cursor.fetchone()
            
            if not jugador_cuestionario:
                connection.close()
                return jsonify({
                    "data": [],
                    "message": "El jugador_cuestionario no existe",
                    "status": 0
                }), 404
            
            # Eliminar
            with connection.cursor() as cursor:
                query = "DELETE FROM Jugador_Cuestionario WHERE id_jugador_cuestionario = %s"
                cursor.execute(query, (id_jugador_cuestionario,))
                connection.commit()
            
            connection.close()
            
            return jsonify({
                "data": [],
                "message": "Jugador_Cuestionario eliminado correctamente",
                "status": 1
            }), 200

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    # ============================================
    # APIs PARA TABLA RESPUESTA
    # ============================================
    
    @app.route("/api_registrar_respuesta", methods=["POST"])
    @jwt_required()
    def api_registrar_respuesta():
        """API para registrar una nueva respuesta"""
        try:
            data = request.json
            id_jugador_cuestionario = data.get("id_jugador_cuestionario")
            id_pregunta = data.get("id_pregunta")
            id_alternativa = data.get("id_alternativa")
            tiempo_utilizado = data.get("tiempo_utilizado", 0)
            
            if not id_jugador_cuestionario or not id_pregunta or not id_alternativa:
                return jsonify({
                    "data": [],
                    "message": "Faltan campos obligatorios: id_jugador_cuestionario, id_pregunta, id_alternativa",
                    "status": 0
                }), 400
            
            # Usar el controlador de respuestas si existe
            if controlador_respuestas:
                puntos = controlador_respuestas.registrar_respuesta(id_jugador_cuestionario, id_pregunta, id_alternativa, tiempo_utilizado)
                
                if puntos is not None:
                    return jsonify({
                        "data": [{"puntos": puntos}],
                        "message": "Respuesta registrada correctamente",
                        "status": 1
                    }), 201
                else:
                    return jsonify({
                        "data": [],
                        "message": "Error al registrar la respuesta",
                        "status": 0
                    }), 500
            
            # Si no existe el controlador, hacer inserción directa
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            try:
                with connection.cursor() as cursor:
                    query = """
                        INSERT INTO Respuesta (id_jugador_cuestionario, id_pregunta, id_alternativa, tiempo_utilizado)
                        VALUES (%s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE 
                            id_alternativa = VALUES(id_alternativa),
                            tiempo_utilizado = VALUES(tiempo_utilizado),
                            fecha_respuesta = CURRENT_TIMESTAMP
                    """
                    cursor.execute(query, (id_jugador_cuestionario, id_pregunta, id_alternativa, tiempo_utilizado))
                    connection.commit()
                
                return jsonify({
                    "data": [],
                    "message": "Respuesta registrada correctamente",
                    "status": 1
                }), 201
            finally:
                connection.close()
                
        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_obtener_respuesta_id", methods=["GET"])
    def api_obtener_respuesta_id():
        """API para obtener una respuesta por su ID (sin autenticación JWT requerida)"""
        try:
            data = request.json if request.is_json else {}
            id_respuesta = data.get("id_respuesta") or request.args.get("id_respuesta")
            
            if not id_respuesta:
                return jsonify({
                    "data": [],
                    "message": "El campo id_respuesta es obligatorio",
                    "status": 0
                }), 400
            
            try:
                id_respuesta = int(id_respuesta)
            except ValueError:
                return jsonify({
                    "data": [],
                    "message": "El id_respuesta debe ser un número",
                    "status": 0
                }), 400
            
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            with connection.cursor() as cursor:
                query = "SELECT id_respuesta, id_jugador_cuestionario, id_pregunta, id_alternativa, tiempo_utilizado, fecha_respuesta FROM Respuesta WHERE id_respuesta = %s"
                cursor.execute(query, (id_respuesta,))
                respuesta = cursor.fetchone()
            
            connection.close()
            
            if not respuesta:
                return jsonify({
                    "data": [],
                    "message": "Respuesta no encontrada",
                    "status": 0
                }), 404
            
            if isinstance(respuesta, dict):
                respuesta_dict = {
                    "ID respuesta": respuesta.get('id_respuesta'),
                    "ID jugador cuestionario": respuesta.get('id_jugador_cuestionario'),
                    "ID pregunta": respuesta.get('id_pregunta'),
                    "ID alternativa": respuesta.get('id_alternativa'),
                    "Tiempo utilizado": respuesta.get('tiempo_utilizado'),
                    "Fecha respuesta": str(respuesta.get('fecha_respuesta')) if respuesta.get('fecha_respuesta') else None
                }
            else:
                respuesta_dict = {
                    "ID respuesta": respuesta[0],
                    "ID jugador cuestionario": respuesta[1],
                    "ID pregunta": respuesta[2],
                    "ID alternativa": respuesta[3],
                    "Tiempo utilizado": respuesta[4] if len(respuesta) > 4 else 0,
                    "Fecha respuesta": str(respuesta[5]) if len(respuesta) > 5 and respuesta[5] else None
                }
            
            return jsonify({
                "data": [respuesta_dict],
                "message": "Respuesta obtenida correctamente",
                "status": 1
            }), 200

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_obtener_respuestas", methods=["GET"])
    def api_obtener_respuestas():
        """API para obtener todas las respuestas de un usuario o pregunta (sin autenticación JWT requerida)"""
        try:
            data = request.json if request.is_json else {}
            id_jugador_cuestionario = data.get("id_jugador_cuestionario") or request.args.get("id_jugador_cuestionario")
            id_pregunta = data.get("id_pregunta") or request.args.get("id_pregunta")
            
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            condiciones = []
            params = []
            
            if id_jugador_cuestionario:
                try:
                    id_jugador_cuestionario = int(id_jugador_cuestionario)
                    condiciones.append("id_jugador_cuestionario = %s")
                    params.append(id_jugador_cuestionario)
                except ValueError:
                    return jsonify({
                        "data": [],
                        "message": "El id_jugador_cuestionario debe ser un número",
                        "status": 0
                    }), 400
            
            if id_pregunta:
                try:
                    id_pregunta = int(id_pregunta)
                    condiciones.append("id_pregunta = %s")
                    params.append(id_pregunta)
                except ValueError:
                    return jsonify({
                        "data": [],
                        "message": "El id_pregunta debe ser un número",
                        "status": 0
                    }), 400
            
            try:
                with connection.cursor() as cursor:
                    query = """
                        SELECT id_respuesta, id_jugador_cuestionario, id_pregunta, id_alternativa,
                               tiempo_utilizado, fecha_respuesta
                        FROM Respuesta
                    """
                    if condiciones:
                        query += " WHERE " + " AND ".join(condiciones)
                    query += " ORDER BY fecha_respuesta DESC, id_respuesta DESC"
                    cursor.execute(query, tuple(params))
                    respuestas = cursor.fetchall()
            finally:
                connection.close()
            
            data_list = []
            
            for respuesta in respuestas:
                if isinstance(respuesta, dict):
                    respuesta_dict = {
                        "ID respuesta": respuesta.get('id_respuesta'),
                        "ID jugador cuestionario": respuesta.get('id_jugador_cuestionario'),
                        "ID pregunta": respuesta.get('id_pregunta'),
                        "ID alternativa": respuesta.get('id_alternativa'),
                        "Tiempo utilizado": respuesta.get('tiempo_utilizado'),
                        "Fecha respuesta": str(respuesta.get('fecha_respuesta')) if respuesta.get('fecha_respuesta') else None
                    }
                else:
                    respuesta_dict = {
                        "ID respuesta": respuesta[0],
                        "ID jugador cuestionario": respuesta[1],
                        "ID pregunta": respuesta[2],
                        "ID alternativa": respuesta[3],
                        "Tiempo utilizado": respuesta[4] if len(respuesta) > 4 else 0,
                        "Fecha respuesta": str(respuesta[5]) if len(respuesta) > 5 and respuesta[5] else None
                    }
                data_list.append(respuesta_dict)
            
            return jsonify({
                "data": data_list,
                "message": "Listado correcto de respuestas",
                "status": 1
            }), 200

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_eliminar_respuesta", methods=["DELETE"])
    @jwt_required()
    def api_eliminar_respuesta():
        """API para eliminar una respuesta"""
        try:
            data = request.json if request.is_json else {}
            id_respuesta = data.get("id_respuesta")
            
            if not id_respuesta:
                return jsonify({
                    "data": [],
                    "message": "El campo id_respuesta es obligatorio",
                    "status": 0
                }), 400
            
            try:
                id_respuesta = int(id_respuesta)
            except ValueError:
                return jsonify({
                    "data": [],
                    "message": "El id_respuesta debe ser un número",
                    "status": 0
                }), 400
            
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            # Verificar que existe
            with connection.cursor() as cursor:
                query = "SELECT id_respuesta FROM Respuesta WHERE id_respuesta = %s"
                cursor.execute(query, (id_respuesta,))
                respuesta = cursor.fetchone()
            
            if not respuesta:
                connection.close()
                return jsonify({
                    "data": [],
                    "message": "La respuesta no existe",
                    "status": 0
                }), 404
            
            # Eliminar
            with connection.cursor() as cursor:
                query = "DELETE FROM Respuesta WHERE id_respuesta = %s"
                cursor.execute(query, (id_respuesta,))
                connection.commit()
            
            connection.close()
            
            return jsonify({
                "data": [],
                "message": "Respuesta eliminada correctamente",
                "status": 1
            }), 200

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    # ============================================
    # APIs PARA TABLA GRUPOMIEMBRO
    # ============================================
    
    @app.route("/api_registrar_grupo_miembro", methods=["POST"])
    @jwt_required()
    def api_registrar_grupo_miembro():
        """API para agregar un miembro a un grupo"""
        try:
            data = request.json
            id_grupo = data.get("id_grupo")
            id_jugador_cuestionario = data.get("id_jugador_cuestionario")
            es_lider = data.get("es_lider", 0)
            
            if not id_grupo or not id_jugador_cuestionario:
                return jsonify({
                    "data": [],
                    "message": "Faltan campos obligatorios: id_grupo, id_jugador_cuestionario",
                    "status": 0
                }), 400
            
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            # Verificar que el grupo existe
            with connection.cursor() as cursor:
                query = "SELECT id_grupo FROM Grupo WHERE id_grupo = %s"
                cursor.execute(query, (id_grupo,))
                grupo = cursor.fetchone()
                
                if not grupo:
                    connection.close()
                    return jsonify({
                        "data": [],
                        "message": "El grupo no existe",
                        "status": 0
                    }), 404
            
            # Insertar miembro (ON DUPLICATE KEY UPDATE para evitar duplicados)
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO GrupoMiembro (id_grupo, id_jugador_cuestionario, es_lider)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE es_lider = VALUES(es_lider)
                """
                cursor.execute(query, (id_grupo, id_jugador_cuestionario, es_lider))
                id_miembro = cursor.lastrowid
                connection.commit()
            
            connection.close()
            
            return jsonify({
                "data": [{"id_miembro": id_miembro}],
                "message": "Miembro agregado al grupo correctamente",
                "status": 1
            }), 201
                
        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_obtener_grupo_miembros", methods=["GET"])
    def api_obtener_grupo_miembros():
        """API para obtener todos los miembros de un grupo (sin autenticación JWT requerida)"""
        try:
            data = request.json if request.is_json else {}
            id_grupo = data.get("id_grupo") or request.args.get("id_grupo")
            
            id_grupo_int = None
            if id_grupo:
                try:
                    id_grupo_int = int(id_grupo)
                except ValueError:
                    return jsonify({
                        "data": [],
                        "message": "El id_grupo debe ser un número",
                        "status": 0
                    }), 400
            
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            try:
                with connection.cursor() as cursor:
                    if id_grupo_int:
                        query = """
                            SELECT id_miembro, id_grupo, id_jugador_cuestionario, fecha_union, es_lider
                            FROM GrupoMiembro
                            WHERE id_grupo = %s
                            ORDER BY id_miembro
                        """
                        cursor.execute(query, (id_grupo_int,))
                    else:
                        query = """
                            SELECT id_miembro, id_grupo, id_jugador_cuestionario, fecha_union, es_lider
                            FROM GrupoMiembro
                            ORDER BY id_grupo, id_miembro
                        """
                        cursor.execute(query)
                    miembros = cursor.fetchall()
            finally:
                connection.close()
            
            data_list = []
            
            for miembro in miembros:
                if isinstance(miembro, dict):
                    miembro_dict = {
                        "ID miembro": miembro.get('id_miembro'),
                        "ID grupo": miembro.get('id_grupo'),
                        "ID jugador cuestionario": miembro.get('id_jugador_cuestionario'),
                        "Fecha union": str(miembro.get('fecha_union')) if miembro.get('fecha_union') else None,
                        "Es lider": bool(miembro.get('es_lider'))
                    }
                else:
                    miembro_dict = {
                        "ID miembro": miembro[0],
                        "ID grupo": miembro[1],
                        "ID jugador cuestionario": miembro[2],
                        "Fecha union": str(miembro[3]) if len(miembro) > 3 and miembro[3] else None,
                        "Es lider": bool(miembro[4]) if len(miembro) > 4 else False
                    }
                data_list.append(miembro_dict)
            
            return jsonify({
                "data": data_list,
                "message": "Listado correcto de miembros del grupo",
                "status": 1
            }), 200

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_eliminar_grupo_miembro", methods=["DELETE"])
    @jwt_required()
    def api_eliminar_grupo_miembro():
        """API para eliminar un miembro de un grupo"""
        try:
            data = request.json if request.is_json else {}
            id_miembro = data.get("id_miembro")
            
            if not id_miembro:
                return jsonify({
                    "data": [],
                    "message": "El campo id_miembro es obligatorio",
                    "status": 0
                }), 400
            
            try:
                id_miembro = int(id_miembro)
            except ValueError:
                return jsonify({
                    "data": [],
                    "message": "El id_miembro debe ser un número",
                    "status": 0
                }), 400
            
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            # Verificar que existe
            with connection.cursor() as cursor:
                query = "SELECT id_miembro FROM GrupoMiembro WHERE id_miembro = %s"
                cursor.execute(query, (id_miembro,))
                miembro = cursor.fetchone()
            
            if not miembro:
                connection.close()
                return jsonify({
                    "data": [],
                    "message": "El miembro no existe",
                    "status": 0
                }), 404
            
            # Eliminar
            with connection.cursor() as cursor:
                query = "DELETE FROM GrupoMiembro WHERE id_miembro = %s"
                cursor.execute(query, (id_miembro,))
                connection.commit()
            
            connection.close()
            
            return jsonify({
                "data": [],
                "message": "Miembro eliminado del grupo correctamente",
                "status": 1
            }), 200

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    # ============================================
    # APIs PARA TABLA PARTICIPANTE
    # ============================================
    
    @app.route("/api_obtener_participante_id", methods=["GET"])
    def api_obtener_participante_id():
        """API para obtener un participante por su ID (sin autenticación JWT requerida)"""
        try:
            data = request.json if request.is_json else {}
            id_participante = data.get("id_participante") or request.args.get("id_participante")
            
            if not id_participante:
                return jsonify({
                    "data": [],
                    "message": "El campo id_participante es obligatorio",
                    "status": 0
                }), 400
            
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            with connection.cursor() as cursor:
                query = "SELECT id_participante FROM Participante WHERE id_participante = %s"
                cursor.execute(query, (id_participante,))
                participante = cursor.fetchone()
            
            connection.close()
            
            if not participante:
                return jsonify({
                    "data": [],
                    "message": "Participante no encontrado",
                    "status": 0
                }), 404
            
            if isinstance(participante, dict):
                participante_dict = {
                    "ID participante": participante.get('id_participante')
                }
            else:
                participante_dict = {
                    "ID participante": participante[0]
                }
            
            return jsonify({
                "data": [participante_dict],
                "message": "Participante obtenido correctamente",
                "status": 1
            }), 200

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_obtener_participantes", methods=["GET"])
    def api_obtener_participantes():
        """API para obtener todos los participantes (sin autenticación JWT requerida)"""
        try:
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            with connection.cursor() as cursor:
                query = "SELECT id_participante FROM Participante"
                cursor.execute(query)
                participantes = cursor.fetchall()
            
            connection.close()
            
            data_list = []
            
            for participante in participantes:
                if isinstance(participante, dict):
                    participante_dict = {
                        "ID participante": participante.get('id_participante')
                    }
                else:
                    participante_dict = {
                        "ID participante": participante[0]
                    }
                data_list.append(participante_dict)
            
            return jsonify({
                "data": data_list,
                "message": "Listado correcto de participantes",
                "status": 1
            }), 200

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_eliminar_participante", methods=["DELETE"])
    @jwt_required()
    def api_eliminar_participante():
        """API para eliminar un participante"""
        try:
            data = request.json if request.is_json else {}
            id_participante = data.get("id_participante")
            
            if not id_participante:
                return jsonify({
                    "data": [],
                    "message": "El campo id_participante es obligatorio",
                    "status": 0
                }), 400
            
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            # Verificar que existe
            with connection.cursor() as cursor:
                query = "SELECT id_participante FROM Participante WHERE id_participante = %s"
                cursor.execute(query, (id_participante,))
                participante = cursor.fetchone()
            
            if not participante:
                connection.close()
                return jsonify({
                    "data": [],
                    "message": "El participante no existe",
                    "status": 0
                }), 404
            
            # Eliminar
            with connection.cursor() as cursor:
                query = "DELETE FROM Participante WHERE id_participante = %s"
                cursor.execute(query, (id_participante,))
                connection.commit()
            
            connection.close()
            
            return jsonify({
                "data": [],
                "message": "Participante eliminado correctamente",
                "status": 1
            }), 200

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    # ============================================
    # APIs PARA TABLA PARTICIPANTE_CUESTIONARIO
    # ============================================
    
    @app.route("/api_registrar_participante_cuestionario", methods=["POST"])
    @jwt_required()
    def api_registrar_participante_cuestionario():
        """API para registrar un participante en un cuestionario"""
        try:
            data = request.json
            id_participante = data.get("id_participante")
            id_cuestionario = data.get("id_cuestionario")
            alias = data.get("alias")
            
            if not id_participante or not id_cuestionario:
                return jsonify({
                    "data": [],
                    "message": "Faltan campos obligatorios: id_participante, id_cuestionario",
                    "status": 0
                }), 400
            
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            # Insertar relación
            with connection.cursor() as cursor:
                query = "INSERT INTO Participante_Cuestionario (id_participante, id_cuestionario, alias) VALUES (%s, %s, %s)"
                cursor.execute(query, (id_participante, id_cuestionario, alias))
                connection.commit()
            
            connection.close()
            
            return jsonify({
                "data": [],
                "message": "Participante registrado en cuestionario correctamente",
                "status": 1
            }), 201
                
        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_obtener_participantes_cuestionario", methods=["GET"])
    def api_obtener_participantes_cuestionario():
        """API para obtener todos los participantes de un cuestionario (sin autenticación JWT requerida)"""
        try:
            data = request.json if request.is_json else {}
            id_cuestionario = data.get("id_cuestionario") or request.args.get("id_cuestionario")
            
            id_cuestionario_int = None
            if id_cuestionario:
                try:
                    id_cuestionario_int = int(id_cuestionario)
                except ValueError:
                    return jsonify({
                        "data": [],
                        "message": "El id_cuestionario debe ser un número",
                        "status": 0
                    }), 400
            
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            try:
                with connection.cursor() as cursor:
                    if id_cuestionario_int:
                        query = """
                            SELECT id_participante, id_cuestionario, alias
                            FROM Participante_Cuestionario
                            WHERE id_cuestionario = %s
                            ORDER BY id_participante
                        """
                        cursor.execute(query, (id_cuestionario_int,))
                    else:
                        query = """
                            SELECT id_participante, id_cuestionario, alias
                            FROM Participante_Cuestionario
                            ORDER BY id_cuestionario, id_participante
                        """
                        cursor.execute(query)
                    participantes = cursor.fetchall()
            finally:
                connection.close()
            
            data_list = []
            
            for participante in participantes:
                if isinstance(participante, dict):
                    participante_dict = {
                        "ID participante": participante.get('id_participante'),
                        "ID cuestionario": participante.get('id_cuestionario'),
                        "Alias": participante.get('alias')
                    }
                else:
                    participante_dict = {
                        "ID participante": participante[0],
                        "ID cuestionario": participante[1],
                        "Alias": participante[2] if len(participante) > 2 else None
                    }
                data_list.append(participante_dict)
            
            return jsonify({
                "data": data_list,
                "message": "Listado correcto de participantes del cuestionario",
                "status": 1
            }), 200

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_eliminar_participante_cuestionario", methods=["DELETE"])
    @jwt_required()
    def api_eliminar_participante_cuestionario():
        """API para eliminar un participante de un cuestionario"""
        try:
            data = request.json if request.is_json else {}
            id_participante = data.get("id_participante")
            id_cuestionario = data.get("id_cuestionario")
            
            if not id_participante or not id_cuestionario:
                return jsonify({
                    "data": [],
                    "message": "Faltan campos obligatorios: id_participante, id_cuestionario",
                    "status": 0
                }), 400
            
            try:
                id_cuestionario = int(id_cuestionario)
            except ValueError:
                return jsonify({
                    "data": [],
                    "message": "El id_cuestionario debe ser un número",
                    "status": 0
                }), 400
            
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            # Verificar que existe
            with connection.cursor() as cursor:
                query = "SELECT id_participante FROM Participante_Cuestionario WHERE id_participante = %s AND id_cuestionario = %s"
                cursor.execute(query, (id_participante, id_cuestionario))
                participante = cursor.fetchone()
            
            if not participante:
                connection.close()
                return jsonify({
                    "data": [],
                    "message": "El participante no está registrado en este cuestionario",
                    "status": 0
                }), 404
            
            # Eliminar
            with connection.cursor() as cursor:
                query = "DELETE FROM Participante_Cuestionario WHERE id_participante = %s AND id_cuestionario = %s"
                cursor.execute(query, (id_participante, id_cuestionario))
                connection.commit()
            
            connection.close()
            
            return jsonify({
                "data": [],
                "message": "Participante eliminado del cuestionario correctamente",
                "status": 1
            }), 200

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    # ============================================
    # APIs PARA TABLA VOTACIONGRUPO
    # ============================================
    
    @app.route("/api_registrar_votacion_grupo", methods=["POST"])
    @jwt_required()
    def api_registrar_votacion_grupo():
        """API para registrar una votación de grupo"""
        try:
            data = request.json
            id_grupo = data.get("id_grupo")
            id_pregunta = data.get("id_pregunta")
            id_jugador_cuestionario = data.get("id_jugador_cuestionario")
            id_alternativa = data.get("id_alternativa")
            
            if not id_grupo or not id_pregunta or not id_jugador_cuestionario or not id_alternativa:
                return jsonify({
                    "data": [],
                    "message": "Faltan campos obligatorios: id_grupo, id_pregunta, id_jugador_cuestionario, id_alternativa",
                    "status": 0
                }), 400
            
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            # Insertar votación (ON DUPLICATE KEY UPDATE para actualizar si ya existe)
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO VotacionGrupo (id_grupo, id_pregunta, id_jugador_cuestionario, id_alternativa)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE 
                        id_alternativa = VALUES(id_alternativa),
                        fecha_votacion = CURRENT_TIMESTAMP
                """
                cursor.execute(query, (id_grupo, id_pregunta, id_jugador_cuestionario, id_alternativa))
                id_votacion = cursor.lastrowid
                connection.commit()
            
            connection.close()
            
            return jsonify({
                "data": [{"id_votacion": id_votacion}],
                "message": "Votación registrada correctamente",
                "status": 1
            }), 201
                
        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_obtener_votaciones_grupo", methods=["GET"])
    def api_obtener_votaciones_grupo():
        """API para obtener todas las votaciones de un grupo y pregunta (sin autenticación JWT requerida)"""
        try:
            data = request.json if request.is_json else {}
            id_grupo = data.get("id_grupo") or request.args.get("id_grupo")
            id_pregunta = data.get("id_pregunta") or request.args.get("id_pregunta")
            
            if not id_grupo or not id_pregunta:
                return jsonify({
                    "data": [],
                    "message": "Faltan campos obligatorios: id_grupo, id_pregunta",
                    "status": 0
                }), 400
            
            try:
                id_grupo = int(id_grupo)
                id_pregunta = int(id_pregunta)
            except ValueError:
                return jsonify({
                    "data": [],
                    "message": "Los IDs deben ser números",
                    "status": 0
                }), 400
            
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            with connection.cursor() as cursor:
                query = "SELECT id_votacion, id_grupo, id_pregunta, id_jugador_cuestionario, id_alternativa, fecha_votacion FROM VotacionGrupo WHERE id_grupo = %s AND id_pregunta = %s"
                cursor.execute(query, (id_grupo, id_pregunta))
                votaciones = cursor.fetchall()
            
            connection.close()
            
            data_list = []
            
            for votacion in votaciones:
                if isinstance(votacion, dict):
                    votacion_dict = {
                        "ID votacion": votacion.get('id_votacion'),
                        "ID grupo": votacion.get('id_grupo'),
                        "ID pregunta": votacion.get('id_pregunta'),
                        "ID usuario": votacion.get('id_usuario'),
                        "ID alternativa": votacion.get('id_alternativa'),
                        "Fecha votacion": str(votacion.get('fecha_votacion')) if votacion.get('fecha_votacion') else None
                    }
                else:
                    votacion_dict = {
                        "ID votacion": votacion[0],
                        "ID grupo": votacion[1],
                        "ID pregunta": votacion[2],
                        "ID usuario": votacion[3],
                        "ID alternativa": votacion[4],
                        "Fecha votacion": str(votacion[5]) if len(votacion) > 5 and votacion[5] else None
                    }
                data_list.append(votacion_dict)
            
            return jsonify({
                "data": data_list,
                "message": "Listado correcto de votaciones",
                "status": 1
            }), 200

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500

    @app.route("/api_eliminar_votacion_grupo", methods=["DELETE"])
    @jwt_required()
    def api_eliminar_votacion_grupo():
        """API para eliminar una votación de grupo"""
        try:
            data = request.json if request.is_json else {}
            id_votacion = data.get("id_votacion")
            
            if not id_votacion:
                return jsonify({
                    "data": [],
                    "message": "El campo id_votacion es obligatorio",
                    "status": 0
                }), 400
            
            try:
                id_votacion = int(id_votacion)
            except ValueError:
                return jsonify({
                    "data": [],
                    "message": "El id_votacion debe ser un número",
                    "status": 0
                }), 400
            
            connection = conectarbd()
            if not connection:
                return jsonify({
                    "data": [],
                    "message": "Error de conexión a la base de datos",
                    "status": 0
                }), 500
            
            try:
                # Verificar que existe
                with connection.cursor() as cursor:
                    query = "SELECT id_votacion FROM VotacionGrupo WHERE id_votacion = %s"
                    cursor.execute(query, (id_votacion,))
                    votacion = cursor.fetchone()
                
                if not votacion:
                    return jsonify({
                        "data": [],
                        "message": "La votación no existe",
                        "status": 0
                    }), 404
                
                # Eliminar
                with connection.cursor() as cursor:
                    query = "DELETE FROM VotacionGrupo WHERE id_votacion = %s"
                    cursor.execute(query, (id_votacion,))
                    connection.commit()
                
                return jsonify({
                    "data": [],
                    "message": "Votación eliminada correctamente",
                    "status": 1
                }), 200
            finally:
                connection.close()

        except Exception as ex:
            return jsonify({"message": str(repr(ex)), "status": 0}), 500
