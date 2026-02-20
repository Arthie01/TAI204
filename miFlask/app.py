from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)
API_URL = "http://localhost:5000"

@app.route('/')
def index():
    try:
        respuesta = requests.get(API_URL + "/v1/usuarios/")
        usuarios = respuesta.json().get('Usarios', [])
    except:
        usuarios = []
    return render_template('index.html', usuarios=usuarios)

@app.route('/agregar', methods=['POST'])
def agregar():

    respuesta = requests.get(API_URL + "/v1/usuarios/")
    usuarios = respuesta.json()['Usarios']
    
    ultimo_id = 0
    for u in usuarios:
        if u['id'] > ultimo_id:
            ultimo_id = u['id']
    
    nuevo = {
        "id": ultimo_id + 1,
        "nombre": request.form['nombre'],
        "edad": request.form['edad']
    }
    
    requests.post(API_URL + "/v1/usuarios/", json=nuevo)
    return redirect(url_for('index'))

@app.route('/editar', methods=['POST'])
def editar():
    usuario = {
        "id": int(request.form['id']),
        "nombre": request.form['nombre'],
        "edad": request.form['edad']
    }
    requests.put(API_URL + "/v1/usuarios/", json=usuario)
    return redirect(url_for('index'))

@app.route('/eliminar/<int:id>')
def eliminar(id):
    requests.delete(API_URL + "/v1/usuarios/", json={"id": id})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
