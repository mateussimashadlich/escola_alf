from flask import Flask, request
from flask_mongoengine import MongoEngine
from models import Gabarito, Resposta
#def create_app():
#    app = Flask(__name__, instance_relative_config=True)
#    app.config_from_mapping(
#        SECRET_KEY='dev',
#        DATABASE=os.path.join(app.instance_path, 'escola_alf.sqlite')
#    )

app = Flask(__name__)

#app.config['MONGODB_SETTINGS'] = {
#    'db': 'escola_alf',
#    'host': 'localhost',
#    'port': 27017
#}

db = MongoEngine()

db.init_app(app)


@app.route('/gabarito', methods=['POST'])
def cadastrar_gabarito():
    for questao in request.json['questoes']:        
        print(type(questao['num_questao']))
        gabarito = Gabarito(
            alternativa=questao['alternativa'],
            id_prova=request.json['id_prova'],
            num_questao=questao['num_questao'],
            peso_questao=questao['peso_questao']
        )
        gabarito.save()   

    print(request.json)
    return request.json
    #print(request.get_json)
    #print(request.json['bla'])
    #return request.json

