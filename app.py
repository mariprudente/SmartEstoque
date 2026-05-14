from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/img'

# =====================================
# CONFIG BANCO (Versão MySQL)
# =====================================
# senha usada no Workbench
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:PISmartEstoque%402026@localhost/smartestoque'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

UPLOAD_FOLDER = 'static/img' 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# =====================================
# MODELS (Estrutura das Tabelas)
# =====================================

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
def estoque():
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
def caixa():
    lancamentos = Caixa.query.order_by(Caixa.data.desc()).all()
    
    total_entradas = db.session.query(db.func.sum(Caixa.valor)).filter(Caixa.tipo == 'entrada').scalar() or 0
    total_saidas = db.session.query(db.func.sum(Caixa.valor)).filter(Caixa.tipo == 'saida').scalar() or 0
    
    return render_template('caixa.html', 
                           lancamentos=lancamentos, 
                           total_entradas=total_entradas, 
                           total_saidas=total_saidas)

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



# =====================================
# INICIAR SISTEMA
# =====================================

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

    if __name__ == "__main__":
        app.run(host='0.0.0.0', port=5000, debug=True)