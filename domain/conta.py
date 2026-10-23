from domain.cliente import Cliente


class Conta:
    """
    Representa a entidade Conta Bancária no domínio.
    Contém as regras e o estado de saldo, histórico de transações e cliente associado.
    Não possui dependência de frameworks, interface gráfica ou persistência.
    """

    def __init__(self, cliente: Cliente, saldo: float = 0.0):
        self.cliente = cliente
        self.saldo = float(saldo)
        # Histórico de transações realizadas com sucesso
        self.historico = []

    def adicionar_transacao(self, transacao: str):
        """Registra uma nova transação no histórico da conta."""
        self.historico.append(transacao)

    def depositar(self, valor: float):
        """
        Realiza a operação de depósito na conta.
        Atualiza o saldo e registra no histórico se o valor for válido.
        """
        if valor <= 0:
            raise ValueError("O valor do depósito deve ser maior que zero.")
        self.saldo += valor
        self.adicionar_transacao(f"Depósito: R$ {valor:.2f}")

    def sacar(self, valor: float):
        """
        Realiza a operação de saque na conta.
        Valida o valor, verifica o saldo disponível, atualiza o saldo e registra no histórico.
        """
        if valor <= 0:
            raise ValueError("O valor do saque deve ser maior que zero.")
        if valor > self.saldo:
            raise ValueError("Saldo insuficiente para realizar o saque.")
        self.saldo -= valor
        self.adicionar_transacao(f"Saque: R$ {valor:.2f}")
