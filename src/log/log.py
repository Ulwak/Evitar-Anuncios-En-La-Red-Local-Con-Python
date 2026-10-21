import logging
from pathlib import Path

ruta_logs = Path(__file__).parent.parent.parent / "logs"
ruta_logs.mkdir(parents=True, exist_ok=True)

registro_logs = {
    "red": "red.log",
    "conexiones": "conexiones.log",
    "database": "database.log",
    "ejecucion": "ejecucion.log",
    "duracion": "duracion.log",
    "puerto": "puerto.log"
}

def crear_logs():
    logs = {}
    for nombre, archivo in registro_logs.items():
        #crea el log
        log = logging.getLogger(nombre)
        #define el nivel del log
        log.setLevel(logging.INFO)
        #comprueba si ya hay handlers del log para evitar duplicado
        if not log.hasHandlers():
        
            escritor = logging.FileHandler(
                ruta_logs / archivo,
                encoding="utf-8"
            )

            formato = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(message)s"
            )

            escritor.setFormatter(formato)
            log.addHandler(escritor)
        
        logs[nombre] = log
    return logs
        