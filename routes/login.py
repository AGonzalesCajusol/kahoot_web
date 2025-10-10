from flask import render_template, request, redirect, url_for
from controladores.login import validar_docente

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
