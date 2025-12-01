from flask import render_template, request, jsonify, session, redirect, url_for, flash
from controladores import grupo as ctrl_grupo
import conexion

def registrar_rutas(app, socketio=None):
    @app.route('/ver_grupos/<int:id_cuestionario>')
    def ver_grupos(id_cuestionario):
        """Vista para que el docente vea los grupos formados"""
        docente_id = session.get('docente_id')
        
        if not docente_id:
            flash("Debes iniciar sesión como docente", "danger")
            return redirect('/login')
        
        # Verificar que el cuestionario pertenece al docente
        connection = conexion.conectarbd()
        if not connection:
            flash("Error al conectar con la base de datos", "danger")
            return redirect('/dashboard')
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT c.id_cuestionario, c.nombre, c.pin, c.tipo_cuestionario
                    FROM Cuestionario c
                    WHERE c.id_cuestionario = %s AND c.id_docente = %s
                """, (id_cuestionario, docente_id))
                cuestionario = cursor.fetchone()
                
                if not cuestionario:
                    flash("Cuestionario no encontrado o no tienes permisos", "danger")
                    return redirect('/dashboard')
                
                if cuestionario.get('tipo_cuestionario') != 'G':
                    flash("Este cuestionario no es grupal", "warning")
                    return redirect('/dashboard')
                
                # Obtener todos los grupos del cuestionario
                grupos = ctrl_grupo.obtener_todos_grupos(id_cuestionario)
                
                # Obtener miembros de cada grupo
                grupos_con_miembros = []
                for grupo in grupos:
                    miembros = ctrl_grupo.obtener_miembros_grupo(grupo.get('id_grupo'))
                    grupo['miembros'] = miembros
                    grupos_con_miembros.append(grupo)
                
                return render_template('grupos/ver_grupos_docente.html',
                                     cuestionario=cuestionario,
                                     grupos=grupos_con_miembros,
                                     id_cuestionario=id_cuestionario)
        except Exception as e:
            print(f"Error en ver_grupos: {e}")
            flash("Error al obtener los grupos", "danger")
            return redirect('/dashboard')
        finally:
            if connection:
                connection.close()
    
    @app.route('/grupos/<int:id_cuestionario>')
    def gestionar_grupos(id_cuestionario):
        """Página principal para gestionar grupos"""
        id_jugador_cuestionario = session.get('id_jugador_cuestionario')
        
        if not id_jugador_cuestionario:
            return redirect('/')
        
        # Verificar si el jugador ya está en un grupo
        grupo_usuario = ctrl_grupo.obtener_grupo_usuario(id_jugador_cuestionario, id_cuestionario)
        
        # Obtener grupos disponibles
        grupos_disponibles = ctrl_grupo.obtener_grupos_disponibles(id_cuestionario)
        
        return render_template('grupos/gestionar_grupos.html', 
                             id_cuestionario=id_cuestionario,
                             grupo_usuario=grupo_usuario,
                             grupos_disponibles=grupos_disponibles,
                             id_jugador_cuestionario=id_jugador_cuestionario)
    
    @app.route('/crear_grupo', methods=['POST'])
    def crear_grupo_route():
        """Crea un nuevo grupo"""
        try:
            data = request.get_json()
            nombre_grupo = data.get('nombre_grupo', '').strip()
            id_cuestionario = data.get('id_cuestionario')
            id_jugador_cuestionario = session.get('id_jugador_cuestionario')
            
            if not id_jugador_cuestionario:
                return jsonify({"code": 0, "message": "Debes estar registrado en el cuestionario primero"}), 401
            
            if not nombre_grupo or len(nombre_grupo) < 2:
                return jsonify({"code": 0, "message": "El nombre del grupo debe tener al menos 2 caracteres"}), 400
            
            if len(nombre_grupo) > 100:
                return jsonify({"code": 0, "message": "El nombre del grupo no puede exceder 100 caracteres"}), 400
            
            id_grupo, mensaje = ctrl_grupo.crear_grupo(nombre_grupo, id_cuestionario, id_jugador_cuestionario)
            
            if id_grupo:
                # Emitir evento Socket.IO para actualizar grupos
                if socketio:
                    grupos_disponibles = ctrl_grupo.obtener_grupos_disponibles(id_cuestionario)
                    socketio.emit('actualizar_grupos', {'grupos': grupos_disponibles}, room=str(id_cuestionario))
                
                return jsonify({"code": 1, "message": mensaje, "id_grupo": id_grupo}), 200
            else:
                return jsonify({"code": 0, "message": mensaje}), 400
                
        except Exception as e:
            print(f"Error en crear_grupo_route: {e}")
            return jsonify({"code": 0, "message": "Error interno del servidor"}), 500
    
    @app.route('/unirse_grupo', methods=['POST'])
    def unirse_grupo_route():
        """Un estudiante se une a un grupo"""
        try:
            data = request.get_json()
            id_grupo = data.get('id_grupo')
            id_jugador_cuestionario = session.get('id_jugador_cuestionario')
            
            if not id_jugador_cuestionario:
                return jsonify({"code": 0, "message": "Debes estar registrado en el cuestionario primero"}), 401
            
            if not id_grupo:
                return jsonify({"code": 0, "message": "ID de grupo requerido"}), 400
            
            exito, mensaje = ctrl_grupo.unirse_grupo(id_grupo, id_jugador_cuestionario)
            
            if exito:
                # Obtener información del grupo para emitir evento
                # Necesitamos obtener el id_cuestionario desde el grupo
                connection = conexion.conectarbd()
                if connection:
                    try:
                        with connection.cursor() as cursor:
                            cursor.execute("SELECT id_cuestionario FROM Grupo WHERE id_grupo = %s", (id_grupo,))
                            grupo_data = cursor.fetchone()
                            if grupo_data and socketio:
                                id_cuestionario_val = grupo_data.get('id_cuestionario')
                                grupos_disponibles = ctrl_grupo.obtener_grupos_disponibles(id_cuestionario_val)
                                socketio.emit('actualizar_grupos', {'grupos': grupos_disponibles}, room=str(id_cuestionario_val))
                    finally:
                        connection.close()
                
                return jsonify({"code": 1, "message": mensaje}), 200
            else:
                return jsonify({"code": 0, "message": mensaje}), 400
                
        except Exception as e:
            print(f"Error en unirse_grupo_route: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({"code": 0, "message": "Error interno del servidor"}), 500
    
    @app.route('/miembros_grupo/<int:id_grupo>')
    def obtener_miembros_grupo_route(id_grupo):
        """Obtiene los miembros de un grupo"""
        try:
            miembros = ctrl_grupo.obtener_miembros_grupo(id_grupo)
            return jsonify({"code": 1, "miembros": miembros}), 200
        except Exception as e:
            print(f"Error en obtener_miembros_grupo_route: {e}")
            return jsonify({"code": 0, "message": "Error al obtener miembros"}), 500
    
    @app.route('/establecer_metodo_evaluacion', methods=['POST'])
    def establecer_metodo_evaluacion_route():
        """Establece el método de evaluación del grupo"""
        try:
            data = request.get_json()
            id_grupo = data.get('id_grupo')
            metodo_evaluacion = data.get('metodo_evaluacion')
            id_jugador_cuestionario = session.get('id_jugador_cuestionario')
            
            if not id_jugador_cuestionario:
                return jsonify({"code": 0, "message": "Debes estar registrado en el cuestionario primero"}), 401
            
            exito, mensaje = ctrl_grupo.establecer_metodo_evaluacion(id_grupo, metodo_evaluacion, id_jugador_cuestionario)
            
            if exito:
                return jsonify({"code": 1, "message": mensaje}), 200
            else:
                return jsonify({"code": 0, "message": mensaje}), 400
                
        except Exception as e:
            print(f"Error en establecer_metodo_evaluacion_route: {e}")
            return jsonify({"code": 0, "message": "Error interno del servidor"}), 500
    
    @app.route('/salir_grupo', methods=['POST'])
    def salir_grupo_route():
        """Un estudiante sale de un grupo"""
        try:
            data = request.get_json()
            id_grupo = data.get('id_grupo')
            id_jugador_cuestionario = session.get('id_jugador_cuestionario')
            
            if not id_jugador_cuestionario:
                return jsonify({"code": 0, "message": "Debes estar registrado en el cuestionario primero"}), 401
            
            exito, mensaje = ctrl_grupo.salir_grupo(id_grupo, id_jugador_cuestionario)
            
            if exito:
                return jsonify({"code": 1, "message": mensaje}), 200
            else:
                return jsonify({"code": 0, "message": mensaje}), 400
                
        except Exception as e:
            print(f"Error en salir_grupo_route: {e}")
            return jsonify({"code": 0, "message": "Error interno del servidor"}), 500
    
    @app.route('/disolver_grupo', methods=['POST'])
    def disolver_grupo_route():
        """El líder disuelve el grupo"""
        try:
            data = request.get_json()
            id_grupo = data.get('id_grupo')
            id_jugador_cuestionario = session.get('id_jugador_cuestionario')
            
            if not id_jugador_cuestionario:
                return jsonify({"code": 0, "message": "Debes estar registrado en el cuestionario primero"}), 401
            
            exito, mensaje = ctrl_grupo.disolver_grupo(id_grupo, id_jugador_cuestionario)
            
            if exito:
                return jsonify({"code": 1, "message": mensaje}), 200
            else:
                return jsonify({"code": 0, "message": mensaje}), 400
                
        except Exception as e:
            print(f"Error en disolver_grupo_route: {e}")
            return jsonify({"code": 0, "message": "Error interno del servidor"}), 500

