from typing import List
import json
from errors import JsonError, SequenceError


def serializar_diccionario(dictionary: dict) -> bytearray:
    try:
        json_string = json.dumps(dictionary)
        caracteres = bytearray(json_string.encode('UTF-8'))
    except TypeError:
        raise JsonError()

    return caracteres


def verificar_secuencia(mensaje: bytearray, secuencia: List[int]) -> None:

    num = max(secuencia)
    largo = len(mensaje)
    if len(secuencia) != len(set(secuencia)) or num >= largo:
        raise SequenceError()
    return None



def codificar_secuencia(secuencia: List[int]) -> bytearray:
    a = bytearray()
    for num in secuencia:
        a.extend(int.to_bytes(num, 2, 'big'))
    return a


def codificar_largo(largo: int) -> bytearray:
    a = bytearray()
    a.extend(int.to_bytes(largo, 4, 'big'))
    return a


def separar_msg(mensaje: bytearray, secuencia: List[int]) -> List[bytearray]:
    m_bytes_secuencia = bytearray()
    m_reducido = bytearray()
    for i in range(len(mensaje)):
        print(mensaje[i])
        if i not in secuencia:
            m_reducido.extend(int.to_bytes((mensaje[i]), 1, 'big'))
    for num in secuencia:
        m_bytes_secuencia.extend(int.to_bytes((mensaje[num]), 1, 'big'))

    return [m_bytes_secuencia, m_reducido]


def encriptar(mensaje: dict, secuencia: List[int]) -> bytearray:
    verificar_secuencia(mensaje, secuencia)

    m_bytes_secuencia, m_reducido = separar_msg(mensaje, secuencia)
    secuencia_codificada = codificar_secuencia(secuencia)

    return (
        codificar_largo(len(secuencia))
        + m_bytes_secuencia
        + m_reducido
        + secuencia_codificada
    )


if __name__ == "__main__":
    original = serializar_diccionario({"tama": 1})
    encriptado = encriptar(original, [1, 5, 10, 3])
    print(original)
    print(encriptado)
