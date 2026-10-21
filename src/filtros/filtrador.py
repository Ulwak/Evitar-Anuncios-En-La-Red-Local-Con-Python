from pathlib import Path
from dnslib import DNSRecord
import logging

log_conexiones = logging.getLogger("conexiones")
log_ejecucion = logging.getLogger("ejecucion")
dominios = set()

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