# Vamos a hacer una interfaz para que se vea lindo, importemos tkinter
import tkinter as TK
from tkinter import messagebox as msg

# Importamos el socket, que es para la cosa del servidor y cliente.
import socket

# Importamos pickle para mandar una lista en lugar de un solo string
import pickle

# Importamos las validaciones.
import validacionesYCalculos as ValCal

# Importamos las funciones para leer los txt
import leerTxt as leer

# Importamos los cifrados
import cifrados as Cif

# Configuramos la conexión con el servidor.
port = 666  # Escojemos el puerto.
server = socket.gethostbyname(socket.gethostname())  # Dirección IPv4
address = (server, port)  # Dirección
format = "utf-8"  # formato en el que vamos a codificar y decodificar.

# Creamos un socket para el cliente y lo conectamos al server.
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(address)


# Esta es la función para poder generar los números aleatorios del rsa
def generar_numeros_rsa():
    # Generamos los números
    p = ValCal.primo_aleatorio()
    q = ValCal.primo_aleatorio()

    # Los insertamos en la interfaz
    pEntry.delete(0, "end")
    pEntry.insert(0, str(p))

    qEntry.delete(0, "end")
    qEntry.insert(0, str(q))

# esta es la función para poder generar los números aleatorios del Elgammal
def generar_numeros_elgammal():
    # Generamos los números aleatorios.
    p = ValCal.primo_aleatorio()
    
    #Buscamos las raices primitivas de P
    posiblesG = ValCal.raices_primitivas(p)
    # Seleccionamos una al azar
    g = ValCal.seleccionar_random_lista(posiblesG)
    if (g == "error"):
        msg.showerror(
                    title="ERROR",
                    message="Se ha producido un error al intentar crear los valores, intente con números más grandes",
                )
        return None
    
    # Los insertamos en la interfaz
    pEntry.delete(0, "end")
    pEntry.insert(0, str(p))
    
    gEntry.delete(0, "end")
    gEntry.insert(0, str(g))
    
# Función para enviar datos al servidor.
def enviar_datos(mensaje, tipoDato):
    mensaje.append(tipoDato)
    data = pickle.dumps(mensaje)
    client.send(data)


# Función para visualizar el mensaje encriptado mejor
def lista_a_texto(lista):
    texto = ""
    for a in lista:
        if a != "spc":
            texto = texto + str(a)
        if a == "spc":
            texto = texto + " "
    return texto


# Función para mostrar los logs
def mostrar_logs(mensaje):
    interacciónClienteServidor.delete("1.0", "end")
    interacciónClienteServidor.insert("end", mensaje)

# Función para enviar variables desde el cliente al servidor.
def desencriptar_rsa():

    # Creamos los logs que se van a mostrar en la interacción del cliente con el servidor
    log = ""

    # Primero se valida que las variables sean valores numéricos.
    if ValCal.es_numerico(pEntry.get()) and ValCal.es_numerico(qEntry.get()):

        # Se transforman de string a int
        p = int(pEntry.get())
        q = int(qEntry.get())

        # Si P y Q son primos
        if ValCal.es_primo(p) and ValCal.es_primo(q):

            # Generamos las claves
            claves = Cif.generar_claves_rsa(p, q)

            # en caso de tener un error lo mostramos
            if claves == "error":
                msg.showerror(
                    title="ERROR",
                    message="Se ha producido un error al intentar crear las claves, intente con números más grandes",
                )
                return None

            # Guardamos cada una de las claves en variables separadas
            clavePublica = claves[0]
            clavePrivada = claves[1]
            
            # Enviamos la clave pública y le indicamos que se trata de esta
            enviar_datos(clavePublica, "clavePublicaRsa")

            # Escribimos en el log lo que acabamos de hacer
            log = (
                log
                + "El usuario ha enviado su llave pública (n = "
                + str(clavePublica[0])
                + " e = "
                + str(clavePublica[1])
                + ")"
            )

            # Recibimos del servidor el mensaje encriptado
            txtEncriptado = pickle.loads(client.recv(1024))

            # Escribimos en el log que nos lllegó el mensaje encriptado
            log = (
                log
                + "\nEl servidor ha enviado el texto encriptado "
                + lista_a_texto(txtEncriptado)
            )

            # Ahora podemos desencriptar el mensaje con nuestra clave privada
            txtDesencriptado = Cif.descifrado_rsa(txtEncriptado, clavePrivada)

            # Vemos que tenía el txt de entrada
            txtEntradaVanilla = leer.leer_texto("mensajeentrada.txt")

            # Hacemos lo que va a tener el texto de salida
            txtSalida = (
                "Mensaje de entrada:\n"
                + str(txtEntradaVanilla)
                + "\nMensaje cifrado:\n"
                + str(lista_a_texto(txtEncriptado))
                + "\nMensaje descencriptado:\n"
                + str(txtDesencriptado)
            )

            # Escribimos en el texto de salida
            leer.escribir_texto_salida(txtSalida)

            # Lo mostramos en la interfaz
            mensajeTxt.delete("1.0", "end")
            mensajeTxt.insert("end", txtSalida)

            log = log + "\nEl mensaje final es: " + str(txtDesencriptado)

            # Mostramos los logs en la interfaz
            mostrar_logs(log)
            
            # Mostramos una ventanita linda
            msg.showinfo(title="¡Exito!", message=txtSalida)

        else:
            msg.showerror(title="ERROR", message="P y Q deben ser números primos")

    elif qEntry.get() == "" or pEntry.get() == "":

        msg.showerror(title="ERROR", message="P y Q no pueden estar vacíos")

    else:
        msg.showerror(title="ERROR", message="P y Q deben ser numéricos")

def desencriptar_elgamal():
    
    msg.showinfo(title="Información", 
    message="Espere a que el servidor ingrese su clave sercreta b.\n(Escríbela por favor)")
    
    log = ""
    
    if (ValCal.es_numerico(pEntry.get()) 
        and ValCal.es_numerico(gEntry.get()) 
        and ValCal.es_numerico(aEntry.get())):
    
        # Se transforman de string a int
        p = int(pEntry.get())
        g = int(gEntry.get())
        a = int(aEntry.get())
        
        if (ValCal.es_primo(p)):
                
            # Generamos la clave pública
            clavePublica = Cif.generar_claves_elgamal(p, g, a)
            
            # Enviamos la clave pública y le indicamos al server que se trata de esta
            enviar_datos(clavePublica, "clavePublicaElgammal")

            # Escribimos en el log lo que acabamos de hacer
            log = (
                log
                + "El usuario ha enviado su llave pública (g = "
                + str(clavePublica[0])
                + " p = "
                + str(clavePublica[1])
                + " k = "
                + str(clavePublica[2])
                + ")"
            )
            
            # Recibimos del servidor el mensaje encriptado
            txtEncriptado = pickle.loads(client.recv(1024))
            
            print(lista_a_texto(txtEncriptado))
            
            # Escribimos en el log que nos lllegó el mensaje encriptado
            log = (
                log
                + "\nEl servidor ha enviado el texto encriptado "
                + lista_a_texto(txtEncriptado)
            )
            
            # Ahora podemos desencriptar el mensaje con nuestra clave privada
            txtDesencriptado = Cif.descifrado_elgamal(txtEncriptado, a, clavePublica)
            
            # Vemos que tenía el txt de entrada
            txtEntradaVanilla = leer.leer_texto("mensajeentrada.txt")
            
            # Hacemos lo que va a tener el texto de salida
            txtSalida = (
                "Mensaje de entrada:\n"
                + str(txtEntradaVanilla)
                + "\nMensaje cifrado:\n"
                + str(lista_a_texto(txtEncriptado))
                + "\nMensaje descencriptado:\n"
                + str(txtDesencriptado)
            )
            
            # Escribimos en el texto de salida
            leer.escribir_texto_salida(txtSalida)
            
            # Lo mostramos en la interfaz
            mensajeTxt.delete("1.0", "end")
            mensajeTxt.insert("end", txtSalida)
            
            log = log + "\nEl mensaje final es: " + str(txtDesencriptado)
            
            # Mostramos los logs en la interfaz
            mostrar_logs(log)
            
            # Mostramos una ventanita linda
            msg.showinfo(title="¡Exito!", message=txtSalida)
            
        else:
            msg.showerror(title="ERROR", message="P debe ser un número primo")
        
    elif (gEntry.get() == "" 
          or pEntry.get() == "" 
          or aEntry.get() == ""):
        
        msg.showerror(title="ERROR", message="P, G y a no pueden estar vacíos")
    
    else:
        msg.showerror(title="ERROR", message="P, G y a deben ser numéricos")

        
    
# Creamos la ventana
ventana = TK.Tk()
ventana.geometry("1000x500")
ventana.resizable(height=False, width=False)
ventana.title("Menú del cliente")
ventana.iconbitmap("miko.ico")

# Fondito
pantalla = TK.PhotoImage(file="akukin.png")
fotopantalla = TK.Label(ventana, image=pantalla)
fotopantalla.place(x=0, y=0)

# Lado derecho de Aqua
# Este es el cosito que dice interacción cliente/servidor
interacciónClienteServidorLabel = TK.Label(ventana, text="Interacción cliente/servidor")
interacciónClienteServidorLabel.place(x=650, y=50, width=330)

# Acá se pondrá el log entre el cliente y el servidor.
interacciónClienteServidor = TK.Text(ventana)
interacciónClienteServidor.place(x=650, y=70, width=330, height=125)

# Este es el cosito que dice mensaje txt
mensajeTxtLabel = TK.Label(ventana, text="Mensaje")
mensajeTxtLabel.place(x=650, y=225, width=330)

# Acá se pondrá el log entre el cliente y el servidor.
mensajeTxt = TK.Text(ventana)
mensajeTxt.place(x=650, y=245, width=330, height=125)

# Lado izquierdo de Aqua
# Este es el cosito que dice menú del cliente
menuClienteLabel = TK.Label(ventana, text="Menú del cliente")
menuClienteLabel.place(x=100, y=50, width=230)

# Título para la a pequeña
aLabel = TK.Label(ventana, text="Introduzca 'a'")
aLabel.place(x=100, y=80, width=230)

# Acá se pondrá la a chiquitita del cliente.
aEntry = TK.Entry(ventana)
aEntry.place(x=100, y=100, width=230, height=20)

# Título para la g pequeña
gLabel = TK.Label(ventana, text="Introduzca 'G'")
gLabel.place(x=100, y=130, width=230)

# Acá se pondrá la g del cliente.
gEntry = TK.Entry(ventana)
gEntry.place(x=100, y=150, width=230, height=20)

# Título para la p pequeña
pLabel = TK.Label(ventana, text="Introduzca 'P'")
pLabel.place(x=100, y=180, width=230)

# Acá se pondrá la p del cliente.
pEntry = TK.Entry(ventana)
pEntry.place(x=100, y=200, width=230, height=20)

# Título para la q pequeña
qLabel = TK.Label(ventana, text="Introduzca 'Q'")
qLabel.place(x=100, y=230, width=230)

# Acá se pondrá la q del cliente.
qEntry = TK.Entry(ventana)
qEntry.place(x=100, y=250, width=230, height=20)

# Boton para hacer los números necesarios para el RSA
TK.Button(
    ventana,
    text="Generar números aleatorios (RSA)",
    command=lambda: generar_numeros_rsa(),
).place(x=100, y=280, width=230)

# Boton para encriptar el archivo txt de entrada con el RSA
TK.Button(
    ventana,
    text="Desencriptar txt de entrada con RSA",
    command=lambda: desencriptar_rsa(),
).place(x=100, y=320, width=230)

# Boton para hacer los números necesearios para el gammal
TK.Button(ventana, text="Generar números aleatorios (ElGamal)",
        command=lambda: generar_numeros_elgammal()).place(
    x=100, y=360, width=230
)
        
# Boton para desencriptar con elgammal
TK.Button(ventana, 
        text="Desencriptar txt de entrada con ElGammal",
        command=lambda: desencriptar_elgamal()).place(
    x=100, y=400, width=230
)

# Coso para que no se cierre
ventana.mainloop()