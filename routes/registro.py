from flask import render_template, request, jsonify, session
import time
from controladores.docente import registrar_docente, modificar_docente, registrar_jugador, correo_disponible
from controladores.correo_config import send_email  
import random


codigos_verificacion = {}

def registrar_rutas(app):
    @app.route("/enviar_codigo", methods=["POST"])
    def enviar_codigo():
        try:
            data = request.get_json()
            email = data.get("email")
            nombres = data.get("nombres")
            apellidos = data.get("apellidos")
            password = data.get("password")

            if not email or not password:
                return jsonify({"code": 0, "message": "Faltan datos obligatorios."}), 400

            codigo = str(random.randint(100000, 999999))
            tipo_usuario = data.get("tipo_usuario", "docente")
            codigos_verificacion[email] = {
                "codigo": codigo,
                "expiracion": time.time() + 600,
                "nombres": nombres,
                "apellidos": apellidos,
                "password": password,
                "tipo_usuario": tipo_usuario
            }


            if send_email(email, codigo):
                return jsonify({
                    "code": 1,
                    "message": f"Código de verificación enviado al correo {email}"
                }), 200
            else:
                return jsonify({
                    "code": 0,
                    "message": "No se pudo enviar el correo. Verifica el servidor SMTP."
                }), 500

        except Exception as e:
            print("Error en /enviar_codigo:", e)
            return jsonify({"code": 0, "message": "Error interno en el servidor."}), 500

    
    @app.route("/verificar_codigo", methods=["POST"])
    def verificar_codigo():
        try:
            data = request.get_json()
            email = data.get("email")
            codigo = data.get("codigo")

            if not email or not codigo:
                return jsonify({"code": 0, "message": "Datos incompletos."}), 400

            registro = codigos_verificacion.get(email)
            if not registro:
                return jsonify({"code": 0, "message": "No se encontró un código asociado a este correo."}), 404

            # Verificar expiración
            if time.time() > registro["expiracion"]:
                codigos_verificacion.pop(email, None)
                return jsonify({"code": 0, "message": "El código ha expirado. Regístrate nuevamente."}), 400

            # Validar código
            if registro["codigo"] != codigo:
                return jsonify({"code": 0, "message": "Código incorrecto."}), 400

            registro_email = email

            tipo_usuario = registro.get("tipo_usuario", "docente")

            if tipo_usuario == "docente":
                response = registrar_docente(
                    registro_email,
                    registro["password"],
                    registro.get("nombres", ""),
                    registro.get("apellidos", "")
                )
            else:
                response = registrar_jugador(
                    registro_email,
                    registro["password"]
                )


            codigos_verificacion.pop(email, None)

            if "exitosamente" in response.lower():
                return jsonify({
                    "code": 1,
                    "message": f"Correo verificado y {tipo_usuario} registrado correctamente."
                }), 200
            else:
                return jsonify({
                    "code": 0,
                    "message": f"Hubo un problema al registrar el {tipo_usuario}: {response}"
                }), 500

        except Exception as e:
            print("Error en /verificar_codigo:", e)
            return jsonify({"code": 0, "message": "Error interno del servidor."}), 500

    @app.route("/verificarcodigo", methods=["GET"])
    def verificarcodigo_pagina():
        return render_template("verificar_codigo.html")
            
    @app.route("/modificar_perfil", methods=["POST"])
    def modificar_perfil():
        try:
            data = request.get_json()
            correo = data.get("correo")
            nuevo_nombre = data.get("nombre")
            nuevo_apellido = data.get("apellido")
            nuevo_correo = data.get("nuevo_correo")
            nueva_contrasena = data.get("nueva_contrasena")
            
            # Validar campos obligatorios
            if not correo or not nuevo_nombre or not nuevo_apellido:
                return jsonify({"code": 0, "message": "Faltan datos obligatorios."}), 400

            # Llamada al controlador para modificar los datos
            response = modificar_docente(
                correo,
                nuevo_nombre,
                nuevo_apellido,
                nuevo_correo,
                nueva_contrasena
            )

            if response[1] == 200:
                session['nombres'] = nuevo_nombre
                session['apellidos'] = nuevo_apellido
                session['correo'] = nuevo_correo if nuevo_correo else correo
    
            return response

        except Exception as e:
            print(f"Error en /modificar_perfil: {e}")
            return jsonify({"code": 0, "message": "Error interno del servidor."}), 500

    @app.route("/validar_correo", methods=["POST"])
    def validar_correo_route():
        try:
            data = request.get_json()
            correo = data.get("email")
            if not correo:
                return jsonify({"code": 0, "message": "Correo no proporcionado"}), 400

            if correo_disponible(correo):
                return jsonify({"code": 1, "message": "Correo disponible"}), 200
            else:
                return jsonify({"code": 0, "message": "Este correo ya está registrado"}), 200

        except Exception as e:
            print("Error en /validar_correo:", e)
            return jsonify({"code": 0, "message": "Error interno del servidor"}), 500
