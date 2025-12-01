from flask import Flask, flash, redirect, render_template, request, session, url_for, make_response, jsonify
from flask_socketio import SocketIO
from flask_jwt import JWT
from datetime import timedelta, datetime
from hashlib import sha256
import logging
import routes.login as login_routes
import routes.repositorios as repositorio_routes
import routes.cuestionario as cuestionario_routes
import routes.registro as registro_routes
import routes.recuperacion as recuperacion_routes
import routes.juego as rjuego
import routes.resultados as resultados_routes
import routes.grupo as grupo_routes
import routes.recompensa as recompensa_routes
import routes.api_todas_tablas as api_todas_tablas_routes
from controladores import jugador as jugador_ctrl
from controladores import docente as docente_ctrl
from controladores.auth_decorators import requiere_login, requiere_docente

app = Flask(__name__)
app.secret_key = 'chui_angel_grupo_web'
app.config['SECRET_KEY'] = 'chui_angel_grupo_web_clave_secreta'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=4)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Configurar SocketIO con threading adecuado para evitar problemas con PyMySQL
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading', logger=True, engineio_logger=True)

# Clase User para JWT
class User(object):
    def __init__(self, id, email, password, tipo_usuario):
        self.id = id
        self.email = email
        self.password = password
        self.tipo_usuario = tipo_usuario  # 'docente' o 'jugador'
    
    def __str__(self):
        return f"User(id='{self.id}', tipo='{self.tipo_usuario}')"


def encriptar_sha256(cadena):
    cadbytes = cadena.encode('utf-8')
    sha256_hash_object = sha256()
    sha256_hash_object.update(cadbytes)
    hex_digest = sha256_hash_object.hexdigest()
    return hex_digest

def authenticate(username, password):
    """
    Función de autenticación para JWT
    Flask-JWT pasa 'username' como primer parámetro
    En nuestro caso, 'username' es el correo del usuario
    """
    correo = username
    user = None
    
    docente = docente_ctrl.obtener_docente_por_email(correo)
    if docente:
        if isinstance(docente, dict):
            docente_id = docente.get('id_docente')
            docente_email = docente.get('correo')
            docente_password = docente.get('password')
        else:
            docente_id = docente[0] if len(docente) > 0 else None
            docente_email = docente[1] if len(docente) > 1 else None
            docente_password = docente[2] if len(docente) > 2 else None
        
        password_hash = encriptar_sha256(password)
        if docente_password and docente_password == password_hash:
            user = User(docente_id, docente_email, docente_password, 'docente')
    
    if not user:
        jugador = jugador_ctrl.obtener_jugador_por_email(correo)
        if jugador:
            if isinstance(jugador, dict):
                jugador_id = jugador.get('id_jugador')
                jugador_email = jugador.get('email')
                jugador_password = jugador.get('contraseña')
            else:
                jugador_id = jugador[0] if len(jugador) > 0 else None
                jugador_email = jugador[1] if len(jugador) > 1 else None
                jugador_password = jugador[2] if len(jugador) > 2 else None
            
            password_hash = encriptar_sha256(password)
            if jugador_password and jugador_password == password_hash:
                user = User(jugador_id, jugador_email, jugador_password, 'jugador')
    
    return user


def identity(payload):
    user_id = payload['identity']
    
    # Intentar primero como docente
    docente = docente_ctrl.obtener_docente_por_id(user_id)
    if docente:
        return User(docente['id_docente'], docente['correo'], docente['password'], 'docente')
    
    # Si no es docente, intentar como jugador
    jugador = jugador_ctrl.obtener_jugador_por_id(user_id)
    if jugador:
        return User(jugador['id_jugador'], jugador['email'], jugador['contraseña'], 'jugador')

    return None

# Configurar JWT
# Flask-JWT crea automáticamente la ruta /auth
# La función authenticate recibe 'username' y 'password' del JSON
jwt = JWT(app, authenticate, identity)

# Configurar sesión para que solo se cree la cookie cuando haya datos en la sesión
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'


@app.before_request
def before_request():
    """Evita que Flask guarde la sesión si está vacía"""
    # Verificar si hay datos relevantes en la sesión (excluyendo flashes)
    tiene_docente = session.get('docente_id') is not None
    tiene_jugador = session.get('jugador_id') is not None
    
    # Si no hay sesión activa, marcar como no modificada para evitar crear cookie
    if not tiene_docente and not tiene_jugador:
        # Forzar que la sesión no se modifique
        session.modified = False
        # También limpiar cualquier dato temporal que pueda causar que se guarde
        # Pero mantener los flashes si existen (se consumirán después)

@app.after_request
def after_request(response):
    """Elimina la cookie de sesión si la sesión está vacía"""
    # Verificar si la sesión tiene datos relevantes (solo docente_id o jugador_id)
    tiene_docente = session.get('docente_id') is not None
    tiene_jugador = session.get('jugador_id') is not None
    
    # Si no hay sesión activa, eliminar la cookie de sesión siempre
    # Esto se ejecuta después de cada request, así que eliminará la cookie
    # incluso si Flask la creó automáticamente para flashes u otros datos temporales
    if not tiene_docente and not tiene_jugador:
        # Eliminar la cookie de sesión de manera agresiva
        # Usar max_age=0 para asegurar eliminación inmediata
        response.set_cookie(
            'session', 
            '', 
            max_age=0,  # Eliminar inmediatamente
            path='/', 
            httponly=True, 
            samesite='Lax',
            secure=False  # Cambiar a True si usas HTTPS en producción
        )
    
    return response

@app.context_processor
def inject_current_year():
    """Inyecta current_year en todos los templates"""
    return dict(current_year=datetime.now().year)

@app.route('/')
@app.route('/index')
def home():
    # Si el usuario ya está logueado, redirigir a su dashboard
    if session.get('docente_id'):
        return redirect(url_for('dashboard'))
    elif session.get('jugador_id'):
        return redirect(url_for('dashboard'))
    # Si no está logueado, mostrar el index
    return render_template('index.html')

@app.route('/pin_estudiante')
def pin_estudiante():
    return render_template('pin_estudiante.html')

@app.route('/preguntas_frecuentes')
def preguntas_frecuentes():
    return render_template('preguntas_frecuentes.html')

@app.route('/guia_uso')
def guia_uso():
    return render_template('guia_uso.html')

@app.route('/plantillas')
def plantillas():
    return render_template('plantillas.html')

@app.route('/tutoriales')
def tutoriales():
    return render_template('tutoriales.html')

@app.route('/nuestro_equipo')
def nuestro_equipo():
    return render_template('nuestro_equipo.html')

@app.route('/sobre_nosotros')
def sobre_nosotros():
    return render_template('sobre_nosotros.html')

@app.route('/contactanos')
def contactanos():
    return render_template('contactanos.html')

@app.route('/soporte_tecnico')
def soporte_tecnico():
    return render_template('soporte_tecnico.html')

@app.route('/enviar_contacto', methods=['POST'])
def enviar_contacto():
    from controladores.correo_config import send_contact_email
    
    try:
        data = request.get_json()
        nombre = data.get('nombre', '').strip()
        correo = data.get('correo', '').strip()
        asunto = data.get('asunto', '').strip()
        mensaje = data.get('mensaje', '').strip()
        
        if not all([nombre, correo, asunto, mensaje]):
            return jsonify({
                'code': 0,
                'message': 'Por favor, completa todos los campos.'
            }), 400
        
        if send_contact_email(nombre, correo, asunto, mensaje):
            return jsonify({
                'code': 1,
                'message': 'Tu mensaje ha sido enviado correctamente. Te responderemos pronto.'
            }), 200
        else:
            return jsonify({
                'code': 0,
                'message': 'No se pudo enviar el mensaje. Por favor, intenta nuevamente más tarde.'
            }), 500
            
    except Exception as e:
        print(f"Error en enviar_contacto: {e}")
        return jsonify({
            'code': 0,
            'message': 'Ocurrió un error al procesar tu mensaje. Por favor, intenta nuevamente.'
        }), 500

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('registro.html')

@app.route('/register_jugador', methods=['GET', 'POST'])
def register_jugador():
    return render_template('registro_jugador.html')


@app.route('/dashboard')
@requiere_login
def dashboard():
    if 'docente_id' in session:
        nombres = session.get('nombres')
        return render_template('dashboard.html', tipo_usuario='docente', nombres=nombres)

    if 'jugador_id' in session:
        id_jugador = session.get('jugador_id')
        juegos = jugador_ctrl.obtener_cuestionarios_jugador(id_jugador)
        return render_template(
            'dashboard_jugador.html',
            tipo_usuario='jugador',
            email=session.get('email'),
            juegos=juegos
        )

    flash("Debes iniciar sesión para acceder al panel.", "warning")
    return redirect(url_for('login'))

@app.route('/mis_recompensas')
@requiere_login
def mis_recompensas():
    """Página para que el jugador vea sus recompensas"""
    if 'jugador_id' not in session:
        flash("Debes ser jugador para acceder a esta página.", "danger")
        return redirect(url_for('dashboard'))
    
    id_jugador = session.get('jugador_id')
    from controladores import recompensa
    puntos_recompensa = recompensa.obtener_total_puntos_jugador(id_jugador)
    recompensas = recompensa.obtener_recompensas_por_jugador(id_jugador)
    
    return render_template(
        'mis_recompensas.html',
        puntos_recompensa=puntos_recompensa,
        recompensas=recompensas
    )





@app.route('/logout')
def logout():
    session.clear()
    resp = make_response(redirect(url_for('home')))
    resp.set_cookie('id_usuario', '', expires=0)
    resp.set_cookie('nombre_usuario', '', expires=0)
    flash("Has cerrado sesión exitosamente", "success")
    return resp


@app.route('/nuevo_cuestionario')
@requiere_docente
def nuevo_cuestionario():
    return render_template('crear_cuestionarios.html')

@app.route('/repositorio')
@requiere_docente
def repositorio():
    return render_template('repositorio.html')

@app.route('/perfil')
@requiere_docente
def perfil():
    return render_template('perfil.html')

@app.route('/estadisticas')
@requiere_docente
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
cuestionario_routes.registrar_rutas(app, socketio)  # Pasar socketio para emitir eventos
registro_routes.registrar_rutas(app)
recuperacion_routes.registrar_rutas_recuperacion(app)
rjuego.registrar_rutas(app,socketio)

resultados_routes.registrar_rutas_resultados(app)
grupo_routes.registrar_rutas(app, socketio)
recompensa_routes.registrar_rutas_recompensa(app)
api_todas_tablas_routes.registrar_rutas_api(app)


@app.errorhandler(404)
def page_not_found(e):
    """Maneja rutas no encontradas (404)"""
    # Verificar si el usuario tiene sesión activa
    tiene_docente = session.get('docente_id') is not None
    tiene_jugador = session.get('jugador_id') is not None
    
    # Preparar mensaje de error
    if not tiene_docente and not tiene_jugador:
        detalle = ['🔐 Debes iniciar sesión para acceder a esta página', '🔄 Intenta acceder desde el inicio', '📞 Si el problema persiste, contacta al soporte.']
        lista_mensaje = ['Acceso Restringido', 'La página que buscas no existe o requiere autenticación', detalle]
    else:
        detalle = ['🔍 Verifica que la URL sea correcta', '🔄 Intenta volver al inicio', '📞 Si el problema persiste, contacta al soporte.']
        lista_mensaje = ['Página No Encontrada', 'La página que buscas no existe', detalle]
    
    mensaje = {
        'mensaje': lista_mensaje, 
        'ruta_foto': 'static/uploads/404_error.svg', 
        'titulo': 'Error 404', 
        'icono': 'static/uploads/errores.png'
    }
    return render_template('/Fallas/maestra_error.html', mensaje=mensaje)


@app.route('/errorsistema')
def errorsistema():
    detalle = [
        '🔌 Verifica tu conexión a internet',
        '🔄 Intenta recargar la página',
        '📞 Si el problema persiste, contacta al soporte.'
    ]
    lista_mensaje = [
        'Error de Conexión',
        'El servicio de BD no está disponible',
        detalle
    ]
    mensaje = {
        'mensaje': lista_mensaje,
        'ruta_foto': 'static/uploads/404_error.svg',
        'titulo': 'Error de conexión',
        'icono': 'static/uploads/errores.png'
    }
    return render_template('/Fallas/maestra_error.html', mensaje=mensaje) 

if __name__ == "__main__":
    app.debug = True
    app.run(debug=True)