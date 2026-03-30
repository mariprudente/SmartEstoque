from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    funcao = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14))
    rg = db.Column(db.String(12))
    data_nascimento = db.Column(db.String(10))
    rua = db.Column(db.String(100))
    numero = db.Column(db.String(10))
    cidade = db.Column(db.String(50))
    estado = db.Column(db.String(2))
    telefone = db.Column(db.String(14))
    celular = db.Column(db.String(15))
    email = db.Column(db.String(100))

class Fornecedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    razao_social = db.Column(db.String(150), nullable=False)
    cnpj = db.Column(db.String(20), unique=True)
    nome_contato = db.Column(db.String(100))
    cep = db.Column(db.String(10))
    endereco = db.Column(db.String(200))
    numero = db.Column(db.String(10))
    complemento = db.Column(db.String(100))
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(2))
    telefone = db.Column(db.String(20))
    celular = db.Column(db.String(20))
    email = db.Column(db.String(100))
    observacoes = db.Column(db.Text)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Gerado automaticamente
    nome = db.Column(db.String(100), nullable=False)
    situacao = db.Column(db.Boolean, default=True) # Checkbox (Ativo/Inativo)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedor.id'))
    marca = db.Column(db.String(50))
    preco_compra = db.Column(db.Float)
    preco_venda = db.Column(db.Float)
    estoque_atual = db.Column(db.Integer, default=0)
    estoque_minimo = db.Column(db.Integer, default=0)
    observacoes = db.Column(db.Text)
    imagem = db.Column(db.String(200)) # Caminho da foto

# ESTA É A CLASSE QUE ESTAVA FALTANDO:
class Movimentacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    tipo = db.Column(db.String(10), nullable=False) # 'Entrada' ou 'Saida'
    quantidade = db.Column(db.Integer, nullable=False)
    data_registro = db.Column(db.DateTime, default=datetime.now)
    observacoes = db.Column(db.Text)
    
    # Relacionamento para facilitar a busca do nome do produto
    produto = db.relationship('Produto', backref=db.backref('movimentacoes', lazy=True))

class Despesa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, default=datetime.now)
    tipo = db.Column(db.String(10), default='Saida')

#kit produtos 
class KitProduto(db.Model):
    __tablename__ = 'kit_produto'
    id = db.Column(db.Integer, primary_key=True)
    kit_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    produto_componente_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    quantidade_neste_kit = db.Column(db.Integer, default=1)

    # Relacionamentos
    produto = db.relationship('Produto', foreign_keys=[produto_componente_id])
    
#parte de baixa do estoque 
class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_venda = db.Column(db.DateTime, default=datetime.now)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    valor_total = db.Column(db.Float, default=0.0)
    forma_pagamento = db.Column(db.String(50))
    
    # Relacionamento
    cliente = db.relationship('Cliente', backref=db.backref('vendas', lazy=True))

class ItemVenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    venda_id = db.Column(db.Integer, db.ForeignKey('venda.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)

    # Relacionamento
    produto = db.relationship('Produto')


    # No models.py
class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    razao_social = db.Column(db.String(150))
    nome_fantasia = db.Column(db.String(150))
    cnpj = db.Column(db.String(20))
    telefone = db.Column(db.String(20))