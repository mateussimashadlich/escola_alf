/*DROP TABLE IF EXISTS aluno;*/
DROP TABLE IF EXISTS gabarito;
DROP TABLE IF EXISTS resposta;

/*CREATE TABLE aluno(
    matricula INTEGER PRIMARY KEY
);*/

CREATE TABLE gabarito(
    id_prova INTEGER,
    num_questao INTEGER,
    peso_questao INTEGER,
    alternativa CHAR,
    PRIMARY KEY(id_prova, num_questao)
);

CREATE TABLE resposta(
    id_prova INTEGER,
    id_aluno INTEGER,
    num_questao INTEGER,
    alternativa CHAR,        
    FOREIGN KEY(id_prova) REFERENCES gabarito(id_prova),
    PRIMARY KEY(id_prova, id_aluno, num_questao)
);
/*
CREATE TABLE prova(
    id INTEGER PRIMARY KEY,
    gabarito INTEGER,
    aluno INTEGER,
    nota INTEGER,
    FOREIGN KEY(gabarito) REFERENCES gabarito(id),
    FOREIGN KEY(aluno) REFERENCES aluno(matricula)
);

CREATE TABLE aluno(
    matricula INTEGER PRIMARY KEY
);

CREATE TABLE gabarito(
    id INTEGER,
    num_questao INTEGER,
    alternativa CHAR,
    PRIMARY KEY(id, num_questao)
);

CREATE TABLE resposta(
    prova INTEGER,
    num_questao INTEGER,
    peso_questao INTEGER,
    alternativa CHAR,
    FOREIGN KEY(prova) REFERENCES prova(id)
);

CREATE TABLE prova(
    id INTEGER PRIMARY KEY,
    gabarito INTEGER,
    aluno INTEGER,
    nota INTEGER,
    FOREIGN KEY(gabarito) REFERENCES gabarito(id),
    FOREIGN KEY(aluno) REFERENCES aluno(matricula)
);
*/