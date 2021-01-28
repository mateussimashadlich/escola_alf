from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Prova(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matricula_aluno = db.Column(db.Integer, primary_key=True)

class Gabarito(db.Model):
    id_prova = db.Column(db.Integer, db.ForeignKey(Prova.id), primary_key=True)
    num_questao = db.Column(db.Integer, primary_key=True)
    peso_questao = db.Column(db.Integer)
    alternativa = db.Column(db.String(1))

class Resposta(db.Model):
    id_prova = db.Column(db.Integer, db.ForeignKey(Prova.id), primary_key=True)
    matricula_aluno = db.Column(db.Integer, db.ForeignKey(Prova.matricula_aluno), primary_key=True)
    num_questao = db.Column(db.Integer, primary_key=True)
    alternativa = db.Column(db.String(1))

