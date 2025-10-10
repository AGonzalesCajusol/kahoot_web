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
    opcion = 1
    if opcion == 1:
        detalle = ['🔌 Verifica tu conexión a internet', '🔄 Intenta recargar la página','📞 Si el problema persiste, contacta al soporte.' ]
        lista_mensaje = ['Error de Conexión', 'El servicio de BD no esta disponible',detalle ]
        mensaje = {'mensaje': lista_mensaje, 'ruta_foto' : 'static/uploads/404_error.svg'}
    else:
        mensaje = {'mensaje': 'La tabla usuarios no esta dispobible', 'ruta_foto' : ''}
    return render_template('/Fallas/maestra_error.html', mensaje = mensaje) 

if __name__ == '__main__':
    app.run(debug=True)
