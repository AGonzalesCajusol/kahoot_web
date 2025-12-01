from flask import render_template, request, jsonify, session
import time
import re
from controladores.docente import registrar_docente, modificar_docente, registrar_jugador, correo_disponible
from controladores.correo_config import send_email
import random


codigos_verificacion = {}
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$')

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

            # Validación de contraseña sólida en backend
            if not PASSWORD_REGEX.match(password):
                return jsonify({
                    "code": 0, 
                    "message": "La contraseña debe tener mínimo 8 caracteres, incluir mayúscula, minúscula, número y símbolo."
                }), 400

            codigo = str(random.randint(100000, 999999))
            tipo_usuario = data.get("tipo_usuario", "docente")
            rostro = data.get("rostro")  # Datos faciales en base64 (opcional)
            
            codigos_verificacion[email] = {
                "codigo": codigo,
                "expiracion": time.time() + 600,
                "nombres": nombres,
                "apellidos": apellidos,
                "password": password,
                "tipo_usuario": tipo_usuario,
                "rostro": rostro  # Guardar datos faciales temporalmente
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
                # Obtener datos faciales si fueron proporcionados
                rostro_data = registro.get("rostro")
                
                response = registrar_docente(
                    registro_email,
                    registro["password"],
                    registro.get("nombres", ""),
                    registro.get("apellidos", ""),
                    rostro_data  # Pasar datos faciales al controlador
                )
                
                # Log para debugging
                print(f"📝 Respuesta de registro: {response}")
            else:
                # Obtener datos faciales si fueron proporcionados
                rostro_data = registro.get("rostro")
                
                response = registrar_jugador(
                    registro_email,
                    registro["password"],
                    rostro_data  # Pasar datos faciales al controlador
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
    
    @app.route("/reenviar_codigo", methods=["POST"])
    def reenviar_codigo():
        """Reenvía el código de verificación para registro"""
        try:
            data = request.get_json()
            email = data.get("email")

            if not email:
                return jsonify({"code": 0, "message": "Debes ingresar tu correo electrónico."}), 400

            # Verificar si hay un código pendiente para este email
            registro = codigos_verificacion.get(email)
            
            if not registro:
                return jsonify({
                    "code": 0, 
                    "message": "No se encontró un registro pendiente. Regístrate nuevamente."
                }), 404

            nuevo_codigo = str(random.randint(100000, 999999))
            
            codigos_verificacion[email] = {
                **registro, 
                "codigo": nuevo_codigo,
                "expiracion": time.time() + 600  
            }

            if send_email(email, nuevo_codigo):
                return jsonify({
                    "code": 1,
                    "message": f"Nuevo código de verificación enviado al correo {email}"
                }), 200
            else:
                return jsonify({
                    "code": 0,
                    "message": "No se pudo enviar el correo. Verifica el servidor SMTP."
                }), 500

        except Exception as e:
            print("Error en /reenviar_codigo:", e)
            return jsonify({"code": 0, "message": "Error interno del servidor."}), 500
            
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
                if nuevo_correo:
                    session['correo'] = nuevo_correo
                else:
                    session['correo'] = correo
    
            return response

        except Exception as e:
            print(f"Error en /modificar_perfil: {e}")
            import traceback
            traceback.print_exc()
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
