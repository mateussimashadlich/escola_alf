<h1>Escola Alf</h1>
<p>API desenvolvida em Flask para o cadastro de provas, gabaritos e respostas de alunos da escola Alf.</p>
<h2>Setup</h2>
<p>Para executar a API, você precisará instalar na sua máquina:</p>
<ul>
  <li><a href="https://www.python.org/downloads/">Python</a></li>
  <li><a href="https://flask.palletsprojects.com/en/1.1.x/">Flask</a></li>
</ul>
<p>Com o Python instalado, utilize no seu terminal o comando a seguir para instalar o Flask:</p>
<p><code>pip install flask</code></p>
<p>Agora para executar a aplicação, vá até a pasta do projeto e digite:</p>
<p><code>flask run</code></p>
<p>O arquivo app.py será executado e o servidor da API será inicializado.</p>
<h2>Endpoints</h2>
A API disponibiliza os seguintes endpoints:
<ul>
  <li>[Cadastrar prova](#/prova)</a></li>
  <li><a href="#post-prova">Cadastrar gabarito da prova</a></li>
  <li><a href="https://github.com/mateussimashadlich/escola_alf/README.md#post-prova">Cadastrar respostas do aluno</a></li>
  <li><a href="#">Verificar nota final do aluno</a></li>
  <li><a href="#">Listar alunos aprovados</a></li>
</ul>
<br>
## Prova
<h3><code>POST /prova</code></h3>
  <p><blockquote>Este endpoint aceita apenas dados formatados em JSON.</blockquote></p>
  <h4>Parâmetros</h4>
  <code>
    <table>
      <tr>
        <td><strong>Nome</strong></td>
        <td><strong>Tipo de dado</strong></td>
        <td><strong>Obrigatório</strong></td>
        <td><strong>Descrição</strong></td>
      </tr>
      <tr>
        <td><i>id</i></td>
        <td>Inteiro</td>
        <td>Sim</td>
        <td>Identificador da prova</td>
      </tr>
      <tr>
        <td><i>matricula_aluno</i></td>
        <td>Inteiro</td>
        <td>Sim</td>
        <td>Matricula do aluno que fará a prova</td>
      </tr>      
    </table>
    <pre><code>curl --header "Content-Type: application/json" --request POST --data '{"id": <valor>, "matricula_aluno": <valor>}" http://127.0.0.1:5000/prova</code></pre>
</section>
<section id="/gabarito">
<h3><code>POST /gabarito</code></h3>
  <p><blockquote>Este endpoint aceita apenas dados formatados em JSON.</blockquote></p>
  <h4>Parâmetros</h4>
    <table>
      <tr>
        <td><strong>Nome</strong></td>
        <td><strong>Tipo de dado</strong></td>
        <td><strong>Obrigatório</strong></td>
        <td><strong>Descrição</strong></td>
      </tr>
      <tr>
        <td><i>id_prova</i></td>
        <td>int</td>
        <td>Sim</td>
        <td>Identificador da prova do gabarito</td>
      </tr>
      <tr>
        <td><i>questoes</i></td>
        <td>list</td>
        <td>Sim</td>
        <td>Lista de questões atreladas ao gabarito</td>        
      </tr>
    </table>
    <h4>Questao</h4>
    <p>Cada questão também precisa estar formatada em JSON, seguindo o modelo de dicionários do Python.</p>
    <table>
      <tr>
        <td><strong>Nome</strong></td>
        <td><strong>Tipo de dado</strong></td>
        <td><strong>Obrigatório</strong></td>
        <td><strong>Descrição</strong></td>          
      </tr>
      <tr>
        <td>num_questao</td>
        <td>int</td>
        <td>Sim</td>
        <td>Número da questão.</td>
      </tr>
      <tr>
        <td>peso_questao</td>
        <td>int</td>
        <td>Sim</td>
        <td>Peso da questão.</td>
      </tr>
      <tr>
        <td>alternativa</td>
        <td>string</td>
        <td>Sim</td>
        <td>Alternativa correta da questão (Ex: A).</td>
      </tr>      
    </table>
    <pre><code>
    #Ex. Gabarito    
    {
      "id_prova": 1,
      "questoes":[
        {
            "num_questao": 1,
            "peso_questao": 1,
            "alternativa": "A"
        },
        {
            "num_questao": 2,
            "peso_questao": 1,
            "alternativa": "C"
        }
      ]
    }
    </code></pre>
  <pre><code>curl --header "Content-Type: application/json" --request POST --data '{gabarito}' http://127.0.0.1:5000/gabarito</code></pre>
</section>
  <section id="/resposta">
<h3><code>POST /resposta</code></h3>
  <p><blockquote>Este endpoint aceita apenas dados formatados em JSON.</blockquote></p>
  <h4>Parâmetros</h4>
    <table>
      <tr>
        <td><strong>Nome</strong></td>
        <td><strong>Tipo de dado</strong></td>
        <td><strong>Obrigatório</strong></td>
        <td><strong>Descrição</strong></td>
      </tr>
      <tr>
        <td><i>id_prova</i></td>
        <td>int</td>
        <td>Sim</td>
        <td>Identificador da prova ao qual a resposta corresponde.</td>
      </tr>
      <tr>
        <td><i>matricula_aluno</i></td>
        <td>int</td>
        <td>Sim</td>
        <td>Matricula do aluno que realizou as respostas.</td>        
      </tr>
      <tr>
        <td><i>respostas</i></td>
        <td>list</td>
        <td>Sim</td>
        <td>Respostas do aluno.</td>        
      </tr>      
    </table>
    <h4>Resposta</h4>
    <p>Cada questão também precisa estar formatada em JSON, seguindo o modelo de dicionários do Python.</p>
    <table>
      <tr>
        <td><strong>Nome</strong></td>
        <td><strong>Tipo de dado</strong></td>
        <td><strong>Obrigatório</strong></td>
        <td><strong>Descrição</strong></td>          
      </tr>
      <tr>
        <td>num_questao</td>
        <td>int</td>
        <td>Sim</td>
        <td>Número da questão.</td>
      </tr>
      <tr>
        <td>alternativa</td>
        <td>string</td>
        <td>Sim</td>
        <td>Alternativa utilizada como resposta para a questão.</td>
      </tr>      
    </table>
    <pre><code>
    #Ex. Respostas   
    {
      "id_prova": 1,
      "matricula_aluno": 1,
      "respostas":[
        {
            "num_questao": 1,
            "alternativa": "A"
        },
        {
            "num_questao": 2,
            "alternativa": "E"
        }
      ]
    }
    </code></pre>
  <pre><code>curl --header "Content-Type: application/json" --request POST --data '{respostas_aluno}' http://127.0.0.1:5000/resposta</code></pre>
</section>
