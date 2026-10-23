from domain.i_conta_repository import IContaRepository
from domain.conta import Conta


class ConsultarContaUseCase:
    """
    Caso de uso responsável por consultar uma conta existente através do CPF.
    """

    def __init__(self, repositorio: IContaRepository):
        self.repositorio = repositorio

    def executar(self, cpf: str) -> Conta:
        """
        Busca uma conta pelo CPF.
        Lança exceção caso a conta não exista.
        """
        conta = self.repositorio.buscar(cpf)
        if conta is None:
            raise ValueError("Conta não encontrada para o CPF informado.")
        return conta
