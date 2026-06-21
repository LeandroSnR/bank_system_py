import unittest
from controllers.cliente_controller import (
    criar_pessoa_fisica,
    sacar_pessoa_fisica,
    extrato_pessoa_fisica,
    criar_pessoa_juridica,
    sacar_pessoa_juridica,
    extrato_pessoa_juridica
)


class TestClienteControllerPF(unittest.TestCase):

    def test_criar_pessoa_fisica(self):
        """Verifica se uma Pessoa Física é criada corretamente."""
        cliente = criar_pessoa_fisica({
            "nome_completo": "Teste Unitário",
            "idade": 25,
            "renda_mensal": 3000.0,
            "celular": "11900000000",
            "email": "teste@email.com",
            "categoria": "comum",
            "saldo": 1000.0
        })

        self.assertEqual(cliente["nome_completo"], "Teste Unitário")
        self.assertEqual(cliente["saldo"], 1000.0)
        self.assertIsNotNone(cliente["id"])

    def test_saque_dentro_do_limite(self):
        """Verifica se um saque válido reduz o saldo corretamente."""
        cliente = criar_pessoa_fisica({"nome_completo": "Saque OK", "saldo": 1000.0})
        resultado = sacar_pessoa_fisica(cliente["id"], 500)

        self.assertEqual(resultado["saldo"], 500.0)

    def test_saque_acima_do_limite_pf(self):
        """Verifica se um saque acima do limite de PF gera erro."""
        cliente = criar_pessoa_fisica({"nome_completo": "Saque Bloqueado", "saldo": 5000.0})

        with self.assertRaises(ValueError):
            sacar_pessoa_fisica(cliente["id"], 3000)  # limite PF é 2000

    def test_extrato_contem_nome_do_cliente(self):
        """Verifica se o extrato traz o nome do cliente correto."""
        cliente = criar_pessoa_fisica({"nome_completo": "Extrato Teste", "saldo": 100.0})
        texto = extrato_pessoa_fisica(cliente["id"])

        self.assertIn("Extrato Teste", texto)

class TestClienteControllerPJ(unittest.TestCase):

    def test_criar_pessoa_juridica(self):
        """Verifica se uma Pessoa juridica é criada corretamente."""
        cliente = criar_pessoa_juridica({
            "razao_social": "Teste Unitário",
            "cnpj": "250000000001",
            "faturamento_mensal": 300000000.0,
            "celular": "11900000000",
            "email": "teste@email.com",
            "categoria": "pública",
            "saldo": 1000000.0
        })

        self.assertEqual(cliente["razao_social"], "Teste Unitário")
        self.assertEqual(cliente["saldo"], 1000000.0)
        self.assertIsNotNone(cliente["id"])

    def test_saque_dentro_do_limite(self):
        """Verifica se um saque válido reduz o saldo corretamente."""
        cliente = criar_pessoa_juridica({"razao_social": "Saque OK", "saldo": 1000000.0})
        resultado = sacar_pessoa_juridica(cliente["id"], 5000)

        self.assertEqual(resultado["saldo"], 995000.0)

    def test_saque_acima_do_limite_pj(self):
        """Verifica se um saque acima do limite de PJ gera erro."""
        cliente = criar_pessoa_juridica({"razao_social": "Saque Bloqueado", "saldo": 50000.0})

        with self.assertRaises(ValueError):
            sacar_pessoa_juridica(cliente["id"], 30000)  # limite PJ é 10000

    def test_extrato_contem_nome_do_cliente(self):
        """Verifica se o extrato traz o nome do cliente correto."""
        cliente = criar_pessoa_juridica({"razao_social": "Extrato Teste", "saldo": 1000000.0})
        texto = extrato_pessoa_juridica(cliente["id"])

        self.assertIn("Extrato Teste", texto)


if __name__ == "__main__":
    unittest.main()