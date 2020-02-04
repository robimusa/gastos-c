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
def index():
    return render_template('index.html')



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


if __name__ == '__main__':
    port = int(os.environ.get("PORT",5000))
    app.run(host='0.0.0.0',port=port,debug=True)