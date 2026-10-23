from domain.i_conta_repository import IContaRepository
from domain.conta import Conta


class RealizarDepositoUseCase:
    """
    Caso de uso responsável pela operação de depósito.
    Depende exclusivamente de IContaRepository e das entidades do domínio.
    """

    def __init__(self, repositorio: IContaRepository):
        self.repositorio = repositorio

    def executar(self, cpf: str, valor: float) -> Conta:
        """
        Executa a operação de depósito:
        - Busca a conta pelo CPF.
        - Valida a existência da conta.
        - Valida se o valor é estritamente positivo.
        - Atualiza o saldo e registra no histórico.
        - Salva a conta atualizada no repositório.
        """
        conta = self.repositorio.buscar(cpf)
        if conta is None:
            raise ValueError("Conta não encontrada para o CPF informado.")

        if valor <= 0:
            raise ValueError("O valor do depósito deve ser maior que zero.")

        conta.saldo += valor
        conta.adicionar_transacao(f"Depósito: R$ {valor:.2f}")
        self.repositorio.salvar(conta)
        return conta
