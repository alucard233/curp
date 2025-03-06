# __init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()  # Definir la instancia aquí

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)  # Inicializar db con la app

    from app.routes import curp_bp  # Importar después de crear la app y db
    app.register_blueprint(curp_bp)

    with app.app_context():
        db.create_all()

    return app
