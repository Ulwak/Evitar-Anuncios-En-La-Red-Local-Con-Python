import socket
import logging

log_red = logging.getLogger("red")

def recibir_datos():
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as puerto:
            try:
                #por si alguien lee esto debe usar ipconfig en un cmd, verificar el ipv4 de su maquina
                #y reemplazar 192.168.100.27 por el numero que tengas en tu caso.
                #no remover las comillas solo reemplazar el numero dentro
                puerto.bind(("192.168.100.27", 53))
                log_red.info("Se creo el puerto para las conexiones")
            except Exception as error_red:
                log_red.exception(f"Ocurrio un error al crear el puerto: {error_red}")
                continue
            while True:
                try:
                    datos, direccion = puerto.recvfrom(4096)
                except Exception as error_red:
                    log_red.exception(f"Ocurrio un error de red al recibir el paquete: {error_red}")
                    continue
                log_red.info(f"Recibidos datos desde la direccion: {direccion[0]} {direccion[1]}")
                yield datos, direccion, puerto
