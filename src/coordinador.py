import sys
from log.log import crear_logs
from database.creador_db import iniciar_db
from receptor.receptor import recibir_datos
from filtros.filtrador import cargar_lista, filtrar, almacenar_consulta_dns
from devolvedor.devolvedor import devolvedor_ads, devolvedor_bien
from database.creador_db import obtener_cantidad_dominios_dispositivo, obtener_dispositivos, registrar_dispositivos, registrar_dominios

logs = crear_logs()

def coordinador():
    try:
        iniciar_db()
    except Exception as error_db:
        logs["database"].exception(f"Error al iniciar la base de datos: {error_db}")


    dominios = cargar_lista()

    if not dominios:
        print("Error al cargar la lista")
        sys.exit()

    print("Lista cargada, esperando paquetes")

    for datos, ip_puerto, socket in recibir_datos():
        valido, dominio, paquete = filtrar(dominios, datos)
        diccionario_dispositivos = obtener_dispositivos()
        if ip_puerto[0] not in diccionario_dispositivos:
            registrar_dispositivos(ip_puerto[0])
            diccionario_dispositivos = obtener_dispositivos()
        if paquete and valido:
            devolvedor_bien(socket, datos, ip_puerto, paquete)
            almacenar_consulta_dns(registrar_dominios, dominio, 0, diccionario_dispositivos[ip_puerto[0]])
        elif paquete:
            devolvedor_ads(socket, ip_puerto, paquete)
            almacenar_consulta_dns(registrar_dominios, dominio, 1, diccionario_dispositivos[ip_puerto[0]])
        else:
            continue

if __name__ == "__main__":
    coordinador()