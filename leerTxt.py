# Este archivo se encarga de leer los archivos txt y compararlos

def leer_texto(archivo):
    txtEntrada = open(archivo, 'r', encoding='utf-8')
    mensajeEntrada = str(txtEntrada.read())
    txtEntrada.close()
    return mensajeEntrada


def escribir_texto_salida(texto):
    txtSalida = open('mensajerecibido.txt', 'w', encoding='utf-8')
    txtSalida.write(texto)
    txtSalida.close()
    return texto
