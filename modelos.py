from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin  

db = SQLAlchemy()

class Terreno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lote = db.Column(db.String(50), unique=True, nullable=False)
    cpf = db.Column(db.String(11), unique=False, nullable=False)
    nome_completo = db.Column(db.String(100), nullable=False)

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Diretoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    cargo = db.Column(db.String(50), unique=False, nullable=False)
    nome_completo = db.Column(db.String(100), nullable=False)
    imagem = db.Column(db.LargeBinary, nullable=True)

class Tesouraria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    terreno_id = db.Column(db.Integer, db.ForeignKey('terreno.id'), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.Date, nullable=False)
    tipo_contribuicao = db.Column(db.String(50), nullable=False)
    observacao = db.Column(db.String(200), nullable=True)
