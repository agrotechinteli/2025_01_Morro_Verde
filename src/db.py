import sqlite3

DB_PATH = 'morro_verde.db'

def criar_conexao():
    """Cria uma conexão com o banco SQLite e ativa as foreign keys."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute('PRAGMA foreign_keys = ON')
    return conn

def criar_tabelas():
    """Cria todas as tabelas necessárias no banco de dados."""
    tabelas = {
        "produto": '''
            CREATE TABLE IF NOT EXISTS produto (
                id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                tipo TEXT NOT NULL
            );
        ''',
        "localizacao": '''
            CREATE TABLE IF NOT EXISTS localizacao (
                id_localizacao INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                tipo TEXT NOT NULL
            );
        ''',
        "preco": '''
            CREATE TABLE IF NOT EXISTS preco (
                id_preco INTEGER PRIMARY KEY AUTOINCREMENT,
                id_produto INTEGER NOT NULL,
                id_localizacao INTEGER NOT NULL,
                data_preco DATE NOT NULL,
                preco_usd TEXT,
                preco_brl TEXT,
                tipo_preco TEXT,
                FOREIGN KEY (id_produto) REFERENCES produto(id_produto),
                FOREIGN KEY (id_localizacao) REFERENCES localizacao(id_localizacao)
            );
        ''',
        "frete": '''
            CREATE TABLE IF NOT EXISTS frete (
                id_frete INTEGER PRIMARY KEY AUTOINCREMENT,
                origem INTEGER NOT NULL,
                destino INTEGER NOT NULL,
                tipo_transporte TEXT NOT NULL,
                preco_usd TEXT,
                preco_brl TEXT,
                data_frete DATE NOT NULL,
                FOREIGN KEY (origem) REFERENCES localizacao(id_localizacao),
                FOREIGN KEY (destino) REFERENCES localizacao(id_localizacao)
            );
        ''',
        "barter": '''
            CREATE TABLE IF NOT EXISTS barter (
                id_barter INTEGER PRIMARY KEY AUTOINCREMENT,
                cultura TEXT NOT NULL,
                id_produto INTEGER NOT NULL,
                estado TEXT NOT NULL,
                preco_npk TEXT,
                preco_cultura TEXT,
                razao_barter TEXT,
                data DATE NOT NULL,
                FOREIGN KEY (id_produto) REFERENCES produto(id_produto)
            );
        '''
    }

    conn = criar_conexao()
    cursor = conn.cursor()
    for nome, ddl in tabelas.items():
        cursor.execute(ddl)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    criar_tabelas()
    print("Tabelas criadas com sucesso.")
