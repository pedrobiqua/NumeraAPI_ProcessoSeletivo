import pymysql
import json

# Configurações de conexão ao banco de dados
config = {
    'user': 'root',
    'password': '1234',
    'host': 'localhost',
    'database': 'pesquisa_funcionarios'
}

def connection_database():
    connection = pymysql.connect(**config)
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    return connection, cursor

def inserir_pesquisa_e_retornar_id(titulo):
    try:
        connection, cursor = connection_database()

        # Inserir dados na tabela de pesquisas
        sql = "INSERT INTO pesquisas (titulo) VALUES (%s)"
        cursor.execute(sql, (titulo,))
        connection.commit()

        # Obter o ID da pesquisa recém inserida
        pesquisa_id = cursor.lastrowid
        return pesquisa_id

    except pymysql.MySQLError as err:
        print(f"Erro: {err}")
    finally:
        cursor.close()
        connection.close()

def inserir_pergunta_e_retornar_id(pesquisa_id, texto_pergunta):
    try:
        connection, cursor = connection_database()

        # Inserir dados na tabela de perguntas
        sql = "INSERT INTO perguntas (pesquisa_id, texto_pergunta) VALUES (%s, %s)"
        cursor.execute(sql, (pesquisa_id, texto_pergunta))
        connection.commit()

        # Obter o ID da pergunta recém inserida
        pergunta_id = cursor.lastrowid
        return pergunta_id

    except pymysql.MySQLError as err:
        print(f"Erro: {err}")
    finally:
        cursor.close()
        connection.close()

def inserir_respostas_em_lote(pesquisa_id, respostas):
    try:
        connection, cursor = connection_database()

        # Filtra respostas válidas e converte para JSON
        respostas_validas = [(pesquisa_id, json.dumps(resposta)) for resposta in respostas]

        if respostas_validas:
            # Cria o SQL para inserir múltiplas respostas
            sql = "INSERT INTO respostas (pergunta_id, resposta) VALUES (%s, %s)"
            cursor.executemany(sql, respostas_validas)
            connection.commit()

    except pymysql.MySQLError as err:
        print(f"Erro: {err}")
    finally:
        cursor.close()
        connection.close()

def processar_e_inserir_dados(dados, survey_name):
    pesquisa_id = inserir_pesquisa_e_retornar_id(survey_name)

    for pergunta, respostas in dados.items():
        if isinstance(respostas, list):
            respostas_json = []
            for resposta in respostas:
                if isinstance(resposta, list):
                    respostas_json.append(resposta)  # Presume que 'resposta' já está no formato correto
                else:
                    respostas_json.append({"option": resposta})  # Assumir que o formato de resposta é texto
            pergunta_id = inserir_pergunta_e_retornar_id(pesquisa_id, pergunta)
            inserir_respostas_em_lote(pergunta_id, respostas_json)
        else:
            print(f"Dados inválidos para a pergunta: {pergunta}")

def select_all_data():
    try:
        connection, cursor = connection_database()

        # Executar a consulta SQL
        sql = """
        SELECT
            p.titulo AS pesquisa_titulo,
            q.texto_pergunta,
            r.resposta AS resposta_json
        FROM
            pesquisas p
        LEFT JOIN
            perguntas q ON p.id = q.pesquisa_id
        LEFT JOIN
            respostas r ON q.id = r.pergunta_id
        ORDER BY
            p.titulo, q.texto_pergunta, r.resposta;
        """
        cursor.execute(sql)
        results = cursor.fetchall()

        # Organizar os resultados em uma estrutura hierárquica
        organized_results = []
        for row in results:
            pesquisa_titulo = row['pesquisa_titulo']
            texto_pergunta = row['texto_pergunta']
            resposta_json = row['resposta_json']
            
            # Verificar se a pesquisa já está na lista
            pesquisa = next((item for item in organized_results if item['titulo'] == pesquisa_titulo), None)
            if not pesquisa:
                pesquisa = {
                    'titulo': pesquisa_titulo,
                    'perguntas': []
                }
                organized_results.append(pesquisa)
            
            # Verificar se a pergunta já está na pesquisa
            pergunta = next((item for item in pesquisa['perguntas'] if item['texto_pergunta'] == texto_pergunta), None)
            if not pergunta and texto_pergunta:
                pergunta = {
                    'texto_pergunta': texto_pergunta,
                    'respostas': []
                }
                pesquisa['perguntas'].append(pergunta)
            
            if resposta_json:
                pergunta['respostas'].append(json.loads(resposta_json))

        return organized_results

    except pymysql.MySQLError as err:
        # Se tiver erro, o resultado será nada
        print(f"Erro: {err}")
        return []

    finally:
        cursor.close()
        connection.close()
