from domain.i_conta_repository import IContaRepository
from domain.cliente import Cliente
from domain.conta import Conta


class CriarContaUseCase:
    """
    Caso de uso responsável pela criação e cadastro de novas contas.
    Depende exclusivamente de IContaRepository e das entidades do domínio.
    """

    def __init__(self, repositorio: IContaRepository):
        self.repositorio = repositorio

    def executar(self, nome: str, cpf: str, saldo_inicial: float = 0.0) -> Conta:
        """
        Cadastra uma nova conta aplicando validações de negócio:
        - Saldo inicial não pode ser negativo.
        - Não permitir mais de uma conta com o mesmo CPF.
        """
        if saldo_inicial < 0:
            raise ValueError("O saldo inicial não pode ser negativo.")

        if self.repositorio.buscar(cpf) is not None:
            raise ValueError("Já existe uma conta cadastrada com este CPF.")

        cliente = Cliente(nome=nome, cpf=cpf)
        conta = Conta(cliente=cliente, saldo=saldo_inicial)
        self.repositorio.salvar(conta)
        return conta
