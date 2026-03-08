from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Cliente(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    telefone = db.Column(db.String(50))
    email = db.Column(db.String(100))


class Produto(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    estoque = db.Column(db.Integer)
    preco = db.Column(db.Float)


class Fornecedor(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    telefone = db.Column(db.String(50))