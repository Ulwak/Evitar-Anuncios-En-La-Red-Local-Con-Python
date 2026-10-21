from time import perf_counter
from log.log import crear_logs
from database.creador_db import iniciar_db
from receptor.receptor import recibir_datos

logs = crear_logs()

try:
    iniciar_db()
except Exception as error_db:
    logs["database"].exception(f"Error al iniciar la base de datos: {error_db}")
    
recibir_datos()
