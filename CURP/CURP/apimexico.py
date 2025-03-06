from flask import Flask, request, jsonify
import re
import unicodedata

app = Flask(__name__)

# Códigos de estados de nacimiento en México
ESTADOS = {
    "AGUASCALIENTES": "AS", "BAJA CALIFORNIA": "BC", "BAJA CALIFORNIA SUR": "BS",
    "CAMPECHE": "CC", "COAHUILA": "CL", "COLIMA": "CM", "CHIAPAS": "CS", "CHIHUAHUA": "CH",
    "CIUDAD DE MÉXICO": "DF", "DURANGO": "DG", "GUANAJUATO": "GT", "GUERRERO": "GR",
    "HIDALGO": "HG", "JALISCO": "JC", "MÉXICO": "MC", "MICHOACÁN": "MN",
    "MORELOS": "MS", "NAYARIT": "NT", "NUEVO LEÓN": "NL", "OAXACA": "OC",
    "PUEBLA": "PL", "QUERÉTARO": "QT", "QUINTANA ROO": "QR", "SAN LUIS POTOSÍ": "SP",
    "SINALOA": "SL", "SONORA": "SR", "TABASCO": "TC", "TAMAULIPAS": "TS",
    "TLAXCALA": "TL", "VERACRUZ": "VZ", "YUCATÁN": "YN", "ZACATECAS": "ZS",
    "NACIDO EN EL EXTRANJERO": "NE"
}

# Función para eliminar acentos y normalizar texto
def normalizar_texto(texto):
    texto = texto.upper()
    texto = ''.join(c for c in unicodedata.normalize('NFKD', texto) if unicodedata.category(c) != 'Mn')
    texto = re.sub(r'[^A-Z ]', '', texto)  # Solo letras y espacios
    return texto

# Función para obtener la primera vocal interna de una palabra
def obtener_primera_vocal(palabra):
    for letra in palabra[1:]:  # Ignoramos la primera letra
        if letra in "AEIOU":
            return letra
    return "X"  # Si no hay vocal, usa "X"

# Generador de CURP (sin los últimos dos dígitos verificadores)
def generar_curp(nombre, apellido_paterno, apellido_materno, fecha_nac, genero, estado):
    nombre = normalizar_texto(nombre)
    apellido_paterno = normalizar_texto(apellido_paterno)
    apellido_materno = normalizar_texto(apellido_materno)
    estado = normalizar_texto(estado)

    if estado not in ESTADOS:
        return None, "Estado de nacimiento inválido"

    # Primera letra y primera vocal del apellido paterno
    curp = apellido_paterno[0] + obtener_primera_vocal(apellido_paterno)
    # Primera letra del apellido materno (si no tiene, usa "X")
    curp += apellido_materno[0] if apellido_materno else "X"
    # Primera letra del primer nombre (evita nombres de uso común como "MARIA" y "JOSE")
    nombres_omitidos = ["MARIA", "JOSE"]
    partes_nombre = nombre.split()
    if len(partes_nombre) > 1 and partes_nombre[0] in nombres_omitidos:
        curp += partes_nombre[1][0]
    else:
        curp += nombre[0]

    # Fecha de nacimiento en formato AAMMDD
    curp += fecha_nac[2:4] + fecha_nac[5:7] + fecha_nac[8:10]
    
    # Género (H para Hombre, M para Mujer)
    curp += genero.upper()

    # Código de estado de nacimiento
    curp += ESTADOS[estado]

    # Primera consonante interna del apellido paterno
    curp += siguiente_consonante(apellido_paterno)
    # Primera consonante interna del apellido materno
    curp += siguiente_consonante(apellido_materno) if apellido_materno else "X"
    # Primera consonante interna del primer nombre
    curp += siguiente_consonante(nombre)

    # Los dos últimos dígitos verificadores los dejamos en "00"
    curp += "00"

    return curp, None

# Función para obtener la primera consonante interna de una palabra
def siguiente_consonante(palabra):
    for letra in palabra[1:]:  # Ignoramos la primera letra
        if letra in "BCDFGHJKLMNPQRSTVWXYZ":
            return letra
    return "X"  # Si no hay consonante interna, usa "X"

@app.route('/generar_curp', methods=['POST'])
def generar_curp_endpoint():
    try:
        data = request.get_json()

        # Validación de datos
        required_fields = ["nombre", "apellido_paterno", "apellido_materno", "fecha_nacimiento", "genero", "estado_nacimiento"]
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"Falta el campo {field}"}), 400

        curp, error = generar_curp(
            data["nombre"],
            data["apellido_paterno"],
            data["apellido_materno"],
            data["fecha_nacimiento"],
            data["genero"],
            data["estado_nacimiento"]
        )

        if error:
            return jsonify({"error": error}), 400

        return jsonify({"curp": curp})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
