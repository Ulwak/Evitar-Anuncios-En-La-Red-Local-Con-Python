from log.log import crear_logs
from database.creador_db import iniciar_db
from receptor.receptor import recibir_datos
from filtros.filtrador import cargar_lista, filtrar
from devolvedor.devolvedor import devolvedor_ads, devolvedor_bien
import sys

logs = crear_logs()

try:
    iniciar_db()
except Exception as error_db:
    logs["database"].exception(f"Error al iniciar la base de datos: {error_db}")


dominios = cargar_lista()

if not dominios:
    print("Error al cargar la lista")
    sys.exit()

for datos, ip_puerto, socket in recibir_datos():
    valido, dominio, paquete = filtrar(dominios, datos)
    if paquete and valido:
        devolvedor_bien(socket, datos, ip_puerto, paquete)
    elif paquete:
        devolvedor_ads(socket, ip_puerto, paquete)
    else:
        continue
    