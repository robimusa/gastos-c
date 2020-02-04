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

registro = {"prueba":"prueba"}
# db.coleccion.insertOne(registro)
coleccion.insert_one(registro)

# RUTAS
@app.route('/', methods=["GET","POST"])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    port = int(os.environ.get("PORT",5000))
    app.run(host='0.0.0.0',port=port,debug=True)