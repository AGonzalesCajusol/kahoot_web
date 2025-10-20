import hashlib
import re
from flask import render_template, request, jsonify
import random, time
from controladores.correo_config import send_email
from conexion import conectarbd  

codigos_recuperacion = {}
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$')


def registrar_rutas_recuperacion(app):

    @app.route("/api_recuperar_contrasena", methods=["POST"])
    def api_recuperar_contrasena():
        try:
            data = request.get_json()
            email = data.get("email")

            if not email:
                return jsonify({"code": 0, "message": "Debes ingresar tu correo electrónico."}), 400

            connection = conectarbd()
            if not connection:
                return jsonify({"code": 0, "message": "Error al conectar con la base de datos."}), 500

            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Docente WHERE correo = %s", (email,))
            docente = cursor.fetchone()
            connection.close()

            if not docente:
                return jsonify({"code": 0, "message": "El correo no está registrado en el sistema."}), 404

            codigo = str(random.randint(100000, 999999))

            codigos_recuperacion[email] = {
                "codigo": codigo,
                "expiracion": time.time() + 600  # 10 minutos
            }

            if send_email(email, codigo):
                return jsonify({
                    "code": 1,
                    "message": f"Se envió un código de verificación al correo {email}. Vigente por 10 minutos."
                }), 200
            else:
                return jsonify({
                    "code": 0,
                    "message": "No se pudo enviar el correo. Verifica el servidor SMTP."
                }), 500

        except Exception as e:
            print("Error en /api_recuperar_contrasena:", e)
            return jsonify({"code": 0, "message": "Error interno del servidor."}), 500


    @app.route("/verificar_codigo_recuperacion", methods=["GET"])
    def mostrar_pagina_verificar_codigo():
        return render_template("/recuperacion/verificar_codigo_recuperacion.html")


    @app.route("/verificar_codigo_recuperacion", methods=["POST"])
    def verificar_codigo_recuperacion():
        try:
            data = request.get_json()
            email = data.get("email")
            codigo = data.get("codigo")

            if not email or not codigo:
                return jsonify({"code": 0, "message": "Datos incompletos."}), 400

            registro = codigos_recuperacion.get(email)
            if not registro:
                return jsonify({"code": 0, "message": "No se encontró un código asociado a este correo."}), 404

            if time.time() > registro["expiracion"]:
                codigos_recuperacion.pop(email, None)
                return jsonify({"code": 0, "message": "El código ha expirado. Solicita uno nuevo."}), 400

            if registro["codigo"] != codigo:
                return jsonify({"code": 0, "message": "El código ingresado es incorrecto."}), 400

            codigos_recuperacion.pop(email, None)
            return jsonify({
                "code": 1,
                "message": "Código verificado correctamente. Puedes restablecer tu contraseña ahora."
            }), 200

        except Exception as e:
            print("Error en /verificar_codigo_recuperacion:", e)
            return jsonify({"code": 0, "message": "Error interno del servidor."}), 500

    @app.route("/actualizar_contrasena", methods=["POST"])
    def actualizar_contrasena():
        try:
            data = request.get_json(force=True, silent=False)
            email = data.get("email")
            nueva_password = data.get("nueva_password")

            if not email or not nueva_password:
                return jsonify({"code": 0, "message": "Datos incompletos."}), 400

            if not PASSWORD_REGEX.match(nueva_password):
                return jsonify({"code": 0, "message": "La contraseña no cumple los requisitos."}), 400

            # Hash SHA-256 (coherente con tu validador de login)
            hashed = hashlib.sha256(nueva_password.encode("utf-8")).hexdigest()

            conn = conectarbd()
            if not conn:
                return jsonify({"code": 0, "message": "No se pudo conectar a la BD."}), 500

            cur = conn.cursor()
            # Ajusta nombres de tabla/campos si difieren
            cur.execute("UPDATE Docente SET password=%s WHERE correo=%s", (hashed, email))
            conn.commit()
            filas = cur.rowcount
            cur.close()
            conn.close()

            if filas == 0:
                return jsonify({"code": 0, "message": "El correo no está registrado."}), 404

            return jsonify({"code": 1, "message": "Contraseña actualizada correctamente."}), 200

        except Exception as e:
            # Log útil en consola
            print("Error en /actualizar_contrasena:", e)
            # Siempre devolver JSON, no HTML, para que el front no falle en resp.json()
            return jsonify({"code": 0, "message": "Error interno del servidor."}), 500

