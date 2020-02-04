from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

# CONEXION MONGODB + BASE DE DATOS + COLECCION
URL_MONGO = 'mongodb+srv://Invitado:Guest5050@cluster0-3lrrr.mongodb.net/test?retryWrites=true&w=majority'
cliente = MongoClient(URL_MONGO, ssl_cert_reqs=False)
db = cliente['primeraBD']
coleccion = db['gastoscoche']

app = Flask(__name__)


# RUTAS
@app.route('/', methods=["GET","POST"])
def home():
    diccionarios = coleccion.find()
    return render_template ('index.html', registros=diccionarios, tituloDelListado="Listado de Gastos") 

@app.route("/nuevo")
def nuevoGasto():
    diccionarios = coleccion.find().limit(5)
    return render_template ('nuevo.html', registros=diccionarios, tituloDelListado="Listado de tus últimos 5 gastos: ")

@app.route("/entrar-nuevo", methods=['GET','POST'])
def entrarNuevoGasto():
    if request.method=='POST':
        fecha = request.form['fecha']
        titulo = request.form['titulo']
        importe = request.form['importe']
        registro = {"fecha":fecha,"titulo":titulo,"importe": importe}
        coleccion.insert_one(registro)
        return redirect (url_for ('nuevoGasto'))
    return redirect (url_for ('nuevoGasto'))

@app.route("/borrar/<id>")
def borrarGasto(id):
    buscarPorId = {"_id": ObjectId(id)}
    datosRegistro = coleccion.find_one(buscarPorId)
    return render_template ('/borrar.html', datosRegistro=datosRegistro)

@app.route("/confirmar-borrado/<string:id>")
def confirmadoBorrado(id):
    buscarPorId = {"_id": ObjectId(id)}
    coleccion.delete_one(buscarPorId)
    return redirect (url_for('home'))

@app.route("/mostrar-todos")
def mostrarTodos():
    diccionarios = coleccion.find()
    tituloDelListado = "Listado de todos los recordatorios"
    return render_template ('mostrar-todos.html', registros=diccionarios, tituloDelListado=tituloDelListado)

@app.route("/editar/<id>")
def editarGasto(id):
    buscarPorId = {"_id": ObjectId(id)}
    datosRegistro = coleccion.find_one(buscarPorId)
    return render_template ('/editar.html', datosRegistro=datosRegistro)

# @app.route("/editar-confirmado/<id>", methods=['GET','POST'])
# def actualizar(id):
#     if request.method=='POST':
#         fecha = request.form['fecha']
#         titulo = request.form['titulo']
#         importe = request.form['importe']
#         registro = {"fecha":fecha,"titulo":titulo,"importe": importe}
#         coleccion.insert_one(registro)

#         nombre = request.form['nombre']
#         telefono = request.form['telefono']
#         email = request.form['email']
#         buscarPor = {"_id": ObjectId(id)}
#         diccionario = {"nombre":nombre,"telefono":telefono,"email":email}
#         coleccionContactos.update_one(buscarPor, {"$set": diccionario})
#         return redirect (url_for ('home'))
#     return redirect (url_for ('home'))


if __name__ == '__main__':
    port = int(os.environ.get("PORT",5000))
    app.run(host='0.0.0.0',port=port,debug=True)