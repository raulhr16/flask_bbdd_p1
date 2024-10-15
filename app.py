from flask import Flask, render_template, request, redirect, url_for, flash, session
import psycopg2
import sys

app = Flask(__name__)
app.secret_key = 'some_secret_key'

#Voy a hacer funciones para obtener tanto el nombre de las bases de datos disponibles como el contenido de ellas
conexion_bbdd = psycopg2.connect(
            dbname="postgres",
            user="raulhr",
            password="raulhr",
            host="192.168.122.97"
        )

def listado_bbdd():
    try:
        conexion_bbdd
        cursor = conexion_bbdd.cursor()
        cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
        lista_bbdd=[i[0] for i in cursor.fetchall()]
        cursor.close()
        return lista_bbdd
    except psycopg2.Error as e:
        print("No puedo conectar a la base de datos:", e)
        return -3
        
def tablas_bbdd(nombre,contraseña,nombre_bbdd):
    try:
        conex2 = psycopg2.connect(
            dbname=nombre_bbdd,
            user=nombre,
            password=contraseña,
            host="192.168.122.97"
        )
        cursor = conex2.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        nombre_tablas_bbdd=[i[0] for i in cursor.fetchall()]
        cursor.close()
        return nombre_tablas_bbdd
    except psycopg2.Error as e:
        print("No puedo conectar a la base de datos:", e)
        return -1

def datos_bbdd(nombre,contraseña,nombre_bbdd,tabla):
    try:
        conex2 = psycopg2.connect(
            dbname=nombre_bbdd,
            user=nombre,
            password=contraseña,
            host="192.168.122.97"
        )
        cursor = conex2.cursor()
        cursor.execute(f"SELECT * FROM {tabla};")
        registros = cursor.fetchall()
        datos_tablas=[i[0] for i in cursor.description]
        cursor.close()
        return datos_tablas, registros
    except psycopg2.Error as e:
        print("No puedo conectar a la base de datos:", e)
        return -4

@app.route('/')
def inicio():
    base_de_datos = listado_bbdd()
    return render_template('index.html',base_de_datos=base_de_datos)

@app.route('/login', methods=['POST','GET'])
def login():
    session['usuario'] = request.form['nombre']
    session['passwd'] = request.form['contraseña']
    session['bbdd'] = request.form['nombre_bbdd']
    tablas = tablas_bbdd(session['usuario'],session['passwd'],session['bbdd'])
    if tablas == -1:
        return render_template ("404.html")
    else:
        return render_template("login.html",tablas=tablas, bbdd=session['bbdd'])
    
@app.route('/login/<nombre_tabla>')
def tabla(nombre_tabla):
    columnas, registros = datos_bbdd(session['usuario'],session['passwd'],session['bbdd'],nombre_tabla)
    return render_template("datos.html", nombre_tabla=nombre_tabla, columnas=columnas, registros=registros)


if __name__ == '__main__':
    app.run(debug=True)
