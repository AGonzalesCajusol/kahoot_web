from flask import render_template, request, redirect, session, url_for, flash
from controladores.login import validar_docente
from controladores.docente import registrar_docente 

def registrar_rutas(app):
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            correo = request.form['email']
            password = request.form['password']

            docente = validar_docente(correo, password)

            if docente:
                # Guardar datos de sesión
                session['docente_id'] = docente['id_docente']
                session['nombres'] = docente['nombres']
                return redirect(url_for('dashboard'))
            else:
                flash("Correo o contraseña incorrectos. Intenta nuevamente.", "danger")
                return render_template('login.html', error="Credenciales incorrectas")

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
    
    