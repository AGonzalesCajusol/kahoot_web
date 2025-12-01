from flask import redirect, render_template, request, jsonify, session, url_for, flash, send_file
import conexion
from controladores import cuestionario
from controladores import docente
from controladores import importar_excel
from controladores.auth_decorators import requiere_docente, requiere_login
import pandas as pd
import os
from werkzeug.utils import secure_filename
from datetime import datetime


def registrar_rutas(app, socketio=None):
    # Configuración para subir imágenes
    UPLOAD_FOLDER = 'static/uploads'
    EXCEL_UPLOAD_FOLDER = 'static/uploads/excel'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    ALLOWED_EXCEL_EXTENSIONS = {'xlsx', 'xls'}
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['EXCEL_UPLOAD_FOLDER'] = EXCEL_UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB máximo (aumentado para Excel)
    
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    def allowed_excel_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXCEL_EXTENSIONS
    
    @app.route('/subir_imagen_cuestionario', methods=['POST'])
    @requiere_docente
    def subir_imagen_cuestionario():
        if 'imagen' not in request.files:
            return jsonify({'estado': False, 'mensaje': 'No se envió ningún archivo'}), 400
        
        file = request.files['imagen']
        if file.filename == '':
            return jsonify({'estado': False, 'mensaje': 'No se seleccionó ningún archivo'}), 400
        
        if file and allowed_file(file.filename):
            # Generar nombre único para el archivo
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = secure_filename(file.filename)
            name, ext = os.path.splitext(filename)
            unique_filename = f"cuestionario_{timestamp}_{name}{ext}"
            
            # Asegurar que la carpeta existe
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            
            # Guardar el archivo
            filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
            file.save(filepath)
            
            # Retornar la ruta relativa para guardar en la BD
            ruta_relativa = f"static/uploads/{unique_filename}"
            return jsonify({'estado': True, 'ruta': ruta_relativa, 'mensaje': 'Imagen subida correctamente'}), 200
        else:
            return jsonify({'estado': False, 'mensaje': 'Tipo de archivo no permitido. Solo se permiten: PNG, JPG, JPEG, GIF'}), 400
    
    @app.route('/eliminar_imagen_cuestionario/<int:id_cuestionario>', methods=['POST'])
    @requiere_docente
    def eliminar_imagen_cuestionario(id_cuestionario):
        try:
            # Verificar que el cuestionario pertenece al docente actual
            id_docente = session.get('docente_id')
            if not id_docente:
                return jsonify({'estado': False, 'mensaje': 'No hay sesión de docente activa'}), 401
            
            connection = conexion.conectarbd()
            if not connection:
                return jsonify({'estado': False, 'mensaje': 'Error al conectar con la base de datos'}), 500
            
            cursor = connection.cursor()
            try:
                # Verificar que el cuestionario pertenece al docente
                cursor.execute("SELECT id_docente, imagen_url FROM Cuestionario WHERE id_cuestionario = %s", (id_cuestionario,))
                cuestionario = cursor.fetchone()
                
                if not cuestionario:
                    return jsonify({'estado': False, 'mensaje': 'El cuestionario no existe'}), 404
                
                if cuestionario.get('id_docente') != id_docente:
                    return jsonify({'estado': False, 'mensaje': 'No tienes permiso para modificar este cuestionario'}), 403
                
                # Obtener la ruta de la imagen para eliminarla del sistema de archivos
                imagen_url = cuestionario.get('imagen_url')
                print(f"[DEBUG] Imagen URL actual: {imagen_url}")
                
                # Actualizar la base de datos estableciendo imagen_url a NULL
                cursor.execute("UPDATE Cuestionario SET imagen_url = NULL WHERE id_cuestionario = %s", (id_cuestionario,))
                rows_affected = cursor.rowcount
                print(f"[DEBUG] Filas afectadas por UPDATE: {rows_affected}")
                
                connection.commit()
                print(f"[DEBUG] Commit realizado exitosamente")
                
                # Verificar que se actualizó correctamente
                cursor.execute("SELECT imagen_url FROM Cuestionario WHERE id_cuestionario = %s", (id_cuestionario,))
                verificacion = cursor.fetchone()
                print(f"[DEBUG] Imagen URL después de UPDATE: {verificacion.get('imagen_url') if verificacion else 'No encontrado'}")
                
                # Eliminar el archivo físico si existe
                if imagen_url:
                    try:
                        # La imagen_url viene como "static/uploads/archivo.jpg"
                        # Necesitamos construir la ruta completa
                        file_path = os.path.join(app.root_path, imagen_url.lstrip('/'))
                        if os.path.exists(file_path):
                            os.remove(file_path)
                            print(f"[DEBUG] Archivo físico eliminado: {file_path}")
                        else:
                            print(f"[DEBUG] Archivo físico no encontrado: {file_path}")
                    except Exception as e:
                        print(f"[DEBUG] Error al eliminar el archivo físico: {e}")
                        # No fallar si no se puede eliminar el archivo físico
                
                return jsonify({'estado': True, 'mensaje': 'Imagen eliminada correctamente'}), 200
            finally:
                if cursor:
                    cursor.close()
                
        except Exception as e:
            print(f"Error al eliminar imagen: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({'estado': False, 'mensaje': f'Error al eliminar la imagen: {str(e)}'}), 500
        finally:
            if connection:
                connection.close()
    
    @app.route('/fn_modificar', methods = ['POST'])
    @requiere_docente
    def fn_modificar():
        datos = request.get_json()
        respuesta = cuestionario.fnmodificardetalleformulario(datos)
        return jsonify(respuesta)

    @app.route('/modificar_cuestionario/<int:id>')
    @requiere_docente
    def modificar_cuestionario(id):
        respuesta = cuestionario.datos_cuestionario1(id)
        print(respuesta)
        return render_template('crear_cuestionarios.html', datos = respuesta)
    
    @app.route('/api_obtener_cuestionario_modificar/<int:id>')
    @requiere_docente
    def api_obtener_cuestionario_modificar(id):
        """API para obtener los datos actualizados del cuestionario (usado después de eliminar imagen)"""
        respuesta = cuestionario.datos_cuestionario1(id)
        return jsonify(respuesta)

    @app.route('/vercuestionario/<int:id>')
    @requiere_docente
    def vercuestionario(id):
        respuesta = cuestionario.datos_cuestionario1(id)
        
        # Verificar si viene desde el repositorio
        desde_repositorio = request.args.get('desde_repositorio', 'false').lower() == 'true'
        
        # Si viene desde el repositorio, SIEMPRE mostrar vista de solo lectura
        if desde_repositorio:
            return render_template('cuestionariover.html', datos=respuesta, es_propietario=False, id_cuestionario=id)
        
        # Si NO viene desde repositorio, verificar si es propietario
        id_docente_actual = session.get('docente_id')
        connection = conexion.conectarbd()
        es_propietario = False
        
        if connection and id_docente_actual:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT id_docente FROM Cuestionario WHERE id_cuestionario = %s", (id,))
                    resultado = cursor.fetchone()
                    if resultado:
                        id_docente_cuestionario = resultado.get('id_docente')
                        # Comparar convirtiendo ambos a int para evitar problemas de tipo
                        if id_docente_cuestionario is not None:
                            try:
                                if int(id_docente_cuestionario) == int(id_docente_actual):
                                    es_propietario = True
                            except (ValueError, TypeError):
                                pass
            except Exception as e:
                print(f"Error verificando propietario: {e}")
            finally:
                connection.close()
        
        # Si es propietario y NO viene del repositorio, redirigir a modificar
        if es_propietario:
            return redirect(url_for('modificar_cuestionario', id=id))
        
        # Si no es propietario, mostrar vista de solo lectura
        return render_template('cuestionariover.html', datos=respuesta, es_propietario=False, id_cuestionario=id)
    
    @app.route('/reutilizar_cuestionario/<int:id>', methods=['POST'])
    @requiere_docente
    def reutilizar_cuestionario_route(id):
        id_docente = session.get('docente_id')
        if not id_docente:
            return jsonify({'estado': False, 'mensaje': 'No hay sesión de docente activa'}), 401
        
        id_cuestionario_nuevo, mensaje = cuestionario.reutilizar_cuestionario(id, id_docente)
        
        if id_cuestionario_nuevo:
            return jsonify({
                'estado': True, 
                'mensaje': mensaje,
                'id_cuestionario': id_cuestionario_nuevo,
                'redirect': url_for('modificar_cuestionario', id=id_cuestionario_nuevo)
            })
        else:
            return jsonify({'estado': False, 'mensaje': mensaje}), 400
    
    @app.route('/registrar_respuestasform', methods=['POST'])
    @requiere_login
    def registrar_respuestasform():
        id_participante = session.get('id_jugador_cuestionario') or session.get('jugador_id')
        if not id_participante:
            return jsonify({'error': 'Usuario no autenticado'}), 401
        datos = request.get_json()
        cuestionario.actualizar_puntaje_usuario(id_participante, datos.get('puntaje'))
        return jsonify({'puntaje': 12})


    @app.route('/registrar_cuestionario', methods=['POST'])
    @requiere_docente
    def registrar_cuestionario():
        datos = request.get_json()
        id_docente = datos.get('id_docente')
        
        if not id_docente:
            return jsonify({"message": "id_docente es requerido"}), 400

        respuesta = cuestionario.registrar_cuestionario(datos, id_docente)

        if respuesta == True:
            return jsonify({"message": "Cuestionario registrado exitosamente"}), 201  
        else:
            return jsonify({"message": "Error al registrar el cuestionario"}), 400

    @app.route('/registrar_pregunta', methods=['POST'])
    @requiere_docente
    def registrar_pregunta():
        datos = request.get_json()
        print("estos son los datos", datos)
        id_docente = session.get('docente_id')
        
        if not id_docente:
            return jsonify({'estado': False, 'mensaje': 'No hay sesión de docente activa'}), 401
        
        # Si tiene id_formulario, es una pregunta nueva para un cuestionario existente
        id_formulario = datos.get('id_formulario')
        if id_formulario:
            # Agregar pregunta a cuestionario existente
            resultado = cuestionario.agregar_pregunta_a_cuestionario(id_formulario, datos)
            if resultado['estado']:
                return jsonify({'estado': True, 'mensaje': resultado['mensaje'], 'id_pregunta': resultado.get('id_pregunta')})
            else:
                return jsonify({'estado': False, 'mensaje': resultado['mensaje']})
        else:
            # Crear nuevo cuestionario completo
            respuesta, mensaje = cuestionario.registrar_cuestionarioSPDF(datos, id_docente)
            if respuesta:
                return jsonify({'estado': True, 'mensaje': mensaje})
            
            return jsonify({'estado': False, 'mensaje': mensaje})

    @app.route('/registrar_alternativa', methods=['POST'])
    def registrar_alternativa_route():
        datos = request.get_json()  
        respuesta_texto = datos.get('respuesta')
        estado = datos.get('estado')
        id_pregunta = datos.get('id_pregunta')

        resultado = cuestionario.registrar_alternativa(respuesta_texto, estado, id_pregunta)

        if "registrada exitosamente" in resultado:
            return jsonify({"message": resultado}), 201
        else:
            return jsonify({"message": resultado}), 400

    @app.route('/fn_modificar_pregunta/<int:id_pregunta>', methods=['PUT'])
    @requiere_docente
    def fn_modificar_pregunta(id_pregunta):
        datos = request.get_json()
        respuesta = cuestionario.modificar_pregunta(id_pregunta, datos)
        return jsonify(respuesta)

    @app.route('/fn_eliminar_pregunta/<int:id_pregunta>', methods=['DELETE'])
    @requiere_docente
    def fn_eliminar_pregunta(id_pregunta):
        respuesta = cuestionario.eliminar_pregunta(id_pregunta)
        return jsonify(respuesta)

    @app.route('/resetear_cuestionario/<int:id_cuestionario>', methods=['POST'])
    @requiere_docente
    def resetear_cuestionario(id_cuestionario):
        respuesta = cuestionario.resetear_cuestionario(id_cuestionario)
        return jsonify(respuesta)

    @app.route('/eliminar_cuestionario/<int:id_cuestionario>', methods=['DELETE'])
    @requiere_docente
    def eliminar_cuestionario(id_cuestionario):
        respuesta = cuestionario.eliminar_cuestionario_completo(id_cuestionario)
        return jsonify(respuesta)

    
    @app.route('/cuestionarios_activos', methods=['GET'], endpoint='cuestionarios_activos_endpoint')
    @requiere_docente
    def cuestionarios_activos():
        id_docente = request.args.get('id_docente') 
        print("ID Docente recibido:", id_docente)
        if not id_docente:
            return jsonify({'error': 'Falta id_docente'}), 400 
        
        
        cuestionarios = cuestionario.obtener_cuestionarios_activos(id_docente)
        print(cuestionarios)
        return jsonify(cuestionarios)

    @app.route('/cuestionarios_archivados', methods=['GET'], endpoint='cuestionarios_archivados_endpoint')
    @requiere_docente
    def cuestionarios_archivados():
        id_docente = request.args.get('id_docente')  
        print("ID Docente recibido:", id_docente)
        if not id_docente:
            return jsonify({'error': 'Falta id_docente'}), 400
        
        cuestionarios = cuestionario.obtener_cuestionarios_archivados(id_docente)
        print(cuestionarios)
        return jsonify(cuestionarios)

    @app.route('/validar_pin', methods=['POST'])
    def validar_pin_route():
        try:
            datos = request.get_json()
            pin = datos.get('pin')

            if not pin:
                return jsonify({"error": "PIN es requerido"}), 400

            resultado = cuestionario.validar_pin(pin)

            if not resultado:
                return jsonify({"error": "PIN inválido o cuestionario inactivo"}), 400

            id_cuestionario = resultado['id_cuestionario']
            tipo_cuestionario = resultado['tipo_cuestionario']
            estado_cuestionario = resultado['estado_cuestionario']
            estado_juego = resultado['estado_juego']

            print(f"id_cuestionario: {id_cuestionario}, tipo_cuestionario: {tipo_cuestionario}, estado_cuestionario: {estado_cuestionario}, estado_juego: {estado_juego}")

            if estado_juego == 'IN':
                return jsonify({"error":"El juego ya inicio"}), 400
            elif estado_juego == 'FN':
                return jsonify({"error": "el juego ya finalizo"}), 400

            session['id_cuestionario'] = id_cuestionario
            session['tipo_cuestionario'] = tipo_cuestionario

            return jsonify({
                "id_cuestionario": id_cuestionario,
                "tipo_cuestionario": tipo_cuestionario,
                "estado_cuestionario": estado_cuestionario,
                "estado_juego" : estado_juego
            }), 200

        except Exception as e:
            print(f"Error en /validar_pin: {e}")
            return jsonify({"error": "Error interno del servidor"}), 500

    @app.route('/registrar_alias')
    def registrar_alias():
        id_cuestionario = session.get('id_cuestionario')
        if not id_cuestionario:
            flash("Debes ingresar un PIN válido primero", "danger")
            return redirect('/pin_estudiante')
        
        # Verificar si ya hay un id_jugador_cuestionario en sesión para este cuestionario
        # Si existe, verificar si es válido
        id_jugador_cuestionario_sesion = session.get('id_jugador_cuestionario')
        if id_jugador_cuestionario_sesion:
            connection = conexion.conectarbd()
            if connection:
                try:
                    with connection.cursor() as cursor:
                        cursor.execute("""
                            SELECT id_jugador_cuestionario, alias, id_cuestionario 
                            FROM Jugador_Cuestionario 
                            WHERE id_jugador_cuestionario = %s AND id_cuestionario = %s
                        """, (id_jugador_cuestionario_sesion, id_cuestionario))
                        jugador_cuestionario_existente = cursor.fetchone()
                        
                        if jugador_cuestionario_existente:
                            # Ya tiene un registro válido para este cuestionario
                            # Redirigir directamente a sala de espera
                            return redirect(f'/sala_espera/{id_cuestionario}')
                        else:
                            # El id_jugador_cuestionario no corresponde a este cuestionario, limpiarlo
                            session.pop('id_jugador_cuestionario', None)
                except Exception as e:
                    print(f"Error al verificar jugador_cuestionario existente: {e}")
                finally:
                    connection.close()
        
        nombre_sugerido = None
        if 'jugador_id' in session:
            nombre_sugerido = session.get('email', '').split('@')[0]
        
        return render_template('alias.html', id_cuestionario=id_cuestionario, nombre_sugerido=nombre_sugerido)

    @app.route('/verificar_alias', methods=['POST'])
    def verificar_alias():
        data = request.get_json()
        alias = data.get('alias')
        id_cuestionario = data.get('id_cuestionario')

        if not alias or not id_cuestionario:
            return jsonify({'error': 'Alias y cuestionario son requeridos'}), 400

        if len(alias) < 2 or len(alias) > 20:
            return jsonify({'error': 'El alias debe tener entre 2 y 20 caracteres'}), 400

        connection = conexion.conectarbd()
        if not connection:
            return jsonify({'error': 'Error al conectar con la base de datos'}), 500

        try:
            with connection.cursor() as cursor:
                # Verificar si el alias ya existe para este cuestionario
                cursor.execute("""
                    SELECT id_jugador_cuestionario FROM Jugador_Cuestionario
                    WHERE alias = %s AND id_cuestionario = %s
                """, (alias, id_cuestionario))
                existente = cursor.fetchone()

                if existente:
                    return jsonify({'error': 'Este alias ya está en uso. ¡Elige otro nombre!'}), 400

                id_jugador = session.get('jugador_id') if 'jugador_id' in session else None
                
                # Crear registro en Jugador_Cuestionario
                # Permitir jugadores con o sin sesión (id_jugador puede ser NULL)
                cursor.execute("""
                    INSERT INTO Jugador_Cuestionario (id_jugador, id_cuestionario, alias, puntaje)
                    VALUES (%s, %s, %s, 0)
                """, (id_jugador, id_cuestionario, alias))
                
                id_jugador_cuestionario = cursor.lastrowid
                session['id_jugador_cuestionario'] = id_jugador_cuestionario
                
                connection.commit()
                
                print(f"[REGISTRO] Participante registrado: alias={alias}, id_cuestionario={id_cuestionario}, id_jugador_cuestionario={id_jugador_cuestionario}")
                
                cursor.execute("SELECT tipo_cuestionario FROM Cuestionario WHERE id_cuestionario = %s", (id_cuestionario,))
                tipo_cuestionario = cursor.fetchone()
                
                if socketio:
                    try:
                        from controladores import cuestionario as ctrl_cuestionario
                        participantes = ctrl_cuestionario.obtener_participantes(id_cuestionario)
                        sala = str(id_cuestionario)
                        print(f"[REGISTRO] 📤 Emitiendo actualizar_participantes después de registro a sala {sala}")
                        socketio.emit('actualizar_participantes', {'participantes': participantes}, room=sala)
                        print(f"[REGISTRO] ✅ Evento emitido exitosamente con {len(participantes)} participantes")
                    except Exception as e:
                        print(f"[REGISTRO] ⚠️ Error al emitir evento Socket.IO: {e}")
                
                tipo_cuestionario_val = tipo_cuestionario.get('tipo_cuestionario', 'I') if tipo_cuestionario else 'I'
                if tipo_cuestionario_val == 'G':
                    return jsonify({
                        'success': True, 
                        'id_jugador_cuestionario': id_jugador_cuestionario,
                        'tipo_cuestionario': 'G',
                        'redirect': f'/grupos/{id_cuestionario}'
                    }), 200
                else:
                    return jsonify({'success': True, 'id_jugador_cuestionario': id_jugador_cuestionario}), 200

        except Exception as e:
            print("Error en verificar_alias:", e)
            import traceback
            traceback.print_exc()
            return jsonify({'error': 'Error interno del servidor'}), 500

        finally:
            connection.close()

    @app.route('/sala_espera/<int:id_cuestionario>')
    def sala_espera(id_cuestionario):
        connection = conexion.conectarbd()
        cursor = connection.cursor()

        query_cuestionario = """
            SELECT 
                c.nombre AS nombre_cuestionario,
                c.pin,
                CONCAT(d.nombres, ' ', d.apellidos) AS nombre_docente
            FROM Cuestionario c
            INNER JOIN Docente d ON c.id_docente = d.id_docente
            WHERE c.id_cuestionario = %s
        """
        cursor.execute(query_cuestionario, (id_cuestionario,))
        cuestionario = cursor.fetchone()

        if not cuestionario:
            cursor.close()
            connection.close()
            return "Cuestionario no encontrado", 404

        query_usuarios = """
            SELECT alias, puntaje
            FROM Jugador_Cuestionario
            WHERE id_cuestionario = %s
            ORDER BY id_jugador_cuestionario ASC
        """
        cursor.execute(query_usuarios, (id_cuestionario,))
        resultados = cursor.fetchall()

        usuarios = [{"alias": row["alias"], "puntaje": row["puntaje"]} for row in resultados]

        cursor.close()
        connection.close()

        return render_template(
            'sala_espera.html',
            cuestionario=cuestionario,
            usuarios=usuarios,
            id_cuestionario=id_cuestionario
        )
    @app.route('/descargar_plantilla_excel', methods=['GET'])
    @requiere_docente
    def descargar_plantilla_excel():
        """Descarga una plantilla Excel para que los docentes puedan llenar con sus preguntas"""
        try:
            # Crear la plantilla
            os.makedirs(EXCEL_UPLOAD_FOLDER, exist_ok=True)
            plantilla_path = os.path.join(EXCEL_UPLOAD_FOLDER, 'plantilla_preguntas.xlsx')
            
            if importar_excel.crear_plantilla_excel(plantilla_path):
                return send_file(
                    plantilla_path,
                    as_attachment=True,
                    download_name='plantilla_preguntas_cuestionario.xlsx',
                    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
            else:
                return jsonify({'estado': False, 'mensaje': 'Error al crear la plantilla'}), 500
        except Exception as e:
            print(f"Error al descargar plantilla: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({'estado': False, 'mensaje': f'Error al generar la plantilla: {str(e)}'}), 500
    
    @app.route('/importar_preguntas_excel', methods=['POST'])
    @requiere_docente
    def importar_preguntas_excel():
        """Importa preguntas desde un archivo Excel y las agrega al cuestionario actual"""
        try:
            id_docente = session.get('docente_id')
            if not id_docente:
                return jsonify({'estado': False, 'mensaje': 'No hay sesión de docente activa'}), 401
            
            if 'excel_archivo' not in request.files:
                return jsonify({'estado': False, 'mensaje': 'No se envió ningún archivo'}), 400
            
            file = request.files['excel_archivo']
            if file.filename == '':
                return jsonify({'estado': False, 'mensaje': 'No se seleccionó ningún archivo'}), 400
            
            if not allowed_excel_file(file.filename):
                return jsonify({'estado': False, 'mensaje': 'Tipo de archivo no permitido. Solo se permiten: XLSX, XLS'}), 400
            
            # Guardar archivo temporalmente
            os.makedirs(EXCEL_UPLOAD_FOLDER, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = secure_filename(file.filename)
            name, ext = os.path.splitext(filename)
            unique_filename = f"import_{timestamp}_{name}{ext}"
            filepath = os.path.join(EXCEL_UPLOAD_FOLDER, unique_filename)
            file.save(filepath)
            
            try:
                # Leer el Excel (retorna detalle, preguntas, errores)
                detalle, preguntas, errores = importar_excel.leer_excel_preguntas(filepath)
                
                if errores:
                    # Si hay errores, retornarlos pero también las preguntas válidas si las hay
                    return jsonify({
                        'estado': len(preguntas) > 0,  # Éxito parcial si hay preguntas válidas
                        'mensaje': f'Se encontraron {len(errores)} error(es) al procesar el archivo',
                        'preguntas': preguntas,
                        'errores': errores,
                        'total_preguntas': len(preguntas),
                        'total_errores': len(errores)
                    }), 200 if len(preguntas) > 0 else 400
                
                if len(preguntas) == 0:
                    return jsonify({
                        'estado': False,
                        'mensaje': 'No se encontraron preguntas válidas en el archivo Excel'
                    }), 400
                
                return jsonify({
                    'estado': True,
                    'mensaje': f'Se importaron {len(preguntas)} pregunta(s) correctamente',
                    'preguntas': preguntas,
                    'total_preguntas': len(preguntas)
                }), 200
                
            finally:
                # Eliminar archivo temporal
                try:
                    if os.path.exists(filepath):
                        os.remove(filepath)
                except Exception as e:
                    print(f"Error al eliminar archivo temporal: {e}")
                    
        except Exception as e:
            print(f"Error al importar preguntas desde Excel: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({'estado': False, 'mensaje': f'Error al procesar el archivo Excel: {str(e)}'}), 500
    
    @app.route('/subirformulario_excel', methods=['POST'])
    @requiere_docente
    def subirformulario_excel():
        try:
            excel = request.files['excel_archivo']
            df = pd.read_excel(excel, header=None)  # Leer sin encabezados para tener control total

            formulario = {}
            
            # Leer detalle del cuestionario desde la fila 2 (índice 1 en pandas)
            # Formato: Fila 1 = encabezados, Fila 2 = datos del cuestionario
            if len(df) >= 2:
                fila_detalle = df.iloc[1]  # Fila 2 (índice 1)
                
                if len(fila_detalle) >= 1 and pd.notna(fila_detalle.iloc[0]):
                    formulario['nombre_formulario'] = str(fila_detalle.iloc[0]).strip()
                else:
                    formulario['nombre_formulario'] = ''
                
                if len(fila_detalle) >= 2 and pd.notna(fila_detalle.iloc[1]):
                    tipo_val = str(fila_detalle.iloc[1]).strip().upper()
                    # Normalizar tipo
                    if tipo_val.startswith('I') or 'INDIVIDUAL' in tipo_val:
                        formulario['tipo_formulario'] = 'I'
                    elif tipo_val.startswith('G') or 'GRUPAL' in tipo_val:
                        formulario['tipo_formulario'] = 'G'
                    else:
                        formulario['tipo_formulario'] = 'I'
                else:
                    formulario['tipo_formulario'] = 'I'
                
                if len(fila_detalle) >= 3 and pd.notna(fila_detalle.iloc[2]):
                    formulario['descripcion_formulario'] = str(fila_detalle.iloc[2]).strip()
                else:
                    formulario['descripcion_formulario'] = ''
                
                if len(fila_detalle) >= 4 and pd.notna(fila_detalle.iloc[3]):
                    estado_val = str(fila_detalle.iloc[3]).strip().upper()
                    # Normalizar estado - solo aceptar P o R, o palabras completas
                    # Si es un número o valor inválido, usar Público por defecto
                    try:
                        # Intentar convertir a número para detectar valores numéricos erróneos
                        float(estado_val)
                        # Si es un número, usar Público por defecto
                        formulario['estado'] = 'Público'
                    except ValueError:
                        # No es un número, procesar normalmente
                        if estado_val.startswith('P') or 'PUBLICO' in estado_val or 'PÚBLICO' in estado_val:
                            formulario['estado'] = 'Público'
                        elif estado_val.startswith('R') or 'PRIVADO' in estado_val:
                            formulario['estado'] = 'Privado'
                        else:
                            formulario['estado'] = 'Público'
                else:
                    formulario['estado'] = 'Público'
            else:
                # Si no hay fila 2, usar valores por defecto
                formulario['nombre_formulario'] = ''
                formulario['tipo_formulario'] = 'I'
                formulario['descripcion_formulario'] = ''
                formulario['estado'] = 'Público'

            # Leer preguntas desde la fila 4 en adelante (índice 3+)
            # Formato: Fila 3 = encabezados de preguntas, Fila 4+ = datos de preguntas
            preguntas = []
            for idx in range(3, len(df)):  # Empezar desde la fila 4 (índice 3)
                row = df.iloc[idx]
                
                # Saltar filas vacías
                if pd.isna(row.iloc[0]) or str(row.iloc[0]).strip() == '':
                    continue
                
                pregunta = {}
                
                # Columna A (índice 0): Pregunta
                if pd.notna(row.iloc[0]):
                    pregunta['nombre_pregunta'] = str(row.iloc[0]).strip()
                else:
                    continue  # Si no hay pregunta, saltar esta fila
                
                # Columna B (índice 1): Tipo pregunta
                if len(row) > 1 and pd.notna(row.iloc[1]):
                    tipo_preg = str(row.iloc[1]).strip().upper()
                    if tipo_preg.startswith('VF') or 'VERDADERO' in tipo_preg or 'FALSO' in tipo_preg:
                        pregunta['tipo_pregunta'] = 'VF'
                    elif tipo_preg.startswith('ALT') or 'ALTERNATIVA' in tipo_preg or 'MULTIPLE' in tipo_preg:
                        pregunta['tipo_pregunta'] = 'ALT'
                    else:
                        pregunta['tipo_pregunta'] = 'ALT'
                else:
                    pregunta['tipo_pregunta'] = 'ALT'
                
                # Columna C (índice 2): Puntos
                if len(row) > 2 and pd.notna(row.iloc[2]):
                    try:
                        pregunta['puntos'] = int(float(row.iloc[2]))
                        if pregunta['puntos'] <= 0 or pregunta['puntos'] > 1000:
                            pregunta['puntos'] = 100
                    except:
                        pregunta['puntos'] = 100
                else:
                    pregunta['puntos'] = 100
                
                # Columna D (índice 3): Tiempo
                if len(row) > 3 and pd.notna(row.iloc[3]):
                    try:
                        pregunta['tiempo'] = int(float(row.iloc[3]))
                        if pregunta['tiempo'] < 2 or pregunta['tiempo'] > 300:
                            pregunta['tiempo'] = 30
                    except:
                        pregunta['tiempo'] = 30
                else:
                    pregunta['tiempo'] = 30
                
                # Columnas E-J (índices 4-9): Alternativas
                alternativas = []
                for col_idx in range(4, 10):  # Columnas E a J
                    if len(row) > col_idx and pd.notna(row.iloc[col_idx]) and str(row.iloc[col_idx]).strip():
                        alternativas.append(str(row.iloc[col_idx]).strip())
                
                # Columna K (índice 10): Respuesta correcta
                respuesta_correcta = ''
                if len(row) > 10 and pd.notna(row.iloc[10]):
                    respuesta_correcta = str(row.iloc[10]).strip()
                
                # Procesar según el tipo
                if pregunta['tipo_pregunta'] == 'VF':
                    pregunta['alternativas'] = ['Verdadero', 'Falso']
                    if respuesta_correcta.upper() in ['VERDADERO', 'V', 'TRUE']:
                        pregunta['respuesta_correcta'] = 'Verdadero'
                    elif respuesta_correcta.upper() in ['FALSO', 'F', 'FALSE']:
                        pregunta['respuesta_correcta'] = 'Falso'
                    else:
                        pregunta['respuesta_correcta'] = 'Verdadero'  # Por defecto
                else:  # ALT
                    if len(alternativas) < 2:
                        continue  # Saltar si no tiene suficientes alternativas
                    
                    pregunta['alternativas'] = alternativas
                    
                    # Buscar la respuesta correcta en las alternativas (case-insensitive)
                    if respuesta_correcta:
                        alternativas_lower = [alt.lower() for alt in alternativas]
                        if respuesta_correcta.lower() in alternativas_lower:
                            idx = alternativas_lower.index(respuesta_correcta.lower())
                            pregunta['respuesta_correcta'] = alternativas[idx]
                        else:
                            pregunta['respuesta_correcta'] = alternativas[0]  # Por defecto, primera alternativa
                    else:
                        pregunta['respuesta_correcta'] = alternativas[0]  # Por defecto
                
                if pregunta.get('nombre_pregunta') and pregunta.get('tipo_pregunta'):
                    preguntas.append(pregunta)

            resultado = {
                "detalle": formulario,
                "preguntas": preguntas
            }
            
            print("=" * 50)
            print("DATOS PROCESADOS DEL EXCEL:")
            print("Detalle:", resultado["detalle"])
            print("Preguntas encontradas:", len(resultado["preguntas"]))
            for i, p in enumerate(resultado["preguntas"][:3], 1):
                print(f"  Pregunta {i}: {p}")
            print("=" * 50)

            id_docente = session.get('docente_id')
            if not id_docente:
                return jsonify({'estado': False, 'mensaje': 'No se encontró la sesión del docente. Inicia sesión nuevamente.'}), 401
            
            response = cuestionario.registrar_cuestionario(resultado, id_docente)
            if response == True:
                return jsonify({'estado': True, 'mensaje': '¡Cuestionario registrado con éxito! La página se actualizará...'})
            elif response == False:
                return jsonify({'estado': False, 'mensaje': 'No cumple con el formato el excel revise el formato de guía'})
            else:
                return jsonify({'estado': False, 'mensaje': f'Error desconocido: {response}'})
                
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({'estado': False, 'mensaje': f'Error al procesar el archivo: {str(e)}'}), 500
    
    