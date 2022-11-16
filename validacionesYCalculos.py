# Importamos el random
import random
# Importamos las matemáticas
import math

# Función para ver si un número es primo
def es_primo(n):
    for i in range(2, n):
        if (n % i) == 0:
            return False
    return True

# Función para calcular el valor de la K.
def calcular_k(g, a, p):
    modulo = (g**a) % p
    return modulo


# Función para ver si un caracter es numérico.
def es_numerico(n):
    if n.isnumeric():
        return True
    else:
        return False


# Función para crear números primos aleatorios
def primo_aleatorio():
    botoncitoSalida = True
    while botoncitoSalida:
        numero = random.randint(300, 1000)
        if es_primo(numero):
            botoncitoSalida = False
            return numero


# Función para crear números primos aleatorios
def numero_aleatorio():
    numero = random.randint(300, 1000)
    return numero

# Función para ver si un número es entero.
def es_entero(n):
    if isinstance(n, int):
        return True
    else:
        return False


# Función para calcular el N del RSA
def calcular_n(p, q):
    n = p * q
    return n


# Función para calcular Phi de N
def calcular_phi_n(p, q):
    phiN = (p - 1) * (q - 1)
    return phiN


# Función para seleccionar un número random
def seleccionar_random_lista(listaNumeros):
    if len(listaNumeros) == 0:
        e = "error"
        return e
    e = random.choice(listaNumeros)
    return e


# Función para el máximo común divisor entre 1 y phi(n)
def maximo_comun_divisor(phiN):
    listaNumeros = []
    for numero in range(1, phiN):
        maxComunDiv = math.gcd(numero, phiN)
        if maxComunDiv == 1:
            listaNumeros.append(numero)
    return listaNumeros


# Función para buscar un número que multiplicado por la
# exponente público nos de 1
def calcular_algoritmo_modular(exponentePublico, phiN):
    listaNumeros = []
    for numero in range(1, phiN):
        if ((exponentePublico * numero) % phiN) == 1:
            listaNumeros.append(numero)
    return listaNumeros

# Función para buscar los raices primitivas
def raices_primitivas(p):
    contador = 0
    raicesPrimitivas = []
    for a in range(1, p):
        contador += 1
        posiblesRaices = []
        for i in range(1, p):
            modulo = (contador ** i) % p
            posiblesRaices.append(modulo)
            setPosiblesRaices = set(posiblesRaices)
            if len(setPosiblesRaices) == len(range(1,p)):
                raicesPrimitivas.append(contador)
    return raicesPrimitivas

print((805727**87)%938477)

# print(calcular_k(68,44,73))