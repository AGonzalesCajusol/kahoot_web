from flask import Flask, render_template
import conexion 
app = Flask(__name__)

@app.route('/')
def home():
    conexion.conectarbd()
    return "Hola mundo"  # O puedes usar return "Hola Flask"




#Ruta si se cayo el servidor de base de datos
@app.route('/errorsistema')
def errorsistema():
    conexion.conectarbd()
    return render_template('/Fallas/maestra_error.html') # O puedes usar return "Hola Flask"

if __name__ == '__main__':
    app.run(debug=True)
