import re
from pathlib import Path

def limpiar_linea(lineas_limpias, linea):
    if not linea.strip():
        lineas_limpias.append("")
        return lineas_limpias
    linea = linea.rstrip()
    linea = linea.lower()
    simbolos_validos = r'[^a-zA-ZáéíóúüñÁÉÍÓÚÜÑ.,;:!?¿¡\-\s]'

    linea_limpia = re.sub(simbolos_validos, "", linea)
    linea_limpia = re.sub(r'\s+', ' ', linea_limpia).strip()
    lineas_limpias.append(linea_limpia)
    return lineas_limpias

def limpiar_texto():
    ruta_don_quijote = Path(__file__).parent.parent / "textos" / "el_quijote.txt"

    with open(ruta_don_quijote ,"r", encoding="utf-8") as don_quijote:
        lineas_limpias = []
        for linea in don_quijote:
            lineas_limpias = limpiar_linea(lineas_limpias, linea)
        lineas_limpias = "\n".join(lineas_limpias)
        return lineas_limpias