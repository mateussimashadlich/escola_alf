import sqlite3
from flask import Flask, request, g, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Prova, Gabarito, Resposta


#db.init_app(app)


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///escola_alf.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app


app = create_app()
app.app_context().push()

#Reinica o BD a cada inicialização
db.drop_all()
db.session.commit()

db.create_all()
db.session.commit()

@app.route('/prova', methods=['POST'])
def cadastrar_prova():
    try:
        prova = Prova(id=request.json['id'], aluno=request.json['aluno'])
        db.session.add(prova)
        db.session.commit()
        return jsonify(message="Prova criada com sucesso!")   
    except Exception as e:
        print(e)

@app.route('/gabarito', methods=['POST'])
def cadastrar_gabarito():
 #   db = get_db()
    if Prova.query.filter_by(id=request.json['id_prova']) == None:
        return jsonify(mensagem='A prova especificada não existe')

    for questao in request.json['questoes']:
        gabarito = Gabarito(
            id_prova = request.json['id_prova'],                        
            num_questao = questao['num_questao'],
            peso_questao = questao['peso_questao'],
            alternativa = questao['alternativa']
        )
        db.session.add(gabarito)
    print(Gabarito.query.all())
    db.session.commit()
    return jsonify(mensagem='Gabarito criado com sucesso!')

@app.route('/resposta', methods=['POST'])
def cadastrar_resposta():    
    if Prova.query.filter_by(id=request.json['id_prova']).first() == None:
        return jsonify(mensagem='A prova especificada não existe')

    if len(db.session.query(Resposta.id_aluno.distinct().label("bla")).all()) == 100:
        return jsonify(mensagem='A quantidade máxima de 100 alunos já foi atingida')

    for resposta in request.json['respostas']:
        resposta = Resposta(
            id_prova = request.json['id_prova'],
            id_aluno = request.json['id_aluno'],                        
            num_questao = resposta['num_questao'],            
            alternativa = resposta['alternativa']
        )
        db.session.add(resposta)
    print(Resposta.query.all())
    db.session.commit()

@app.route('/nota_final', methods=['GET'])
def get_nota_final_aluno():
    return verificar_nota(request.json['aluno'])

def verificar_nota(aluno):
    provas_aluno = Prova.query.filter_by(aluno=aluno).all()
    nota_final = 0
    for prova in provas_aluno:
        nota_prova = 0
        respostas = Resposta.query.filter_by(id_prova=prova.id, id_aluno=prova.aluno).all()
        gabaritos = Gabarito.query.filter_by(id_prova=prova.id).all()
        for resposta in respostas:
            for gabarito in gabaritos:
                if resposta.num_questao == gabarito.num_questao:
                    if resposta.alternativa == gabarito.alternativa:
                        nota_prova += 1 * gabarito.peso_questao
                    break
        nota_final += nota_prova/len(provas_aluno)

    return jsonify(nota_final=nota_final)

@app.route('/alunos_aprovados', methods=['GET'])
def get_alunos_aprovados():
    alunos = db.session.query(Prova.aluno.distinct()).all()
    for aluno in alunos:           
        #aluno é uma tupla com o campo aluno da tabela prova dentro
        #[!] jsonify retorna um objeto Reponse, temos que ver como pegar os valores dele
        if verificar_nota(aluno[0]).get_json()['nota_final'] < 7:
            alunos.remove(aluno)
    return jsonify(alunos_aprovados=alunos)
            
 
    print(request.json)
    return request.json


