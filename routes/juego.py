from flask import render_template, request, redirect, session, url_for, flash
from flask_socketio import SocketIO, emit, join_room

from  controladores  import cuestionario
def registrar_rutas(app, socketio):
    @app.route('/prueba/<int:id_form>')
    def prueba(id_form):
        session['datos_sala'] = {'id_sala' : id_form, 'tipo': 'EST'}
        return render_template('/juego/prueba.html')
    
    @app.route('/iniciar_juego/', methods = ['POST'])
    def iniciar_juego():
        id_form = request.form['id_cuestionario']
        #verificamos que ese formulario le pertenezca a ese docente
        datos_fmr = cuestionario.retornar_dartosformuario(id_form)
        data = cuestionario.datos_cuestionario(id_form)
        session['datos_sala'] = {'id_sala' : id_form, 'tipo': 'ADM'}
        return render_template('/juego/principal.html', datos_frm=datos_fmr, data=data)
    
    @socketio.on('unirme_sala')
    def unirme_sala(data):
        # si es admi administrador sino usuario
        #sala = session['datos_sala'].get('id_sala')
        sala = str(data['sala'])  # recibida desde JS
        join_room(sala)
        print('alguien se unio a sala', sala)
        emit('configuracion', '', room=sala)

    @socketio.on('enviar_temporizador')
    def enviar_temporizador(data):
        sala = str(data['sala']) 
        tiempo = data.get('tiempo')
        print("Tiempo ejecutandose ....", tiempo)
        emit('tiempo', {'tiempo': tiempo}, room=sala)

    @socketio.on('juego')
    def mostrar_aternativas(data):
        sala = str(data['sala'])
        emit('alternativas', data , room = sala)

    
