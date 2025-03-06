from app import db  # db ya está inicializado en __init__.py

class Curp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido_paterno = db.Column(db.String(100), nullable=False)
    apellido_materno = db.Column(db.String(100), nullable=True)
    fecha_nacimiento = db.Column(db.String(10), nullable=False)
    genero = db.Column(db.String(1), nullable=False)
    estado_nacimiento = db.Column(db.String(50), nullable=False)
    curp = db.Column(db.String(18), nullable=False, unique=True)

    def __repr__(self):
        return f'<Curp {self.curp}>'
