import mongoengine as me

class Gabarito(me.Document):
    id_prova = me.IntField()
    num_questao = me.IntField()
    peso_questao = me.IntField()
    alternativa = me.StringField(max_length=1)    

class Resposta(me.Document):
    gabarito = me.ReferenceField(Gabarito)
    id_aluno = me.IntField
    num_questao = me.IntField
    alternativa = me.StringField(max_length=1)
         
#FOREIGN KEY(id_prova) REFERENCES gabarito(id_prova),
#PRIMARY KEY(id_prova, id_aluno, num_questao)

