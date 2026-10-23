class Cliente:
    """
    Representa a entidade de um cliente no domínio bancário.
    Possui apenas nome e CPF, sem acoplamento a frameworks ou persistência.
    """

    def __init__(self, nome: str, cpf: str):
        self.nome = nome
        self.cpf = cpf
