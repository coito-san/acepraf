from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from modelos import db, Terreno, Usuario
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///terrenos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/')
def index():
    return redirect(url_for('terrenos'))

@app.route('/terrenos')
def terrenos():
    page = request.args.get('page', 1, type=int)
    terrenos_paginados = Terreno.query.order_by(Terreno.lote).paginate(page=page, per_page=20)
    return render_template('terrenos.html', terrenos=terrenos_paginados.items, pagination=terrenos_paginados)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Usuario.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('admin'))
        else:
            flash('Login inválido. Por favor, tente novamente.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin')
@login_required
def admin():
    page = request.args.get('page', 1, type=int)
    terrenos_paginados = Terreno.query.paginate(page=page, per_page=20)
    return render_template('admin.html', terrenos=terrenos_paginados.items, pagination=terrenos_paginados)

@app.route('/admin/cadastro', methods=['GET', 'POST'])
@login_required
def cadastro():
    if request.method == 'POST':
        lote = request.form['lote']
        cpf = request.form['cpf']
        nome_completo = request.form['nome_completo']
        terreno = Terreno.query.filter_by(lote=lote).first()
        if terreno:
            terreno.cpf = cpf  # Atualiza o CPF do dono existente
            terreno.nome_completo = nome_completo  # Atualiza o nome do dono
        else:
            novo_terreno = Terreno(lote=lote, cpf=cpf, nome_completo=nome_completo)
            db.session.add(novo_terreno)
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('cadastro.html')

@app.route('/admin/cadastro_usuario', methods=['GET', 'POST'])
@login_required
def cadastro_usuario():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        novo_usuario = Usuario(username=username, password=password)
        db.session.add(novo_usuario)
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('cadastro_usuario.html')

@app.route('/admin/deletar_terreno')
@login_required
def listar_terrenos_para_deletar():
    terrenos = Terreno.query.order_by(Terreno.lote).all()
    return render_template('deletar_terrenos.html', terrenos=terrenos)

@app.route('/admin/deletar_terreno/<int:id>', methods=['POST'])
@login_required
def deletar_terreno(id):
    terreno = Terreno.query.get(id)
    if terreno:
        db.session.delete(terreno)
        db.session.commit()
        flash('Terreno excluído com sucesso!')
    else:
        flash('Terreno não encontrado.')
    return redirect(url_for('listar_terrenos_para_deletar'))

# Função para criar as tabelas
def init_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    init_db()  # Cria as tabelas antes de iniciar o servidor
    app.run(debug=True)
