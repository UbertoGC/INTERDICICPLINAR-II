import json
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL,MySQLdb
from sonido import *

#https://www.it-swarm-es.com/es/python/usando-mysql-en-flask/941923326/
# Para ejecutar el servicio debo ejecutar main.py

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Hardware+10'
app.config['MYSQL_DB'] = 'almacen'
mysql = MySQL(app)
loop = asyncio.get_event_loop()
valor=["Presiona el boton de play para iniciar",0]
app.secret_key='mysecretkey'
dic_cantidad={'un':'1','uno':'1','dos':'2','tres':'3','cuatro':'4','cinco':'5','seis':'6','siete':'7','ocho':'8','nueve':'9','cero':'0'}
dic_productos=['cebolla','zanahoria','papa','aceite']
dic_u_medidas=['kilo','litro']
valor = []
@app.route('/transcripcion',methods = ['POST','GET'])
def transcripcion():
    if(estado[0]):
        guardado.clear()
        loop.run_until_complete(Recibir_Enviar())
        resultados=[]
        for i in guardado:
            menor=i.lower()
            diack=menor[:-1]
            resultados.append(diack.split())
        for j in resultados:
            lista=["","",""]
            for i in j:
                if(i in dic_cantidad):
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

@app.route('/contact',methods=["GET","POST"])
def contact():
    return render_template('contact.html')

@app.route('/info',methods=["GET","POST"])
def info():
    return render_template('info.html')

@app.route('/signUp', methods = ['POST','GET'])
def signUp():
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    if  _email and _password:
        conn = mysql.connection
        if (conn):
            print("Conexion establecida")
        else:
            print("Conexion fallida")
        cursor = conn.cursor()
        cursor.callproc('crearUsuario',(_email, _password))
        data = cursor.fetchall()
        if len(data) ==0:
            conn.commit()
            print("Usuario fue creado!")
            return json.dumps({'mensaje':'usuario fue creado!'})
        else:
            print({'error':str(data[0])})
    else:
        return json.dumps({'mensaje': 'Campos estan vacios!'})
    cursor.close()
    conn.close()


if __name__=='__main__':#si el archivo que se esta ejecutando es el main es decir el main.py entonces arranca el servidor
    app.run(port=3000,debug=True)#corre el servidor