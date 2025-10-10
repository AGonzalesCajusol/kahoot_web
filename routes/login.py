from flask import render_template, request, redirect, url_for, flash
from controladores.login import validar_docente 
from controladores import docente
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
        response = docente.registrardocente(correo, password, nombres, apellidos)
        print(response)
        if response == True:
            flash(response, "success")
            return render_template('login.html')
        flash(response, "danger")
        return render_template('registro.html')
        
