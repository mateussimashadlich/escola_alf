from flask import Flask, request, g, jsonify
from models import db, Prova, Gabarito, Resposta
from sqlalchemy.exc import IntegrityError


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///escola_alf.db'
    #Recurso que não será utilizado e que consome muitos recursos
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.app_context().push()

    #Reinica o BD a cada inicialização (a fim de facilitar os testes)
    db.drop_all()
    db.create_all()
    db.session.commit()

    return app

app = create_app()


@app.route('/prova', methods=['POST', 'GET'])
def prova():
    if request.method == 'POST':
        return cadastrar_prova()
    elif request.method == 'GET':
        return visualizar_provas()
def cadastrar_prova():
    try:
        if request.get_json() == None:
            return jsonify(message="Apenas requisições JSON são válidas"), 400 
        
        if Prova.query.filter_by(matricula_aluno=request.json['matricula_aluno']).first() == None and len(db.session.query(Prova.matricula_aluno.distinct()).all()) >= 100:
            return jsonify(mensagem='A quantidade máxima de 100 alunos já foi atingida.')

        if Prova.query.filter_by(id=request.json['id'], matricula_aluno=request.json['matricula_aluno']).first() == None:
            prova = Prova(id=request.json['id'], matricula_aluno=request.json['matricula_aluno'])
            db.session.add(prova)
            db.session.commit()
            return jsonify(message="Prova criada com sucesso!")

        return jsonify(message='Prova ' + str(request.json['id']) + ' já existe para o aluno de matricula ' + str(request.json['matricula_aluno']) + '.')

    except KeyError:
        return jsonify(
                        message="Parâmetro especificado inválido",
                        documentacao="https://github.com/mateussimashadlich/escola_alf/blob/master/README.md"
                    ), 400
    except:
        db.session.rollback()
        return cadastrar_prova()

def visualizar_provas():
    provas = []
    for prova in Prova.query.all():
        provas.append({'id': prova.id, 'matricula_aluno': prova.matricula_aluno})

    return jsonify(provas=provas)

@app.route('/gabarito', methods=['POST', 'GET'])
def gabarito():
    if request.method == 'POST':
        return cadastrar_gabarito()
    elif request.method == 'GET':
        return visualizar_gabaritos()

def cadastrar_gabarito():
    try:
        if request.get_json() == None:
            return jsonify(message="Apenas requisições JSON são válidas"), 400 

        if Prova.query.filter_by(id=request.json['id_prova']).first() == None:
            return jsonify(mensagem='A prova especificada não existe'), 404   

        nota_total = 0.
        for questao in request.json['questoes']:
            if int(questao['peso_questao']) <= 0:
                return jsonify(mensagem='O peso da questão ' + str(questao['num_questao']) + ' precisa ser um inteiro maior do que 0.'), 400

            nota_total += questao['peso_questao']

        if nota_total <= 0 or nota_total > 10:
            return jsonify(mensagem='A nota da prova precisa estar acima de 0 e não ser maior do que 10'), 400

        if Gabarito.query.filter_by(id_prova=request.json['id_prova']).first() != None:
            return jsonify(mensagem='Já existe um gabarito para a prova ' +  str(request.json['id_prova']) + '.')
            
        for questao in request.json['questoes']:
            gabarito = Gabarito(
                id_prova = request.json['id_prova'],                        
                num_questao = questao['num_questao'],
                peso_questao = questao['peso_questao'],
                alternativa = questao['alternativa']
            )
            db.session.add(gabarito)
        
        db.session.commit()
        return jsonify(mensagem='Gabarito criado com sucesso!')

    except KeyError:
        return jsonify(
                        message="Parâmetro especificado inválido",
                        documentacao="https://github.com/mateussimashadlich/escola_alf/blob/master/README.md"
                    ), 400         
    
def visualizar_gabaritos():
    gabaritos = []
    for prova_gabarito in db.session.query(Gabarito.id_prova.distinct()).all():
        questoes_gabarito = []
        for questao_gabarito in Gabarito.query.filter_by(id_prova=prova_gabarito[0]).all(): 
            questoes_gabarito.append({
                'num_questao': questao_gabarito.num_questao, 
                'peso_questao': questao_gabarito.peso_questao,
                'alternativa': questao_gabarito.alternativa
            })

        gabaritos.append({
        'id_prova': prova_gabarito[0], 
        'questoes': questoes_gabarito
        })

    return jsonify(gabaritos=gabaritos)

@app.route('/resposta', methods=['POST', 'GET'])
def resposta():
    if request.method == 'POST':
        return cadastrar_resposta()
    elif request.method == 'GET':
        return visualizar_respostas()

def cadastrar_resposta():
    try:
        if request.get_json() == None:
            return jsonify(message="Apenas requisições JSON são válidas"), 400

        if Prova.query.filter_by(id=request.json['id_prova'], matricula_aluno=request.json['matricula_aluno']).first() == None:
            return jsonify(mensagem='A prova especificada não existe'), 404

        for resposta in request.json['respostas']:
            if Gabarito.query.filter_by(id_prova=request.json['id_prova'], num_questao=resposta['num_questao']).first() == None:
                return jsonify(mensagem='A questão ' + str(resposta['num_questao']) + ' não existe para a prova ' + str(request.json['id_prova']) + '.'), 404
        

        for resposta in request.json['respostas']:
            resposta = Resposta(
                id_prova = request.json['id_prova'],
                matricula_aluno = request.json['matricula_aluno'],                        
                num_questao = resposta['num_questao'],            
                alternativa = resposta['alternativa']
            )
            db.session.add(resposta)

        db.session.commit()
        return jsonify(mensagem='Resposta(s) cadastrada(s) com sucesso!')
    except KeyError:
        return jsonify(
                        message="Parâmetro especificado inválido",
                        documentacao="https://github.com/mateussimashadlich/escola_alf/blob/master/README.md"
                    ), 400
    except IntegrityError as e:
        db.session.rollback()
        respostas_cadastradas = {}
        for resposta in Resposta.query.filter_by(id_prova=request.json['id_prova'], matricula_aluno=request.json['matricula_aluno']).all():
            respostas_cadastradas[resposta.num_questao] = resposta.alternativa
        
        return jsonify(
                        message="Erro de integridade, não podem haver respostas duplicadas, verifique se não há números de questão duplicados.",
                        respostas_cadastradas=respostas_cadastradas
                    )                                  
    
def visualizar_respostas():
    respostas = []
    for matricula_aluno in db.session.query(Resposta.matricula_aluno.distinct()).all():
        respostas_aluno = []
        for resposta in Resposta.query.filter_by(matricula_aluno=matricula_aluno[0]).all(): 
            respostas_aluno.append({
                'num_questao': resposta.num_questao,                 
                'alternativa': resposta.alternativa
            })

        respostas.append({
        'matricula_aluno': matricula_aluno[0], 
        'respostas_aluno': respostas_aluno
        })

    return jsonify(respostas=respostas)


@app.route('/nota_final', methods=['GET'])
def get_nota_final_aluno():
    try:
        if request.get_json() == None:            
            return jsonify(message="Apenas requisições JSON são válidas"), 400 
        if Prova.query.filter_by(matricula_aluno=request.json['matricula_aluno']).first() == None:
            return jsonify(mensagem='A matricula especificada não existe.'), 404

        return verificar_nota(request.json['matricula_aluno'])
    except KeyError:
        return jsonify(
                        message="Parâmetro especificado inválido",
                        documentacao="https://github.com/mateussimashadlich/escola_alf/blob/master/README.md"
                    ), 400          

def verificar_nota(matricula_aluno):
    provas_aluno = Prova.query.filter_by(matricula_aluno=matricula_aluno).all()
    nota_final = 0
    for prova in provas_aluno:
        nota_prova = 0
        respostas = Resposta.query.filter_by(id_prova=prova.id, matricula_aluno=prova.matricula_aluno).all()
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
    alunos = []
    for aluno in db.session.query(Prova.matricula_aluno.distinct()).all():
        #aluno[0] equivale à matricula do aluno
        if verificar_nota(aluno[0]).get_json()['nota_final'] >= 7:     
            alunos.append(aluno[0])

    return jsonify(matricula_alunos_aprovados=alunos)


