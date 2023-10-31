import json

'''
Aqui al inicio se encuentran los metodos de encriptar
y desencriptar que se solicitaron rellenar, pero mas
adelante se encuentran todos los metodos para enviar
mensajes encriptados y codificados y recibirlos para
decodificarlos y desencriptarlos uwu.
'''


def encriptar(msg: bytearray, num: int) -> bytearray:
    largo = len(msg)
    desp = largo - num

    # desplazamos los bytes num veces a la derecha
    m_encriptado = msg[desp:] + msg[:desp]

    # Ahora intercambiamos el byte en la pos 0 con el de la pos num
    if largo > num:
        m_encriptado[0], m_encriptado[num] = m_encriptado[num], m_encriptado[0]

    return m_encriptado


def desencriptar(msg: bytearray, num: int):
    # hacemos los pasos al reves
    # hacemos swap
    largo = len(msg)
    if largo > num:
        msg[0], msg[num] = msg[num], msg[0]

    # retornamos a la posicion original
    m_desencriptado = msg[num:] + msg[:num]

    return m_desencriptado


'''
ENCRIPTAR Y CODIFICAR MENSAJE vvvvv
'''


def serializar_diccionario(dictionary: dict) -> bytearray:
    try:
        json_string = json.dumps(dictionary)
        serializado = bytearray(json_string.encode('UTF-8'))
    except TypeError:
        raise 'WA'

    return serializado


'''
En la siguiente parte se codificara
el mensaje encriptado anteriormente.
Usamos metodos distintos para codificar
el num de bloque y el largo pq usan
endians distintos :p
'''


def codificar_largo_mesaje(largo: int) -> bytearray:
    num = bytearray()
    num.extend(int.to_bytes(largo, 4, 'little'))
    return num


def codificar_numero(largo: int) -> bytearray:
    num = bytearray()
    num.extend(int.to_bytes(largo, 4, 'big'))
    return num


def chunks(mensaje: bytearray):
    chunk = 128
    msg = mensaje
    mensaje_codificado = bytearray()
    largo_mensaje = codificar_largo_mesaje(len(mensaje))
    mensaje_codificado.extend(largo_mensaje)

    contador = 0
    for i in range(0, len(msg), chunk):
        # Primero añadimos el numero del bloque
        mensaje_codificado.extend(codificar_numero(contador))
        # añdimos el chunk
        mensaje_codificado.extend(msg[i:i+chunk])

        # Si el chunk no esta lleno rellenamos con null bytes
        if len(msg[i:i+chunk]) != chunk:
            resto = chunk-len(msg[i:i+chunk])
            mensaje_codificado.extend(bytearray(resto))

        contador += 1

    return mensaje_codificado


'''
Resumimos todo en el siguiente metodo para llamar
solo este al encriptar, codificar y mandar cositas al cliente.
'''


def enviar(informacion: dict, num) -> bytearray:
    serializado = serializar_diccionario(informacion)
    encriptado = encriptar(serializado, num)
    codificado = chunks(encriptado)

    return codificado


'''
DECODIFICAR Y DESENCRIPTAR MENSAJE vvvvv
'''

'''
Ahora hay que hacer un poco de reverse engenieering
para decodificar nuestro mensaje encriptado y luego
desencriptarlo.
'''


def desencriptar_largo(msg: bytearray) -> int:
    largo = int.from_bytes(msg[:4], 'little')
    return largo


def decodificar_numero(msg: bytearray) -> int:
    largo = int.from_bytes(msg[:4], 'big')
    return largo


def separar_chunks(msg: bytearray, largo: int) -> bytearray:
    chunk = 128
    # Primero vemos cuantos chunks son en total
    numero_chunks = (largo // chunk) + 1

    # Calculamos la cantidad de bytes del mensaje codificado
    cantidad_bytes = (numero_chunks + 4) * chunk

    # el mensaje ahora no tendra los bytes que indican su largo
    msg = msg[4:]

    # extraemos el mensaje encriptado de los chunks
    m_encriptado = bytearray()
    for i in range(0, cantidad_bytes, 132):
        mensaje_chunk_i = msg[i + 4:i + 132]
        m_encriptado.extend(mensaje_chunk_i)

    # nos deshacemos de los null bytes del final si es q hay
    m_encriptado = m_encriptado[:largo]

    return m_encriptado


'''
Luego de haber decodificado el mensaje lo
desencriptamos.
'''


def deserializar(msg: bytearray) -> dict:
    try:
        deserializado = json.loads(msg)
    except TypeError:
        raise 'AA'

    return deserializado


'''
Igual que con la encriptacion, resumimos
todo en un solo metodo.
'''


def recibir(msg: bytearray, num) -> dict:
    try:
        largo = desencriptar_largo(msg)
        m_encriptado = separar_chunks(msg, largo)
        mensaje_original_serializado = desencriptar(m_encriptado, num)
        mensaje_original = deserializar(mensaje_original_serializado)
    except ValueError:
        mensaje_original = ' '
    return mensaje_original


'''
TEST vvvv
'''

if __name__ == "__main__":
    # Testear encriptar
    N = 1
    msg_original = bytearray(b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x00\x01\x02\x03\x04\x05')
    msg_esperado = bytearray(b'\x01\x05\x02\x03\x04\x05\x06\x07\x08\x09\x00\x01\x02\x03\x04')
    msg_encriptado = encriptar(msg_original, N)
    if msg_encriptado != msg_esperado:
        print("[ERROR] Mensaje escriptado erroneamente")
    else:
        print("[SUCCESSFUL] Mensaje escriptado correctamente")

    # Testear desencriptar
    msg_desencriptado = desencriptar(msg_esperado, N)
    if msg_desencriptado != msg_original:
        print("[ERROR] Mensaje descencriptado erroneamente")
    else:
        print("[SUCCESSFUL] Mensaje descencriptado correctamente")
