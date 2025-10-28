from flask import render_template, request, redirect, session, url_for, flash
from flask_socketio import SocketIO, emit, join_room
import time

from  controladores  import cuestionario
def registrar_rutas(app, socketio):
    @app.route('/preguntas')
    def preguntas():
        return render_template('/preguntas.html')



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
        session['id_sala'] =id_form
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
        tiempo = data.get('tiempo')

    @socketio.on('juego')
    def mostrar_aternativas(data):
        sala = str(data['sala'])
        emit('alternativas', data , room = sala)


    @socketio.on('iniciar_juego')
    def iniciar_juego(data):
        id_sala = session['id_sala']
        tiempo = data.get('tiempo')
        print(id_sala, tiempo)
        daa = cuestionario.datos_cuestionario(id_sala)
        print(daa)
        while tiempo> 0:
            time.sleep(1)
            tiempo-=1
            print("tiempo", tiempo)
            socketio.emit('actualizar_tiempoAD', {'tiempo': tiempo})
            socketio.emit('actualizar_tiempoUS', {'tiempo': tiempo})
        cuestionario.actualizar_estado_juego(id_sala, 'IN')

        #mostrar las preguntas, puntos, tiempo
        for dt in daa:
            print("preguintas" , dt)
            tiempo = dt.get('tiempo_respuesta')
            datos =  {
                'pregunta': dt.get('pregunta'), 
                'puntaje' : dt.get('puntaje'),
                'tiempo_respuesta': tiempo,
                'id_pregunta':dt.get('id_pregunta')
            }
            
            print(datos) 
            socketio.emit('datos_cuestionario', datos)
            socketio.emit('respuesta_cuestionario', dt.get('alternativas'))
            while tiempo>0:
                time.sleep(1)
                tiempo-=1
                print("tiempo", tiempo)
                socketio.emit('actualiza_tiempocuestionario', {'tiempo': tiempo})
        cuestionario.actualizar_estado_juego(id_sala, 'FN')
        socketio.emit('pantalla_finalizada')
        ##actualizo su tiempo
        emit('alternativas')


    
