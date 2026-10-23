from abc import ABC, abstractmethod
from typing import Optional


class IContaRepository(ABC):
    """
    Interface abstrata para armazenamento e recuperação de contas (Contrato DIP).
    O núcleo da aplicação depende exclusivamente desta abstração, e não de implementações concretas.
    """

    @abstractmethod
    def salvar(self, conta) -> None:
        """Salva ou atualiza a conta no repositório."""
        pass

    @abstractmethod
    def buscar(self, cpf: str) -> Optional[object]:
        """Busca e retorna a conta pelo CPF, ou None se não encontrada."""
        pass
