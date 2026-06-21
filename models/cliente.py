from abc import ABC, abstractmethod


class Cliente(ABC):
    """
    Interface (classe abstrata) que representa um cliente do banco.
    Qualquer classe que herdar de Cliente é obrigada a implementar
    os métodos sacar() e extrato().
    """

    @abstractmethod
    def sacar(self, valor: float) -> None:
        """Realiza o saque de um valor da conta do cliente."""
        pass

    @abstractmethod
    def extrato(self) -> str:
        """Retorna uma representação textual do extrato do cliente."""
        pass