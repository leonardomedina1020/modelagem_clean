from infrastructure.arquivo_conta_repository import ArquivoContaRepository
from use_cases.criar_conta import CriarContaUseCase
from use_cases.consultar_conta import ConsultarContaUseCase
from use_cases.realizar_deposito import RealizarDepositoUseCase
from use_cases.realizar_saque import RealizarSaqueUseCase
from use_cases.consultar_historico import ConsultarHistoricoUseCase
from view.conta_view import ContaView
from controller.conta_controller import ContaController


def main():
    # 1. Camada de Infraestrutura: repositório de persistência em arquivo TXT (implementa IContaRepository)
    repositorio = ArquivoContaRepository()

    # 2. Camada de Casos de Uso: regras da aplicação com Inversão de Dependência (DIP)
    criar_conta_uc = CriarContaUseCase(repositorio)
    consultar_conta_uc = ConsultarContaUseCase(repositorio)
    realizar_deposito_uc = RealizarDepositoUseCase(repositorio)
    realizar_saque_uc = RealizarSaqueUseCase(repositorio)
    consultar_historico_uc = ConsultarHistoricoUseCase(repositorio)

    # 3. Camada de Visão (Interface gráfica Tkinter)
    view = ContaView()

    # 4. Camada de Controle: orquestração entre View e Casos de Uso
    controller = ContaController(
        view=view,
        criar_conta_uc=criar_conta_uc,
        consultar_conta_uc=consultar_conta_uc,
        realizar_deposito_uc=realizar_deposito_uc,
        realizar_saque_uc=realizar_saque_uc,
        consultar_historico_uc=consultar_historico_uc
    )

    # Inicia o loop principal da interface gráfica
    controller.iniciar()


if __name__ == "__main__":
    main()
