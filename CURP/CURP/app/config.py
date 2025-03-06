# config.py
class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123456@localhost:5432/mexico'  # Replace with your PostgreSQL credentials
    SQLALCHEMY_TRACK_MODIFICATIONS = False