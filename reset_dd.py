from flask import Flask
from modelos import db, Terreno, Usuario, Diretoria, Tesouraria

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///terrenos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    # Drop all tables
    db.drop_all()
    print("Todas as tabelas foram removidas!")

    # Create all tables
    db.create_all()
    print("Todas as tabelas foram criadas com sucesso!")
