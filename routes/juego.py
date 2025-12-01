from flask import render_template, request, session
from flask_socketio import emit, join_room
import time
import json
import threading

from controladores import cuestionario
from controladores import respuestas
from controladores import respuestas_grupo
from controladores import grupo as ctrl_grupo
from conexion import conectarbd

estados_juego = {}

def registrar_rutas(app, socketio):
    @app.route('/preguntas')
    def preguntas():
        return render_template('/preguntas.html')

    @app.route('/prueba/<int:id_form>')
    def prueba(id_form):
        session['datos_sala'] = {'id_sala': id_form, 'tipo': 'EST'}
        session['id_cuestionario'] = id_form
        session['id_sala'] = id_form  # Asegura que las respuestas sepan a qué sala pertenecen
        
        # Verificar si el jugador está en un grupo
        id_jugador_cuestionario = session.get('id_jugador_cuestionario')
        grupo_info = None
        if id_jugador_cuestionario:
            grupo_info = ctrl_grupo.obtener_grupo_usuario(id_jugador_cuestionario, id_form)
        
        return render_template('/juego/prueba.html', 
                             id_cuestionario=id_form,
                             grupo_info=grupo_info)
    
    @app.route('/iniciar_juego/', methods=['POST'])
    def iniciar_juego():
        id_form = request.form['id_cuestionario']
        datos_fmr = cuestionario.retornar_dartosformuario(id_form)
        data = cuestionario.datos_cuestionario(id_form)
        session['id_sala'] = id_form
        return render_template('/juego/principal.html', datos_frm=datos_fmr, data=data, id_cuestionario=id_form)
    
    def procesar_alternativas(alternativas):
        """Procesa alternativas y las convierte a JSON string"""
        if not alternativas:
            return None
        if isinstance(alternativas, list):
            return json.dumps(alternativas)
        elif isinstance(alternativas, str):
            try:
                alternativas_lista = json.loads(alternativas)
                return json.dumps(alternativas_lista)
            except Exception:
                return None
        else:
            return json.dumps(alternativas)

    @socketio.on('unirme_sala')
    def unirme_sala(data):
        sala = str(data['sala'])
        join_room(sala)
        
        # Si es un jugador, también unirse a su sala personal para recibir actualizaciones de grupo
        id_jugador_cuestionario = session.get('id_jugador_cuestionario')
        if id_jugador_cuestionario:
            join_room(f"jugador_{id_jugador_cuestionario}")
        
        try:
            id_cuestionario = int(sala)
            participantes = cuestionario.obtener_participantes(id_cuestionario)
            socketio.emit('actualizar_participantes', {'participantes': participantes}, room=sala)
        except (ValueError, Exception):
            socketio.emit('actualizar_participantes', {'participantes': []}, room=sala)
        
        emit('configuracion', '', room=sala)
        
        if sala in estados_juego:
            estado = estados_juego[sala]
            if estado.get('activo') and estado.get('indice_actual') is not None and estado['indice_actual'] >= 0:
                if estado['indice_actual'] < len(estado['preguntas']):
                    pregunta_actual = estado['preguntas'][estado['indice_actual']]
                    
                    datos = {
                        'pregunta': pregunta_actual.get('pregunta'),
                        'puntaje': pregunta_actual.get('puntaje'),
                        'tiempo_respuesta': pregunta_actual.get('tiempo_respuesta'),
                        'id_pregunta': pregunta_actual.get('id_pregunta'),
                        'numero_pregunta': estado['indice_actual'] + 1,
                        'total_preguntas': len(estado['preguntas'])
                    }
                    
                    emit('datos_cuestionario', datos)
                    
                    def enviar_alternativas_nuevo_jugador():
                        time.sleep(0.1)
                        alternativas_json = procesar_alternativas(pregunta_actual.get('alternativas'))
                        if alternativas_json:
                            emit('respuesta_cuestionario', alternativas_json)
                    
                    threading.Thread(target=enviar_alternativas_nuevo_jugador, daemon=True).start()
    
    @socketio.on('solicitar_participantes')
    def solicitar_participantes(data):
        sala = str(data.get('sala', ''))
        if not sala:
            return
        
        try:
            id_cuestionario = int(sala)
            participantes = cuestionario.obtener_participantes(id_cuestionario)
            emit('actualizar_participantes', {'participantes': participantes})
        except (ValueError, Exception):
            emit('actualizar_participantes', {'participantes': []})

    @socketio.on('enviar_temporizador')
    def enviar_temporizador(data):
        pass

    @socketio.on('juego')
    def mostrar_alternativas(data):
        sala = str(data['sala'])
        emit('alternativas', data, room=sala)

    def procesar_preguntas(datos_cuestionario):
        """Procesa las preguntas y normaliza las alternativas"""
        preguntas_procesadas = []
        for pregunta in datos_cuestionario:
            alternativas_str = pregunta.get('alternativas')
            if alternativas_str:
                try:
                    if isinstance(alternativas_str, str):
                        pregunta['alternativas'] = json.loads(alternativas_str)
                    else:
                        pregunta['alternativas'] = alternativas_str
                except Exception:
                    pregunta['alternativas'] = []
            preguntas_procesadas.append(pregunta)
        return preguntas_procesadas

    def crear_timer_pregunta(id_sala, estado, datos_pregunta, tiempo_respuesta):
        """Crea un thread para el temporizador de una pregunta"""
        def timer_thread():
            tiempo_restante = tiempo_respuesta
            socketio.emit('actualiza_tiempocuestionario', {'tiempo': tiempo_restante}, room=str(id_sala))
            
            while tiempo_restante > 0 and estado['indice_actual'] == datos_pregunta['numero_pregunta'] - 1:
                time.sleep(1)
                tiempo_restante -= 1
                socketio.emit('actualiza_tiempocuestionario', {'tiempo': tiempo_restante}, room=str(id_sala))
            
            if tiempo_restante == 0 and estado['indice_actual'] == datos_pregunta['numero_pregunta'] - 1:
                socketio.emit('actualiza_tiempocuestionario', {'tiempo': 0}, room=str(id_sala))
                estado['respuesta_bloqueada'] = True
                socketio.emit('estado_respuestas', {
                    'bloqueada': True,
                    'id_pregunta': estado['id_pregunta_activa']
                }, room=str(id_sala))
                
                time.sleep(1.5)
                
                id_cuestionario_estadisticas = int(id_sala) if isinstance(id_sala, str) else id_sala
                estadisticas = respuestas.obtener_estadisticas_respuestas(
                    datos_pregunta['id_pregunta'],
                    id_cuestionario_estadisticas
                )
                socketio.emit('tiempo_agotado', {
                    'numero_pregunta': datos_pregunta['numero_pregunta'],
                    'estadisticas': estadisticas
                }, room=str(id_sala))
        
        return timer_thread

    def enviar_pregunta(id_sala, estado, pregunta_data, indice):
        """Envía una pregunta a la sala"""
        datos = {
            'pregunta': pregunta_data.get('pregunta'),
            'puntaje': pregunta_data.get('puntaje'),
            'tiempo_respuesta': pregunta_data.get('tiempo_respuesta'),
            'id_pregunta': pregunta_data.get('id_pregunta'),
            'numero_pregunta': indice + 1,
            'total_preguntas': len(estado['preguntas'])
        }
        
        socketio.emit('datos_cuestionario', datos, room=str(id_sala))
        
        estado['id_pregunta_activa'] = pregunta_data.get('id_pregunta')
        estado['respuesta_bloqueada'] = False
        socketio.emit('estado_respuestas', {
            'bloqueada': False,
            'id_pregunta': estado['id_pregunta_activa']
        }, room=str(id_sala))
        
        def enviar_alternativas():
            time.sleep(0.1)
            alternativas_json = procesar_alternativas(pregunta_data.get('alternativas'))
            if alternativas_json:
                socketio.emit('respuesta_cuestionario', alternativas_json, room=str(id_sala))
        
        threading.Thread(target=enviar_alternativas, daemon=True).start()
        
        timer_thread = crear_timer_pregunta(id_sala, estado, datos, pregunta_data.get('tiempo_respuesta'))
        threading.Thread(target=timer_thread, daemon=True).start()
        
        socketio.emit('pregunta_mostrada', {
            'numero_pregunta': datos['numero_pregunta'],
            'total_preguntas': datos['total_preguntas']
        }, room=str(id_sala))
        
        return datos

    @socketio.on('iniciar_juego')
    def iniciar_juego(data):
        id_sala = session['id_sala']
        tiempo = data.get('tiempo')
        datos_cuestionario = cuestionario.datos_cuestionario(id_sala)
        
        preguntas_procesadas = procesar_preguntas(datos_cuestionario)
        
        estados_juego[id_sala] = {
            'preguntas': preguntas_procesadas,
            'indice_actual': -1,
            'activo': False,
            'tiempo_inicial': tiempo,
            'id_pregunta_activa': None,
            'respuesta_bloqueada': True
        }
        
        tiempo_restante = tiempo
        while tiempo_restante > 0:
            time.sleep(1)
            tiempo_restante -= 1
            socketio.emit('actualizar_tiempoAD', {'tiempo': tiempo_restante}, room=str(id_sala))
            socketio.emit('actualizar_tiempoUS', {'tiempo': tiempo_restante}, room=str(id_sala))
        
        socketio.emit('actualizar_tiempoAD', {'tiempo': 0}, room=str(id_sala))
        socketio.emit('actualizar_tiempoUS', {'tiempo': 0}, room=str(id_sala))
        
        cuestionario.actualizar_estado_juego(id_sala, 'IN')
        estados_juego[id_sala]['activo'] = True
        
        socketio.emit('juego_iniciado', {
            'total_preguntas': len(preguntas_procesadas),
            'mensaje': 'Temporizador inicial completado. Iniciando primera pregunta...'
        }, room=str(id_sala))
        
        def iniciar_primera_pregunta():
            time.sleep(2.0)
            estado = estados_juego.get(id_sala)
            if estado and estado['activo']:
                estado['indice_actual'] = 0
                if estado['indice_actual'] < len(estado['preguntas']):
                    pregunta_actual = estado['preguntas'][estado['indice_actual']]
                    enviar_pregunta(id_sala, estado, pregunta_actual, estado['indice_actual'])
        
        threading.Thread(target=iniciar_primera_pregunta, daemon=True).start()

    def finalizar_cuestionario_automatico(id_sala):
        """Función auxiliar para finalizar el cuestionario automáticamente"""
        if not id_sala or id_sala not in estados_juego:
            return
        
        cuestionario.actualizar_estado_juego(id_sala, 'FN')
        estados_juego[id_sala]['activo'] = False
        
        # Otorgar recompensas automáticamente a todos los jugadores según su posición
        from controladores import recompensa
        recompensa.otorgar_recompensas_automaticas(id_sala)
        
        socketio.emit('pantalla_finalizada', room=str(id_sala))
        
        def limpiar_estado():
            time.sleep(60)
            if id_sala in estados_juego:
                del estados_juego[id_sala]
        
        threading.Thread(target=limpiar_estado, daemon=True).start()

    @socketio.on('siguiente_pregunta')
    def siguiente_pregunta(data=None):
        id_sala = session.get('id_sala')
        
        if not id_sala or id_sala not in estados_juego:
            emit('error_control', {'mensaje': 'No se encontró el juego activo.'})
            return
        
        estado = estados_juego[id_sala]
        estado['indice_actual'] += 1
        
        if estado['indice_actual'] >= len(estado['preguntas']):
            # No hay más preguntas, finalizar automáticamente
            emit('sin_mas_preguntas', {'mensaje': 'No hay más preguntas disponibles. Finalizando cuestionario...'})
            # Finalizar automáticamente después de un breve delay
            def finalizar_con_delay():
                time.sleep(1)
                finalizar_cuestionario_automatico(id_sala)
            threading.Thread(target=finalizar_con_delay, daemon=True).start()
            return
        
        pregunta_actual = estado['preguntas'][estado['indice_actual']]
        enviar_pregunta(id_sala, estado, pregunta_actual, estado['indice_actual'])

    @socketio.on('finalizar_cuestionario')
    def finalizar_cuestionario(data=None):
        id_sala = session.get('id_sala')
        
        if not id_sala or id_sala not in estados_juego:
            emit('error_control', {'mensaje': 'No se encontró el juego activo.'})
            return
        
        # Finalizar cuestionario (esto también otorgará recompensas automáticamente)
        finalizar_cuestionario_automatico(id_sala)

    @socketio.on('enviar_respuesta')
    def recibir_respuesta(data):
        import logging
        logger = logging.getLogger(__name__)
        
        id_pregunta = data.get('id_pregunta')
        id_alternativa = data.get('id_alternativa')
        tiempo_utilizado = data.get('tiempo_utilizado', 0)
        
        id_jugador_cuestionario = session.get('id_jugador_cuestionario')
        id_sala = session.get('id_sala') or data.get('sala') or session.get('id_cuestionario')
        if id_sala is not None:
            id_sala = str(id_sala)
        
        logger.info(f"Recibiendo respuesta - jugador_cuestionario={id_jugador_cuestionario}, pregunta={id_pregunta}, alternativa={id_alternativa}, tiempo={tiempo_utilizado}, sala={id_sala}")
        
        if not id_jugador_cuestionario:
            logger.warning("No se encontró id_jugador_cuestionario en la sesión")
            emit('error_respuesta', {'mensaje': 'No se encontró tu sesión. Por favor, vuelve a ingresar el PIN.'})
            return
        
        if not id_sala or id_sala not in estados_juego:
            logger.warning(f"No se encontró el juego activo para sala {id_sala}")
            emit('error_respuesta', {'mensaje': 'No se encontró el juego activo.'})
            return

        estado = estados_juego[id_sala]

        if estado.get('respuesta_bloqueada'):
            logger.warning("Respuesta bloqueada - tiempo agotado")
            emit('respuesta_rechazada', {'mensaje': 'El tiempo de la pregunta ha finalizado.'})
            return

        if estado.get('id_pregunta_activa') != id_pregunta:
            logger.warning(f"Pregunta no coincide: activa={estado.get('id_pregunta_activa')}, recibida={id_pregunta}")
            emit('respuesta_rechazada', {'mensaje': 'La pregunta ya no está disponible.'})
            return

        try:
            # Verificar si el jugador está en un grupo
            conexion_db = conectarbd()
            id_grupo = None
            metodo_evaluacion = None
            if conexion_db:
                try:
                    with conexion_db.cursor() as cursor:
                        cursor.execute("""
                            SELECT g.id_grupo, g.metodo_evaluacion
                            FROM Grupo g
                            INNER JOIN GrupoMiembro gm ON g.id_grupo = gm.id_grupo
                            WHERE gm.id_jugador_cuestionario = %s AND g.id_cuestionario = %s AND g.estado = 'A'
                        """, (id_jugador_cuestionario, int(id_sala)))
                        grupo_data = cursor.fetchone()
                        if grupo_data:
                            id_grupo = grupo_data['id_grupo']
                            metodo_evaluacion = grupo_data['metodo_evaluacion']
                finally:
                    conexion_db.close()
            
            if id_grupo:
                # Es un cuestionario grupal - registrar votación del miembro
                try:
                    id_jugador_cuestionario = int(id_jugador_cuestionario)
                    id_pregunta = int(id_pregunta)
                    id_alternativa = int(id_alternativa)
                except (ValueError, TypeError) as e:
                    logger.error(f"Error al convertir valores a enteros: {e}")
                    emit('error_respuesta', {'mensaje': 'Error en los datos de la respuesta.'})
                    return
                
                # Registrar la votación del miembro
                respuestas_grupo.registrar_votacion_miembro(id_grupo, id_pregunta, id_jugador_cuestionario, id_alternativa)
                
                # Determinar si ya se puede establecer la respuesta final del grupo
                respuesta_final = respuestas_grupo.determinar_respuesta_grupo(id_grupo, id_pregunta, metodo_evaluacion)
                
                if respuesta_final:
                    # Ya se determinó la respuesta final - registrar la respuesta del grupo
                    puntos_obtenidos = respuestas_grupo.registrar_respuesta_grupo(id_grupo, id_pregunta, respuesta_final, tiempo_utilizado)
                    
                    # Emitir a todos los miembros del grupo que la respuesta fue registrada
                    conexion_db = conectarbd()
                    if conexion_db:
                        try:
                            with conexion_db.cursor() as cursor:
                                cursor.execute("""
                                    SELECT id_jugador_cuestionario FROM GrupoMiembro
                                    WHERE id_grupo = %s
                                """, (id_grupo,))
                                miembros = cursor.fetchall()
                                for miembro in miembros:
                                    socketio.emit('respuesta_grupo_registrada', {
                                        'puntos': puntos_obtenidos,
                                        'id_alternativa': respuesta_final
                                    }, room=f"jugador_{miembro['id_jugador_cuestionario']}")
                        finally:
                            conexion_db.close()
                else:
                    # Aún no se puede determinar - esperar más votaciones
                    emit('votacion_registrada', {
                        'mensaje': 'Tu votación ha sido registrada. Esperando a los demás miembros del grupo...'
                    })
                
                # Actualizar votaciones en tiempo real para todos los miembros
                votaciones = respuestas_grupo.obtener_votaciones_grupo(id_grupo, id_pregunta)
                conexion_db = conectarbd()
                if conexion_db:
                    try:
                        with conexion_db.cursor() as cursor:
                            cursor.execute("""
                                SELECT id_jugador_cuestionario FROM GrupoMiembro
                                WHERE id_grupo = %s
                            """, (id_grupo,))
                            miembros = cursor.fetchall()
                            for miembro in miembros:
                                socketio.emit('actualizar_votaciones', {
                                    'votaciones': votaciones
                                }, room=f"jugador_{miembro['id_jugador_cuestionario']}")
                    finally:
                        conexion_db.close()
            else:
                # Es un cuestionario individual - comportamiento normal
                if id_alternativa:
                    try:
                        id_jugador_cuestionario = int(id_jugador_cuestionario)
                        id_pregunta = int(id_pregunta)
                        id_alternativa = int(id_alternativa)
                    except (ValueError, TypeError) as e:
                        logger.error(f"Error al convertir valores a enteros: {e}")
                        emit('error_respuesta', {'mensaje': 'Error en los datos de la respuesta.'})
                        return
                    
                    logger.info(f"Llamando a registrar_respuesta con: jugador_cuestionario={id_jugador_cuestionario}, pregunta={id_pregunta}, alternativa={id_alternativa}, tiempo={tiempo_utilizado}")
                    puntos_obtenidos = respuestas.registrar_respuesta(id_jugador_cuestionario, id_pregunta, id_alternativa, tiempo_utilizado)
                    logger.info(f"Puntos obtenidos: {puntos_obtenidos}")
                    
                    conexion_db = conectarbd()
                    puntaje_total = 0
                    if conexion_db:
                        try:
                            with conexion_db.cursor() as cursor:
                                cursor.execute("""
                                    SELECT puntaje FROM Jugador_Cuestionario WHERE id_jugador_cuestionario = %s
                                """, (id_jugador_cuestionario,))
                                resultado = cursor.fetchone()
                                if resultado:
                                    puntaje_total = float(resultado.get('puntaje', 0) or 0)
                        finally:
                            conexion_db.close()
                    
                    emit('respuesta_registrada', {
                        'puntos': puntos_obtenidos,
                        'puntaje_total': round(puntaje_total, 2)
                    })
                    
                    def actualizar_marcador_docente():
                        time.sleep(0.5)
                        try:
                            id_cuestionario = int(id_sala) if isinstance(id_sala, str) else id_sala
                            participantes = cuestionario.obtener_participantes(id_cuestionario)
                            socketio.emit('actualizar_participantes', {
                                'participantes': participantes
                            }, room=str(id_sala))
                        except Exception:
                            pass
                    
                    threading.Thread(target=actualizar_marcador_docente, daemon=True).start()
                else:
                    emit('respuesta_registrada', {'puntos': 0, 'puntaje_total': 0})
        except Exception as e:
            logger.error(f"Error al procesar respuesta: {e}")
            import traceback
            traceback.print_exc()
            emit('error_respuesta', {'mensaje': f'Error al registrar tu respuesta: {str(e)}'})
