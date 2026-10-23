import tkinter as tk
from tkinter import ttk, messagebox


class ContaView:
    """
    Camada de Visão (Interface Gráfica com Tkinter).
    Responsável exclusivamente pela interface com o usuário:
    apresentação visual, captura de dados e exibição de resultados.
    Não contém regras de negócio bancárias nem manipulação de persistência.
    """

    def __init__(self, root=None):
        # Permite receber uma janela existente (útil para testes) ou criar uma nova
        if root is None:
            self.root = tk.Tk()
            self._root_proprio = True
        else:
            self.root = root
            self._root_proprio = False

        self.controller = None
        self.tela_atual = "criar"

        # Configuração da janela principal
        self.root.title("Sistema Bancário - Clean Architecture")
        self.root.geometry("760x600")
        self.root.minsize(700, 550)

        # Constrói os componentes da interface
        self._criar_layout()

    def definir_controlador(self, controller):
        """Conecta a View ao Controller para delegação das ações do usuário."""
        self.controller = controller

    # -------------------------------------------------------------
    # Construção da Interface Gráfica
    # -------------------------------------------------------------
    def _criar_layout(self):
        """Cria e organiza todos os painéis e widgets da interface."""
        # 1. Cabeçalho superior
        cabecalho = tk.Frame(self.root, bg="#1a365d", pady=10)
        cabecalho.pack(fill="x")

        lbl_titulo = tk.Label(
            cabecalho,
            text="SISTEMA BANCÁRIO",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#1a365d"
        )
        lbl_titulo.pack()

        lbl_subtitulo = tk.Label(
            cabecalho,
            text="Clean Architecture & Inversão de Dependência (DIP)",
            font=("Arial", 9, "italic"),
            fg="#cbd5e1",
            bg="#1a365d"
        )
        lbl_subtitulo.pack()

        # 2. Área principal (Menu lateral à esquerda + Conteúdo à direita)
        corpo = ttk.Frame(self.root, padding=10)
        corpo.pack(fill="both", expand=True)

        # Menu lateral de opções / navegação
        self._criar_menu_lateral(corpo)

        # Painel direito (Formulários + Apresentação de dados da conta)
        painel_direito = ttk.Frame(corpo)
        painel_direito.pack(side="left", fill="both", expand=True, padx=(10, 0))

        # Container dos formulários das operações
        self._criar_formularios(painel_direito)

        # Painel inferior de exibição de dados e histórico da conta
        self._criar_painel_dados(painel_direito)

        # 3. Barra de status inferior
        self._criar_barra_status()

        # Exibe o formulário inicial (Criar Conta)
        self.navegar_para("criar")

    def _criar_menu_lateral(self, parent):
        """Cria o painel lateral com as 6 opções de navegação."""
        frame_menu = ttk.LabelFrame(parent, text=" Operações ", padding=10)
        frame_menu.pack(side="left", fill="y")

        # Botões de cada funcionalidade do sistema
        botoes = [
            ("Criar conta", lambda: self.navegar_para("criar")),
            ("Consultar conta", lambda: self.navegar_para("consultar")),
            ("Depositar", lambda: self.navegar_para("depositar")),
            ("Sacar", lambda: self.navegar_para("sacar")),
            ("Consultar histórico", lambda: self.navegar_para("historico")),
        ]

        for texto, comando in botoes:
            btn = ttk.Button(frame_menu, text=texto, width=18, command=comando)
            btn.pack(pady=4, fill="x")

        ttk.Separator(frame_menu, orient="horizontal").pack(fill="x", pady=12)

        # Botão para Sair
        btn_sair = ttk.Button(frame_menu, text="Sair", width=18, command=self._ao_clicar_sair)
        btn_sair.pack(pady=4, fill="x")

    def _criar_formularios(self, parent):
        """Cria os formulários individuais para cada operação."""
        self.container_forms = ttk.Frame(parent)
        self.container_forms.pack(fill="x", pady=(0, 10))

        self.formularios = {}

        # --- Formulário 1: Criar Conta ---
        f_criar = ttk.LabelFrame(self.container_forms, text=" 1. Criar Conta ", padding=10)
        self.formularios["criar"] = f_criar

        ttk.Label(f_criar, text="Nome completo:").grid(row=0, column=0, sticky="w", pady=3)
        self.campo_nome = ttk.Entry(f_criar, width=35)
        self.campo_nome.grid(row=0, column=1, sticky="w", pady=3, padx=5)

        ttk.Label(f_criar, text="CPF:").grid(row=1, column=0, sticky="w", pady=3)
        self.campo_cpf_criar = ttk.Entry(f_criar, width=20)
        self.campo_cpf_criar.grid(row=1, column=1, sticky="w", pady=3, padx=5)

        ttk.Label(f_criar, text="Saldo inicial (R$):").grid(row=2, column=0, sticky="w", pady=3)
        self.campo_saldo_inicial = ttk.Entry(f_criar, width=20)
        self.campo_saldo_inicial.grid(row=2, column=1, sticky="w", pady=3, padx=5)

        botoes_criar = ttk.Frame(f_criar)
        botoes_criar.grid(row=3, column=0, columnspan=2, pady=(8, 0), sticky="w")
        ttk.Button(botoes_criar, text="Cadastrar Conta", command=self._ao_clicar_criar).pack(side="left", padx=(0, 5))
        ttk.Button(botoes_criar, text="Limpar", command=self.limpar_campos).pack(side="left")

        # --- Formulário 2: Consultar Conta ---
        f_consultar = ttk.LabelFrame(self.container_forms, text=" 2. Consultar Conta ", padding=10)
        self.formularios["consultar"] = f_consultar

        ttk.Label(f_consultar, text="CPF da conta:").grid(row=0, column=0, sticky="w", pady=3)
        self.campo_cpf_consultar = ttk.Entry(f_consultar, width=20)
        self.campo_cpf_consultar.grid(row=0, column=1, sticky="w", pady=3, padx=5)

        botoes_consultar = ttk.Frame(f_consultar)
        botoes_consultar.grid(row=1, column=0, columnspan=2, pady=(8, 0), sticky="w")
        ttk.Button(botoes_consultar, text="Consultar Conta", command=self._ao_clicar_consultar).pack(side="left", padx=(0, 5))
        ttk.Button(botoes_consultar, text="Limpar", command=self.limpar_campos).pack(side="left")

        # --- Formulário 3: Depositar ---
        f_depositar = ttk.LabelFrame(self.container_forms, text=" 3. Realizar Depósito ", padding=10)
        self.formularios["depositar"] = f_depositar

        ttk.Label(f_depositar, text="CPF da conta:").grid(row=0, column=0, sticky="w", pady=3)
        self.campo_cpf_depositar = ttk.Entry(f_depositar, width=20)
        self.campo_cpf_depositar.grid(row=0, column=1, sticky="w", pady=3, padx=5)

        ttk.Label(f_depositar, text="Valor do depósito (R$):").grid(row=1, column=0, sticky="w", pady=3)
        self.campo_valor_depositar = ttk.Entry(f_depositar, width=20)
        self.campo_valor_depositar.grid(row=1, column=1, sticky="w", pady=3, padx=5)

        botoes_depositar = ttk.Frame(f_depositar)
        botoes_depositar.grid(row=2, column=0, columnspan=2, pady=(8, 0), sticky="w")
        ttk.Button(botoes_depositar, text="Confirmar Depósito", command=self._ao_clicar_depositar).pack(side="left", padx=(0, 5))
        ttk.Button(botoes_depositar, text="Limpar", command=self.limpar_campos).pack(side="left")

        # --- Formulário 4: Sacar ---
        f_sacar = ttk.LabelFrame(self.container_forms, text=" 4. Realizar Saque ", padding=10)
        self.formularios["sacar"] = f_sacar

        ttk.Label(f_sacar, text="CPF da conta:").grid(row=0, column=0, sticky="w", pady=3)
        self.campo_cpf_sacar = ttk.Entry(f_sacar, width=20)
        self.campo_cpf_sacar.grid(row=0, column=1, sticky="w", pady=3, padx=5)

        ttk.Label(f_sacar, text="Valor do saque (R$):").grid(row=1, column=0, sticky="w", pady=3)
        self.campo_valor_sacar = ttk.Entry(f_sacar, width=20)
        self.campo_valor_sacar.grid(row=1, column=1, sticky="w", pady=3, padx=5)

        botoes_sacar = ttk.Frame(f_sacar)
        botoes_sacar.grid(row=2, column=0, columnspan=2, pady=(8, 0), sticky="w")
        ttk.Button(botoes_sacar, text="Confirmar Saque", command=self._ao_clicar_sacar).pack(side="left", padx=(0, 5))
        ttk.Button(botoes_sacar, text="Limpar", command=self.limpar_campos).pack(side="left")

        # --- Formulário 5: Consultar Histórico ---
        f_historico = ttk.LabelFrame(self.container_forms, text=" 5. Consultar Histórico ", padding=10)
        self.formularios["historico"] = f_historico

        ttk.Label(f_historico, text="CPF da conta:").grid(row=0, column=0, sticky="w", pady=3)
        self.campo_cpf_historico = ttk.Entry(f_historico, width=20)
        self.campo_cpf_historico.grid(row=0, column=1, sticky="w", pady=3, padx=5)

        botoes_historico = ttk.Frame(f_historico)
        botoes_historico.grid(row=1, column=0, columnspan=2, pady=(8, 0), sticky="w")
        ttk.Button(botoes_historico, text="Buscar Histórico", command=self._ao_clicar_consultar_historico).pack(side="left", padx=(0, 5))
        ttk.Button(botoes_historico, text="Limpar", command=self.limpar_campos).pack(side="left")

    def _criar_painel_dados(self, parent):
        """Cria o painel que exibe dados da conta (Nome, CPF, Saldo) e o Histórico."""
        painel = ttk.LabelFrame(parent, text=" Dados da Conta e Histórico ", padding=10)
        painel.pack(fill="both", expand=True)

        # Informações textuais da conta
        info_frame = ttk.Frame(painel)
        info_frame.pack(fill="x", pady=(0, 8))

        self.lbl_titular = ttk.Label(info_frame, text="Titular: -", font=("Arial", 10, "bold"))
        self.lbl_titular.pack(anchor="w")

        self.lbl_cpf = ttk.Label(info_frame, text="CPF:     -", font=("Arial", 10))
        self.lbl_cpf.pack(anchor="w")

        self.lbl_saldo = ttk.Label(
            info_frame,
            text="Saldo:   R$ 0,00",
            font=("Arial", 11, "bold"),
            foreground="#0d6efd"
        )
        self.lbl_saldo.pack(anchor="w", pady=(2, 0))

        ttk.Separator(painel, orient="horizontal").pack(fill="x", pady=6)

        # Lista de transações do histórico
        ttk.Label(painel, text="Histórico de transações realizadas:", font=("Arial", 9, "bold")).pack(anchor="w")

        frame_lista = ttk.Frame(painel)
        frame_lista.pack(fill="both", expand=True, pady=(4, 0))

        self.listbox_historico = tk.Listbox(frame_lista, height=6, font=("Consolas", 9))
        self.listbox_historico.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=self.listbox_historico.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox_historico.config(yscrollcommand=scrollbar.set)

    def _criar_barra_status(self):
        """Barra de status inferior para mensagens de confirmação e erro."""
        frame_status = tk.Frame(self.root, relief="sunken", bd=1, bg="#f8f9fa", padx=8, pady=4)
        frame_status.pack(side="bottom", fill="x")

        self.lbl_status = tk.Label(
            frame_status,
            text="Pronto. Escolha uma operação no menu lateral.",
            font=("Arial", 9),
            anchor="w",
            bg="#f8f9fa",
            fg="#495057"
        )
        self.lbl_status.pack(fill="x")

    # -------------------------------------------------------------
    # Navegação entre funcionalidades
    # -------------------------------------------------------------
    def navegar_para(self, nome_tela: str):
        """Alterna o formulário ativo na interface sem reiniciar a aplicação."""
        if nome_tela not in self.formularios:
            return

        # Oculta todos os formulários
        for f in self.formularios.values():
            f.pack_forget()

        # Exibe o formulário selecionado
        self.formularios[nome_tela].pack(fill="x")
        self.tela_atual = nome_tela

        # Foca no primeiro campo da tela selecionada
        if nome_tela == "criar":
            self.campo_nome.focus_set()
        elif nome_tela == "consultar":
            self.campo_cpf_consultar.focus_set()
        elif nome_tela == "depositar":
            self.campo_cpf_depositar.focus_set()
        elif nome_tela == "sacar":
            self.campo_cpf_sacar.focus_set()
        elif nome_tela == "historico":
            self.campo_cpf_historico.focus_set()

    # -------------------------------------------------------------
    # Métodos de Coleta de Dados (usados pelo Controller)
    # -------------------------------------------------------------
    def obter_dados_criar_conta(self):
        """Retorna os valores informados no formulário de criação de conta."""
        nome = self.campo_nome.get().strip()
        cpf = self.campo_cpf_criar.get().strip()
        saldo_str = self.campo_saldo_inicial.get().strip()
        return nome, cpf, saldo_str

    def obter_cpf_consulta(self) -> str:
        """Retorna o CPF informado no formulário de consulta."""
        return self.campo_cpf_consultar.get().strip()

    def obter_dados_deposito(self):
        """Retorna CPF e valor informados no formulário de depósito."""
        cpf = self.campo_cpf_depositar.get().strip()
        valor_str = self.campo_valor_depositar.get().strip()
        return cpf, valor_str

    def obter_dados_saque(self):
        """Retorna CPF e valor informados no formulário de saque."""
        cpf = self.campo_cpf_sacar.get().strip()
        valor_str = self.campo_valor_sacar.get().strip()
        return cpf, valor_str

    def obter_cpf_historico(self) -> str:
        """Retorna o CPF informado no formulário de histórico."""
        return self.campo_cpf_historico.get().strip()

    # -------------------------------------------------------------
    # Métodos de Apresentação de Dados (chamados pelo Controller)
    # -------------------------------------------------------------
    def mostrar_conta(self, conta):
        """Exibe nome, CPF e saldo da conta no painel de dados."""
        self.lbl_titular.config(text=f"Titular: {conta.cliente.nome}")
        self.lbl_cpf.config(text=f"CPF:     {conta.cliente.cpf}")
        self.lbl_saldo.config(text=f"Saldo:   R$ {conta.saldo:.2f}")

    def mostrar_historico(self, conta_ou_historico):
        """Exibe o histórico de transações e atualiza os dados da conta."""
        self.listbox_historico.delete(0, tk.END)

        if hasattr(conta_ou_historico, "historico"):
            self.mostrar_conta(conta_ou_historico)
            historico = conta_ou_historico.historico
        else:
            historico = conta_ou_historico

        if not historico:
            self.listbox_historico.insert(tk.END, "Nenhuma transação realizada.")
        else:
            for i, transacao in enumerate(historico, start=1):
                self.listbox_historico.insert(tk.END, f"{i}. {transacao}")

    def mostrar_mensagem(self, mensagem: str, tipo: str = "info", exibir_popup: bool = True):
        """
        Exibe mensagens de erro ou confirmação diretamente na interface
        (tanto na barra de status quanto em caixas de diálogo).
        """
        if tipo == "sucesso":
            self.lbl_status.config(text=f"✔ {mensagem}", fg="#198754")
            if exibir_popup:
                messagebox.showinfo("Sucesso", mensagem)
        elif tipo == "erro":
            self.lbl_status.config(text=f"✖ {mensagem}", fg="#dc3545")
            if exibir_popup:
                messagebox.showerror("Erro", mensagem)
        else:
            self.lbl_status.config(text=f"ℹ {mensagem}", fg="#0d6efd")
            if exibir_popup:
                messagebox.showinfo("Informação", mensagem)

    def limpar_campos(self):
        """Limpa os campos de entrada dos formulários."""
        self.campo_nome.delete(0, tk.END)
        self.campo_cpf_criar.delete(0, tk.END)
        self.campo_saldo_inicial.delete(0, tk.END)
        self.campo_cpf_consultar.delete(0, tk.END)
        self.campo_cpf_depositar.delete(0, tk.END)
        self.campo_valor_depositar.delete(0, tk.END)
        self.campo_cpf_sacar.delete(0, tk.END)
        self.campo_valor_sacar.delete(0, tk.END)
        self.campo_cpf_historico.delete(0, tk.END)

    def encerrar(self):
        """Fecha a interface gráfica."""
        if self.root:
            self.root.destroy()

    def iniciar(self):
        """Inicia o loop de eventos da interface gráfica."""
        self.root.mainloop()

    # -------------------------------------------------------------
    # Callbacks dos Botões (repassam a ação diretamente ao Controller)
    # Nenhuma regra de negócio é executada aqui.
    # -------------------------------------------------------------
    def _ao_clicar_criar(self):
        if self.controller:
            self.controller.criar_conta()

    def _ao_clicar_consultar(self):
        if self.controller:
            self.controller.consultar_conta()

    def _ao_clicar_depositar(self):
        if self.controller:
            self.controller.depositar()

    def _ao_clicar_sacar(self):
        if self.controller:
            self.controller.sacar()

    def _ao_clicar_consultar_historico(self):
        if self.controller:
            self.controller.consultar_historico()

    def _ao_clicar_sair(self):
        if self.controller:
            self.controller.sair()
        else:
            self.encerrar()
