from flask import Blueprint, request, jsonify
from app.curp_generator import generar_curp
from app.models import Curp
from app import db  # Importa db correctamente

curp_bp = Blueprint('curp', __name__)

@curp_bp.route('/generar_curp', methods=['POST'])
def generar_curp_api():
    data = request.json
    nombre = data.get("nombre")
    apellido_paterno = data.get("apellido_paterno")
    apellido_materno = data.get("apellido_materno")
    fecha_nacimiento = data.get("fecha_nacimiento")
    genero = data.get("genero")
    estado_nacimiento = data.get("estado_nacimiento")

    if not all([nombre, apellido_paterno, fecha_nacimiento, genero, estado_nacimiento]):
        return jsonify({"error": "Faltan datos"}), 400

    curp = generar_curp(nombre, apellido_paterno, apellido_materno, fecha_nacimiento, genero, estado_nacimiento)

    nuevo_curp = Curp(
        nombre=nombre,
        apellido_paterno=apellido_paterno,
        apellido_materno=apellido_materno,
        fecha_nacimiento=fecha_nacimiento,
        genero=genero,
        estado_nacimiento=estado_nacimiento,
        curp=curp
    )

    try:
        db.session.add(nuevo_curp)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al guardar en la base de datos: {str(e)}"}), 500

    return jsonify({"curp": curp}), 200
