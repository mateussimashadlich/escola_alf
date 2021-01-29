<h1>Escola Alf</h1>
<p>API desenvolvida em Flask para o cadastro de provas, gabaritos e respostas de alunos da escola Alf.</p>
<h2>Instalação</h2>
<p>Para executar a API, você precisará instalar na sua máquina:</p>
<ul>
  <li><a href="https://www.python.org/downloads/">Python</a></li>
  <li><a href="https://flask.palletsprojects.com/en/1.1.x/">Flask</a></li>
  <li><a href="https://flask-sqlalchemy.palletsprojects.com/en/2.x/">Flask-SQLAlchemy</a></li>
</ul>
<p>Com o Python instalado, utilize no seu terminal o comando a seguir para instalar o Flask:</p>
<p><code>pip install flask</code></p>
<p>E para o SQLAlchemy:</p>
<p><code>pip install flask-sqlalchemy</code></p>
<h2>Utilização</h2>
<p>Agora para executar a aplicação, vá até a pasta do projeto e digite:</p>
<p><code>flask run</code></p>
<p>O arquivo app.py será executado e o servidor da API será inicializado.</p>
<h3>Endpoints</h3>
<p>A API disponibiliza os seguintes endpoints:</p>
<ul>
  <li><a href="#post-prova">Cadastrar prova</a></li>
  <li><a href="#post-gabarito">Cadastrar gabarito da prova</a></li>
  <li><a href="#post-resposta">Cadastrar respostas do aluno</a></li>
  <li><a href="#get-nota_final">Verificar nota final do aluno</a></li>
  <li><a href="#get-alunos_aprovados">Listar alunos aprovados</a></li>
  <li><a href="#get-prova">Listar provas</a></li>
  <li><a href="#get-gabarito">Listar gabaritos</a></li>
  <li><a href="#get-resposta">Listar respostas dos alunos</a></li>
  
</ul>
<br>
<section id="/prova">
<h3><code>POST /prova</code></h3>
  <p><blockquote>Este endpoint aceita apenas dados formatados em JSON.</blockquote></p>
  <p>Cadastra uma prova com uma matricula de aluno. Não é possível ter mais de 100 alunos diferentes cadastrados em todas as provas.</p>
  <h4>Parâmetros</h4>
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
    <pre><code>curl --location --request POST 'http://127.0.0.1:5000/prova' --header 'Content-Type: application/json' --data-raw '{"id": x, "matricula_aluno": y}'</code></pre>
    <p>Exemplo de resposta em uma requisição bem-sucedida:</p>
    <pre><code>  
    {
      "mensagem": "Prova criada com sucesso!"
    } 
    </code></pre>
<br>
<h3><code>GET /prova</code></h3>
  <p>Retorna as provas dos alunos.</p>
    <pre><code>curl --location --request GET 'http://127.0.0.1:5000/prova'</code></pre>
    <p>Exemplo de resposta:</p>
    <pre><code>  
    {
      "provas": [
        {
          "id": 5,
          "matricula_aluno": 2
        }
      ]
    } 
    </code></pre>
</section>
<br>
<section id="/gabarito">
<h3><code>POST /gabarito</code></h3>
  <p><blockquote>Este endpoint aceita apenas dados formatados em JSON.</blockquote></p>
  <p>Cria um gabarito para uma prova previamente criada, a soma dos pontos das questões precisa estar acima de 0 e não ser maior do que 10.</p>
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
    <h4>Questão</h4>
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
    <p>Exemplo de dados em uma requisição:</p>
    <pre><code>
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
  <pre><code>curl --location --request POST 'http://127.0.0.1:5000/gabarito' --header 'Content-Type: application/json' --data-raw '{"id_prova": x, "questoes": questoes}'</code></pre>
  <p>Exemplo de resposta em uma requisição bem-sucedida:</p>
  <pre><code>  
    {
      "mensagem": "Gabarito criado com sucesso!"
    }</code></pre>
    
<br>
<h3><code>GET /gabarito</code></h3>
  <p>Retorna os gabaritos das provas.</p>
    <pre><code>curl --location --request GET 'http://127.0.0.1:5000/gabarito'</code></pre>
    <p>Exemplo de resposta:</p>
    <pre><code>  
    {
      "gabaritos": [
        {
            "id_prova": 4,
            "questoes": [
                {
                    "alternativa": "A",
                    "num_questao": 4,
                    "peso_questao": 3
                },
                {
                    "alternativa": "A",
                    "num_questao": 8,
                    "peso_questao": 3
                },
                {
                    "alternativa": "B",
                    "num_questao": 9,
                    "peso_questao": 3
                }
            ]
        },
        {
            "id_prova": 5,
            "questoes": [
                {
                    "alternativa": "A",
                    "num_questao": 4,
                    "peso_questao": 3
                },
                {
                    "alternativa": "A",
                    "num_questao": 8,
                    "peso_questao": 3
                },
                {
                    "alternativa": "B",
                    "num_questao": 9,
                    "peso_questao": 3
                }
            ]
        }
    ]
  }
    </code></pre>
</section>
<br>
<section id="/resposta">
  <h3><code>POST /resposta</code></h3>
    <p><blockquote>Este endpoint aceita apenas dados formatados em JSON.</blockquote></p>
    <p>Registra as respostas do aluno para a prova dele.</p>    
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
      <p>Exemplo de dados em uma requisição:</p>
      <pre><code>
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
      }</code></pre>
    <pre><code>curl --location --request POST 'http://127.0.0.1:5000/resposta' --header 'Content-Type: application/json' --data-raw '{"id_prova": x, "matricula_aluno": y, "respostas": respostas}'</code></pre>
  <p>Exemplo de resposta em uma requisição bem-sucedida:</p>
  <pre><code>  
  {
    "mensagem": "Resposta(s) cadastrada(s) com sucesso!"
  }</code></pre>
 
<h3><code>GET /resposta</code></h3>
  <p>Retorna as respostas dos alunos nas provas.</p>
    <pre><code>curl --location --request GET 'http://127.0.0.1:5000/resposta'</code></pre>
    <p>Exemplo de resposta:</p>
    <pre><code>  
      {
        "respostas": [
            {
              "matricula_aluno": 2,
              "respostas_aluno": [
                {
                  "alternativa": "A",
                  "num_questao": 8
                },
                {
                  "alternativa": "A",
                  "num_questao": 4
                },
                {
                  "alternativa": "B",
                  "num_questao": 9
                }
             }
          ]
      }
    </code></pre>
</section>
<section id="/nota_final">
  <h3><code>GET /nota_final</code></h3>
  <p><blockquote>Este endpoint aceita apenas dados formatados em JSON.</blockquote></p>
  <p>Retorna a nota final do aluno, baseado na média aritmética de suas provas.</p>
  <h4>Parâmetros</h4>
  <table>
    <tr>
      <td><strong>Nome</strong></td>
      <td><strong>Tipo de dado</strong></td>
      <td><strong>Obrigatório</strong></td>
      <td><strong>Descrição</strong></td>
    </tr>
    <tr>
      <td><i>matricula_aluno</i></td>
      <td>int</td>
      <td>Sim</td>
      <td>Matricula do aluno</td>
    </tr>
  </table>
  <p>Exemplo de dados em uma requisição:</p>
  <pre><code>
  {
    "matricula_aluno": 1
  }
  </code></pre>
  <pre><code>curl --location --request GET 'http://127.0.0.1:5000/nota_final' --header 'Content-Type: application/json' --data-raw '{"matricula_aluno": x}'</code></pre>
  <p>Exemplo de resposta:</p>
  <pre><code>  
  {
    "nota_final": 6.5
  }</code></pre>
</section>
<br>
<section id="/alunos_aprovados">
  <h3><code>GET /alunos_aprovados</code></h3>    
  <p>Lista todos os alunos com média de notas maior ou igual a 7, ou seja, aprovados.</p>
  <pre><code>curl --location --request GET 'http://127.0.0.1:5000/alunos_aprovados'</code></pre>
  <p>Exemplo de resposta:</p>
  <pre><code> 
  {
    "matricula_alunos_aprovados": [1234, 5678]
  }</code></pre>
</section>
