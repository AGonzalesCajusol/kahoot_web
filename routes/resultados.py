from flask import render_template, jsonify, session
from controladores.resultados import obtener_resultados_por_cuestionario

def registrar_rutas_resultados(app):

    @app.route('/resultados/<int:id_cuestionario>')
    def ver_resultados(id_cuestionario):
        id_jugador_cuestionario = session.get('id_jugador_cuestionario')
        resultados = obtener_resultados_por_cuestionario(id_cuestionario, id_jugador_cuestionario)

        if "error" in resultados:
            return render_template("error.html", mensaje=resultados["error"])

        return render_template(
            "estadistica.html",
            quiz=resultados["quiz"],
            top3=resultados["top3"],
            participantes=resultados["participantes"]
        )

    @app.route('/api/resultados/<int:id_cuestionario>')
    def api_resultados(id_cuestionario):        
        id_jugador_cuestionario = session.get('id_jugador_cuestionario')
        id_docente = session.get('docente_id')
        resultados = obtener_resultados_por_cuestionario(id_cuestionario, id_jugador_cuestionario, id_docente)
        return jsonify(resultados)

    @app.route('/resultados_inter/<int:id>')
    def ver_resultados_inter(id):
        return render_template('resultados.html', id_cuestionario=id)
    
    @app.route('/api/puntos_recompensa_jugador/<int:id_cuestionario>')
    def api_puntos_recompensa_jugador(id_cuestionario):
        """API para obtener los puntos de recompensa del jugador actual en un cuestionario"""
        id_jugador_cuestionario = session.get('id_jugador_cuestionario')
        
        # Si no hay id_jugador_cuestionario en sesión, intentar obtenerlo del cuestionario
        if not id_jugador_cuestionario:
            id_jugador = session.get('jugador_id')
            if id_jugador:
                # Buscar el id_jugador_cuestionario basado en el id_jugador y id_cuestionario
                from conexion import conectarbd
                connection = conectarbd()
                if connection:
                    try:
                        with connection.cursor() as cursor:
                            cursor.execute("""
                                SELECT id_jugador_cuestionario 
                                FROM Jugador_Cuestionario 
                                WHERE id_cuestionario = %s AND id_jugador = %s
                                ORDER BY fecha_participacion DESC
                                LIMIT 1
                            """, (id_cuestionario, id_jugador))
                            resultado = cursor.fetchone()
                            if resultado:
                                id_jugador_cuestionario = resultado.get('id_jugador_cuestionario')
                    except Exception as e:
                        print(f"Error al buscar id_jugador_cuestionario: {e}")
                    finally:
                        connection.close()
        
        if not id_jugador_cuestionario:
            return jsonify({'puntos_recompensa': 0})
        
        from controladores import recompensa
        puntos = recompensa.obtener_puntos_recompensa_jugador_cuestionario(id_jugador_cuestionario, id_cuestionario)
        print(f"[DEBUG] Puntos de recompensa para jugador_cuestionario {id_jugador_cuestionario} en cuestionario {id_cuestionario}: {puntos}")
        return jsonify({'puntos_recompensa': puntos})

