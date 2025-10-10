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
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html', error="Credenciales incorrectas")

        return render_template('login.html')
    
    @app.route('/registrarusuario', methods = ['POST'])
    def registrarusuario():
        correo = request.form['email']
        password = request.form['password']
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']

        # Llamar al controlador para registrar al docente
        response = registrar_docente(correo, password, nombres, apellidos)

        # Si el registro es exitoso, redirigir al login
        if "exitosamente" in response:
            flash(response, "success")  # Mostrar mensaje flash de éxito
            return redirect(url_for('login'))  # Redirigir al login

        flash(response, "danger")  # Mostrar mensaje flash de error
        return render_template('registro.html') 
    