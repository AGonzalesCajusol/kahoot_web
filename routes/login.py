from flask import render_template, request, redirect, session, url_for, flash, jsonify, make_response
from controladores.login import validar_docente, validar_docente_facial, validar_jugador_facial
from controladores.docente import registrar_docente 
from controladores.jugador import validar_jugador
from controladores.cookies_utils import establecer_cookie_encriptada

def registrar_rutas(app):
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            correo = request.form['email']
            password = request.form['password']

            docente = validar_docente(correo, password)
            if docente:
                session['docente_id'] = docente['id_docente']
                session['nombres'] = docente['nombres']
                session['tipo_usuario'] = 'docente'
                
                # Crear cookies encriptadas (similar al ejemplo)
                response = make_response(redirect(url_for('dashboard')))
                id_usuario = str(docente['id_docente'])
                nombre_usuario = docente['nombres']
                
                # Establecer cookies encriptadas con SHA256 (como en el ejemplo)
                establecer_cookie_encriptada(response, 'id_usuario', id_usuario)
                establecer_cookie_encriptada(response, 'nombre_usuario', nombre_usuario)
                
                return response

            jugador = validar_jugador(correo, password)
            if jugador:
                session['jugador_id'] = jugador['id_jugador']
                session['email'] = jugador['email']
                session['tipo_usuario'] = 'jugador'
                
                # Crear cookies encriptadas (similar al ejemplo)
                response = make_response(redirect(url_for('dashboard')))
                id_usuario = str(jugador['id_jugador'])
                nombre_usuario = jugador.get('email', 'Jugador')  # Usar email como nombre si no hay nombre
                
                # Establecer cookies encriptadas con SHA256 (como en el ejemplo)
                establecer_cookie_encriptada(response, 'id_usuario', id_usuario)
                establecer_cookie_encriptada(response, 'nombre_usuario', nombre_usuario)
                
                return response

            flash("Correo o contraseña incorrectos. Intenta nuevamente.", "danger")
            return render_template('login.html')

        return render_template('login.html')

    
    @app.route('/registrarusuario', methods = ['POST'])
    def registrarusuario():
        correo = request.form['email']
        password = request.form['password']
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']

        response = registrar_docente(correo, password, nombres, apellidos)

        if "exitosamente" in response:
            flash(response, "success")  
            return redirect(url_for('login'))

        flash(response, "danger")  
        return render_template('registro.html')

    @app.route('/login_facial', methods=['POST'])
    def login_facial():
        try:
            data = request.get_json()
            rostro_data = data.get('rostro')

            if not rostro_data:
                return jsonify({
                    'success': False,
                    'message': 'No se proporcionaron datos faciales'
                }), 400

            docente = validar_docente_facial(rostro_data)
            if docente:
                session['docente_id'] = docente['id_docente']
                session['nombres'] = docente['nombres']
                session['apellidos'] = docente.get('apellidos', '')
                session['correo'] = docente['correo']
                session['tipo_usuario'] = 'docente'

                response = make_response(jsonify({
                    'success': True,
                    'message': 'Login exitoso',
                    'redirect': url_for('dashboard')
                }))

                establecer_cookie_encriptada(response, 'id_usuario', str(docente['id_docente']))
                establecer_cookie_encriptada(response, 'nombre_usuario', docente['nombres'])

                return response

            jugador = validar_jugador_facial(rostro_data)
            if jugador:
                session['jugador_id'] = jugador['id_jugador']
                session['email'] = jugador['email']
                session['tipo_usuario'] = 'jugador'

                response = make_response(jsonify({
                    'success': True,
                    'message': 'Login exitoso',
                    'redirect': url_for('dashboard')
                }))

                establecer_cookie_encriptada(response, 'id_usuario', str(jugador['id_jugador']))
                establecer_cookie_encriptada(response, 'nombre_usuario', jugador.get('email', 'Jugador'))

                return response

            return jsonify({
                'success': False,
                'message': 'Rostro no reconocido. No se encontró una coincidencia con los usuarios registrados. Por favor, intenta nuevamente o usa tu correo y contraseña.'
            }), 401

        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Error interno del servidor'
            }), 500
    