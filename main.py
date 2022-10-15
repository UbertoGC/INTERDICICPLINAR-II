from asyncio import get_event_loop
import json
from multiprocessing.connection import wait
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysql_connector import MySQL
from sonido import *

#https://www.it-swarm-es.com/es/python/usando-mysql-en-flask/941923326/
# Para ejecutar el servicio debo ejecutar main.py

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Hardware+10'
app.config['MYSQL_DB'] = 'almacen'
mysql = MySQL(app)
valor=["Presiona el boton de play para iniciar",0]
app.secret_key='mysecretkey'
dic_cantidad={'un':'1','uno':'1','dos':'2','tres':'3','cuatro':'4','cinco':'5','seis':'6','siete':'7','ocho':'8','nueve':'9','cero':'0'}
dic_productos=['cebolla','zanahoria','papa','aceite']
dic_u_medidas=['kilo','litro']
valor = []
@app.route('/transcripcion',methods = ['POST','GET'])
def transcripcion():
    if(loop.is_running() and (not estado[0])):
        while(loop.is_running()):
            resultados=[]
        resultados=[]
        for i in guardado:
            menor=i.lower()
            diack=menor[:-1]
            resultados.append(diack.split())
        for j in resultados:
            lista=["-","-","-"]
            for i in j:
                if(i in dic_cantidad):
                    if(lista[0]=="-"):
                        lista[0]=""
                    lista[0]=lista[0]+dic_cantidad[i]
                elif (i in dic_u_medidas):
                    lista[1]=i
                elif (i[:-1] in dic_u_medidas):
                    lista[1]=i[:-1]
                elif (i in dic_productos):
                    lista[2]=i
                elif (i[:-1] in dic_productos):
                    lista[2]=i[:-1]
            valor.append(lista)
    elif(estado[0] and (not loop.is_running())):
        guardado.clear()
        loop.run_until_complete(Recibir_Enviar())
    return render_template('transcripcion.html', texto=guardado,valores=valor)

@app.route('/transenviplay')
def transenviplay():
    estado[0]=True
    return redirect(url_for('transcripcion'))

@app.route('/transenvistop')
def transenvistop():
    estado[0]=False
    return redirect(url_for('transcripcion'))

@app.route('/')
def home():
    return redirect(url_for('main'))

@app.route('/main')
def main():
    return render_template('home.html')

@app.route('/sign_in',methods=["GET","POST"])
def sign_in():
    return render_template('index.html')

@app.route('/logout')
def logout():
    if 'correo' in session:
        session.pop('correo', None)
        return redirect(url_for('sign_in'))

@app.route('/contact',methods=["GET","POST"])
def contact():
    return render_template('contact.html')

@app.route('/info',methods=["GET","POST"])
def info():
    return render_template('info.html')

@app.route('/uso',methods=["GET","POST"])
def uso():
    return render_template('uso.html')

@app.route('/signUp', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        _email = request.form['correo']
        _password = request.form['contra']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO usuario (correo, password_) VALUES (%s,%s)", (_email, _password))
        #cursor.callproc('crearUsuario',(_email,_password))
        mysql.connection.commit()
        flash('Nuevo contacto agregado')
        return render_template('index.html')
    cursor.close()

@app.route('/validateLogin', methods = ['POST'])
def validateLogin():
    _email = request.form['correo']
    _password = request.form['contra']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM usuario WHERE correo = %s AND password_ = %s", (_email, _password))
    data = cursor.fetchall()
    if len(data) > 0:
        session['user'] = _email
        return redirect(url_for('transcripcion'))
    cursor.close()
    return render_template('index.html', error = 'Usuario no existe')

if __name__=='__main__':#si el archivo que se esta ejecutando es el main es decir el main.py entonces arranca el servidor
    app.run(port=3000,debug=True)#corre el servidor