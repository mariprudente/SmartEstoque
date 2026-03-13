from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# CONFIG BANCO
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =====================================
# MODELS
# =====================================

# CLIENTES
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


# FORNECEDORES
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


# PRODUTOS
class Produto(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(150))
    ativo = db.Column(db.Boolean)

    marca = db.Column(db.String(100))
    codigo = db.Column(db.String(50))

    preco_compra = db.Column(db.Float)
    preco_venda = db.Column(db.Float)

    estoque = db.Column(db.Integer, default=0)

    observacoes = db.Column(db.Text)

    foto = db.Column(db.String(200))

    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedor.id'))

    fornecedor = db.relationship('Fornecedor')


# MOVIMENTAÇÃO DE ESTOQUE
class Movimentacao(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'))

    produto = db.relationship('Produto')

    tipo = db.Column(db.String(20))

    quantidade = db.Column(db.Integer)

    data = db.Column(db.String(20))

    observacao = db.Column(db.Text)


# =====================================
# ROTAS
# =====================================

# TELA INICIAL
@app.route('/')
def index():
    return render_template("index.html")


# =====================================
# CLIENTES
# =====================================

@app.route('/clientes')
def clientes():

    busca = request.args.get("busca")

    if busca:
        clientes = Cliente.query.filter(
            Cliente.nome.contains(busca) |
            Cliente.cpf.contains(busca)
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


# =====================================
# FORNECEDORES
# =====================================

@app.route('/fornecedores')
def fornecedores():

    busca = request.args.get("busca")

    if busca:
        fornecedores = Fornecedor.query.filter(
            Fornecedor.razao_social.contains(busca)
        ).all()
    else:
        fornecedores = Fornecedor.query.all()

    return render_template("fornecedores.html", fornecedores=fornecedores)


@app.route('/salvar_fornecedor', methods=['POST'])
def salvar_fornecedor():

    fornecedor = Fornecedor(

        razao_social=request.form['razao_social'],
        cnpj=request.form['cnpj'],
        contato=request.form['contato'],

        cep=request.form['cep'],
        endereco=request.form['endereco'],
        numero=request.form['numero'],
        complemento=request.form['complemento'],

        bairro=request.form['bairro'],
        cidade=request.form['cidade'],
        uf=request.form['uf'],

        telefone=request.form['telefone'],
        celular=request.form['celular'],

        email=request.form['email'],

        observacoes=request.form['observacoes']
    )

    db.session.add(fornecedor)
    db.session.commit()

    return redirect('/fornecedores')


@app.route('/excluir_fornecedor/<int:id>')
def excluir_fornecedor(id):

    fornecedor = Fornecedor.query.get(id)

    db.session.delete(fornecedor)
    db.session.commit()

    return redirect('/fornecedores')


@app.route('/fornecedor/<int:id>')
def fornecedor_detalhe(id):

    fornecedor = Fornecedor.query.get(id)

    return render_template("fornecedor_detalhe.html", fornecedor=fornecedor)


# =====================================
# PRODUTOS
# =====================================

@app.route('/produtos')
def produtos():

    produtos = Produto.query.all()
    fornecedores = Fornecedor.query.all()

    return render_template(
        "produtos.html",
        produtos=produtos,
        fornecedores=fornecedores
    )


# =====================================
# ESTOQUE
# =====================================

@app.route('/estoque')
def estoque():

    produtos = Produto.query.all()
    movimentacoes = Movimentacao.query.all()

    return render_template(
        "estoque.html",
        produtos=produtos,
        movimentacoes=movimentacoes
    )


@app.route('/movimentar_estoque', methods=['POST'])
def movimentar_estoque():

    produto_id = request.form['produto']
    tipo = request.form['tipo']
    quantidade = int(request.form['quantidade'])
    observacao = request.form['observacao']

    produto = Produto.query.get(produto_id)

    if tipo == "entrada":
        produto.estoque += quantidade
    else:
        produto.estoque -= quantidade

    mov = Movimentacao(

        produto_id=produto_id,
        tipo=tipo,
        quantidade=quantidade,
        data=datetime.now().strftime("%d/%m/%Y"),
        observacao=observacao

    )

    db.session.add(mov)
    db.session.commit()

    return redirect('/estoque')


# =====================================
# INICIAR SISTEMA
# =====================================

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)