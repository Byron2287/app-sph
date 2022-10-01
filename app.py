import os
from xml.dom.minidom import Document
from flask import Flask, render_template, request,jsonify
import json
#importa libreria os
from os import getcwd
import shutil

#Importa la libreria de SQLITE
import sqlite3

app=Flask(__name__)

#variables
nombre =""
apellido =""
fecha =""
edad =0
email =""
telefono =""
genero =""
estCivil=""
alias =""
password =""
user =""
perfil=""
pathFileImage =getcwd()+"/static/img/"

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
            passwordBD = str(row[1])#dato password del query
            Usuario = str(row[2])#dato alias del query 
            Perfil =str(row[3])
            Carpeta =str(row[0])

           #si todo esta correcto envia el template main
            if password ==passwordBD:
                #carga la informacion de la primera foto que tenga el usuario
                with sqlite3.connect("BD/SPH.db") as con:

                  # Convierte el registro en un diccionario
                               
                   con.row_factory = sqlite3.Row

                    # Crea un apuntador para manipular la BD
                   cur = con.cursor()                   
                   cur.execute("SELECT * FROM Imagenes WHERE Usuario = ?",[user])
                   row = cur.fetchall()
                   Imagen1=""
                   #Si hay datos
                   if row:
                      Imagen1=str(row[0][1])
                      #capatura la cantidad de fotos
                      Cantidad = 0
                
                      dir = getcwd()+"\\static\\img\\"+user
                      for path in os.listdir(dir):
                        if os.path.isfile(os.path.join(dir, path)):
                           Cantidad += 1
                           
                      
                      return  render_template("main.html",usuario =Usuario,PerfilUsu=Perfil,Carpeta =Carpeta,Imagen1=Imagen1,Cantidad=Cantidad)

                   else :
                      return  render_template("main.html",usuario =Usuario,PerfilUsu=Perfil,Carpeta =Carpeta,Imagen1=Imagen1,Cantidad=Cantidad)


            else:
                errada ="errada"

                return render_template("index.html",contraerrada =errada)
                


        else:
           return render_template("index.html",contraerrada ="NoExiste")

#crear ruta de registro
@app.route("/Registro",methods=["POST"])
def register():
    Mensaje=""
    return render_template("registro.html")

#crear ruta despues de registrar al usuario
@app.route("/Ingresando",methods=["POST"])
def Ingreso():
    #captura todos los datos en las variables
    nombre =request.form["nombres"]
    apellido =request.form["apellidos"]
    fecha =request.form["fecha"]
    edad =request.form["edad"]
    telefono =request.form["celular"]
    genero =request.form["genero"]
    estCivil=request.form["estado"]
    user=request.form["correo"]
    password = str(request.form["contraseña"])
    perfil="Usuario"
    alias =str(request.form["Alias"])
        #realiza consulta sql para saber si los datos son correctos    
    with sqlite3.connect("BD/SPH.db") as con:
    # Crea un apuntador para manipular la BD
        cur = con.cursor()
        #envia info restante a la tabla de info personal
        cur.execute(" INSERT INTO PersonalInfo (Nombre,Apellido,edad,Email,Telefono,Genero,EstaCivil,Alias)VALUES(?,?,?,?,?,?,?,?)",[nombre,apellido,edad,user,telefono,genero,estCivil,alias])
        con.commit()
        cur.execute(" INSERT INTO Users (Email,Password,Alias,Perfil)VALUES(?,?,?,?)",[user,password,alias,perfil])
        con.commit()


        Mensaje ="Ok"
        #crea la carpeta para guardar las fotos
        pathFileImage=getcwd()+"\\static\\img\\"+user
        os.mkdir(pathFileImage)
        pathFileImage=pathFileImage+"\\perfil"
        os.mkdir(pathFileImage)
        #guarda una foto por defecto
        Origen =getcwd()+"\\Default.png"
        destino =pathFileImage+"\\Default.png"
        shutil.copy(Origen,destino)

        


    return render_template("registro.html",Mensaje =Mensaje)


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