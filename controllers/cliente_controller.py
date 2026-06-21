from database.db import get_connection
from models.pessoa_fisica import PessoaFisica
from models.pessoa_juridica import PessoaJuridica


def criar_pessoa_fisica(dados: dict) -> dict:
    """
    Recebe um dicionário com os dados de uma Pessoa Física,
    salva no banco e retorna o cliente criado (já com id).
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO pessoa_fisica (renda_mensal, idade, nome_completo, celular, email, categoria, saldo)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            dados.get("renda_mensal", 0.0),
            dados.get("idade", 0),
            dados.get("nome_completo", ""),
            dados.get("celular", ""),
            dados.get("email", ""),
            dados.get("categoria", ""),
            dados.get("saldo", 0.0),
        )
    )
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()

    cliente = PessoaFisica(id=novo_id, **dados)
    return cliente.to_dict()


def criar_pessoa_juridica(dados: dict) -> dict:
    """
    Recebe um dicionário com os dados de uma Pessoa Jurídica,
    salva no banco e retorna o cliente criado (já com id).
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO pessoa_juridica (razao_social, cnpj, faturamento_mensal, celular, email, categoria, saldo)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            dados.get("razao_social", ""),
            dados.get("cnpj", ""),
            dados.get("faturamento_mensal", 0.0),
            dados.get("celular", ""),
            dados.get("email", ""),
            dados.get("categoria", ""),
            dados.get("saldo", 0.0),
        )
    )
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()

    cliente = PessoaJuridica(id=novo_id, **dados)
    return cliente.to_dict()


def listar_pessoas_fisicas() -> list:
    """Retorna todas as Pessoas Físicas cadastradas, como lista de dicionários."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pessoa_fisica")
    linhas = cursor.fetchall()
    conn.close()

    clientes = [PessoaFisica(**dict(linha)) for linha in linhas]
    return [c.to_dict() for c in clientes]


def listar_pessoas_juridicas() -> list:
    """Retorna todas as Pessoas Jurídicas cadastradas, como lista de dicionários."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pessoa_juridica")
    linhas = cursor.fetchall()
    conn.close()

    clientes = [PessoaJuridica(**dict(linha)) for linha in linhas]
    return [c.to_dict() for c in clientes]

def sacar_pessoa_fisica(id_cliente: int, valor: float) -> dict:
    """
    Busca uma Pessoa Física pelo id, realiza o saque e retorna
    o cliente atualizado.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pessoa_fisica WHERE id = ?", (id_cliente,))
    linha = cursor.fetchone()
    conn.close()

    if linha is None:
        raise ValueError(f"Pessoa Física com id {id_cliente} não encontrada.")

    cliente = PessoaFisica(**dict(linha))
    cliente.sacar(valor)  # aqui a regra de negócio do Model é aplicada
    return cliente.to_dict()


def extrato_pessoa_fisica(id_cliente: int) -> str:
    """Busca uma Pessoa Física pelo id e retorna o extrato."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pessoa_fisica WHERE id = ?", (id_cliente,))
    linha = cursor.fetchone()
    conn.close()

    if linha is None:
        raise ValueError(f"Pessoa Física com id {id_cliente} não encontrada.")

    cliente = PessoaFisica(**dict(linha))
    return cliente.extrato()

def sacar_pessoa_juridica(id_cliente: int, valor: float) -> dict:
    """
    Busca uma Pessoa Juridica pelo id, realiza o saque e retorna
    o cliente atualizado.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pessoa_juridica WHERE id = ?", (id_cliente,))
    linha = cursor.fetchone()
    conn.close()

    if linha is None:
        raise ValueError(f"Pessoa Juridica com id {id_cliente} não encontrada.")

    cliente = PessoaJuridica(**dict(linha))
    cliente.sacar(valor)  # aqui a regra de negócio do Model é aplicada
    return cliente.to_dict()


def extrato_pessoa_juridica(id_cliente: int) -> str:
    """Busca uma Pessoa Juridica pelo id e retorna o extrato."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pessoa_juridica WHERE id = ?", (id_cliente,))
    linha = cursor.fetchone()
    conn.close()

    if linha is None:
        raise ValueError(f"Pessoa Juridica com id {id_cliente} não encontrada.")

    cliente = PessoaJuridica(**dict(linha))
    return cliente.extrato()