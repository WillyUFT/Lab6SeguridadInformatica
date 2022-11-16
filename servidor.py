# Importamos la biblioteca para la cosa del servidor y cliente.
import pickle
import socket

# Importamos las validaciones y calculos
import validacionesYCalculos as ValCal

# Importamos los cifrados
import cifrados as Cif

# Importamos el archivo para leer txt
import leerTxt


# Configuramos el servidor.
port = 666  # Escojemos el puerto.
SERVER = socket.gethostbyname(socket.gethostname())  # Dirección IPv4
address = (SERVER, port)  # Dirección
format = "utf-8"  # formato en el que vamos a codificar y decodificar.

# Creamos el socket para el servidor.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Hacemos el bind con la dirección
server.bind(address)

# Función para comenzar la conexión.
def comenzar_conexion():

    print("El servidor está funcionando en " + SERVER)

    server.listen()

    # Aceptar conexión y retorna una nueva conexión con el cliente.
    conn, addr = server.accept()

    while True:

        # 1024 representa la máxima cantidad de data
        # que puede ser recibida.
        # data = conn.recv(1024).decode()
        data = pickle.loads(conn.recv(1024))

        # Si no mandamos nada salimos del while
        if not data:
            break
        
        if (data[len(data)-1] == "clavePublicaRsa"):
            txtEntrada = leerTxt.leer_texto("mensajeentrada.txt")
            txtEncriptado = Cif.cifrado_rsa(txtEntrada, data)
            data = pickle.dumps(txtEncriptado)
            conn.send(data)
            
        if (data[len(data)-1] == "clavePublicaElgammal"):
            botonPreguntarB = True
            while botonPreguntarB:
                # b del servidor
                b = int(input("Escoja un b, por favor: "))
                if (ValCal.es_entero(b)
                    and b > 1
                    and b < data[1] - 1):
                    botonPreguntarB = False
                    
            txtEntrada = leerTxt.leer_texto("mensajeentrada.txt")
            textoEncriptado = Cif.cifrado_elgamal(txtEntrada, data, b)
            data = pickle.dumps(textoEncriptado)
            conn.send(data)

    conn.close()


comenzar_conexion()
