from flask import render_template, request, redirect, session, url_for, flash, jsonify
from controladores.login import validar_docente
from controladores.docente import registrar_docente 
from controladores.jugador import validar_jugador

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
                return redirect(url_for('dashboard'))

            jugador = validar_jugador(correo, password)
            if jugador:
                session['jugador_id'] = jugador['id_jugador']
                session['email'] = jugador['email']
                session['tipo_usuario'] = 'jugador'
                return redirect(url_for('dashboard'))

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
    def login_facial_route():
        data = request.get_json()
        image_base64 = data.get('image')

        if not image_base64:
            return jsonify({"success": False, "message": "Faltan datos."}), 400

        from controladores.login import login_facial
        resultado = login_facial(image_base64)

        if resultado['success']:
            return jsonify(resultado)
        else:
            return jsonify(resultado), 401    
    