# Importamos los cálculos y validaciones
import validacionesYCalculos as ValCal

# Función para generar las claves RSA
def generar_claves_rsa(p, q):
    # Calculamos N
    n = ValCal.calcular_n(p, q)
    # Calculamos phi(n)
    phiN = ValCal.calcular_phi_n(p, q)
    # Generamos la clave pública
    # Para ello primero buscamos los números entre 0 y phi(n),
    # como máximo común divisor sean 1, para nuestro posible e
    listaPublica = ValCal.maximo_comun_divisor(phiN)
    # Ahora seleccionamos uno al azar
    exponentePublico = ValCal.seleccionar_random_lista(listaPublica)
    # En caso de que la lista esté vacía (Sé que pasa con el 2, pero no sé si otro número)
    if exponentePublico == "error":
        return "error"
    # Generamos la clave privada
    # Vamos a buscar el algoritmo modular
    listaPrivada = ValCal.calcular_algoritmo_modular(exponentePublico, phiN)
    # Ahora escogemos alguno de estos
    exponentePrivado = ValCal.seleccionar_random_lista(listaPrivada)
    # Armamos finalmente las claves
    clavePublica = [n, exponentePublico]
    clavePrivada = [n, exponentePrivado]
    # Las vamos a meter a una lista
    claves = [clavePublica, clavePrivada]
    # Y la retornamos
    return claves


# Función para cifrar en RSA
def cifrado_rsa(mensaje, clavePublica):
    # Hacemos las varibales
    n = clavePublica[0]
    e = clavePublica[1]
    textoRsa = []
    # Recorremos el mensaje letra por letra
    for letra in mensaje:
        # Si es mayúscula
        if letra.isupper():
            # Lo cambiamos a decimal
            letraDec = ord(letra) - 65
            # Lo encriptamos
            letraRsa = (letraDec**e) % n
            # Lo añadimos a la lista
            textoRsa.append(letraRsa)
        elif letra.islower():
            letraDec = ord(letra) - 97
            letraRsa = (letraDec**e) % n
            textoRsa.append(letraRsa)
        elif letra.isspace():
            textoRsa.append("spc")
    return textoRsa


# Función para descifrar en  RSA
def descifrado_rsa(mensaje, clavePrivada):
    # Hacemos las variables
    n = clavePrivada[0]
    d = clavePrivada[1]
    mensajeDescrifrado = ""
    # Recorremos la lista que se llama mensaje
    for letra in mensaje:
        # Si es un espacio lo agregamos
        if letra == "spc":
            mensajeDescrifrado = mensajeDescrifrado + " "
        # Si es una letra normal
        else:
            # La transformamos a decimal
            letraDec = ((int(letra) ** d) % n) + 65
            # Luego la transformamos a caracter
            letraRsa = chr(letraDec)
            # Lo agregamos al mensaje descrifrado
            mensajeDescrifrado = mensajeDescrifrado + letraRsa
    # Retornamos el mensaje descifrado
    return mensajeDescrifrado


# Función para generar claves de ElGamal
def generar_claves_elgamal(p, g, a):

    k = ValCal.calcular_k(g, a, p)
    clavePublica = [g, p, k]

    return clavePublica


# Función para cifrar con Elgamal
def cifrado_elgamal(mensaje, clavePublica, b):
    # Definimos las variables
    g = clavePublica[0]
    p = clavePublica[1]
    k = clavePublica[2]
    textoEg = []
    for letra in mensaje:
        # Si es mayuscula
        if letra.isupper():
            # Lo cambiamos a decimal
            letraDec = ord(letra) - 65
            # Lo encriptamos
            letraEg1 = (g**b) % p
            letraEg2 = letraDec * (k**b) % p
            # Hacemos el set de la letra Eg
            letraEg = [letraEg1, letraEg2]
            # Y lo metemos al mensaje
            textoEg.append(letraEg)
        elif letra.islower():
            # Lo cambiamos a decimal
            letraDec = ord(letra) - 97
            # Lo encriptamos
            letraEg1 = (g**b) % p
            letraEg2 = letraDec * (k**b) % p
            # Hacemos el set de la letra Eg
            letraEg = [letraEg1, letraEg2]
            # Y lo metemos al mensaje
            textoEg.append(letraEg)
        elif letra.isspace():
            textoEg.append("spc")
    return textoEg
            
# Función para descifrar con Elgamal
def descifrado_elgamal(mensaje, clavePrivada, clavePublica):
    # Hacemos las variables
    p = clavePublica[1]
    a = clavePrivada
    mensajeDescrifrado = ""
    # Recorremos la lista que se llama mensaje
    for letra in mensaje:
        # Si es un espacio lo agregamos
        if letra == "spc":
            mensajeDescrifrado = mensajeDescrifrado + " "
        # Si es una letra normal
        else:
            # Sacamos las dos variables del mensaje cifrado
            letraEg1 = letra[0]
            letraEg2 = letra[1]
            # Calculamos la x
            x = (letraEg1 ** a) % p
            # desencriptamos el mensaje
            m = ((letraEg2 * (x ** (p-2))) % p) + 65
            # Luego la transformamos a caracter
            letraEg = chr(m)
            # Lo agregamos al mensaje descrifrado
            mensajeDescrifrado = mensajeDescrifrado + letraEg
    # Retornamos el mensaje descifrado
    return mensajeDescrifrado
        

