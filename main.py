from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from flask_socketio import SocketIO, emit
import conexion 
import routes.login as login_routes
import routes.repositorios as repositorio_routes
import routes.cuestionario as cuestionario_routes 
import routes.registro as registro_routes
import routes.recuperacion as recuperacion_routes
import routes.juego as rjuego
import routes.juegoo as juego

import routes.resultados as resultados_routes



app = Flask(__name__)
app.secret_key = 'chui_angel_grupo_web' 
socketio = SocketIO(app, cors_allowed_origins="*") 

@app.route('/')
@app.route('/index')
def home():
    return render_template('pin_estudiante.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('registro.html')

# @app.route('/dashboard')
# def dashboard():
#     if 'docente_id' not in session:
#         return redirect(url_for('login'))  
#     return render_template('dashboard.html', id_docente=session['docente_id'])

@app.route('/dashboard')
def dashboard():
    id_docente = session.get('docente_id')
    nombres = session.get('nombres')

    # Renderiza igual, pero pasando si hay sesión o no
    return render_template('dashboard.html', id_docente=id_docente, nombres=nombres)


# @app.route('/logout')
# def logout():    
#     session.clear()  
#     flash("Has cerrado sesión exitosamente", "success")  
#     return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('dashboard'))


@app.route('/nuevo_cuestionario')
def nuevo_cuestionario():    
    return render_template('crear_cuestionarios.html')

@app.route('/repositorio')
def repositorio():    
    return render_template('repositorio.html')

@app.route('/perfil')
def perfil():    
    return render_template('perfil.html')

@app.route('/estadisticas')
def estadisticas():    
    return render_template('estadistica.html')

@app.route('/recuperar_contra')
def recuperar_contra():    
    return render_template('/recuperacion/recuperar_contrasena.html')

@app.route("/nueva_contrasena", methods=["GET"])
def nueva_contrasena_page():
    return render_template("recuperacion/nueva_contrasena.html")


login_routes.registrar_rutas(app)
repositorio_routes.registrar_rutas(app)
cuestionario_routes.registrar_rutas(app)
registro_routes.registrar_rutas(app)
recuperacion_routes.registrar_rutas_recuperacion(app)
rjuego.registrar_rutas(app,socketio)
juego.registrar_rutas(app,socketio)

resultados_routes.registrar_rutas_resultados(app)




@app.route('/errorsistema')
def errorsistema():
    opcion = 1
    if opcion == 1:
        detalle = ['🔌 Verifica tu conexión a internet', '🔄 Intenta recargar la página','📞 Si el problema persiste, contacta al soporte.' ]
        lista_mensaje = ['Error de Conexión', 'El servicio de BD no esta disponible',detalle ]
        mensaje = {'mensaje': lista_mensaje, 'ruta_foto' : 'static/uploads/404_error.svg', 'titulo' : 'Error de conexión', 'icono': 'static/uploads/errores.png'}
    else:
        mensaje = {'mensaje': 'La tabla usuarios no esta dispobible', 'ruta_foto' : ''}
    return render_template('/Fallas/maestra_error.html', mensaje = mensaje) 

if __name__ == "__main__":
    app.debug = True  
    app.run(debug=True)