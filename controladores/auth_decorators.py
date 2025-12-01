"""
Decoradores para control de acceso a rutas según autenticación
Similar al ejemplo: verifica session y cookies
"""
from functools import wraps
from flask import redirect, url_for, flash, session, request, render_template
from controladores.cookies_utils import obtener_cookie_encriptada

def requiere_login(f):
    """
    Decorador que requiere que el usuario esté autenticado (docente o jugador)
    Similar al ejemplo: if 'username' in session
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificar sesión (similar al ejemplo)
        tiene_docente = 'docente_id' in session
        tiene_jugador = 'jugador_id' in session
        
        # Verificar cookies encriptadas como respaldo (solo verificar existencia)
        id_usuario_cookie = obtener_cookie_encriptada(request, 'id_usuario')
        nombre_usuario_cookie = obtener_cookie_encriptada(request, 'nombre_usuario')
        
        if not tiene_docente and not tiene_jugador:
            # Si no hay sesión, verificar si hay cookies
            if not (id_usuario_cookie and nombre_usuario_cookie):
                detalle = ['🔐 Debes iniciar sesión para acceder a esta página', '🔄 Intenta acceder desde el inicio', '📞 Si el problema persiste, contacta al soporte.']
                lista_mensaje = ['Acceso Restringido', 'Esta página requiere autenticación', detalle]
                mensaje = {
                    'mensaje': lista_mensaje, 
                    'ruta_foto': 'static/uploads/404_error.svg', 
                    'titulo': 'Acceso Restringido', 
                    'icono': 'static/uploads/errores.png'
                }
                return render_template('/Fallas/maestra_error.html', mensaje=mensaje)
            else:
                # Hay cookies pero no sesión, redirigir a login para reautenticar
                detalle = ['⏰ Tu sesión ha expirado', '🔄 Por favor, inicia sesión nuevamente', '📞 Si el problema persiste, contacta al soporte.']
                lista_mensaje = ['Sesión Expirada', 'Tu sesión ha caducado', detalle]
                mensaje = {
                    'mensaje': lista_mensaje, 
                    'ruta_foto': 'static/uploads/404_error.svg', 
                    'titulo': 'Sesión Expirada', 
                    'icono': 'static/uploads/errores.png'
                }
                return render_template('/Fallas/maestra_error.html', mensaje=mensaje)
        
        return f(*args, **kwargs)
    return decorated_function

def requiere_docente(f):
    """
    Decorador que requiere que el usuario sea un docente autenticado
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificar sesión
        tiene_docente = 'docente_id' in session
        
        # Verificar cookies encriptadas como respaldo
        id_usuario_cookie = obtener_cookie_encriptada(request, 'id_usuario')
        nombre_usuario_cookie = obtener_cookie_encriptada(request, 'nombre_usuario')
        
        if not tiene_docente and not (id_usuario_cookie and nombre_usuario_cookie):
            detalle = ['👨‍🏫 Solo los docentes pueden acceder a esta página', '🔄 Intenta acceder desde el inicio', '📞 Si el problema persiste, contacta al soporte.']
            lista_mensaje = ['Acceso Restringido', 'Esta página es exclusiva para docentes', detalle]
            mensaje = {
                'mensaje': lista_mensaje, 
                'ruta_foto': 'static/uploads/404_error.svg', 
                'titulo': 'Acceso Restringido', 
                'icono': 'static/uploads/errores.png'
            }
            return render_template('/Fallas/maestra_error.html', mensaje=mensaje)
        
        return f(*args, **kwargs)
    return decorated_function

def requiere_jugador(f):
    """
    Decorador que requiere que el usuario sea un jugador autenticado
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificar sesión
        tiene_jugador = 'jugador_id' in session
        
        # Verificar cookies encriptadas como respaldo (solo verificar existencia)
        id_usuario_cookie = obtener_cookie_encriptada(request, 'id_usuario')
        nombre_usuario_cookie = obtener_cookie_encriptada(request, 'nombre_usuario')
        
        if not tiene_jugador:
            # Si no hay sesión, verificar si hay cookies
            if not (id_usuario_cookie and nombre_usuario_cookie):
                detalle = ['🎮 Solo los jugadores pueden acceder a esta página', '🔄 Intenta acceder desde el inicio', '📞 Si el problema persiste, contacta al soporte.']
                lista_mensaje = ['Acceso Restringido', 'Esta página es exclusiva para jugadores', detalle]
                mensaje = {
                    'mensaje': lista_mensaje, 
                    'ruta_foto': 'static/uploads/404_error.svg', 
                    'titulo': 'Acceso Restringido', 
                    'icono': 'static/uploads/errores.png'
                }
                return render_template('/Fallas/maestra_error.html', mensaje=mensaje)
            else:
                # Hay cookies pero no sesión, redirigir a login para reautenticar
                detalle = ['⏰ Tu sesión ha expirado', '🔄 Por favor, inicia sesión nuevamente', '📞 Si el problema persiste, contacta al soporte.']
                lista_mensaje = ['Sesión Expirada', 'Tu sesión ha caducado', detalle]
                mensaje = {
                    'mensaje': lista_mensaje, 
                    'ruta_foto': 'static/uploads/404_error.svg', 
                    'titulo': 'Sesión Expirada', 
                    'icono': 'static/uploads/errores.png'
                }
                return render_template('/Fallas/maestra_error.html', mensaje=mensaje)
        
        return f(*args, **kwargs)
    return decorated_function

