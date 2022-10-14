import hashlib
import os

from flask import Flask, render_template, request,jsonify,redirect, url_for,session
import json
#importa libreria os
from os import getcwd
import shutil
from werkzeug.utils import secure_filename

#Importa la libreria de SQLITE
import sqlite3

app=Flask(__name__)
#este comando es para poder utilizar el cifrado
app.secret_key = os.urandom(24)


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
Cantidad = 0
Carpeta =""
Imagen1 =""
pathFileImage =getcwd()+"/static/img/"
Imagenes=[]
Imagen1Busqueda=[]
Mensaje=""
actualizado=""


#Endpoint

@app.route("/") #Ruta principal en esta ruta carga la pagina de logueo
def home(): #Función manejadora
    return render_template("index.html") #Respuesta


#en esta estaria la valiDACION DE L USUARIO
@app.route("/login",methods=["POST"])
def login():
    session["Mensaje"]=""
    user = request.form["txtUsuario"]
    password = str(request.form["txtPassword"])
    #cifra la clave
    Clave =hashlib.sha256(password.encode())
    ClaveCifrada =Clave.hexdigest()

    #realiza consulta sql para saber si los datos son correctos    
    with sqlite3.connect("BD/SPH.db") as con:
        con.row_factory = sqlite3.Row

    # Crea un apuntador para manipular la BD
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE email = ?",[user])
        row = cur.fetchone()
        if row:
            #si el estudiante existe llena las variables y valida si es la misma contraseña
            passwordBD = row["Password"]#dato password del query
            session["Alias"]=row["Alias"]#dato alias del query       
#            Usuario = str(row[2])#dato alias del query 
            #global Perfil
            session["Perfil"]=row["Perfil"]
            if session["Perfil"]=="Bloqueado":                    
               return render_template("index.html",contraerrada ="Bloqueado")
            #Perfil =str(row[3])

            global Carpeta
            Carpeta =row["Email"]#el correo del usuario
            

           #si todo esta correcto envia el template main
            if ClaveCifrada ==passwordBD:
                #Guarda el dato en una sesion
                session["Usuario"]=user
                #carga la informacion de la primera foto que tenga el usuario
                with sqlite3.connect("BD/SPH.db") as con:

                  # Convierte el registro en un diccionario
                               
                   con.row_factory = sqlite3.Row

                    # Crea un apuntador para manipular la BD
                   cur = con.cursor()
                   #carga consulta para traer la foto del usuario                   
                   cur.execute("SELECT * FROM Imagenes WHERE Usuario = ?",[user])
                   row = cur.fetchall()
                   global Imagen1
                   Imagen1=""
                   #Si hay datos
                   if row:
                      
                      #Imagen1=str(row[0][1])
                      #capatura la cantidad de fotos
                      Cantidad = 3
                
                   #carga consulta para traer                   
                   cur.execute("SELECT * FROM Imagenes WHERE Usuario = ?",[user])
                   row = cur.fetchall()
                   Imagen1=""
                   
                   #Si hay datos
                   if row:
                      global Imagenes
                      Imagenes =row
                     # Imagen1=str(row[0][1])
                     #separa el comentario en split



                           
                      
                      return redirect("/main")

                   else :
                      return  render_template("main.html",Carpeta =Carpeta,Imagen1=Imagen1,Cantidad=1)


            else:
                errada ="errada"

                return render_template("index.html",contraerrada =errada)
                


        else:
           return render_template("index.html",contraerrada ="NoExiste")
#
#crear ruta de registro
@app.route("/main")
def main():
    if "Usuario" in session:
        return  render_template("main.html",Imagenes=Imagenes,Mensaje=session["Mensaje"])
    return  redirect("/")    

           

#crear ruta de registro
@app.route("/Registro")
def register():
    if "Mensaje" in session:
        return render_template("registro.html",Mensaje=session["Mensaje"])
    else :
        return render_template("registro.html",Mensaje="")


#crear ruta despues de registrar al usuario
@app.route("/Ingresando",methods=["POST"])
def Ingreso():
    #captura todos los datos en las variables
    global nombre
    nombre =request.form["nombres"]
    apellido =request.form["apellidos"]
    fecha =request.form["fecha"]
    edad =request.form["edad"]
    telefono =request.form["celular"]
    genero =request.form["genero"]
    estCivil=request.form["estado"]
    user=request.form["correo"]
    password = request.form["contraseña"]
    #cifra la clave
    Clave =hashlib.sha256(password.encode())
    ClaveCifrada =Clave.hexdigest()
    perfil="Usuario"
    alias =str(request.form["Alias"])
    #crea una consulta para saber si este usuario existe
        #creo conexion a la base de datos para buscar el nombre que escribi
    with sqlite3.connect("BD/SPH.db") as con:
        con.row_factory = sqlite3.Row
    # Crea un apuntador para manipular la BD
        cur = con.cursor()
        cur.execute("SELECT * FROM Users WHERE Email = ?",[user])
        row = cur.fetchone()
        if row:
            session["Mensaje"]="Usuario Ya existe"

        else :
                #realiza consulta sql para saber si los datos son correctos    
            with sqlite3.connect("BD/SPH.db") as con:
            # Crea un apuntador para manipular la BD
                cur = con.cursor()
                #envia info restante a la tabla de info personal
                cur.execute(" INSERT INTO PersonalInfo (Nombre,Apellido,edad,Email,Telefono,Genero,EstaCivil,Alias)VALUES(?,?,?,?,?,?,?,?)",[nombre,apellido,edad,user,telefono,genero,estCivil,alias])
                con.commit()
                cur.execute(" INSERT INTO Users (Email,Password,Alias,Perfil)VALUES(?,?,?,?)",[user,ClaveCifrada,alias,perfil])
                con.commit()

                session["Mensaje"] ="Ok"
                #crea la carpeta para guardar las fotos
                pathFileImage=getcwd()+"\\static\\img\\"+user
                os.mkdir(pathFileImage)
                pathFileImage=pathFileImage+"\\perfil"
                os.mkdir(pathFileImage)
                #guarda una foto por defecto
                Origen =getcwd()+"\\Default.png"
                destino =pathFileImage+"\\Default.png"
                shutil.copy(Origen,destino)

                
        return redirect("/Registro")




#crea ruta de info personal
@app.route("/infoPersonal")
def Infopersonal():
    with sqlite3.connect("BD/SPH.db") as con:

    # Convierte el registro en un diccionario
                
        con.row_factory = sqlite3.Row

        # Crea un apuntador para manipular la BD
        cur = con.cursor()                   
        cur.execute("SELECT * FROM PersonalInfo WHERE Email = ?",[Carpeta])
        row = cur.fetchall()
        
    #Crea la consulta sql para traer la info
    return render_template("infopersonal.html",Carpeta=Carpeta,edad=str(row[0][2]),apellido=str(row[0][1]),
                            usuario=str(row[0][7]),EstCivil=str(row[0][6]),nombreperfil =str(row[0][0]),genero =str(row[0][5]))

#crea ruta de actualizacion de info personal
@app.route("/infoPersonal/actualizar", methods=["POST"])
def Actualizar():
    #captura toda la info que haya en el fomulario
    nombreAct =request.form["nombres"]
    apellidoAct =request.form["apellidos"]
    edadAct =int(request.form["edad"])
    generoAct =request.form["genero"]
    estCivilAct=request.form["civil"]
    emailact =request.form["email"]
    AliasAct =request.form["alias"]
    #Crea conexion para actualizar todos los datos
    with sqlite3.connect("BD/SPH.db") as con:

        cur = con.cursor()
        #envia info restante a la tabla de info personal    
        cur.execute(" UPDATE PersonalInfo SET Nombre = ?, Apellido= ?,Edad = ?, email= ?,Alias = ?, Genero= ?, EstaCivil= ?  WHERE Email =?",[nombreAct,apellidoAct,edadAct,emailact,AliasAct,generoAct,estCivilAct,Carpeta])
        con.commit()
    #valida si el usuario ingreso algun dato para actualizar la foto
            # Se obtiene la imagen
        foto = request.files["txtAvatar"]
        if not foto  :
           nom_archivo =""

        else :    
            #Obtiene el nombre del archivo
            nom_archivo = foto.filename
            nom_archivo="Default.png"
            # Crea la ruta
            pathFileImage=getcwd()+"\\static\\img\\"+Carpeta+"\\perfil\\"
            ruta = pathFileImage + secure_filename(nom_archivo)
            #Guarda el archivo en disco duro
            foto.save(ruta)
    session["Mensaje"]="Actualizado con exito"        
    return redirect ("/main") 



#ruta para cerrar 
@app.route("/logout")
def logout():
    #reinicia la sesion de usuarios
    session.pop('Usuario',None)
    return redirect("/")

#ruta para buscar usuarios 
@app.route("/Busqueda", methods=["POST"])
def Busqueda():
    #crea variable Global
    
    global nombreBuscado
    nombreBuscado =request.form["CampoBusqueda"]
    session["nombreBuscado"]=nombreBuscado
    #creo conexion a la base de datos para buscar el nombre que escribi
    with sqlite3.connect("BD/SPH.db") as con:
        con.row_factory = sqlite3.Row
    # Crea un apuntador para manipular la BD
        cur = con.cursor()
        cur.execute("SELECT * FROM PersonalInfo WHERE email = ?",[nombreBuscado])
        row = cur.fetchone()
        if row:
        
            #trae info de personal buscada
            NombreBusqueda=str(row[0])
            session["NombreBusqueda"]=NombreBusqueda
            apellidoBusqueda=str(row[1])
            session[apellidoBusqueda]=apellidoBusqueda
            edadBusqueda=str(row[2])
            session[edadBusqueda]=edadBusqueda
            AliasBusqueda=row["Alias"]
            session["AliasBusqueda"]=AliasBusqueda
            EmailBusqueda=row["Email"]
            session["EmailBusqueda"]=EmailBusqueda


            #carga la informacion de la primera foto que tenga el usuario de Busqueda
            with sqlite3.connect("BD/SPH.db") as con:

                  # Convierte el registro en un diccionario
                               
                   con.row_factory = sqlite3.Row

                    # Crea un apuntador para manipular la BD
                   cur = con.cursor()                   
                   cur.execute("SELECT * FROM Imagenes WHERE Usuario = ?",[EmailBusqueda])
                   row = cur.fetchall()
                   Imagen1=""
                   #Si hay datos
                   if row:
                      global Imagen1Busqueda
                      Imagen1Busqueda=row   
                      #capatura la cantidad de fotos
                      Cantidad = 3

            return redirect("/BusquedaOk")


            

                #Crea la consulta sql para traer la info
            


        else :
            return "Usuario no existe" 


#crear ruta de registro
@app.route("/BusquedaOk")
def BusquedaOk():
   return   render_template("mainBusqueda.html",Imagen1Busqueda=Imagen1Busqueda,actualizado=actualizado,Mensaje=session["Mensaje"])
   


      
#ruta para buscar usuarios 
@app.route("/GuardarImagen", methods=["POST"])
def FotoCargar():

        foto2 = request.files["Avatar2"]

        if  foto2  :
            ruta=""
            pathFileImage=""

            #Obtiene el nombre del archivo
            NombreFoto =foto2.filename
            # Crea la ruta
            pathFileImage=getcwd()+"\\static\\img\\"+Carpeta+"\\"
            ruta = pathFileImage + secure_filename(NombreFoto)
            #Guarda el archivo en disco duro
            foto2.save(ruta)
            #Procede a guardar la fot en BD
            with sqlite3.connect("BD/SPH.db") as con:
                # Crea un apuntador para manipular la BD
                  cur = con.cursor()
                  #envia info restante a la tabla de info personal
                  cur.execute ("INSERT INTO Imagenes (Usuario,NombreImagen)VALUES(?,?)",[Carpeta,NombreFoto])
                  con.commit()
                  session["Mensaje"]="Guardado con exito"

            return  redirect("/main")
           
        return redirect("/main")       


       



#crea ruta de info personal
@app.route("/infoPersonalBusqueda")
def InfopersonalBusqueda():
    #resetea los mensajes
    session["Mensaje"]=""
    with sqlite3.connect("BD/SPH.db") as con:

    # Convierte el registro en un diccionario
                
        con.row_factory = sqlite3.Row

        # Crea un apuntador para manipular la BD
        cur = con.cursor()                   
        cur.execute("SELECT * FROM PersonalInfo WHERE Email = ?",[nombreBuscado])
        row = cur.fetchall()
        #crea sesiones para cargar
        session["edadBuscado"]=str(row[0][2])
        session["apellidoBuscado"]=str(row[0][1]) 
        session["usuarioBuscado"]=str(row[0][7]) 
        session["EstCivilBuscado"]=str(row[0][6]) 
        session["nombreperfil"]=str(row[0][0]) 
        session["generoBuscado"]=str(row[0][5]) 
        session["emailBuscado"]=str(row[0][3]) 
 
        
    #Crea la consulta sql para traer la info
    return redirect("/infoPersonalBuscado")

@app.route("/infoPersonalBuscado")
def infoPersonalBuscado():
       return render_template("infopersonalBusqueda.html")


@app.route("/limpiarComents", methods=["POST"])
def limpiarComents():
    comentario =request.form["comment"]
    Limpiar=""
       #Crea conexion para actualizar todos los datos
    with sqlite3.connect("BD/SPH.db") as con:

        cur = con.cursor()
        #envia info restante a la tabla de info personal    
        cur.execute(" UPDATE Imagenes SET Comentarios = ? WHERE Usuario = ? AND Comentarios =?",[Limpiar,session["Usuario"],comentario])
        con.commit()
        session["Mensaje"]="Comentario eliminado exitosamente"
        return redirect("/main")
#bloquea los usuarios
@app.route("/BloquearUsuario")
def BloquearUsuario():
        with sqlite3.connect("BD/SPH.db") as con:

    # Convierte el registro en un diccionario
                
            con.row_factory = sqlite3.Row

            # Crea un apuntador para manipular la BD
            cur = con.cursor()                   
            cur.execute("UPDATE Users SET Perfil = 'Bloqueado' WHERE Email = ?",[nombreBuscado])
            con.commit()

        return redirect("/BusquedaOk")    
 

@app.route("/Mensaje")
def EnviarMensaje():
        HistoricoRemitente=""

    #realiza consulta para traer info
        with sqlite3.connect("BD/SPH.db") as con:

            # Convierte el registro en un diccionario
                        
            con.row_factory = sqlite3.Row

            # Crea un apuntador para manipular la BD
            cur = con.cursor()
            #carga consulta para traer la info del usuario                   
            cur.execute("SELECT * from MensajesPrivados WHERE Remitente= ? AND Destinatario= ? union ALL SELECT * from MensajesPrivados WHERE Remitente=? AND Destinatario=? ORDER BY date ASC",[session["Usuario"],nombreBuscado,nombreBuscado,session["Usuario"]])
            
            row = cur.fetchall()
            #Si hay datos
            if row:
                HistoricoRemitente=row
            

        return render_template("message.html",Historico=HistoricoRemitente)




            




@app.route("/MensajesPrivado", methods=["POST"])
def MensajesPrivado():
    EnviarMensaje = request.form["campotexto"]
    if EnviarMensaje == "":
        return redirect("/Mensaje")
    else :



        with sqlite3.connect("BD/SPH.db") as con:

            # Convierte el registro en un diccionario
                
                con.row_factory = sqlite3.Row

                # Crea un apuntador para manipular la BD
                cur = con.cursor()                   
                cur.execute("INSERT INTO MensajesPrivados (Remitente,Destinatario,Mensaje)VALUES(?,?,?)",[session["Usuario"],nombreBuscado,EnviarMensaje])
                con.commit()

                return redirect("/Mensaje")    



           

@app.route("/CambiarPerfil", methods=["POST"])
def CambiarPerfil():
    Perfil=request.form["Perfil"]
    #actualiza el perfil que tenga el usuario por el que hay marcado
    with sqlite3.connect("BD/SPH.db") as con:

    # Convierte el registro en un diccionario
                
            con.row_factory = sqlite3.Row

            # Crea un apuntador para manipular la BD
            cur = con.cursor()                   
            cur.execute("UPDATE Users SET Perfil = ? WHERE Email = ?",[Perfil,nombreBuscado])
            con.commit()
            session["actualizado"] ="ok"

    return redirect("/BusquedaOk")    


    return Perfil


   

@app.route("/EnviarComentario", methods=["POST"])
def EnviarComentario():
    Comentario = request.form["Texto"]
    NombreFoto=request.form["foto"]
    #Conecta con la base de datos para validar si trae comentarios
    with sqlite3.connect("BD/SPH.db") as con:

        # Convierte el registro en un diccionario
                    
        con.row_factory = sqlite3.Row

        # Crea un apuntador para manipular la BD
        cur = con.cursor()
        #carga consulta para traer los mensajes privados del usuario                  
        cur.execute("SELECT Comentarios FROM Imagenes WHERE Usuario = ? AND NombreImagen =?",[session["Usuario"],NombreFoto])
        
        row = cur.fetchone()
        #Si hay datos
        if row :
           ComenHistorico=row[0]+"---"+session["Usuario"]+" "+Comentario
                       #procede a realizar un insert de el mensaje enviado
           with sqlite3.connect("BD/SPH.db") as con:

            # Convierte el registro en un diccionario
                
                con.row_factory = sqlite3.Row

                # Crea un apuntador para manipular la BD
                cur = con.cursor()                   
                cur.execute("UPDATE Imagenes SET comentarios = ? WHERE Usuario = ? AND NombreImagen =?",[ComenHistorico,session["Usuario"],NombreFoto])
                session["Mensaje"]="Comentario Guardado con exito"
                return redirect("/main")    


            #CAPTURA LO QUE HAYA Y LO CONCATENA CON LO NUEVO

    return "NO HAY DATOS"      


@app.route("/EnviarComentarioBusqueda", methods=["POST"])
def EnviarComentarioBusqueda():
    Comentario = request.form["Texto"]
    NombreFoto=request.form["foto"]
    #Conecta con la base de datos para validar si trae comentarios
    with sqlite3.connect("BD/SPH.db") as con:

        # Convierte el registro en un diccionario
                    
        con.row_factory = sqlite3.Row

        # Crea un apuntador para manipular la BD
        cur = con.cursor()
        #carga consulta para traer los mensajes privados del usuario                  
        cur.execute("SELECT Comentarios FROM Imagenes WHERE Usuario = ? AND NombreImagen =?",[session["nombreBuscado"],NombreFoto])
        
        row = cur.fetchone()
        #Si hay datos
        if row :
            ComenHistorico=row[0]
            ComenHistorico=ComenHistorico+"---"+session["Usuario"]+" "+Comentario
                       #procede a realizar un insert de el mensaje enviado
            with sqlite3.connect("BD/SPH.db") as con:

            # Convierte el registro en un diccionario
                
                con.row_factory = sqlite3.Row

                # Crea un apuntador para manipular la BD
                cur = con.cursor()                   
                cur.execute("UPDATE Imagenes SET comentarios = ? WHERE Usuario = ? AND NombreImagen =?",[ComenHistorico,session["nombreBuscado"],NombreFoto])
                session["Mensaje"]="Comentario Guardado con exito"
                return redirect("/BusquedaOk")    


            #CAPTURA LO QUE HAYA Y LO CONCATENA CON LO NUEVO
        else :
            ComenHistorico="---"+session["Usuario"]+" "+Comentario
                       #procede a realizar un insert de el mensaje enviado
            with sqlite3.connect("BD/SPH.db") as con:

                # Convierte el registro en un diccionario
                    
                    con.row_factory = sqlite3.Row

                    # Crea un apuntador para manipular la BD
                    cur = con.cursor()                   
                    cur.execute("UPDATE Imagenes SET comentarios = ? WHERE Usuario = ? AND NombreImagen =?",[ComenHistorico,session["nombreBuscado"],NombreFoto])
                    session["Mensaje"]="Comentario Guardado con exito"
                    return redirect("/BusquedaOk")    
    



@app.route("/producto/guardar", methods=["POST"])
def productoSave():
    nomProducto = request.form["nomProducto"]
    preProducto = request.form["preProducto"]
    canProducto = request.form["canProducto"]
    return f"Producto {nomProducto}. Guardado con éxito"

@app.route("/Main")
def principal():
    if "Usuario" in session:
        return render_template("main.html",Mensaje=session["Mensaje"])

if __name__ == '__main__':
    app.run()

    

