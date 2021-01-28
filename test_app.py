import requests
import unittest
import json
import app

class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.app = app.app
        self.db = app.db
        self.cliente = self.app.test_client()

    def tearDown(self):
        self.db.drop_all()
        self.db.create_all()
        self.db.session.commit()

    def test_cadastrar_prova(self):
        data = {
            'id': 1, 
            'matricula_aluno': 2
        }

        res = self.cliente.post(path='/prova', json=data)
        self.assertEqual(res.status_code, 200)

    #A quantidade máxima de alunos é 100
    def test_cadastrar_101_alunos(self):
        for i in range(0, 101):
            data = {
                'id': 1, 
                'matricula_aluno': i
            }
            res = self.cliente.post(path='/prova', json=data)
                
        mensagem = {"mensagem": 'A quantidade máxima de 100 alunos já foi atingida.'}        
        self.assertEqual(mensagem, res.get_json())

    def test_cadastrar_gabarito(self):
        data = {
            'id': 1, 
            'matricula_aluno': 1234
        }
        res = self.cliente.post(path='/prova', json=data)
        
        data = {
            'id_prova': 1,
            'questoes':[
            {
                'num_questao': 1,
                'peso_questao': 5,
                'alternativa': 'A'
            },
            {
                'num_questao': 2,
                'peso_questao': 5,
                'alternativa': 'C'
            }]
        }
        res = self.cliente.post(path='/gabarito', json=data)
        self.assertEqual(res.status_code, 200)
        
    #A nota total da prova é sempre maior que 0 e menor que 10
    def test_cadastrar_nota_invalida(self):
        data = {
            'id': 1, 
            'matricula_aluno': 2
        }
        res = self.cliente.post(path='/prova', json=data)
        
        data = {
            'id_prova': 1,
            'questoes':[
            {
                'num_questao': 1,
                'peso_questao': 5,
                'alternativa': 'A'
            },
            {
                'num_questao': 2,
                'peso_questao': 10,
                'alternativa': 'C'
            }]
        }
        res = self.cliente.post(path='/gabarito', json=data)
        self.assertEqual(res.status_code, 400)

    #O peso de cada questão é sempre um inteiro maior que 0.
    def test_cadastrar_peso_invalido(self):
        data = {
            'id': 1, 
            'matricula_aluno': 2
        }
        res = self.cliente.post(path='/prova', json=data)
        
        data = {
            'id_prova': 1,
            'questoes':[
            {
                'num_questao': 1,
                'peso_questao': 0,
                'alternativa': 'A'
            },
            {
                'num_questao': 2,
                'peso_questao': 10,
                'alternativa': 'C'
            }]
        }
        res = self.cliente.post(path='/gabarito', json=data)
        self.assertEqual(res.status_code, 400)

    #Os alunos aprovados tem média de notas maior do que 7
    def test_alunos_aprovados(self):
        
        #cadastrar_prova
        data = {
            'id': 1, 
            'matricula_aluno': 1234
        }
        res = self.cliente.post(path='/prova', json=data)
        data['id'] = 2
        res = self.cliente.post(path='/prova', json=data)

        #cadastrar_gabarito
        data = {
            'id_prova': 1,
            'questoes':[
            {
                'num_questao': 1,
                'peso_questao': 5,
                'alternativa': 'A'
            },
            {
                'num_questao': 2,
                'peso_questao': 5,
                'alternativa': 'C'
            }]
        }
        res = self.cliente.post(path='/gabarito', json=data)
        data['id_prova'] = 2
        res = self.cliente.post(path='/gabarito', json=data)

        #cadastrar_resposta
        data = {
            "id_prova": 1,
            "matricula_aluno": 1234,
            "respostas": [
            {
                "num_questao": 1,
                "alternativa": 'A'
            },
            {
                "num_questao": 2,
                "alternativa": 'C'
            }            
        ]}
        res = self.cliente.post(path='/resposta', json=data)
        data['id_prova'] = 2
        res = self.cliente.post(path='/resposta', json=data)

        res = self.cliente.get(path='/alunos_aprovados')
        self.assertTrue(res.get_json()['matricula_alunos_aprovados'] != [])

    #A entrada e saída de dados deverá ser em JSON
    def test_validar_entrada_dados(self):
        data = 'Não é JSON'

        res = self.cliente.post(path='/prova', data=data)
        self.assertEqual(res.status_code, 400)

        res = self.cliente.post(path='/gabarito', data=data)
        self.assertEqual(res.status_code, 400)

        res = self.cliente.post(path='/resposta', data=data)
        self.assertEqual(res.status_code, 400)

        res = self.cliente.get(path='/nota_final', data=data)
        self.assertEqual(res.status_code, 400)

    def test_validar_saida_dados(self):
        data = {}

        res = self.cliente.post(path='/prova', data=data)
        self.assertIs(res.is_json, True)

        res = self.cliente.post(path='/gabarito', data=data)
        self.assertIs(res.is_json, True)

        res = self.cliente.post(path='/resposta', data=data)
        self.assertIs(res.is_json, True)

        res = self.cliente.get(path='/nota_final', data=data)
        self.assertIs(res.is_json, True) 

if __name__ == '__main__':
    unittest.main()

