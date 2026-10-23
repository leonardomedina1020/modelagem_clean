from domain.i_conta_repository import IContaRepository
from domain.conta import Conta


class RealizarSaqueUseCase:
    """
    Caso de uso responsável pela operação de saque.
    Aplica o Princípio da Inversão de Dependência (DIP): depende exclusivamente
    da interface abstrata IContaRepository e das entidades do domínio.
    Não depende de implementações concretas de persistência nem manipula arquivos.
    """

    def __init__(self, repositorio: IContaRepository):
        self.repositorio = repositorio

    def executar(self, cpf: str, valor: float) -> Conta:
        """
        Executa a operação de saque aplicando as regras de negócio:
        - Busca a conta pelo CPF.
        - Valida se a conta existe.
        - Valida se o valor do saque é maior que zero.
        - Verifica se existe saldo suficiente.
        - Atualiza o saldo.
        - Registra o saque no histórico.
        - Salva a conta atualizada no repositório.
        """
        conta = self.repositorio.buscar(cpf)
        if conta is None:
            raise ValueError("Conta não encontrada para o CPF informado.")

        if valor <= 0:
            raise ValueError("O valor do saque deve ser maior que zero.")

        if valor > conta.saldo:
            raise ValueError("Saldo insuficiente para realizar o saque.")

        conta.saldo -= valor
        conta.adicionar_transacao(f"Saque: R$ {valor:.2f}")
        self.repositorio.salvar(conta)
        return conta
