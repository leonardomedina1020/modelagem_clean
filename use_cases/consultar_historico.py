from typing import List
from domain.i_conta_repository import IContaRepository


class ConsultarHistoricoUseCase:
    """
    Caso de uso responsável pela consulta do histórico de transações de uma conta.
    """

    def __init__(self, repositorio: IContaRepository):
        self.repositorio = repositorio

    def executar(self, cpf: str) -> List[str]:
        """
        Retorna a lista de transações registradas para a conta informada.
        """
        conta = self.repositorio.buscar(cpf)
        if conta is None:
            raise ValueError("Conta não encontrada para o CPF informado.")
        return list(conta.historico)
