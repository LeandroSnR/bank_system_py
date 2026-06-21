from models.cliente import Cliente
from database.db import get_connection

# Tem que ser MAIOR que o limite de Pessoa Física (2000.0)
LIMITE_SAQUE_PJ = 10000.0


class PessoaJuridica(Cliente):
    """
    Representa um cliente Pessoa Jurídica do banco.
    Implementa o contrato definido pela interface Cliente.
    """

    def __init__(self, id=None, razao_social="", cnpj="", faturamento_mensal=0.0,
        celular="", email="", categoria="", saldo=0.0):
        self.id = id
        self.razao_social = razao_social
        self.cnpj = cnpj
        self.faturamento_mensal = faturamento_mensal
        self.celular = celular
        self.email = email
        self.categoria = categoria
        self.saldo = saldo

    def sacar(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("O valor do saque deve ser maior que zero.")

        if valor > LIMITE_SAQUE_PJ:
            raise ValueError(
                f"Valor excede o limite de saque para Pessoa Jurídica "
                f"(limite: R$ {LIMITE_SAQUE_PJ:.2f})."
            )

        if valor > self.saldo:
            raise ValueError("Saldo insuficiente.")

        self.saldo -= valor
        self._atualizar_saldo_no_banco()

    def extrato(self) -> str:
        return (
            f"Extrato - Pessoa Jurídica\n"
            f"Razão Social: {self.razao_social}\n"
            f"Categoria: {self.categoria}\n"
            f"Saldo atual: R$ {self.saldo:.2f}"
        )

    def _atualizar_saldo_no_banco(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE pessoa_juridica SET saldo = ? WHERE id = ?",
            (self.saldo, self.id)
        )
        conn.commit()
        conn.close()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "razao_social": self.razao_social,
            "cnpj": self.cnpj,
            "faturamento_mensal": self.faturamento_mensal,
            "celular": self.celular,
            "email": self.email,
            "categoria": self.categoria,
            "saldo": self.saldo,
        }