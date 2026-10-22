import sqlite3
import logging
from pathlib import Path

log_db = logging.getLogger("database")

ruta_db = Path(__file__).parent.parent.parent / "Base-Registros-Conexiones" / "registro.db"

def conectar_db():
    conectado = sqlite3.connect(ruta_db)
    guia = conectado.cursor()
    return guia, conectado

def desconectar_db(conectado):
    conectado.close()

def iniciar_db():
    ruta_sql = Path(__file__).parent.parent.parent / "Base-Registros-Conexiones" / "registro.sql"
    
    guia = conectar_db()

    with open(ruta_sql, "r") as sql:
        codigo_sql = sql.read()

    guia[0].executescript(codigo_sql)
    
    guia[1].commit()
    desconectar_db(guia[1])

def obtener_dispositivos():
    guia = conectar_db()
    try:
        guia[0].execute("SELECT Dispositivo, ID FROM dispositivos")
        lista = guia[0].fetchall()
        return dict(lista)
    except Exception as error_db:
        log_db.exception(f"Ocurrio un error mientras se obtenian los dispositivos: {error_db}")
    finally:
        desconectar_db(guia[1])

def registrar_dispositivos(ip):
    guia = conectar_db()
    try:
        guia[0].execute("INSERT INTO dispositivos (Dispositivo) VALUES (?)", (ip, ))
        guia[1].commit()
    except Exception as error_db:
        log_db.exception(f"Ocurrio un error mientras se registraban los dispositivos: {error_db}")
    finally:
        desconectar_db(guia[1])

def registrar_dominios(lista_de_tupla_con_los_datos):
    guia = conectar_db()
    try:
        guia[0].executemany("INSERT INTO conexiones (Dominio, Fecha_Consulta, Bloqueado, Dispositivo) VALUES (?, ?, ?, ?)", lista_de_tupla_con_los_datos)
        guia[1].commit()
    except Exception as error_db:
        log_db.exception(f"Ocurrio un error mientras se registraban los dominios: {error_db}")
    finally:
        desconectar_db(guia[1])

def obtener_cantidad_dominios_dispositivo(diccionario_dispositivos):
    guia = conectar_db()
    try:
        for id in diccionario_dispositivos.values():
            guia[0].execute("SELECT ID, Dominio FROM conexiones WHERE Dispositivo = ?", (id, ))
            lista_dominios = dict(guia[0].fetchall())
        return lista_dominios
    except Exception as error_db:
        log_db.exception(f"Ocurrio un error mientras se obtenian la cantidad de dominios por dispositivo: {error_db}")
    finally:
        desconectar_db(guia[1])