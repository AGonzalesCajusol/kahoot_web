from flask import render_template, request, jsonify, session, redirect, url_for, flash
from controladores import recompensa
from controladores.auth_decorators import requiere_docente, requiere_login

def registrar_rutas_recompensa(app):
    
    @app.route('/recompensa/<int:id_cuestionario>')
    def pagina_recompensa(id_cuestionario):
        """Página para que el participante reciba su recompensa"""
        id_jugador_cuestionario = session.get('id_jugador_cuestionario')
        
        if not id_jugador_cuestionario:
            flash("No tienes permiso para acceder a esta página. Debes estar en una sesión de juego activa.", "danger")
            return redirect(url_for('dashboard'))
        
        # Obtener información del jugador
        jugador_info = recompensa.obtener_info_jugador_cuestionario(id_jugador_cuestionario, id_cuestionario)
        if not jugador_info:
            flash("Jugador no encontrado.", "danger")
            return redirect(url_for('dashboard'))
        
        # Verificar si ya recibió recompensa
        ya_recibio = recompensa.verificar_recompensa_recibida(id_cuestionario, id_jugador_cuestionario)
        
        # Obtener posición del jugador
        posicion_info = recompensa.obtener_posicion_jugador(id_jugador_cuestionario, id_cuestionario)
        
        return render_template(
            'recompensa/recibir_recompensa.html',
            jugador=jugador_info,
            id_cuestionario=id_cuestionario,
            id_jugador_cuestionario=id_jugador_cuestionario,
            ya_recibio=ya_recibio,
            posicion=posicion_info
        )
    
    @app.route('/api/recibir_recompensa', methods=['POST'])
    def api_recibir_recompensa():
        """API para recibir la recompensa"""
        data = request.get_json()
        id_cuestionario = data.get('id_cuestionario')
        id_jugador_cuestionario = session.get('id_jugador_cuestionario')
        
        # Verificar sesión
        if not id_jugador_cuestionario:
            return jsonify({'success': False, 'message': 'No tienes permiso. Debes estar en una sesión de juego activa.'}), 403
        
        # Verificar si ya recibió recompensa
        if recompensa.verificar_recompensa_recibida(id_cuestionario, id_jugador_cuestionario):
            return jsonify({'success': False, 'message': 'Ya recibiste tu recompensa.'}), 400
        
        # Obtener información del jugador
        jugador_info = recompensa.obtener_info_jugador_cuestionario(id_jugador_cuestionario, id_cuestionario)
        if not jugador_info:
            return jsonify({'success': False, 'message': 'Jugador no encontrado.'}), 404
        
        # Obtener posición y calcular recompensa
        posicion_info = recompensa.obtener_posicion_jugador(id_jugador_cuestionario, id_cuestionario)
        if not posicion_info:
            return jsonify({'success': False, 'message': 'No se pudo calcular tu posición.'}), 500
        
        puntos_recompensa = recompensa.calcular_puntos_recompensa(
            posicion_info['posicion'],
            posicion_info['total_participantes']
        )
        
        # Registrar recompensa (id_jugador puede ser NULL si no está registrado)
        id_jugador = jugador_info.get('id_jugador')
        if recompensa.registrar_recompensa(id_cuestionario, id_jugador_cuestionario, id_jugador, puntos_recompensa):
            return jsonify({
                'success': True,
                'message': f'¡Felicidades! Has recibido {puntos_recompensa} puntos de recompensa.',
                'puntos': puntos_recompensa,
                'posicion': posicion_info['posicion']
            })
        else:
            return jsonify({'success': False, 'message': 'Error al registrar la recompensa.'}), 500
    
    @app.route('/recompensas_cuestionario/<int:id_cuestionario>')
    @requiere_docente
    def ver_recompensas_cuestionario(id_cuestionario):
        """Página para que el docente vea las recompensas otorgadas en un cuestionario"""
        # Verificar que el cuestionario pertenece al docente
        if 'docente_id' not in session:
            flash("Debes ser docente para ver esta página.", "danger")
            return redirect(url_for('dashboard'))
        
        # Verificar que el cuestionario pertenece al docente
        from conexion import conectarbd
        connection = conectarbd()
        if connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT id_docente FROM Cuestionario
                WHERE id_cuestionario = %s
            """, (id_cuestionario,))
            cuestionario = cursor.fetchone()
            connection.close()
            
            if not cuestionario or cuestionario['id_docente'] != session['docente_id']:
                flash("No tienes permiso para ver este cuestionario.", "danger")
                return redirect(url_for('dashboard'))
        
        # Obtener recompensas
        recompensas = recompensa.obtener_recompensas_por_cuestionario(id_cuestionario)
        
        return render_template(
            'recompensa/ver_recompensas.html',
            id_cuestionario=id_cuestionario,
            recompensas=recompensas
        )
    
    @app.route('/recompensas_docente')
    @requiere_docente
    def ver_recompensas_docente():
        """Página para que el docente vea todas las recompensas otorgadas en sus cuestionarios"""
        if 'docente_id' not in session:
            flash("Debes ser docente para ver esta página.", "danger")
            return redirect(url_for('dashboard'))
        
        id_docente = session['docente_id']
        recompensas = recompensa.obtener_recompensas_por_docente(id_docente)
        
        return render_template(
            'recompensa/ver_recompensas_docente.html',
            recompensas=recompensas
        )

