"""
Módulo de utilidades para gestionar cookies encriptadas
Similar al ejemplo proporcionado
"""
import hashlib

def encriptar_sha256(cadena):
    """
    Encripta una cadena usando SHA256
    Similar al ejemplo proporcionado
    """
    if not cadena:
        return None
    cadbytes = cadena.encode('utf-8')
    sha256_hash_object = hashlib.sha256()
    sha256_hash_object.update(cadbytes)
    hex_digest = sha256_hash_object.hexdigest()
    return hex_digest

def establecer_cookie_encriptada(response, nombre_cookie, valor):
    """
    Establece una cookie encriptada en la respuesta
    Similar al ejemplo: resp.set_cookie('username', encriptar_sha256(username))
    """
    if valor:
        valor_encriptado = encriptar_sha256(str(valor))
        response.set_cookie(nombre_cookie, valor_encriptado)
    return response

def obtener_cookie_encriptada(request, nombre_cookie):
    """
    Obtiene una cookie encriptada de la petición
    Nota: Las cookies encriptadas con SHA256 no se pueden desencriptar
    ya que es un hash unidireccional. Se usan para comparación.
    """
    return request.cookies.get(nombre_cookie)

