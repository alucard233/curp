# curp_generator.py
import unicodedata
import re

ESTADOS = {
    "AGUASCALIENTES": "AS",
    "BAJA CALIFORNIA": "BC",
    "BAJA CALIFORNIA SUR": "BS",
    "CAMPECHE": "CC",
    "COAHUILA": "CL",
    "COLIMA": "CM",
    "CHIAPAS": "CS",
    "CHIHUAHUA": "CH",
    "CDMX": "DF",
    "DURANGO": "DG",
    "GUANAJUATO": "GT",
    "GUERRERO": "GR",
    "HIDALGO": "HG",
    "JALISCO": "JC",
    "MÉXICO": "MC",
    "MICHOACÁN": "MN",
    "MORELOS": "MS",
    "NAYARIT": "NT",
    "NUEVO LEÓN": "NL",
    "OAXACA": "OC",
    "PUEBLA": "PL",
    "QUERÉTARO": "QT",
    "QUINTANA ROO": "QR",
    "SAN LUIS POTOSÍ": "SP",
    "SINALOA": "SL",
    "SONORA": "SR",
    "TABASCO": "TC",
    "TAMAULIPAS": "TS",
    "TLAXCALA": "TL",
    "VERACRUZ": "VZ",
    "YUCATÁN": "YN",
    "ZACATECAS": "ZS"
}

def limpiar_texto(texto):
    texto = texto.upper()
    texto = unicodedata.normalize("NFKD", texto).encode("ASCII", "ignore").decode("utf-8")
    return re.sub(r"[^A-Z]", "", texto)

def obtener_primera_consonante_interna(texto):
    # Busca la primera consonante después de la primera letra
    consonantes = "BCDFGHJKLMNPQRSTVWXYZ"
    for letra in texto[1:]:  # Ignora la primera letra
        if letra in consonantes:
            return letra
    return "X"  # Si no hay consonantes internas, usa "X"

def generar_curp(nombre, apellido_paterno, apellido_materno, fecha_nacimiento, genero, estado):
    nombre = limpiar_texto(nombre)
    apellido_paterno = limpiar_texto(apellido_paterno)
    apellido_materno = limpiar_texto(apellido_materno if apellido_materno else "X")
    
    # Parte inicial del CURP
    curp = (
        apellido_paterno[0] +  # Primera letra del apellido paterno
        (re.search(r"[AEIOU]", apellido_paterno[1:]).group(0) if re.search(r"[AEIOU]", apellido_paterno[1:]) else "X") +  # Primera vocal interna
        (apellido_materno[0] if apellido_materno else "X") +  # Primera letra del apellido materno
        nombre[0] +  # Primera letra del nombre
        fecha_nacimiento[2:4] +  # Año (2 dígitos)
        fecha_nacimiento[5:7] +  # Mes
        fecha_nacimiento[8:10] +  # Día
        genero.upper() +  # Género (H o M)
        ESTADOS.get(estado.upper(), "NE")  # Código del estado
    )

    # Agregar las consonantes internas
    curp += (
        obtener_primera_consonante_interna(apellido_paterno) +  # Primera consonante interna del apellido paterno
        obtener_primera_consonante_interna(apellido_materno) +  # Primera consonante interna del apellido materno
        obtener_primera_consonante_interna(nombre)  # Primera consonante interna del nombre
    )

    # Agregar los últimos dos dígitos (por ahora "00", en un CURP real se calculan)
    curp += "00"

    return curp