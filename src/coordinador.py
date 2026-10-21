from log.log import crear_logs
from database.creador_db import iniciar_db
from receptor.receptor import recibir_datos
from filtros.filtrador import cargar_lista, filtrar

logs = crear_logs()

try:
    iniciar_db()
except Exception as error_db:
    logs["database"].exception(f"Error al iniciar la base de datos: {error_db}")


dominios = cargar_lista()

for datos, ip, puerto in recibir_datos():
    valido, id = filtrar(dominios, datos)
    if valido:
        pass
    