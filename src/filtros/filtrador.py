import logging
from datetime import datetime
from pathlib import Path
from dnslib import DNSRecord

log_conexiones = logging.getLogger("conexiones")
log_ejecucion = logging.getLogger("ejecucion")
dominios = set()
lista_tuplas_dominios = []

def cargar_lista():
    try:
        ruta_lista = Path(__file__).parent.parent.parent / "lista_dns_prohibidos" / "lista.txt"
        with open(ruta_lista, "r", encoding="utf-8") as lista:
            contenido = lista.read()
    except Exception as error_lista:
        log_ejecucion.exception(f"Se produjo un error al cargar la lista: {error_lista}")
        return None
    for linea in contenido.splitlines():
        if not linea or linea.startswith("#"):
            continue

        partes = linea.split()

        if len(partes) >= 2:
            dominio = partes[1].lower()
            dominios.add(dominio)

        elif len(partes) == 1:
            dominio = partes[0].lower()
            dominios.add(dominio)

    return dominios

def filtrar(set_dominios, datos):
    try:
        paquete = DNSRecord.parse(datos)
        dominio = str(paquete.questions[0].qname).lower().rstrip(".")
        print(f"Recibidos datos de: {dominio}")
    except Exception as error_dns:
        log_conexiones.exception(f"Se produjo un error al procesar el DNS: {error_dns}")
        return False, None, None
    partes_dominio = dominio.split(".")
    for i in range(len(partes_dominio) - 1):
        prueba = ".".join(partes_dominio[i:])
        if prueba in set_dominios:
            log_conexiones.info(f"Se bloqueo el dominio: {dominio}")
            return False, dominio, paquete
    log_conexiones.info(f"Se permitio la conexion al dominio: {dominio}")
    return True, dominio , paquete

def almacenar_consulta_dns(registrar_dominios, dominio, bloqueado, dispositivo):
    tiempo_ahora = datetime.now().isoformat()
    lista_tuplas_dominios.append((dominio, tiempo_ahora, bloqueado, dispositivo))
    if len(lista_tuplas_dominios) >= 30:
        registrar_dominios(lista_tuplas_dominios)
        lista_tuplas_dominios.clear()
