from modelos import db, Usuario
from acepraf import app

with app.app_context():
    db.create_all()  # Certifica-se de que todas as tabelas estão criadas

    # Troque por um nome de usuário e senha adequados e defina a role
    admin = Usuario(username='admin', password='admin')

    db.session.add(admin)
    db.session.commit()

    print("Administrador criado com sucesso!")
