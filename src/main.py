from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)


# RUTAS
@app.route('/', methods=["GET","POST"])
def index():
    # DOCUMENTACION
    """ bla,bla,bla """
    return render_template('index.html')


# RUN DE LA APP
if __name__ == '__main__':
    app.run(debug=True)


