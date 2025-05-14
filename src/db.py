import sqlite3

def criar_tabelas():
    conn = sqlite3.connect("morro_verde.db")
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS fertilizantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco TEXT NOT NULL,
            fornecedor TEXT NOT NULL,
            data_atualizacao DATE NOT NULL
        );     

        CREATE TABLE IF NOT EXISTS produto (
            id_produto INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            tipo TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS localizacao (
            id_localizacao INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            tipo TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS preco (
            id_preco INTEGER PRIMARY KEY,
            id_produto INTEGER NOT NULL,
            id_localizacao INTEGER NOT NULL,
            data_preco DATE NOT NULL,
            preco_usd TEXT,
            preco_brl TEXT,
            tipo_preco TEXT
        );

        CREATE TABLE IF NOT EXISTS frete (
            id_frete INTEGER PRIMARY KEY,
            origem INTEGER NOT NULL,
            destino INTEGER NOT NULL,
            tipo_transporte TEXT NOT NULL,
            preco_usd TEXT,
            preco_brl TEXT,
            data_frete DATE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS barter (
            id_barter INTEGER PRIMARY KEY,
            cultura TEXT NOT NULL,
            id_produto INTEGER NOT NULL,
            estado TEXT NOT NULL,
            preco_npk TEXT,
            preco_cultura TEXT,
            razao_barter TEXT,
            data DATE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS acordos_barter (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produtor_nome TEXT,
            cpf_cnpj TEXT,
            insumo_fornecido TEXT,
            quantidade_insumo REAL,
            unidade_insumo TEXT,
            valor_estimado REAL,
            cultura_destinada TEXT,
            producao_estimativa_tons REAL,
            data_contrato DATE,
            data_entrega_prevista DATE,
            status_contrato TEXT
        );

        CREATE TABLE IF NOT EXISTS produtores (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()

   

def inserir_fertilizante(nome, preco, fornecedor, data):
    conn = sqlite3.connect("morro_verde.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO fertilizantes (nome, preco, fornecedor, data_atualizacao)
        VALUES (?, ?, ?, ?)
    """, (nome, preco, fornecedor, data))
    conn.commit()
    conn.close()


def consultar_fertilizantes():
    """
    Retorna uma lista de todos os fertilizantes cadastrados.
    """
    conn = sqlite3.connect("morro_verde.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fertilizantes")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def filtrar_fertilizantes(filtro):
    conn = sqlite3.connect("morro_verde.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fertilizantes WHERE nome LIKE ?", ('%' + filtro + '%',))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def consultar_frete():
    conn = sqlite3.connect("morro_verde.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM frete")
    resultados = cursor.fetchall()
    conn.close()
    return resultados
