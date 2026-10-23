import json
import os
from typing import Optional, Dict

from domain.i_conta_repository import IContaRepository
from domain.cliente import Cliente
from domain.conta import Conta


class ArquivoContaRepository(IContaRepository):
    """
    Implementação concreta de IContaRepository baseada em arquivo TXT (formato JSON).
    Camada de Infraestrutura.
    
    Responsável pela persistência e recuperação dos dados das contas bancárias
    sem que o domínio ou os casos de uso dependam dos detalhes do sistema de arquivos.
    """

    def __init__(self, caminho_arquivo: Optional[str] = None):
        if caminho_arquivo is None:
            # Caminho padrão: pasta dados/contas.txt a partir da raiz do projeto
            diretorio_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.caminho_arquivo = os.path.join(diretorio_base, "dados", "contas.txt")
        else:
            self.caminho_arquivo = os.path.abspath(caminho_arquivo)

        # Garante que o diretório de destino exista
        self._garantir_diretorio()

    def _garantir_diretorio(self):
        """Cria o diretório de persistência caso ainda não exista."""
        diretorio = os.path.dirname(self.caminho_arquivo)
        if diretorio and not os.path.exists(diretorio):
            os.makedirs(diretorio, exist_ok=True)

    def _carregar_dados(self) -> Dict[str, dict]:
        """
        Recupera os dados persistidos no arquivo TXT utilizando json.load().
        Trata primeira execução quando o arquivo ainda não existe ou está vazio.
        """
        if not os.path.exists(self.caminho_arquivo):
            return {}

        try:
            with open(self.caminho_arquivo, "r", encoding="utf-8") as f:
                conteudo = f.read().strip()
                if not conteudo:
                    return {}
                return json.loads(conteudo)
        except (json.JSONDecodeError, OSError):
            return {}

    def _gravar_dados(self, dados: Dict[str, dict]):
        """Grava os dicionários das contas no arquivo TXT utilizando json.dump()."""
        self._garantir_diretorio()
        with open(self.caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    def salvar(self, conta: Conta) -> None:
        """
        Converte os objetos Cliente e Conta em dicionários e salva no arquivo TXT,
        utilizando o CPF como chave identificadora e preservando as contas já cadastradas.
        """
        dados = self._carregar_dados()

        # Converte a entidade Conta e Cliente para dicionário
        dados_conta = {
            "cliente": {
                "nome": conta.cliente.nome,
                "cpf": conta.cliente.cpf
            },
            "saldo": float(conta.saldo),
            "historico": list(conta.historico)
        }

        # Armazena ou atualiza no dicionário com o CPF como chave
        dados[conta.cliente.cpf] = dados_conta

        # Persiste o dicionário atualizado no arquivo TXT
        self._gravar_dados(dados)

    def buscar(self, cpf: str) -> Optional[Conta]:
        """
        Recupera os dados do arquivo TXT e reconstrói as entidades Cliente e Conta.
        Retorna None se a conta com o CPF não existir.
        """
        dados = self._carregar_dados()
        dados_conta = dados.get(cpf)

        if dados_conta is None:
            return None

        # Reconstrução dos objetos a partir do dicionário
        cliente_dados = dados_conta.get("cliente", {})
        nome = cliente_dados.get("nome") or dados_conta.get("nome", "")
        cpf_cliente = cliente_dados.get("cpf") or dados_conta.get("cpf", cpf)
        saldo = float(dados_conta.get("saldo", 0.0))
        historico = list(dados_conta.get("historico", []))

        cliente = Cliente(nome=nome, cpf=cpf_cliente)
        conta = Conta(cliente=cliente, saldo=saldo)
        conta.historico = historico

        return conta
