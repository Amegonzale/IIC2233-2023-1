from typing import List
import json
from errors import JsonError, SequenceError


def deserializar_diccionario(mensaje_codificado: bytearray) -> dict:
    try:
        json_string = json.loads(mensaje_codificado)
    except:
        raise JsonError()

    return json_string


def decodificar_largo(mensaje: bytearray) -> int:

    a = int.from_bytes(mensaje[:4], 'big')
    return a


def separar_msg_encriptado(mensaje: bytearray) -> List[bytearray]:
    largo = decodificar_largo(mensaje)

    msg = mensaje[4:largo + 4]

    m_bytes_secuencia = bytearray()
    m_reducido = bytearray()
    secuencia_codificada = bytearray()
    largo_sec = len(mensaje[largo + 4:])

    secuencia_codificada.extend(mensaje[largo_sec+1:])
    m_bytes_secuencia.extend(msg[:largo_sec+1])
    m_reducido.extend(msg[largo_sec:])

    return [m_bytes_secuencia, m_reducido, secuencia_codificada]


def decodificar_secuencia(secuencia_codificada: bytearray) -> List[int]:
    # Completar
    pass


def desencriptar(mensaje: bytearray) -> bytearray:
    # Completar
    pass


if __name__ == "__main__":
    mensaje = bytearray(b'\x00\x00\x00\x04"a}a{tm": 1\x00\x01\x00\x05\x00\n\x00\x03')
    desencriptado = desencriptar(mensaje)
    diccionario = deserializar_diccionario(desencriptado)
    print(diccionario)
