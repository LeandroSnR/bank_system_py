import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "banco.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def criar_tabelas():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS pessoa_fisica(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    renda_mensal REAL,
                    idade INTEGER,
                    nome_completo TEXT,
                    celular TEXT,
                    email TEXT,
                    categoria TEXT,
                    saldo REAL);
                    """)
    
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS pessoa_juridica(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    razao_social TEXT,
                    cnpj TEXT,
                    faturamento_mensal REAL,
                    celular TEXT,
                    email TEXT,
                    categoria TEXT,
                    saldo REAL);
                    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    criar_tabelas()
    print(f"Banco de dados criado/atualizado em {DB_PATH}")
