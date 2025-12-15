from datetime import date, datetime

def formatear_fecha(fecha):
    if isinstance(fecha, (date, datetime)):
        return fecha.strftime("%d/%m/%Y")
    return str(fecha)
