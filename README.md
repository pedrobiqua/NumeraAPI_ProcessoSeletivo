### Passo a Passo Para Utilizar a API localmente

#### 1. **Instalar MariaDB**

1. **Atualizar o sistema**:

   ```bash
   sudo apt update
   sudo apt upgrade
   ```

2. **Instalar MariaDB**:

   ```bash
   sudo apt install mariadb-server
   ```

3. **Verificar o status do MariaDB**:

   ```bash
   sudo systemctl status mariadb
   ```

   O status deve indicar que o serviço está ativo e em execução.

4. **Configurar MariaDB**:

   Execute o script de segurança para configurar a senha do root e remover usuários desnecessários:

   ```bash
   sudo mysql_secure_installation
   ```

   Siga as instruções para definir a senha do root e ajustar as configurações de segurança conforme desejado.

5. **Criar Banco de Dados e Tabelas**:

   Acesse o MariaDB:

   ```bash
   sudo mysql -u root -p
   ```

   Digite a senha do root quando solicitado.

   Execute os seguintes comandos no prompt do MariaDB para criar o banco de dados e as tabelas necessárias:

   ```sql
   CREATE DATABASE pesquisa_funcionarios;

   USE pesquisa_funcionarios;

   CREATE TABLE pesquisas (
       id INT AUTO_INCREMENT PRIMARY KEY,
       titulo VARCHAR(255) NOT NULL
   );

   CREATE TABLE perguntas (
       id INT AUTO_INCREMENT PRIMARY KEY,
       pesquisa_id INT,
       texto_pergunta TEXT,
       FOREIGN KEY (pesquisa_id) REFERENCES pesquisas(id)
   );

   CREATE TABLE respostas (
       id INT AUTO_INCREMENT PRIMARY KEY,
       pergunta_id INT,
       resposta JSON,
       FOREIGN KEY (pergunta_id) REFERENCES perguntas(id)
   );
   ```

   Saia do MariaDB digitando `exit`.

#### 2. **Preparar o Ambiente**

1. **Baixar as dependências do projeto**:

   Certifique-se de que você tem um arquivo `requirements.txt` no repositório. Para instalar as dependências listadas no `requirements.txt`, execute:

   ```bash
   pip install -r requirements.txt
   ```

   O arquivo `requirements.txt` deve conter todas as dependências necessárias para o projeto.
   
#### 3. **Rodar a Aplicação**

1. **Comando**
  ```bash
  python3 run.py
  ```
