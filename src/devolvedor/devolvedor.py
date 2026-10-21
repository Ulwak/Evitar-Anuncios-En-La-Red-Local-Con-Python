import socket
from dnslib import DNSRecord, QTYPE, RR, A, RCODE
import logging

log_red = logging.getLogger("red")
log_conexiones = logging.getLogger("conexiones")

def devolvedor_bien(socket_usuario, datos, ip_puerto, paquete):
    dns_cloudfare = ("1.1.1.1", 53)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as socket_cloudfare:
        socket_cloudfare.settimeout(2.0)
        intentos = 0
        enviado = False
        while intentos != 3:
            try:
                socket_cloudfare.sendto(datos, dns_cloudfare)
                datos, _ = socket_cloudfare.recvfrom(4096)
                socket_usuario.sendto(datos, ip_puerto)
                enviado = True
                break
            except Exception as error_conexion:
                log_conexiones.exception(f"Hubo un error al conectar con cloudfare: {error_conexion}")
                intentos += 1
        if enviado:
            return
        else:
            respuesta = paquete.reply()
            respuesta.header.rcode = RCODE.SERVFAIL

            try:
                socket_usuario.sendto(respuesta.pack(), ip_puerto)
            except Exception as error_red:
                log_conexiones.exception(f"Hubo un error al enviar el codigo de error: {error_red}")
        
def devolvedor_ads(socket__, ip_puerto, paquete):

    respuesta = paquete.reply()

    respuesta.add_answer(RR(
        rname=respuesta.q.qname,  
        rtype=QTYPE.A,           
        rdata=A("0.0.0.0"),      
        ttl=3600                   
    ))

    try:
        socket__.sendto(respuesta.pack(), ip_puerto)
    except Exception as error_red:
        log_red.exception(f"Se produjo un error al devolver el paquete: {error_red}")