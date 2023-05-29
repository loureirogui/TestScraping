############################# GUILHERME C. LOUREIRO ############################################################
# O código abaixo tem como objetivo coletar o conteudo de elementos html pela classe, além de lidar com o sistema de paginação do site
# disponível na variável 'URL'. Utilizando laços de repetição e try/excepts para apenas ser notificado em caso de erro,
# mas não interromper a execução do código e continuar alimentanto o banco de dados mySQL para fins de estudos.

# O código abaixo disponibilizado na data disponível em detalhes do reposítório Github tem como objetivo, apenas estudos, isentando o criador de reproduções indevidas por parte de terceiros.


import requests  #Caso não possua o pacote instalado, favor executar o comando (pip install requests) no seu terminal.
from bs4 import BeautifulSoup #Caso não possua o pacote instalado, favor executar o comando (pip install beautifulsoup4) 
import mysql.connector #Python mySQL connector download link https://dev.mysql.com/downloads/connector/python/

# Configurações de conexão com o banco de dados MySQL
config = {
    'host': '##########',  # Nome do host do seu banco de dados MySQL
    'user': '####',  # Nome de usuário do banco de dados
    'password': '#####',  # Senha do banco de dados
    'database': '#####'  # Nome do banco de dados a ser utilizado
}

url = 'https://www.telenumeros.com/?dir=pesquisa&nome=&telefone=&endereco=&cidade=Curitiba&estado=PR'
#Link onde vamos realizar o scrape para testes, como sou de curitiba, filtrei os cadastros no site. 
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
}

site = requests.get(url, headers=headers)
soup = BeautifulSoup(site.content, 'html.parser')
cadastros = soup.find_all('div', id='content')
ultima_pagina = 104011

# Estabelecer conexão com o banco de dados MySQL
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

# Criar tabela no banco de dados MySQL usando um auto increment de id para facilitar a navegação entre os cadastros para futuros testes
create_table_query = '''
CREATE TABLE IF NOT EXISTS MYTABLE (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255),
    telefone VARCHAR(255),
    endereco VARCHAR(255)
)
'''
cursor.execute(create_table_query)
conn.commit()

for i in range(1, int(ultima_pagina)): #De 1 até 104011 
    url_pag = f'https://www.telenumeros.com/?dir=pesquisa&pesquisa=cidade:Curitiba%20AND%20estado:PR%20&da={i}'
    site = requests.get(url_pag, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    cadastros = soup.find_all('div', id='content')

    for cadastro in cadastros:
        try:
            nome = cadastro.find('td', class_='cerca').get_text().strip()
            telefone = cadastro.find('td', class_='dativ').get_text().strip()[11:]
            endereco = cadastro.find('td', class_='dati').get_text().strip()
        except (AttributeError, IndexError) as e:
            # Caso ocorra um erro, pular para o próximo cadastro
            print(f"Erro ao obter dados do cadastro: {e}")
            continue

            # Inserir os dados no banco de dados MySQL
        try:
            insert_query = 'INSERT INTO loremar (nome, telefone, endereco) VALUES (%s, %s, %s)'
            values = (nome, telefone, endereco)
            cursor.execute(insert_query, values)
            conn.commit()
            linha = nome + ';' + telefone + ';' + endereco + '\n'
            print(linha)
        except mysql.connector.Error as e:
            # Tratar o erro ao inserir no banco de dados
            print(f"Erro ao inserir dados no banco de dados: {e}")
            continue
# Fechar a conexão com o banco de dados MySQL
cursor.close()
conn.close()
        