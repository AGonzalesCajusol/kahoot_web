from flask import render_template, jsonify
from controladores.resultados import obtener_resultados_por_cuestionario

def registrar_rutas_resultados(app):

    @app.route('/resultados/<int:id_cuestionario>')
    def ver_resultados(id_cuestionario):
        resultados = obtener_resultados_por_cuestionario(id_cuestionario)

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
        resultados = obtener_resultados_por_cuestionario(id_cuestionario)
        return jsonify(resultados)

    @app.route('/resultados_inter/<int:id>')
    def ver_resultados_inter(id):
        return render_template('resultados.html', id_cuestionario=id)

