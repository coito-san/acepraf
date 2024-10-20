from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Terreno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lote = db.Column(db.String(50), unique=True, nullable=False)
    cpf = db.Column(db.String(11), nullable=False)
    nome_completo = db.Column(db.String(100), nullable=False)

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    
