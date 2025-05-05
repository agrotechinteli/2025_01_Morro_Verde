import sqlite3

# Função para criar a conexão com o banco de dados SQLite
def criar_conexao():
    return sqlite3.connect('morro_verde.db')

# Função para criar a tabela no banco de dados (caso não exista)
def criar_tabela():
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS fertilizantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        preco REAL NOT NULL,
        fornecedor TEXT NOT NULL,
        data_atualizacao TEXT NOT NULL
    );
    ''')
    conn.commit()
    conn.close()

# Função para inserir dados no banco de dados
def inserir_fertilizante(nome, preco, fornecedor, data_atualizacao):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO fertilizantes (nome, preco, fornecedor, data_atualizacao)
    VALUES (?, ?, ?, ?)
    ''', (nome, preco, fornecedor, data_atualizacao))
    conn.commit()
    conn.close()

# Função para consultar os dados no banco de dados
def consultar_fertilizantes():
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM fertilizantes')
    dados = cursor.fetchall()
    conn.close()
    return dados
