from flask import Flask, render_template, request, redirect, url_for, flash, session
import psycopg2

app = Flask(__name__)
app.secret_key = 'some_secret_key'

#Voy a hacer funciones para obtener tanto el nombre de las bases de datos disponibles como el contenido de ellas



@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/login', methods=['POST','GET'])
def login():
    conexion = psycopg2.connect(
        dbname=""
    )
    if request.method == 'POST':
        usuario = request.form['username']
        passwd = request.form['password']
    else:
        return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
