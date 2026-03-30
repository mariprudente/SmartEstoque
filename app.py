import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
from sqlalchemy import func
from models import db, Usuario, Cliente, Fornecedor, Produto, Movimentacao, Despesa, KitProduto, Venda, ItemVenda, Empresa

app = Flask(__name__)
app.secret_key = "chave_mestra_smart_estoque"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smart_estoque.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# --- ROTAS DE AUTENTICAÇÃO ---

@app.route('/')
def login():
    return render_template('auth/login.html')

@app.route('/autenticar', methods=['POST'])
def autenticar():
    username = request.form.get('username')
    senha = request.form.get('senha')
    user = Usuario.query.filter_by(username=username, senha=senha).first()
    if user:
        session['usuario_id'] = user.id
        session['usuario_nome'] = user.nome_completo
        return redirect(url_for('index'))
    flash("Usuário ou senha incorretos.")
    return redirect(url_for('login'))

@app.route('/cadastro_usuario', methods=['GET', 'POST'])
def cadastro_usuario():
    if request.method == 'POST':
        novo = Usuario(
            nome_completo=request.form.get('nome_completo'),
            username=request.form.get('username'),
            funcao=request.form.get('funcao'),
            senha=request.form.get('senha')
        )
        db.session.add(novo)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('auth/cadastro_usuario.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- DASHBOARD ---

@app.route('/index')
def index():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

# --- GESTÃO DE CLIENTES ---

@app.route('/clientes')
def clientes():
    if 'usuario_id' not in session: return redirect(url_for('login'))
    lista = Cliente.query.all()
    return render_template('clientes/clientes.html', clientes=lista)

@app.route('/clientes/salvar', methods=['POST'])
def salvar_cliente():
    novo_cliente = Cliente(
        nome=request.form.get('nome'),
        cpf=request.form.get('cpf'),
        rg=request.form.get('rg'),
        data_nascimento=request.form.get('data_nascimento'),
        email=request.form.get('email'),
        rua=request.form.get('rua'),
        numero=request.form.get('numero'),
        cidade=request.form.get('cidade'),
        estado=request.form.get('estado'),
        telefone=request.form.get('telefone'),
        celular=request.form.get('celular')
    )
    db.session.add(novo_cliente)
    db.session.commit()
    return redirect(url_for('clientes'))

@app.route('/clientes/visualizar/<int:id>')
def visualizar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    return render_template('clientes/visualizar.html', cliente=cliente)

@app.route('/clientes/editar/<int:id>')
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    return render_template('clientes/editar.html', cliente=cliente)

@app.route('/clientes/atualizar/<int:id>', methods=['POST'])
def atualizar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    cliente.nome = request.form.get('nome')
    cliente.cpf = request.form.get('cpf')
    cliente.rg = request.form.get('rg')
    cliente.data_nascimento = request.form.get('data_nascimento')
    cliente.email = request.form.get('email')
    cliente.rua = request.form.get('rua')
    cliente.numero = request.form.get('numero')
    cliente.cidade = request.form.get('cidade')
    cliente.estado = request.form.get('estado')
    cliente.telefone = request.form.get('telefone')
    cliente.celular = request.form.get('celular')
    db.session.commit()
    return redirect(url_for('clientes'))

@app.route('/clientes/excluir/<int:id>')
def excluir_cliente(id):
    if 'usuario_id' not in session: return redirect(url_for('login'))
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return redirect(url_for('clientes'))

# ---- GESTÃO DE FORNECEDORES ------

@app.route('/fornecedores')
def fornecedores():
    if 'usuario_id' not in session: return redirect(url_for('login'))
    lista = Fornecedor.query.all()
    return render_template('fornecedores/fornecedores.html', fornecedores=lista)

@app.route('/fornecedores/salvar', methods=['POST'])
def salvar_fornecedor():
    novo = Fornecedor(
        razao_social=request.form.get('razao_social'),
        cnpj=request.form.get('cnpj'),
        nome_contato=request.form.get('nome_contato'),
        cep=request.form.get('cep'),
        endereco=request.form.get('endereco'),
        numero=request.form.get('numero'),
        complemento=request.form.get('complemento'),
        bairro=request.form.get('bairro'),
        cidade=request.form.get('cidade'),
        estado=request.form.get('estado'),
        telefone=request.form.get('telefone'),
        celular=request.form.get('celular'),
        email=request.form.get('email'),
        observacoes=request.form.get('observacoes')
    )
    db.session.add(novo)
    db.session.commit()
    return redirect(url_for('fornecedores'))

@app.route('/fornecedores/visualizar/<int:id>')
def visualizar_fornecedor(id):
    f = Fornecedor.query.get_or_404(id)
    return render_template('fornecedores/visualizar.html', fornecedor=f)

@app.route('/fornecedores/editar/<int:id>')
def editar_fornecedor(id):
    f = Fornecedor.query.get_or_404(id)
    return render_template('fornecedores/editar.html', fornecedor=f)

@app.route('/fornecedores/atualizar/<int:id>', methods=['POST'])
def atualizar_fornecedor(id):
    f = Fornecedor.query.get_or_404(id)
    f.razao_social = request.form.get('razao_social')
    f.cnpj = request.form.get('cnpj')
    f.nome_contato = request.form.get('nome_contato')
    f.cep = request.form.get('cep')
    f.endereco = request.form.get('endereco')
    f.numero = request.form.get('numero')
    f.complemento = request.form.get('complemento')
    f.bairro = request.form.get('bairro')
    f.cidade = request.form.get('cidade')
    f.estado = request.form.get('estado')
    f.telefone = request.form.get('telefone')
    f.celular = request.form.get('celular')
    f.email = request.form.get('email')
    f.observacoes = request.form.get('observacoes')
    db.session.commit()
    return redirect(url_for('fornecedores'))

@app.route('/fornecedores/excluir/<int:id>')
def excluir_fornecedor(id):
    f = Fornecedor.query.get_or_404(id)
    db.session.delete(f)
    db.session.commit()
    return redirect(url_for('fornecedores'))

# --- GESTÃO DE PRODUTOS ---

@app.route('/produtos')
def produtos():
    if 'usuario_id' not in session: return redirect(url_for('login'))
    lista_produtos = Produto.query.all()
    lista_fornecedores = Fornecedor.query.all()
    return render_template('produtos/produtos.html', produtos=lista_produtos, fornecedores=lista_fornecedores)

@app.route('/produtos/salvar', methods=['POST'])
def salvar_produto():
    nome = request.form.get('nome')
    situacao = True if request.form.get('situacao') == 'on' else False
    fornecedor_id = request.form.get('fornecedor_id')
    marca = request.form.get('marca')
    preco_compra = float(request.form.get('preco_compra') or 0)
    preco_venda = float(request.form.get('preco_venda') or 0)
    estoque_atual = int(request.form.get('estoque_atual') or 0)
    estoque_minimo = int(request.form.get('estoque_minimo') or 0)
    observacoes = request.form.get('observacoes')

    novo_prod = Produto(
        nome=nome,
        situacao=situacao,
        fornecedor_id=fornecedor_id if fornecedor_id else None,
        marca=marca,
        preco_compra=preco_compra,
        preco_venda=preco_venda,
        estoque_atual=estoque_atual,
        estoque_minimo=estoque_minimo,
        observacoes=observacoes
    )
    db.session.add(novo_prod)
    db.session.commit()
    return redirect(url_for('produtos'))

@app.route('/produtos/visualizar/<int:id>')
def visualizar_produto(id):
    if 'usuario_id' not in session: return redirect(url_for('login'))
    produto = Produto.query.get_or_404(id)
    itens_kit = []
    if produto.marca == "KIT/COMBO":
        itens_kit = KitProduto.query.filter_by(kit_id=id).all()
    return render_template('produtos/visualizar.html', produto=produto, itens_kit=itens_kit)

@app.route('/produtos/editar/<int:id>')
def editar_produto(id):
    if 'usuario_id' not in session: return redirect(url_for('login'))
    produto = Produto.query.get_or_404(id)
    fornecedores = Fornecedor.query.all()
    return render_template('produtos/editar.html', produto=produto, fornecedores=fornecedores)

@app.route('/produtos/atualizar/<int:id>', methods=['POST'])
def atualizar_produto(id):
    produto = Produto.query.get_or_404(id)
    produto.nome = request.form.get('nome')
    produto.situacao = True if request.form.get('situacao') == 'on' else False
    produto.fornecedor_id = request.form.get('fornecedor_id') or None
    produto.marca = request.form.get('marca')
    produto.preco_compra = float(request.form.get('preco_compra') or 0)
    produto.preco_venda = float(request.form.get('preco_venda') or 0)
    produto.estoque_atual = int(request.form.get('estoque_atual') or 0)
    produto.estoque_minimo = int(request.form.get('estoque_minimo') or 0)
    produto.observacoes = request.form.get('observacoes')
    db.session.commit()
    return redirect(url_for('produtos'))

@app.route('/produtos/excluir/<int:id>')
def excluir_produto(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for('produtos'))

# --- KIT/COMBO -----

@app.route('/produtos/salvar_kit', methods=['POST'])
def salvar_kit():
    if 'usuario_id' not in session: return redirect(url_for('login'))
    
    novo_kit = Produto(
        nome=request.form.get('nome'),
        marca="KIT/COMBO",
        preco_venda=float(request.form.get('preco_venda') or 0),
        estoque_atual=int(request.form.get('estoque_atual') or 0),
        situacao=True
    )
    db.session.add(novo_kit)
    db.session.commit()
    
    flash("Kit cadastrado com sucesso!")
    return redirect(url_for('produtos'))

# --- FINANCEIRO E CAIXA ---

@app.route('/caixa')
def caixa():
    if 'usuario_id' not in session: return redirect(url_for('login'))
    vendas = Venda.query.all()
    despesas = Despesa.query.all()
    total_vendas = sum(v.valor_total for v in vendas)
    total_despesas = sum(d.valor for d in despesas)
    saldo = total_vendas - total_despesas

    lucro_vendas = 0
    itens_vendidos = ItemVenda.query.all()
    for item in itens_vendidos:
        custo = item.produto.preco_compra or 0
        lucro_vendas += (item.preco_unitario - custo) * item.quantidade

    return render_template('caixa/caixa.html', 
                           vendas=vendas, despesas=despesas,
                           total_vendas=total_vendas, total_despesas=total_despesas, 
                           saldo=saldo, lucro_vendas=lucro_vendas)

@app.route('/caixa/nova_venda')
def nova_venda():
    if 'usuario_id' not in session: return redirect(url_for('login'))
    clientes = Cliente.query.all()
    produtos = Produto.query.filter_by(situacao=True).all() 
    return render_template('caixa/nova_venda.html', clientes=clientes, produtos=produtos)

@app.route('/caixa/finalizar_venda', methods=['POST'])
def finalizar_venda():
    if 'usuario_id' not in session: return redirect(url_for('login'))
    cliente_id = request.form.get('cliente_id')
    forma_pagamento = request.form.get('forma_pagamento')
    valor_total = float(request.form.get('valor_total_hidden') or 0)
    produtos_ids = request.form.getlist('produtos[]')
    quantidades = request.form.getlist('quantidades[]')

    nova_venda = Venda(cliente_id=cliente_id, valor_total=valor_total, 
                        forma_pagamento=forma_pagamento, data_venda=datetime.now())
    db.session.add(nova_venda)
    db.session.flush()

    for i in range(len(produtos_ids)):
        p_id = int(produtos_ids[i])
        qtd_vendida = int(quantidades[i])
        produto = Produto.query.get(p_id)
        
        item = ItemVenda(venda_id=nova_venda.id, produto_id=p_id, 
                         quantidade=qtd_vendida, preco_unitario=produto.preco_venda)
        db.session.add(item)

        # BAIXA DE ESTOQUE
        produto.estoque_atual -= qtd_vendida
        if produto.marca == "KIT/COMBO":
            itens_do_kit = KitProduto.query.filter_by(kit_id=p_id).all()
            for componente in itens_do_kit:
                prod_real = Produto.query.get(componente.produto_componente_id)
                prod_real.estoque_atual -= (componente.quantidade_neste_kit * qtd_vendida)

    db.session.commit()
    flash("Venda realizada com sucesso!")
    return redirect(url_for('nova_venda'))

@app.route('/caixa/despesa/salvar', methods=['POST'])
def salvar_despesa():
    if 'usuario_id' not in session: return redirect(url_for('login'))
    nova_despesa = Despesa(
        descricao=request.form.get('descricao'),
        valor=float(request.form.get('valor') or 0),
        data=datetime.now()
    )
    db.session.add(nova_despesa)
    db.session.commit()
    flash("Despesa registrada!")
    return redirect(url_for('caixa'))

# --- ESTOQUE ---
@app.route('/estoque')
def estoque():
    if 'usuario_id' not in session: 
        return redirect(url_for('login'))
    
    dados_loja = Empresa.query.first()
    vendas = Venda.query.all()
    despesas = Despesa.query.all()

    historico = []
    total_entradas = 0
    total_saidas = 0

    for v in vendas:
        total_entradas += v.valor_total
        historico.append({
            "data": v.data_venda,
            "origem": "Produto",
            "descricao": f"Venda #{v.id} - Cliente: {v.cliente.nome if v.cliente else 'Consumidor'}",
            "tipo": "Entrada",
            "valor": v.valor_total
        })

    for d in despesas:
        total_saidas += d.valor
        historico.append({
            "data": d.data,
            "origem": "Outros",
            "descricao": d.descricao,
            "tipo": "Saída",
            "valor": d.valor
        })

    historico.sort(key=lambda x: x['data'], reverse=True)

    return render_template('estoque/estoque.html', 
                           historico_unificado=historico,
                           total_entradas=total_entradas,
                           total_saidas=total_saidas,
                           loja=dados_loja)

@app.route('/movimentacao', methods=['GET', 'POST'])
def movimentacao():
    if 'usuario_id' not in session: return redirect(url_for('login'))
    
    if request.method == 'POST':
        p_id = request.form.get('produto_id')
        tipo = request.form.get('tipo')
        qtd = int(request.form.get('quantidade'))
        obs = request.form.get('observacoes')
        
        produto = Produto.query.get(p_id)
        if tipo == 'Entrada':
            produto.estoque_atual += qtd
        else:
            produto.estoque_atual -= qtd
            
        nova_mov = Movimentacao(produto_id=p_id, tipo=tipo, quantidade=qtd, 
                                observacoes=obs, data_registro=datetime.now())
        db.session.add(nova_mov)
        db.session.commit()
        return redirect(url_for('movimentacao'))

    lista_produtos = Produto.query.order_by(Produto.nome).all()
    lista_mov = Movimentacao.query.order_by(Movimentacao.data_registro.desc()).all()
    return render_template('estoque/movimentacao.html', 
                           produtos=lista_produtos, 
                           movimentacoes=lista_mov)

# --- CONFIGURAÇÕES ---

@app.route('/configuracoes')
def configuracoes():
    if 'usuario_id' not in session: 
        return redirect(url_for('login'))
    return render_template('config/configuracoes.html')

@app.route('/configuracoes/nome-sistema', methods=['POST'])
def atualizar_nome_sistema():
    novo_nome = request.form.get('nome_sistema')
    session['nome_sistema'] = novo_nome 
    flash("Nome do sistema atualizado!")
    return redirect(url_for('configuracoes'))

@app.route('/configuracoes/empresa', methods=['GET', 'POST'])
def dados_empresa():
    if 'usuario_id' not in session: 
        return redirect(url_for('login'))
    empresa = Empresa.query.first() or Empresa() 
    return render_template('config/empresa.html', empresa=empresa)

@app.route('/configuracoes/empresa/salvar', methods=['POST'])
def salvar_dados_empresa():
    if 'usuario_id' not in session: 
        return redirect(url_for('login'))
        
    empresa = Empresa.query.first()
    if not empresa:
        empresa = Empresa()
        db.session.add(empresa)
        
    empresa.razao_social = request.form.get('razao_social')
    empresa.nome_fantasia = request.form.get('nome_fantasia')
    empresa.cnpj = request.form.get('cnpj')
    empresa.telefone = request.form.get('telefone')
    
    db.session.commit()
    return redirect(url_for('configuracoes'))

# --- GERENCIAMENTO DE USUÁRIOS ---

@app.route('/configuracoes/usuarios')
def gerenciar_usuarios():
    if 'usuario_id' not in session: 
        return redirect(url_for('login'))
    todos_usuarios = Usuario.query.all()
    return render_template('config/usuarios.html', usuarios=todos_usuarios)

@app.route('/configuracoes/usuarios/visualizar/<int:id>', methods=['GET'])
def visualizar_usuario(id):
    if 'usuario_id' not in session: 
        return redirect(url_for('login'))
        
    usuario = Usuario.query.get_or_404(id)
    return render_template('config/visualizar_usuario.html', usuario=usuario)

@app.route('/configuracoes/usuarios/editar/<int:id>', methods=['POST'])
def editar_usuario(id):
    if 'usuario_id' not in session: 
        return redirect(url_for('login'))
        
    usuario = Usuario.query.get_or_404(id)
    usuario.nome_completo = request.form.get('nome_completo')
    usuario.username = request.form.get('username')
    usuario.funcao = request.form.get('funcao')
    
    nova_senha = request.form.get('password')
    if nova_senha:
        usuario.senha = nova_senha 
        
    db.session.commit()
    return redirect(url_for('gerenciar_usuarios'))

@app.route('/configuracoes/usuarios/excluir/<int:id>')
def excluir_usuario(id):
    if 'usuario_id' not in session: 
        return redirect(url_for('login'))
        
    usuario = Usuario.query.get_or_404(id)
    
    # Não deixa o usuário logado excluir a si mesmo
    if usuario.id == session.get('usuario_id'):
        flash("Você não pode excluir a sua própria conta!")
        return redirect(url_for('gerenciar_usuarios'))
        
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('gerenciar_usuarios'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 

        pasta_config = os.path.join(app.template_folder, 'config')
        arquivo_html = os.path.join(pasta_config, 'visualizar_usuario.html')

        if not os.path.exists(arquivo_html):
            os.makedirs(pasta_config, exist_ok=True)
            with open(arquivo_html, 'w', encoding='utf-8') as f:
                f.write("""{% extends 'base.html' %}
{% block content %}
<div class="container">
    <h2><i class="fa fa-user-edit"></i> Detalhes e Edição de Usuário</h2>
    <div class="card-box">
        <form action="{{ url_for('editar_usuario', id=usuario.id) }}" method="POST" class="form-grid">
            <div class="form-group" style="grid-column: span 2;">
                <label>Nome Completo:</label>
                <input type="text" name="nome_completo" value="{{ usuario.nome_completo }}" class="input-full" required>
            </div>
            <div class="form-group">
                <label>Nome de Usuário (Login):</label>
                <input type="text" name="username" value="{{ usuario.username }}" class="input-full" required>
            </div>
            <div class="form-group">
                <label>Função / Cargo:</label>
                <select name="funcao" class="select-full">
                    <option value="Proprietário" {{ 'selected' if usuario.funcao == 'Proprietário' }}>Proprietário</option>
                    <option value="Gerente" {{ 'selected' if usuario.funcao == 'Gerente' }}>Gerente</option>
                    <option value="Funcionário" {{ 'selected' if usuario.funcao == 'Funcionário' }}>Funcionário</option>
                </select>
            </div>
            <div class="form-group" style="grid-column: span 2;">
                <label>Nova Senha (deixe em branco para não alterar):</label>
                <input type="password" name="password" placeholder="******" class="input-full">
            </div>
            <div style="grid-column: span 2; margin-top: 20px; display: flex; gap: 10px;">
                <button type="submit" class="btn-save">Atualizar Cadastro</button>
                <a href="{{ url_for('gerenciar_usuarios') }}" class="btn-main" style="background: #95a5a6;">Voltar</a>
            </div>
        </form>
    </div>
</div>
{% endblock %}""")
# ----------------------------------------------

    app.run(debug=True)