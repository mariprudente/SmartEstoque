from flask import Flask, render_template, request, redirect
from models import db, Cliente, Produto, Fornecedor

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


# ======================
# INICIO
# ======================

@app.route('/')
def index():

    return render_template('menu.html')


# ======================
# CLIENTES
# ======================

@app.route('/clientes')
def clientes():

    lista = Cliente.query.all()

    return render_template(
        'clientes.html',
        clientes=lista
    )


@app.route('/add_cliente', methods=['POST'])
def add_cliente():

    nome = request.form['nome']
    telefone = request.form['telefone']
    email = request.form['email']

    novo = Cliente(
        nome=nome,
        telefone=telefone,
        email=email
    )

    db.session.add(novo)
    db.session.commit()

    return redirect('/clientes')


# ======================
# PRODUTOS
# ======================

@app.route('/produtos')
def produtos():

    lista = Produto.query.all()

    return render_template(
        'produtos.html',
        produtos=lista
    )


# ======================
# FORNECEDORES
# ======================

@app.route('/fornecedores')
def fornecedores():

    lista = Fornecedor.query.all()

    return render_template(
        'fornecedores.html',
        fornecedores=lista
    )


# ======================
# BANCO
# ======================

with app.app_context():

    db.create_all()


# ======================
# RODAR
# ======================

if __name__ == '__main__':

    app.run(debug=True)