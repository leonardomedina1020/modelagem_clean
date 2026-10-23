from use_cases.criar_conta import CriarContaUseCase
from use_cases.consultar_conta import ConsultarContaUseCase
from use_cases.realizar_deposito import RealizarDepositoUseCase
from use_cases.realizar_saque import RealizarSaqueUseCase
from use_cases.consultar_historico import ConsultarHistoricoUseCase


class ContaController:
    """
    Camada de Controle (Controller).
    Coordena as ações disparadas pela View e as encaminha para os respectivos Casos de Uso.
    O Controller apenas organiza o fluxo de dados e trata exceções, sem regras de negócio bancárias.
    """

    def __init__(
        self,
        view=None,
        criar_conta_uc: CriarContaUseCase = None,
        consultar_conta_uc: ConsultarContaUseCase = None,
        realizar_deposito_uc: RealizarDepositoUseCase = None,
        realizar_saque_uc: RealizarSaqueUseCase = None,
        consultar_historico_uc: ConsultarHistoricoUseCase = None,
        repositorio=None,
        *args,
        **kwargs,
    ):
        # Suporte flexível para injeção de dependências:
        # Permite passar (view, casos_de_uso...) ou (repositorio, view)
        primeiro_arg = view
        if primeiro_arg is not None and not hasattr(primeiro_arg, "obter_dados_criar_conta"):
            # O primeiro argumento recebido foi um repositório ou serviço
            repositorio = primeiro_arg
            self.view = args[0] if len(args) > 0 else kwargs.get("view")
        else:
            self.view = view

        # Caso um repositório tenha sido fornecido, instancia casos de uso não fornecidos
        if repositorio is not None:
            if criar_conta_uc is None:
                criar_conta_uc = CriarContaUseCase(repositorio)
            if consultar_conta_uc is None:
                consultar_conta_uc = ConsultarContaUseCase(repositorio)
            if realizar_deposito_uc is None:
                realizar_deposito_uc = RealizarDepositoUseCase(repositorio)
            if realizar_saque_uc is None:
                realizar_saque_uc = RealizarSaqueUseCase(repositorio)
            if consultar_historico_uc is None:
                consultar_historico_uc = ConsultarHistoricoUseCase(repositorio)

        self.criar_conta_uc = criar_conta_uc
        self.consultar_conta_uc = consultar_conta_uc
        self.realizar_deposito_uc = realizar_deposito_uc
        self.realizar_saque_uc = realizar_saque_uc
        self.consultar_historico_uc = consultar_historico_uc

        # Vincula o controller à View gráfica para recebimento de eventos
        if self.view and hasattr(self.view, "definir_controlador"):
            self.view.definir_controlador(self)

    def iniciar(self):
        """Inicia a execução da interface gráfica."""
        if self.view and hasattr(self.view, "iniciar"):
            self.view.iniciar()

    def criar_conta(self):
        """Coleta dados da View, solicita criação ao caso de uso e exibe o resultado."""
        nome, cpf, saldo_str = self.view.obter_dados_criar_conta()

        if not nome:
            self.view.mostrar_mensagem("O nome não pode ficar em branco.", tipo="erro")
            return

        if not cpf:
            self.view.mostrar_mensagem("O CPF não pode ficar em branco.", tipo="erro")
            return

        saldo_inicial = 0.0
        if saldo_str:
            try:
                saldo_inicial = float(saldo_str.replace(",", "."))
            except ValueError:
                self.view.mostrar_mensagem("Valor inválido! Digite um número válido para o saldo.", tipo="erro")
                return

        try:
            # Delega para o caso de uso de criação de conta
            conta = self.criar_conta_uc.executar(nome, cpf, saldo_inicial)
            self.view.mostrar_mensagem("Conta criada com sucesso!", tipo="sucesso")
            self.view.mostrar_conta(conta)
            self.view.limpar_campos()
        except ValueError as erro:
            self.view.mostrar_mensagem(f"Erro: {erro}", tipo="erro")

    def consultar_conta(self):
        """Coleta o CPF pela View e busca a conta através do caso de uso."""
        cpf = self.view.obter_cpf_consulta()

        if not cpf:
            self.view.mostrar_mensagem("O CPF não pode ficar em branco.", tipo="erro")
            return

        try:
            conta = self.consultar_conta_uc.executar(cpf)
            self.view.mostrar_conta(conta)
            self.view.mostrar_mensagem("Conta consultada com sucesso!", tipo="sucesso")
        except ValueError as erro:
            self.view.mostrar_mensagem(f"Erro: {erro}", tipo="erro")

    def depositar(self):
        """Coleta CPF e valor pela View e delega a operação ao caso de uso de depósito."""
        cpf, valor_str = self.view.obter_dados_deposito()

        if not cpf:
            self.view.mostrar_mensagem("O CPF não pode ficar em branco.", tipo="erro")
            return

        if not valor_str:
            self.view.mostrar_mensagem("Informe um valor para depósito.", tipo="erro")
            return

        try:
            valor = float(valor_str.replace(",", "."))
        except ValueError:
            self.view.mostrar_mensagem("Valor inválido! Digite um número válido para o depósito.", tipo="erro")
            return

        try:
            conta = self.realizar_deposito_uc.executar(cpf, valor)
            self.view.mostrar_mensagem(f"Depósito de R$ {valor:.2f} realizado com sucesso!", tipo="sucesso")
            self.view.mostrar_conta(conta)
            self.view.limpar_campos()
        except ValueError as erro:
            self.view.mostrar_mensagem(f"Erro: {erro}", tipo="erro")

    def sacar(self):
        """Coleta CPF e valor pela View e delega o saque ao RealizarSaqueUseCase."""
        cpf, valor_str = self.view.obter_dados_saque()

        if not cpf:
            self.view.mostrar_mensagem("O CPF não pode ficar em branco.", tipo="erro")
            return

        if not valor_str:
            self.view.mostrar_mensagem("Informe um valor para saque.", tipo="erro")
            return

        try:
            valor = float(valor_str.replace(",", "."))
        except ValueError:
            self.view.mostrar_mensagem("Valor inválido! Digite um número válido para o saque.", tipo="erro")
            return

        try:
            conta = self.realizar_saque_uc.executar(cpf, valor)
            self.view.mostrar_mensagem(f"Saque de R$ {valor:.2f} realizado com sucesso!", tipo="sucesso")
            self.view.mostrar_conta(conta)
            self.view.limpar_campos()
        except ValueError as erro:
            self.view.mostrar_mensagem(f"Erro: {erro}", tipo="erro")

    def consultar_historico(self):
        """Coleta o CPF pela View e busca a conta e histórico de transações."""
        cpf = self.view.obter_cpf_historico()

        if not cpf:
            self.view.mostrar_mensagem("O CPF não pode ficar em branco.", tipo="erro")
            return

        try:
            conta = self.consultar_conta_uc.executar(cpf)
            self.view.mostrar_historico(conta)
            self.view.mostrar_mensagem("Histórico consultado com sucesso!", tipo="sucesso")
        except ValueError as erro:
            self.view.mostrar_mensagem(f"Erro: {erro}", tipo="erro")

    def sair(self):
        """Encerra a aplicação."""
        if hasattr(self.view, "encerrar"):
            self.view.encerrar()
