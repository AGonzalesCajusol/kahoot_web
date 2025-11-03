from flask import render_template, request, redirect, session, url_for, flash
from flask_socketio import SocketIO, emit, join_room
import time

from  controladores  import cuestionario
def registrar_rutas(app, socketio):
    @app.route('/preguntas')
    def preguntas():
        return render_template('/preguntas.html')