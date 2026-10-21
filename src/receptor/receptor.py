import socket
import logging

log_red = logging.getLogger("red")

def recibir_datos():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as puerto:
        try:
            puerto.bind(("0.0.0.0", 53))
        except Exception as error_red:
            log_red.exception(f"Ocurrio un error de red: {error_red}")

        while True:
            datos, direccion = puerto.recvfrom(4096)
            log_red.info(f"Recibidos datos desde la direccion: {direccion[0], " ", direccion[1]}")
            yield datos, direccion[0], direccion[1]
