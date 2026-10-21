from pathlib import Path
from dnslib import DNSRecord
import logging

log_conexiones = logging.getLogger("conexiones")

dominios = set()

def cargar_lista():
    ruta_lista = Path(__file__).parent.parent.parent / "lista_dns_prohibidos" / "lista.txt"

    with open(ruta_lista, "r", encoding="utf-8") as lista:
        contenido = lista.read()

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
    paquete = DNSRecord.parse(datos)
    dominio = str(paquete.question.qname).lower().split(".")
    for i in range(len(dominio) - 1):
        prueba = ".".join(dominio[i:])
        if prueba in set_dominios:
            log_conexiones.info(f"Se bloqueo el dominio: {dominio}")
            return False, paquete.header.id
    log_conexiones.info(f"Se permitio la conexion al dominio: {dominio}")
    return True, paquete.header.id