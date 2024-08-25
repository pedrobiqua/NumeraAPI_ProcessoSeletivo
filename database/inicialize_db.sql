-- script_pesquisa_funcionarios.sql

-- Remover o banco de dados se ele já existir
DROP DATABASE IF EXISTS pesquisa_funcionarios;

-- Criação do banco de dados
CREATE DATABASE pesquisa_funcionarios;

-- Uso do banco de dados criado
USE pesquisa_funcionarios;

-- Criação da tabela de pesquisas
CREATE TABLE pesquisas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL
);

-- Criação da tabela de perguntas
CREATE TABLE perguntas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pesquisa_id INT,
    texto_pergunta TEXT NOT NULL,
    FOREIGN KEY (pesquisa_id) REFERENCES pesquisas(id)
);

-- Criação da tabela de respostas
CREATE TABLE respostas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pergunta_id INT,
    resposta JSON NULL,
    FOREIGN KEY (pergunta_id) REFERENCES perguntas(id)
);

-- Inserção de dados na tabela de pesquisas
INSERT INTO pesquisas (titulo) VALUES
('Pesquisa de Satisfação 2024'),
('Avaliação de Desempenho 2024');

-- Inserção de dados na tabela de perguntas
INSERT INTO perguntas (pesquisa_id, texto_pergunta) VALUES
(1, 'Como você avalia sua satisfação geral com a empresa?'),
(1, 'Quais áreas da empresa você acredita que precisam de melhorias?'),
(2, 'Como você avalia seu desempenho no último ano?'),
(2, 'Você se sente apoiado pela gerência em suas tarefas diárias?');

-- Exibir todas as tabelas criadas
SHOW TABLES;
