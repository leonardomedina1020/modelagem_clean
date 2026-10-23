import os
import shutil
import tempfile
import unittest
from typing import Optional, Dict

from domain.cliente import Cliente
from domain.conta import Conta
from domain.i_conta_repository import IContaRepository
from infrastructure.arquivo_conta_repository import ArquivoContaRepository
from use_cases.criar_conta import CriarContaUseCase
from use_cases.realizar_deposito import RealizarDepositoUseCase
from use_cases.realizar_saque import RealizarSaqueUseCase


class RepositorioEmMemoriaFake(IContaRepository):
    """
    Repositório falso em memória para demonstrar o Princípio da Inversão de Dependência (DIP).
    Implementa a interface IContaRepository sem tocar em nenhum arquivo em disco.
    """

    def __init__(self):
        self._contas: Dict[str, Conta] = {}

    def salvar(self, conta: Conta) -> None:
        self._contas[conta.cliente.cpf] = conta

    def buscar(self, cpf: str) -> Optional[Conta]:
        return self._contas.get(cpf)


class TestSistemaBancarioCleanArchitecture(unittest.TestCase):
    """
    Suíte de testes automatizados do Exercício 3 — Clean Architecture e Inversão de Dependência (DIP).
    Contém exatamente 5 testes organizados com o padrão AAA (Arrange, Act, Assert).
    """

    def setUp(self):
        # Cria um diretório temporário isolado para não alterar o arquivo real contas.txt
        self.diretorio_temp = tempfile.mkdtemp()
        self.arquivo_temp = os.path.join(self.diretorio_temp, "contas_teste.txt")

    def tearDown(self):
        # Limpa o diretório temporário após cada teste
        if os.path.exists(self.diretorio_temp):
            shutil.rmtree(self.diretorio_temp)

    def test_1_persistencia_conta(self):
        """
        Teste 1: Persistência de conta.
        Cadastra uma conta, recria o repositório e verifica se os dados foram recuperados do TXT.
        """
        # [Arrange]
        repositorio_origem = ArquivoContaRepository(self.arquivo_temp)
        criar_conta_uc = CriarContaUseCase(repositorio_origem)
        nome = "Carlos Silva"
        cpf = "111.222.333-44"
        saldo_inicial = 150.0

        # [Act]
        criar_conta_uc.executar(nome, cpf, saldo_inicial)
        # Recria uma nova instância do repositório apontando para o mesmo arquivo TXT
        repositorio_novo = ArquivoContaRepository(self.arquivo_temp)
        conta_recuperada = repositorio_novo.buscar(cpf)

        # [Assert]
        self.assertIsNotNone(conta_recuperada, "A conta deveria ter sido encontrada no arquivo TXT.")
        self.assertEqual(conta_recuperada.cliente.nome, nome)
        self.assertEqual(conta_recuperada.cliente.cpf, cpf)
        self.assertEqual(conta_recuperada.saldo, 150.0)
        self.assertEqual(conta_recuperada.historico, [])

    def test_2_deposito(self):
        """
        Teste 2: Depósito.
        Realiza um depósito e verifica se o saldo e o histórico foram atualizados e persistidos.
        """
        # [Arrange]
        repositorio = ArquivoContaRepository(self.arquivo_temp)
        criar_conta_uc = CriarContaUseCase(repositorio)
        deposito_uc = RealizarDepositoUseCase(repositorio)
        cpf = "222.333.444-55"
        criar_conta_uc.executar("Mariana Santos", cpf, saldo_inicial=100.0)

        # [Act]
        conta_atualizada = deposito_uc.executar(cpf, valor=50.0)
        # Recria o repositório para certificar que os dados foram gravados em disco
        repositorio_verificacao = ArquivoContaRepository(self.arquivo_temp)
        conta_persistida = repositorio_verificacao.buscar(cpf)

        # [Assert]
        self.assertEqual(conta_atualizada.saldo, 150.0)
        self.assertIsNotNone(conta_persistida)
        self.assertEqual(conta_persistida.saldo, 150.0)
        self.assertIn("Depósito: R$ 50.00", conta_persistida.historico)
        self.assertEqual(len(conta_persistida.historico), 1)

    def test_3_saque_valido(self):
        """
        Teste 3: Saque válido.
        Realiza um saque e verifica se o saldo e o histórico foram atualizados e persistidos.
        """
        # [Arrange]
        repositorio = ArquivoContaRepository(self.arquivo_temp)
        criar_conta_uc = CriarContaUseCase(repositorio)
        saque_uc = RealizarSaqueUseCase(repositorio)
        cpf = "333.444.555-66"
        criar_conta_uc.executar("Roberto Almeida", cpf, saldo_inicial=200.0)

        # [Act]
        conta_atualizada = saque_uc.executar(cpf, valor=70.0)
        # Recria o repositório para certificar a persistência dos dados atualizados
        repositorio_verificacao = ArquivoContaRepository(self.arquivo_temp)
        conta_persistida = repositorio_verificacao.buscar(cpf)

        # [Assert]
        self.assertEqual(conta_atualizada.saldo, 130.0)
        self.assertIsNotNone(conta_persistida)
        self.assertEqual(conta_persistida.saldo, 130.0)
        self.assertIn("Saque: R$ 70.00", conta_persistida.historico)
        self.assertEqual(len(conta_persistida.historico), 1)

    def test_4_saque_invalido(self):
        """
        Teste 4: Saque inválido.
        Tenta sacar um valor superior ao saldo disponível e verifica se o saldo
        e o histórico permanecem inalterados no arquivo.
        """
        # [Arrange]
        repositorio = ArquivoContaRepository(self.arquivo_temp)
        criar_conta_uc = CriarContaUseCase(repositorio)
        saque_uc = RealizarSaqueUseCase(repositorio)
        cpf = "444.555.666-77"
        criar_conta_uc.executar("Fernanda Lima", cpf, saldo_inicial=50.0)

        # [Act]
        with self.assertRaises(ValueError) as context:
            saque_uc.executar(cpf, valor=120.0)

        # Recria o repositório para inspecionar os dados persistidos no arquivo
        repositorio_verificacao = ArquivoContaRepository(self.arquivo_temp)
        conta_persistida = repositorio_verificacao.buscar(cpf)

        # [Assert]
        self.assertIn("Saldo insuficiente para realizar o saque.", str(context.exception))
        self.assertIsNotNone(conta_persistida)
        self.assertEqual(conta_persistida.saldo, 50.0, "O saldo não deve ser alterado após saque inválido.")
        self.assertEqual(conta_persistida.historico, [], "O histórico não deve registrar saques recusados.")

    def test_5_inversao_dependencia(self):
        """
        Teste 5: Inversão de Dependência (DIP).
        Testa RealizarSaqueUseCase utilizando um repositório falso em memória que implemente
        IContaRepository, demonstrando que o caso de uso funciona sem depender do arquivo TXT.
        """
        # [Arrange]
        repositorio_fake = RepositorioEmMemoriaFake()
        saque_uc = RealizarSaqueUseCase(repositorio_fake)

        cliente = Cliente(nome="Lucas Ferreira", cpf="555.666.777-88")
        conta = Conta(cliente=cliente, saldo=300.0)
        repositorio_fake.salvar(conta)

        # [Act]
        conta_resultado = saque_uc.executar("555.666.777-88", valor=100.0)
        conta_fake_armazenada = repositorio_fake.buscar("555.666.777-88")

        # [Assert]
        self.assertEqual(conta_resultado.saldo, 200.0)
        self.assertIsNotNone(conta_fake_armazenada)
        self.assertEqual(conta_fake_armazenada.saldo, 200.0)
        self.assertIn("Saque: R$ 100.00", conta_fake_armazenada.historico)
        self.assertIsInstance(repositorio_fake, IContaRepository)


if __name__ == "__main__":
    unittest.main()
