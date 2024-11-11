from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from modelos import db, Terreno, Usuario, Diretoria,Tesouraria
from sqlalchemy.sql import func
import logging
from datetime import datetime
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
    return redirect(url_for('terrenos'))

@app.route('/admin',methods=['GET','POST'])
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


@app.route('/admin/atualiza_membro_diretoria', methods=['GET', 'POST'])
def atualiza_membro_diretoria():
    if request.method == 'POST':
        cargo = request.form['cargo']
        cpf = request.form['cpf']
        nome_completo = request.form['nome_completo']
        imagem = request.files['imagem'].read() if 'imagem' in request.files else None

        membro = Diretoria.query.filter_by(cargo=cargo).first()
        if membro:
            membro.cpf = cpf  # Atualiza o CPF do membro da diretoria caso haja mudança
            membro.nome_completo = nome_completo  # Atualiza o nome do membro da diretoria
            if imagem:
                membro.imagem = imagem
            else:
                # Exclui a imagem antiga caso não haja nova imagem
                membro.imagem = None
        else:
            novo_membro = Diretoria(
                cargo=cargo,
                cpf=cpf,
                nome_completo=nome_completo,
                imagem=imagem
            )
            db.session.add(novo_membro)
        db.session.commit()
        return redirect(url_for('atualiza_membro_diretoria'))

    return render_template('cadastro_diretoria.html')

@app.route('/admin/tesouraria')
@login_required
def tesouraria():
    return render_template('tesouraria.html')

@app.route('/registrar_contribuicao', methods=['GET', 'POST'])
def registrar_contribuicao():
    tipos_contribuicao_padrao = ['Água', 'Estradas', 'Manutenção','Mensalidade da associação']
    if request.method == 'POST':
        terreno_id = request.form['terreno_id']
        valor = float(request.form['valor'])
        data = datetime.strptime(request.form['data'], '%Y-%m-%d')
        tipo_contribuicao = request.form['tipo_contribuicao']
        observacao = request.form['observacao']

        nova_contribuicao = Tesouraria(
            terreno_id=terreno_id,
            valor=valor,
            data=data,
            tipo_contribuicao=tipo_contribuicao,
            observacao=observacao
        )
        db.session.add(nova_contribuicao)
        db.session.commit()
        return redirect(url_for('registrar_contribuicao'))

    terrenos = Terreno.query.all()
    return render_template('registrar_contribuicao.html', terrenos=terrenos, tipos_contribuicao_padrao=tipos_contribuicao_padrao)



@app.route('/visualizar_contribuicoes', methods=['GET', 'POST'])
def visualizar_contribuicoes():
    tipos_contribuicao_padrao = ['Água', 'Estradas', 'Manutenção']
    contribuicoes = None
    if request.method == 'POST':
        tipo_contribuicao = request.form['tipo_contribuicao']
        mes = request.form['mes']
        ano = request.form['ano']
        
        inicio_mes = f'{ano}-{mes}-01'
        fim_mes = f'{ano}-{mes}-31'

        contribuicoes = Tesouraria.query.filter(
            Tesouraria.tipo_contribuicao == tipo_contribuicao,
            Tesouraria.data.between(inicio_mes, fim_mes)
        ).all()

    return render_template('visualizar_contribuicoes.html', contribuicoes=contribuicoes, tipos_contribuicao_padrao=tipos_contribuicao_padrao)

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

@app.route('/admin/deletar_terreno', methods=['GET', 'POST'])
@login_required
def listar_terrenos_para_deletar():
    busca = request.form.get('busca')
    if busca:
        terrenos = Terreno.query.filter(Terreno.lote.contains(busca)).order_by(Terreno.lote).all()
    else:
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

@app.route('/diretoria')
def diretoria ():
    membro_diretoria = Diretoria.query.all()
    return render_template('diretoria.html')


# Função para criar as tabelas
def init_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    init_db()  # Cria as tabelas antes de iniciar o servidor
    app.run(debug=True)
