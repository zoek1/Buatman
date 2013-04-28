from http.cookiejar import Cookie
from http.cookiejar import CookieJar
import urllib.error
import urllib.request
import re

'''
Verificacion de los servicios de red.
'''

def checkRed(url, tiempoEspera):
    try:
        urllib.request.urlopen(url, None, tiempoEspera)
    except urllib.error.URLError as coneccionError:
        return False
    
    return True



# Verificacion de cookie
re_sseid = re.compile(r'^SESSID=(?i)[A-Z0-9]{19}=$')


def crearCookie(nombre, valor, dominio, ruta):
    """Creacion de cookie.
    
    @param: 
        nombre: Clave de la cookie
        valor: Valor de la cookie
        dominio: dominio asigando a la cookie
        ruta: ruta de la cookie

    @return: cookie
    """
    return Cookie(
        version=0,
        name=nombre,
        value=valor,
        port=None,
        port_specified=False,
        domain=dominio,
        domain_specified=True,
        domain_initial_dot=False,
        path=ruta,
        path_specified=True,
        secure=False,
        expires=None,
        discard=False,
        comment=None,
        comment_url=None,
        rest=None
    )
 

def enviaPeticion(url, dominio, ruta, cookieDicc={"TESTID": "set"}):
    try:
        # Empaquetador de cookies.
        jar = CookieJar()
        # Genera un objeto request para posterior peticion.
        peticion = urllib.request.Request(url=url)
        
        # crearCookie to generate a cookie and add it to the cookie jar.
        for key, item in cookieDicc.items():
            jar.set_cookie(crearCookie(key, item, dominio, ruta))

        # print(crearCookie(key, item))

        jar.add_cookie_header(peticion)
 
        # Generar peticion.
        edmundoDantes = urllib.request.build_opener()
        abreteSesamo = edmundoDantes.open(peticion)
    
        RiquezaYVenganza = verificacionAcceso(abreteSesamo)

        if RiquezaYVenganza:
            print( "Busca tu propio Arbol")
        else:
            print( "!(Busca tu propio arbol)")

        return RiquezaYVenganza
    except urllib.error.HTTPError as err:
        print("Pagina fuera de servicio")
        return "Pagina fuera de servicio"

def verificacionAcceso(respuesta):
    print("La respuesta del server es: ")
    # print(respuesta.headers)
    SSEID=respuesta.headers['set-cookie']

    re_sseid.match(SSEID)
    # print(SSEID)
    return True if re_sseid.search(SSEID) else False


if __name__ == "__main__":
    import data
    print(checkRed('http://www.google.com', 1))
    print(enviaPeticion(data.manejadorDatos.urlBase + 
                        data.manejadorDatos.fragmentoLogin + "?sid=201024269&PIN=Jet%27aimemonique" ,
                        data.manejadorDatos.urlBase[7:],
                        data.manejadorDatos.ruta))
