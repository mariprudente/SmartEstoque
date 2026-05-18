from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/img'
app.config['SECRET_KEY'] = 'your-secret-key'

# =====================================
# CONFIG BANCO (Versão MySQL)
# =====================================
# senha usada no Workbench

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:PISmartEstoque%402026@localhost/smartestoque'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

UPLOAD_FOLDER = 'static/img' 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# =====================================
# MODELS (Estrutura das Tabelas)
# =====================================

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    nome = db.Column(db.String(100))
    role = db.Column(db.String(20), default='vendedor') 
    
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    cpf = db.Column(db.String(20))
    rg = db.Column(db.String(20))
    nascimento = db.Column(db.String(20))
    rua = db.Column(db.String(150))
    numero = db.Column(db.String(10))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(50))
    telefone = db.Column(db.String(20))
    celular = db.Column(db.String(20))
    email = db.Column(db.String(120))

class Fornecedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    razao_social = db.Column(db.String(150))
    cnpj = db.Column(db.String(20))
    contato = db.Column(db.String(100))
    cep = db.Column(db.String(10))
    endereco = db.Column(db.String(150))
    numero = db.Column(db.String(10))
    complemento = db.Column(db.String(50))
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    uf = db.Column(db.String(2))
    telefone = db.Column(db.String(20))
    celular = db.Column(db.String(20))
    email = db.Column(db.String(120))
    observacoes = db.Column(db.Text)
    ativo = db.Column(db.Boolean, default=True)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    ativo = db.Column(db.Boolean)
    marca = db.Column(db.String(100))
    codigo = db.Column(db.String(50))
    preco_compra = db.Column(db.Float)
    preco_venda = db.Column(db.Float)
    estoque = db.Column(db.Integer, default=0)
    estoque_minimo = db.Column(db.Integer, default=5)
    observacoes = db.Column(db.Text)
    foto = db.Column(db.String(200))
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedor.id'))
    fornecedor = db.relationship('Fornecedor')

class Movimentacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'))
    produto = db.relationship('Produto')
    tipo = db.Column(db.String(20))
    quantidade = db.Column(db.Integer)
    data = db.Column(db.String(20))
    observacao = db.Column(db.Text)

class Caixa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    descricao = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(10), nullable=False) 
    valor = db.Column(db.Float, nullable=False)   


# =====================================
# ROTAS DE AUTENTICAÇÃO E SESSÃO
# =====================================

@login_manager.user_loader
def load_user(user_id):
        return db.session.get(Usuario, int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        usuario = Usuario.query.filter_by(username=username).first()
        
        if usuario and check_password_hash(usuario.password, password):
            login_user(usuario)
            
            if password == 'Mudar123':
                flash("Sua senha foi resetada ou este é seu primeiro acesso. Por segurança, altere-a agora.", "aviso")
                return redirect(url_for('alterar_senha'))
            
            if usuario.role == 'admin':
                return redirect(url_for('dashboard'))
            elif usuario.role == 'vendedor':
                return redirect(url_for('vendas'))
            else:
                return redirect(url_for('index'))
                
        return render_template('login.html', erro="Usuário ou senha inválidos")
        
    return render_template('login.html')

@app.route('/alterar_senha', methods=['GET', 'POST'])
@login_required
def alterar_senha():
    if request.method == 'POST':
        nova_senha = request.form.get('nova_senha')
        confirmar_senha = request.form.get('confirmar_senha')
        
        if nova_senha != confirmar_senha:
            return render_template('alterar_senha.html', erro="As senhas não coincidem!")
            
        if nova_senha == 'Mudar123':
            return render_template('alterar_senha.html', erro="Você não pode usar a senha padrão!")
            
        current_user.password = generate_password_hash(nova_senha)
        current_user.primeiro_acesso = False
        db.session.commit()
        
        if current_user.role == 'admin':
            return redirect(url_for('dashboard'))
        elif current_user.role == 'vendedor':
            return redirect(url_for('vendas'))
        else:
            return redirect(url_for('index'))
            
    return render_template('alterar_senha.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# =====================================
# ROTAS DE GESTÃO DE EQUIPA (ADMIN)
# =====================================

@app.route('/usuarios')
@login_required
def gerenciar_usuarios():
    if current_user.role != 'admin':
        return "Acesso negado. Apenas administradores podem gerir a equipa.", 403
    usuarios_lista = Usuario.query.all()
    return render_template('usuarios.html', usuarios=usuarios_lista)


import random

@app.route('/cadastrar_usuario', methods=['POST'])
@login_required
def cadastrar_usuario():
    if current_user.role != 'admin':
        return "Acesso negado.", 403
        
    nome = request.form.get('nome').strip()
    role = request.form.get('role')
    
    if not nome:
        return "O nome é obrigatório.", 400

    partes_nome = nome.split()
    if len(partes_nome) >= 2:
        iniciais = partes_nome[0][0] + partes_nome[-1][0]
    else:
        iniciais = partes_nome[0][:2]
        
    iniciais = iniciais.lower()
    
    while True:
        numero_aleatorio = random.randint(10, 99)
        username_gerado = f"{iniciais}{numero_aleatorio}"
        if not Usuario.query.filter_by(username=username_gerado).first():
            break

    novo_usuario = Usuario(
        username=username_gerado,
        nome=nome,
        role=role,
        password=generate_password_hash('Mudar123')
    )
    
    db.session.add(novo_usuario)
    db.session.commit()
    
    flash(f"Usuário criado com sucesso! LOGIN: {username_gerado} | SENHA PADRÃO: Mudar123", "sucesso")
    return redirect(url_for('gerenciar_usuarios'))

@app.route('/deletar_usuario/<int:user_id>', methods=['POST'])
@login_required
def deletar_usuario(user_id):
    if current_user.role != 'admin':
        flash("Acesso negado. Permissão exclusiva do administrador.", "erro")
        return redirect(url_for('gerenciar_usuarios'))
        
    usuario = db.session.get(Usuario, user_id)
    
    if usuario:
        if usuario.id == current_user.id or usuario.username == 'admin':
            flash("Operação inválida! Você não pode remover o administrador principal do sistema.", "erro")
            return redirect(url_for('gerenciar_usuarios'))
            
        nome_deletado = usuario.nome
        db.session.delete(usuario)
        db.session.commit()
        flash(f"Usuário '{nome_deletado}' foi removido do sistema com sucesso.", "sucesso")
    else:
        flash("Usuário não encontrado.", "erro")
        
    return redirect(url_for('gerenciar_usuarios'))


@app.route('/resetar_senha/<int:user_id>', methods=['POST'])
@login_required
def resetar_senha(user_id):
    if current_user.role != 'admin':
        return "Acesso negado.", 403
        
    usuario = db.session.get(Usuario, user_id)
    if usuario:
        usuario.password = generate_password_hash('Mudar123')
        db.session.commit()
        flash(f"A senha de {usuario.nome} foi resetada com sucesso para 'Mudar123'!", "sucesso")
        
    return redirect(url_for('gerenciar_usuarios'))

# =====================================
# ROTAS
# =====================================


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/clientes')
def clientes():
    busca = request.args.get("busca")
    if busca:
        clientes = Cliente.query.filter(
            Cliente.nome.contains(busca) | Cliente.cpf.contains(busca)
        ).all()
    else:
        clientes = Cliente.query.all()
    return render_template("clientes.html", clientes=clientes)

@app.route('/salvar_cliente', methods=['POST'])
def salvar_cliente():
    cliente = Cliente(
        nome=request.form['nome'],
        cpf=request.form['cpf'],
        rg=request.form['rg'],
        nascimento=request.form['nascimento'],
        rua=request.form['rua'],
        numero=request.form['numero'],
        cidade=request.form['cidade'],
        estado=request.form['estado'],
        telefone=request.form['telefone'],
        celular=request.form['celular'],
        email=request.form['email']
    )
    db.session.add(cliente)
    db.session.commit()
    return redirect('/clientes')

@app.route('/cliente/<int:id>')
def cliente_detalhe(id):
    cliente = Cliente.query.get(id)
    return render_template("cliente_detalhe.html", cliente=cliente)

@app.route('/excluir_cliente/<int:id>')
def excluir_cliente(id):
    cliente = Cliente.query.get(id)
    db.session.delete(cliente)
    db.session.commit()
    return redirect('/clientes')

@app.route('/atualizar_cliente/<int:id>', methods=['POST'])
def atualizar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    cliente.nome = request.form.get('nome')
    cliente.cpf = request.form.get('cpf')
    cliente.rg = request.form.get('rg')
    cliente.nascimento = request.form.get('nascimento')
    cliente.rua = request.form.get('rua')
    cliente.numero = request.form.get('numero')
    cliente.cidade = request.form.get('cidade')
    cliente.estado = request.form.get('estado')
    cliente.telefone = request.form.get('telefone')
    cliente.celular = request.form.get('celular')
    cliente.email = request.form.get('email')

    try:
        db.session.commit() 
        return redirect('/clientes') 
    except:
        db.session.rollback()
        return "Houve um erro ao atualizar o cliente."

@app.route('/editar_cliente/<int:id>')
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    return render_template('editar_cliente.html', cliente=cliente)    

@app.route('/fornecedores')
def fornecedores():
    busca = request.args.get("busca")
    
    if busca:
        fornecedores = Fornecedor.query.filter(
            Fornecedor.razao_social.contains(busca), 
            Fornecedor.ativo == True 
        ).all()
    else:
        fornecedores = Fornecedor.query.filter_by(ativo=True).all()
        
    return render_template("fornecedores.html", fornecedores=fornecedores)

@app.route('/salvar_fornecedor', methods=['POST'])
def salvar_fornecedor():
    
    fornecedor = Fornecedor(
        razao_social=request.form.get('razao_social'),
        cnpj=request.form.get('cnpj'),
        contato=request.form.get('contato'),
        cep=request.form.get('cep'),
        endereco=request.form.get('endereco'),
        numero=request.form.get('numero'),
        complemento=request.form.get('complemento'), 
        bairro=request.form.get('bairro'),
        cidade=request.form.get('cidade'),
        uf=request.form.get('uf'),
        telefone=request.form.get('telefone'),
        celular=request.form.get('celular'),
        email=request.form.get('email'),
        observacoes=request.form.get('observacoes'),
        ativo=True 
    )
    
    try:
        db.session.add(fornecedor)
        db.session.commit()
    except:
        db.session.rollback()
        return "Erro ao salvar no banco de dados."
        
    return redirect('/fornecedores')

@app.route('/excluir_fornecedor/<int:id>')
def excluir_fornecedor(id):
    fornecedor = db.session.get(Fornecedor, id)
    if fornecedor:
        fornecedor.ativo = False 
        db.session.commit()
    return redirect(url_for('fornecedores'))

@app.route('/fornecedor/<int:id>')
def fornecedor_detalhe(id):
    fornecedor = Fornecedor.query.get(id)
    return render_template("fornecedor_detalhe.html", fornecedor=fornecedor)

@app.route('/editar_fornecedor/<int:id>')
def editar_fornecedor(id):
    fornecedor = Fornecedor.query.get_or_404(id)
    return render_template('editar_fornecedor.html', fornecedor=fornecedor)

@app.route('/atualizar_fornecedor/<int:id>', methods=['POST'])
def atualizar_fornecedor(id):
    fornecedor = Fornecedor.query.get_or_404(id)
    
    fornecedor.razao_social = request.form.get('razao_social')
    fornecedor.cnpj = request.form.get('cnpj')
    fornecedor.inscricao_estadual = request.form.get('inscricao_estadual')
    fornecedor.rua = request.form.get('rua')
    fornecedor.numero = request.form.get('numero')
    fornecedor.cidade = request.form.get('cidade')
    fornecedor.estado = request.form.get('estado')
    fornecedor.telefone = request.form.get('telefone')
    fornecedor.celular = request.form.get('celular')
    fornecedor.email = request.form.get('email')

    try:
        db.session.commit()
        return redirect('/fornecedores')
    except:
        db.session.rollback()
        return "Erro ao atualizar fornecedor."

@app.route('/produtos')
def produtos():
    busca = request.args.get("busca")
    if busca:
        produtos = Produto.query.filter(Produto.nome.contains(busca)).all()
    else:
        produtos = Produto.query.all()
    
    fornecedores = Fornecedor.query.all()
    
    return render_template("produtos.html", produtos=produtos, fornecedores=fornecedores)

@app.route('/salvar_produto', methods=['POST'])
def salvar_produto():
    
    nome = request.form.get('nome')
    marca = request.form.get('marca')
    codigo = request.form.get('codigo')
    arquivo = request.files.get('foto') 
    nome_foto = 'sem-imagem.png'
    if arquivo and arquivo.filename != '':
        filename = secure_filename(arquivo.filename)
        arquivo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        nome_foto = filename
    preco_compra = float(request.form.get('preco_compra', 0).replace(',', '.'))
    preco_venda = float(request.form.get('preco_venda', 0).replace(',', '.'))
    estoque_inicial = int(request.form.get('estoque', 0))
    estoque_minimo = int(request.form.get('estoque_minimo', 5))
    fornecedor_id = request.form.get('fornecedor')
    ativo = True if request.form.get('ativo') else False

    novo_produto = Produto(
        nome=nome,
        marca=marca,
        codigo=codigo,
        preco_compra=preco_compra,
        preco_venda=preco_venda,
        estoque=estoque_inicial,
        estoque_minimo=estoque_minimo,
        fornecedor_id=fornecedor_id,
        ativo=ativo,
        observacoes=request.form.get('observacoes', ''),
        foto=nome_foto
    )

    db.session.add(novo_produto)
    db.session.commit()
    
    return redirect('/produtos')

@app.route('/excluir_produto/<int:id>')
def excluir_produto(id):

    produto = db.session.get(Produto, id)
    
    if produto:
 
        db.session.delete(produto)
        db.session.commit()
    
    return redirect('/produtos')

@app.route('/produto/<int:id>')
def produto_detalhe(id):

    produto = db.session.get(Produto, id)
    return render_template("produto_detalhe.html", produto=produto)

@app.route('/editar_produto/<int:id>')
def editar_produto(id):
    produto = db.session.get(Produto, id)
    fornecedores = Fornecedor.query.all()
    return render_template("editar_produto.html", produto=produto, fornecedores=fornecedores)

@app.route('/estoque')
@login_required
def estoque():
    if current_user.role == 'vendedor':
        return "Acesso negado. Apenas administradores e operadores de estoque.", 403
    produtos = Produto.query.all()
    movimentacoes = Movimentacao.query.all()
    return render_template("estoque.html", produtos=produtos, movimentacoes=movimentacoes)

@app.route('/movimentar_estoque', methods=['POST'])
def movimentar_estoque():
    id_p = request.form.get('produto')
    tipo = request.form.get('tipo')
    qtd = int(request.form.get('quantidade'))
    obs = request.form.get('observacao')
    
    produto = db.session.get(Produto, id_p)
    
    if not produto:
        return "Erro: Produto não encontrado.", 404

    if tipo == 'entrada':
        produto.estoque += qtd
        
        valor_total_custo = produto.preco_compra * qtd 
        
        novo_gasto = Caixa(
            descricao=f"Compra de estoque: {produto.nome} (x{qtd})",
            tipo='saida', 
            valor=valor_total_custo,
            data=datetime.now()
        )
        db.session.add(novo_gasto)
        msg_obs = f"Compra: {obs}" if obs else "Entrada de mercadoria (Custo Fornecedor)"
        
    else: 
        if produto.estoque < qtd:
            return "Erro: Quantidade de saída maior que o estoque atual.", 400
        
        produto.estoque -= qtd
        msg_obs = f"Ajuste/Perda: {obs}" if obs else "Saída manual"

    nova_mov = Movimentacao(
        produto_id=id_p,
        tipo=tipo,
        quantidade=qtd,
        observacao=msg_obs,
        data=datetime.now().strftime('%d/%m/%Y %H:%M')
    )
    
    db.session.add(nova_mov)
    
    try:
        db.session.commit()
        return redirect(url_for('estoque'))
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao movimentar: {e}")
        return "Erro interno ao processar movimentação.", 500

@app.route('/atualizar_produto/<int:id>', methods=['POST'])
def atualizar_produto(id):
    produto = db.session.get(Produto, id) 
    
    produto.nome = request.form.get('nome')
    produto.marca = request.form.get('marca')
    produto.codigo = request.form.get('codigo')
    produto.preco_compra = float(request.form.get('preco_compra', 0))
    produto.preco_venda = float(request.form.get('preco_venda', 0))
    produto.estoque = int(request.form.get('estoque', 0))
    produto.estoque_minimo = int(request.form.get('estoque_minimo', 5))
    produto.fornecedor_id = request.form.get('fornecedor')
    produto.observacoes = request.form.get('observacoes')

    db.session.commit()
    return redirect('/produtos')

@app.route('/caixa')
@login_required
def caixa():
    if current_user.role != 'admin':
        return "Acesso restrito ao administrador financeiro.", 403
    hoje = datetime.now()
    primeiro_dia_mes = hoje.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    data_inicio_str = request.args.get('data_inicio', primeiro_dia_mes.strftime('%Y-%m-%d'))
    data_fim_str = request.args.get('data_fim', hoje.strftime('%Y-%m-%d'))
    
    data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d').replace(hour=0, minute=0, second=0)
    data_fim = datetime.strptime(data_fim_str, '%Y-%m-%d').replace(hour=23, minute=59, second=59)

    # Consulta filtrada pelo período selecionado
    lancamentos = Caixa.query.filter(Caixa.data.between(data_inicio, data_fim)).order_by(Caixa.data.desc()).all()
    
    total_entradas = sum(l.valor for l in lancamentos if l.tipo == 'entrada')
    total_saidas = sum(l.valor for l in lancamentos if l.tipo == 'saida')

    return render_template('caixa.html',
                           lancamentos=lancamentos,
                           total_entradas=total_entradas,
                           total_saidas=total_saidas,
                           data_inicio=data_inicio_str,
                           data_fim=data_fim_str)

@app.route('/vendas')
def vendas():
    produtos = Produto.query.filter(Produto.estoque > 0).all() 
    clientes = Cliente.query.all()
    return render_template('vendas.html', produtos=produtos, clientes=clientes)

@app.route('/finalizar_venda', methods=['POST'])
def finalizar_venda():
    p_ids = request.form.getlist('produto_id[]')
    quantidades = request.form.getlist('quantidade[]')
    
    if not p_ids:
        return "Erro: Nenhum produto selecionado.", 400

    valor_total_venda = 0
    itens_descritos = []

    try:
        for p_id, qtd in zip(p_ids, quantidades):
            qtd = int(qtd)
            produto = db.session.get(Produto, p_id)
            
            if produto.estoque < qtd:
                db.session.rollback()
                return f"Estoque insuficiente para {produto.nome}!"

            produto.estoque -= qtd
            valor_item = produto.preco_venda * qtd
            valor_total_venda += valor_item
            itens_descritos.append(f"{produto.nome} (x{qtd})")
            nova_mov = Movimentacao(
                produto_id=p_id,
                tipo='saida',
                quantidade=qtd,
                observacao="Venda Casada",
                data=datetime.now().strftime('%d/%m/%Y %H:%M')
            )
            db.session.add(nova_mov)

        novo_caixa = Caixa(
            descricao=f"Venda: {', '.join(itens_descritos)}",
            tipo='entrada',
            valor=valor_total_venda,
            data=datetime.now()
        )
        db.session.add(novo_caixa)
        
        db.session.commit()
        return redirect(url_for('caixa'))

    except Exception as e:
        db.session.rollback()
        print(f"Erro na venda casada: {e}")
        return "Erro ao processar a venda.", 500

@app.route('/relatorios')
@login_required
def dashboard():
    if current_user.role != 'admin':
        return "Acesso restrito ao administrador.", 403

    # 1. Captura as datas do filtro (Vazio por padrão para listar tudo)
    data_inicio_str = request.args.get('data_inicio', '')
    data_fim_str = request.args.get('data_fim', '')

    # 2. Consultas Base do Caixa (Financeiro)
    query_faturamento = db.session.query(func.sum(Caixa.valor)).filter(Caixa.tipo == 'entrada')
    query_investimento = db.session.query(func.sum(Caixa.valor)).filter(Caixa.tipo == 'saida')
    query_vendas_count = db.session.query(func.count(Caixa.id)).filter(Caixa.tipo == 'entrada', Caixa.descricao.like('Venda%'))
    
    # 3. Consulta Base do Gráfico (Idêntica à sua que funcionava)
    query_mais_vendidos = db.session.query(
        Produto.nome, 
        func.sum(Movimentacao.quantidade)
    ).join(Movimentacao).filter(Movimentacao.tipo == 'saida')

    # 4. Se o usuário aplicou o filtro, aplica de forma segura usando func.date()
    if data_inicio_str and data_fim_str:
        query_faturamento = query_faturamento.filter(func.date(Caixa.data).between(data_inicio_str, data_fim_str))
        query_investimento = query_investimento.filter(func.date(Caixa.data).between(data_inicio_str, data_fim_str))
        query_vendas_count = query_vendas_count.filter(func.date(Caixa.data).between(data_inicio_str, data_fim_str))
        
        # Tentativa segura: filtra a data da movimentação. Se o campo no banco for 'data', o SQLAlchemy resolve.
        # Caso o gráfico continue sumindo COM FILTRO, comente a linha abaixo colocando um # na frente.
        #query_mais_vendidos = query_mais_vendidos.filter(func.date(Movimentacao.data).between(data_inicio_str, data_fim_str))

    # 5. Executa e calcula os resultados financeiros
    faturamento_total = query_faturamento.scalar() or 0
    investimento_estoque = query_investimento.scalar() or 0
    lucro_real = faturamento_total - investimento_estoque

    total_vendas_count = query_vendas_count.scalar() or 0
    ticket_medio = (faturamento_total / total_vendas_count) if total_vendas_count > 0 else 0

    # 6. Executa e monta os dados do Gráfico
    mais_vendidos = query_mais_vendidos.group_by(Produto.nome)\
                                       .order_by(func.sum(Movimentacao.quantidade).desc())\
                                       .limit(5).all()

    labels_produtos = [item[0] for item in mais_vendidos]
    valores_produtos = [int(item[1]) for item in mais_vendidos]

    # 7. Ranking de Margem (Global - Mantido exatamente igual ao seu)
    produtos_lista = Produto.query.all()
    ranking_lucro = []
    for p in produtos_lista:
        ranking_lucro.append({
            'nome': p.nome, 
            'margem': (p.preco_venda or 0) - (p.preco_compra or 0)
        })
    ranking_lucro = sorted(ranking_lucro, key=lambda x: x['margem'], reverse=True)[:5]

    # 8. Estoque Baixo (Global - Mantido exatamente igual ao seu)
    estoque_baixo = Produto.query.filter(Produto.estoque < 5).all()

    return render_template("dashboard.html", 
                           faturamento=faturamento_total,
                           investimento=investimento_estoque,
                           lucro_real=lucro_real,
                           ticket_medio=ticket_medio,
                           labels_produtos=labels_produtos,
                           valores_produtos=valores_produtos,
                           ranking_lucro=ranking_lucro,
                           estoque_baixo=estoque_baixo,
                           data_inicio=data_inicio_str,
                           data_fim=data_fim_str,
                           now=datetime.now())
# =====================================
# INICIAR SISTEMA
# =====================================

if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
        
        from sqlalchemy import text
        try:
            db.session.execute(text('ALTER TABLE usuario ADD COLUMN nome VARCHAR(100)'))
            db.session.commit()
            print("Coluna 'nome' verificada/adicionada com sucesso!")
        except Exception:
            db.session.rollback()

        try:
            db.session.execute(text('ALTER TABLE usuario ADD COLUMN primeiro_acesso BOOLEAN DEFAULT TRUE'))
            db.session.commit()
            print("Coluna 'primeiro_acesso' verificada/adicionada com sucesso!")
        except Exception:
            db.session.rollback()
            
        user_admin = Usuario.query.filter_by(username='admin').first()
        if not user_admin:
            novo_admin = Usuario(
                username='admin',
                nome='Jessé Admin',
                role='admin',
                password=generate_password_hash('admin123'),
                primeiro_acesso=False 
            )
            db.session.add(novo_admin)
            db.session.commit()
            print("Usuário Admin padrão verificado/criado com sucesso (admin / admin123)!")

    app.run(host='0.0.0.0', port=5000, debug=True)