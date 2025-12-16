import re

def validar_telefono(telefono):
    patron = r"^[0-9 +-]+$"
    return re.match(patron, telefono) is not None

def validar_nombre(nombre):
    return bool(nombre and nombre.strip())


