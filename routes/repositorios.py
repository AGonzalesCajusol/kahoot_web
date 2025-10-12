from flask import render_template, request, redirect, session, url_for, flash, jsonify
from controladores.repositorios import obtener_cuestionarios_publicos

def registrar_rutas(app):    
    @app.route('/cuestionarios_publicos', methods=['GET'])    
    def cuestionarios_publicos():
        cuestionarios = obtener_cuestionarios_publicos()
        
        if cuestionarios:
            print(cuestionarios) 
            return jsonify(cuestionarios), 200 
        else:
            print("No se encontraron cuestionarios") 
            return jsonify({"mensaje": "No se encontraron cuestionarios públicos"}), 404
