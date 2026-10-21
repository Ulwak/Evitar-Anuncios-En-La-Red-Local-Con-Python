import sqlite3
import logging
from pathlib import Path

log_db = logging.getLogger("database")

ruta_db = Path(__file__).parent.parent.parent / "database" / "registro.db"

def conectar_db():
    conectado = sqlite3.connect(ruta_db)
    guia = conectado.cursor()
    return guia, conectado

def desconectar_db(conectado):
    conectado.close()

def iniciar_db():
    ruta_sql = Path(__file__).parent.parent.parent / "database" / "registro.sql"
    
    guia = conectar_db()

    with open(ruta_sql, "r") as sql:
        codigo_sql = sql.read()

    guia[0].executescript(codigo_sql)
    
    guia[1].commit()
    desconectar_db(guia[1])