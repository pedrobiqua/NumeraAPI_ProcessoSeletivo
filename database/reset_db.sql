-- Limpar o conteúdo das tabelas no banco de dados pesquisa_funcionarios

-- Uso do banco de dados
USE pesquisa_funcionarios;

-- Desabilitar restrições de chave estrangeira temporariamente
SET FOREIGN_KEY_CHECKS = 0;

-- Limpar o conteúdo das tabelas
TRUNCATE TABLE respostas;
TRUNCATE TABLE perguntas;
TRUNCATE TABLE pesquisas;

-- Habilitar novamente as restrições de chave estrangeira
SET FOREIGN_KEY_CHECKS = 1;

-- Exibir todas as tabelas para verificar se foram limpas
SHOW TABLES;

