from models.cliente import Cliente
from database.db import get_connection

# Regra de negócio: limite de saque da Pessoa Física tem que ser
# MENOR que o limite de Pessoa Jurídica
LIMITE_SAQUE_PF = 2000.0


class PessoaFisica(Cliente):
    """
    Representa um cliente Pessoa Física do banco.
    Implementa o contrato definido pela interface Cliente.
    """

    def __init__(self, id=None, renda_mensal=0.0, idade=0, nome_completo="",
                 celular="", email="", categoria="", saldo=0.0):
        self.id = id
        self.renda_mensal = renda_mensal
        self.idade = idade
        self.nome_completo = nome_completo
        self.celular = celular
        self.email = email
        self.categoria = categoria
        self.saldo = saldo

    def sacar(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("O valor do saque deve ser maior que zero.")

        if valor > LIMITE_SAQUE_PF:
            raise ValueError(
                f"Valor excede o limite de saque para Pessoa Física "
                f"(limite: R$ {LIMITE_SAQUE_PF:.2f})."
            )

        if valor > self.saldo:
            raise ValueError("Saldo insuficiente.")

        self.saldo -= valor
        self._atualizar_saldo_no_banco()

    def extrato(self) -> str:
        return (
            f"Extrato - Pessoa Física\n"
            f"Nome: {self.nome_completo}\n"
            f"Categoria: {self.categoria}\n"
            f"Saldo atual: R$ {self.saldo:.2f}"
        )

    def _atualizar_saldo_no_banco(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE pessoa_fisica SET saldo = ? WHERE id = ?",
            (self.saldo, self.id)
        )
        conn.commit()
        conn.close()

    def to_dict(self) -> dict:
        """Facilita transformar o objeto em JSON na hora de responder na API."""
        return {
            "id": self.id,
            "renda_mensal": self.renda_mensal,
            "idade": self.idade,
            "nome_completo": self.nome_completo,
            "celular": self.celular,
            "email": self.email,
            "categoria": self.categoria,
            "saldo": self.saldo,
        }