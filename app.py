from xml.dom.minidom import Document
from flask import Flask, render_template, request,jsonify
import json

#Importa la libreria de SQLITE
import sqlite3

app=Flask(__name__)

nomProducto = ""
preProducto = ""
canProducto = ""

#Endpoint

@app.route("/") #Ruta principal en esta ruta carga la pagina de logueo
def home(): #Función manejadora
    return render_template("index.html") #Respuesta
#en esta estaria la valiDACION DE L USUARIO
@app.route("/login",methods=["POST"])
def login():
    ##########FALTA###########################################
    #EN esta parte esta informacion deberia viajar a la tabla sql con los usuarios y contraseñas para validar si la info es correcta
    #hariamos un select del usuario para saber si la contraseña es correcta
    password =""
    user = request.form["txtUsuario"]
    password = str(request.form["txtPassword"])
    #realiza consulta sql para saber si los datos son correctos    
    with sqlite3.connect("BD/SPH.db") as con:
    # Crea un apuntador para manipular la BD
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE email = ?",[user])
        row = cur.fetchone()
        if row:
            #si el estudiante existe llena las variables y valida si es la misma contraseña
            passwordBD = str(row[3])
            Usuario = str(row[1])


            if password ==passwordBD:
                return render_template("main.html",usuario =Usuario)
            else:
                errada ="True"

                return render_template("index.html",contraerrada =errada)
                


        else:
          return "Usuario no existe"

#    if (user == 'victor' and password == '123456'):
#        return render_template("main.html",usuario =user)
#    else:
#        return "Usuario no existe"
#crear ruta de registro
@app.route("/Registro",methods=["POST"])
def register():
    return render_template("registro.html")

@app.route("/producto/guardar", methods=["POST"])
def productoSave():
    nomProducto = request.form["nomProducto"]
    preProducto = request.form["preProducto"]
    canProducto = request.form["canProducto"]
    return f"Producto {nomProducto}. Guardado con éxito"

@app.route("/producto")
def producto():
    return render_template("admin/producto.html")

if __name__ == '__main__':
    app.run(debug=True)