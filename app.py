from flask import Flask, render_template, request, redirect
from models import db, Produto

app = Flask(__name__)

# configuração do banco
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# cria banco automaticamente
with app.app_context():
    db.create_all()


# MENU PRINCIPAL
@app.route('/')
def home():
    return render_template('menu.html')


# TELA PRODUTOS
@app.route('/produtos')
def produtos():
    produtos = Produto.query.all()
    return render_template('index.html', produtos=produtos)


# CADASTRAR PRODUTO
@app.route('/cadastrar', methods=['POST'])
def cadastrar():

    nome = request.form['nome']
    quantidade = int(request.form['quantidade'])
    estoque_minimo = int(request.form['estoque_minimo'])

    novo_produto = Produto(
        nome=nome,
        quantidade=quantidade,
        estoque_minimo=estoque_minimo
    )

    db.session.add(novo_produto)
    db.session.commit()

    return redirect('/produtos')


# DELETAR PRODUTO
@app.route('/deletar/<int:id>')
def deletar(id):

    produto = Produto.query.get(id)

    db.session.delete(produto)
    db.session.commit()

    return redirect('/produtos')


# TELA CLIENTES
@app.route('/clientes')
def clientes():
    return render_template('clientes.html')


if __name__ == '__main__':
    app.run(debug=True)