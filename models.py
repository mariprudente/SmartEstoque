from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Cliente(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(120))
    cpf = db.Column(db.String(14))
    rg = db.Column(db.String(12))
    nascimento = db.Column(db.String(10))

    rua = db.Column(db.String(120))
    numero = db.Column(db.String(10))
    cidade = db.Column(db.String(60))
    estado = db.Column(db.String(30))

    telefone = db.Column(db.String(14))
    celular = db.Column(db.String(15))
    email = db.Column(db.String(120))


class Produto(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120))
    preco_compra = db.Column(db.Float)
    preco_venda = db.Column(db.Float)


class Fornecedor(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120))
    telefone = db.Column(db.String(20))