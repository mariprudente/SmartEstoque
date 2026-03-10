from flask import Flask, render_template
from models import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/clientes')
def clientes():
    return render_template('clientes.html')


@app.route('/fornecedores')
def fornecedores():
    return render_template('fornecedores.html')


@app.route('/produtos')
def produtos():
    return render_template('produtos.html')


@app.route('/movimentacao')
def movimentacao():
    return "<h2>Movimentação em construção</h2>"


@app.route('/caixa')
def caixa():
    return "<h2>Caixa em construção</h2>"


@app.route('/relatorios')
def relatorios():
    return "<h2>Relatórios em construção</h2>"


if __name__ == '__main__':
    app.run(debug=True)