import tkinter as tk
from tkinter import ttk, messagebox
from calculos import gerar_relatorio

class CalculadoraSalarioApp:
    def __init__(self, root: tk.Tk) -> None:
        """
        Inicializa a interface gráfica da Calculadora de Salário.

        Args:
            root (tk.Tk): A janela principal da aplicação Tkinter.
        """
        self.root = root
        self.root.title("Calculadora de Salário")
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.tipo_var = tk.StringVar(value="Mensalista")

        # Frame para seleção do tipo de trabalhador
        tipo_frame = ttk.LabelFrame(root, text="Tipo de Trabalhador")
        tipo_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        tipos = ["Mensalista", "Horista", "Diarista"]
        for i, t in enumerate(tipos):
            rb = ttk.Radiobutton(
                tipo_frame,
                text=t,
                value=t,
                variable=self.tipo_var,
                command=self.atualizar_campos
            )
            rb.grid(row=0, column=i, padx=5, pady=5)

        # Frame para campos de entrada
        self.campos_frame = ttk.LabelFrame(root, text="Dados para Cálculo")
        self.campos_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.campos_widgets = {}
        self.labels_widgets = {}
        self.criar_campos()

        # Frame para botões
        botoes_frame = ttk.Frame(root)
        botoes_frame.grid(row=2, column=0, padx=10, pady=5, sticky='ew')

        calcular_btn = ttk.Button(botoes_frame, text="Calcular", command=self.calcular)
        calcular_btn.pack(side='left', padx=5)

        limpar_btn = ttk.Button(botoes_frame, text="Limpar Campos", command=self.limpar_campos)
        limpar_btn.pack(side='left', padx=5)

        # Frame para exibir resultado
        resultado_frame = ttk.LabelFrame(root, text="Resultado")
        resultado_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        self.resultado_text = tk.Text(
            resultado_frame,
            height=12,
            width=60,
            state='disabled',
            wrap='word'
        )
        self.resultado_text.pack(padx=5, pady=5, fill='both', expand=True)

        # Configuração para expandir área do resultado
        root.grid_rowconfigure(3, weight=1)
        root.grid_columnconfigure(0, weight=1)

        # Bind tecla Enter para disparar cálculo
        root.bind('<Return>', lambda event: self.calcular())

        self.atualizar_campos()  # Inicializa exibindo campos do tipo padrão

    def criar_campos(self) -> None:
        """
        Cria os labels e entradas de dados para o cálculo, armazenando-os
        em dicionários para controle dinâmico conforme o tipo de trabalhador.
        """
        labels = {
            "salario_base": "Salário Base (R$):",
            "valor_hora": "Valor Hora (R$):",
            "horas_trabalhadas": "Horas Trabalhadas:",
            "valor_diaria": "Valor Diária (R$):",
            "dias_trabalhados": "Dias Trabalhados:",
            "beneficios": "Benefícios (R$):",
            "horas_extras": "Horas Extras:",
            "minutos_extras": "Minutos Extras:"
        }

        for i, (key, texto) in enumerate(labels.items()):
            lbl = ttk.Label(self.campos_frame, text=texto)
            lbl.grid(row=i, column=0, sticky='w', padx=5, pady=3)
            entry = ttk.Entry(self.campos_frame)
            entry.grid(row=i, column=1, sticky='ew', padx=5, pady=3)
            self.campos_widgets[key] = entry
            self.labels_widgets[key] = lbl

        self.campos_frame.grid_columnconfigure(1, weight=1)

    def limpar_campos(self) -> None:
        """
        Limpa os campos de entrada atualmente visíveis e o texto do resultado.
        """
        for key, entry in self.campos_widgets.items():
            if entry.winfo_ismapped():
                entry.delete(0, tk.END)

        self.resultado_text.config(state='normal')
        self.resultado_text.delete(1.0, tk.END)
        self.resultado_text.config(state='disabled')

    def atualizar_campos(self) -> None:
        """
        Atualiza os campos de entrada visíveis de acordo com o tipo
        de trabalhador selecionado, escondendo os demais campos.
        """
        tipo = self.tipo_var.get()
        campos_por_tipo = {
            "Mensalista": ["salario_base", "beneficios", "horas_extras", "minutos_extras"],
            "Horista": ["valor_hora", "horas_trabalhadas", "beneficios", "horas_extras", "minutos_extras"],
            "Diarista": ["valor_diaria", "dias_trabalhados", "beneficios", "horas_extras", "minutos_extras"]
        }

        campos_ativos = set(campos_por_tipo[tipo])

        for key in self.campos_widgets:
            widget = self.campos_widgets[key]
            label = self.labels_widgets[key]
            if key in campos_ativos:
                widget.grid()
                label.grid()
            else:
                widget.grid_remove()
                label.grid_remove()

        self.limpar_campos()

        # Foco no primeiro campo ativo
        primeiro_campo = campos_por_tipo[tipo][0]
        self.campos_widgets[primeiro_campo].focus_set()

    def coletar_dados(self) -> dict:
        """
        Coleta os dados digitados nos campos atualmente visíveis.

        Returns:
            dict: Dicionário com os dados dos campos visíveis,
                  onde as chaves são os nomes dos campos e os valores as entradas como strings.
        """
        dados = {}
        for key, entry in self.campos_widgets.items():
            if entry.winfo_ismapped():
                dados[key] = entry.get().strip()
        return dados

    def validar_campos(self, dados: dict) -> bool:
        """
        Valida os campos numéricos, garantindo que sejam números positivos e adequados
        ao tipo esperado (int ou float). Mostra mensagens de erro em caso de entrada inválida.

        Args:
            dados (dict): Dicionário com dados coletados dos campos.

        Returns:
            bool: True se todos os dados forem válidos, False caso contrário.
        """
        campos_float = ['salario_base', 'valor_hora', 'valor_diaria', 'beneficios']
        campos_int = ['horas_trabalhadas', 'dias_trabalhados', 'horas_extras', 'minutos_extras']

        for campo in campos_float:
            if campo in dados and dados[campo] != '':
                try:
                    v = float(dados[campo])
                    if v < 0:
                        raise ValueError
                except ValueError:
                    messagebox.showerror(
                        "Erro de entrada",
                        f"Campo '{campo.replace('_', ' ').title()}' deve ser um número decimal positivo."
                    )
                    return False

        for campo in campos_int:
            if campo in dados and dados[campo] != '':
                try:
                    v = int(dados[campo])
                    if v < 0:
                        raise ValueError
                except ValueError:
                    messagebox.showerror(
                        "Erro de entrada",
                        f"Campo '{campo.replace('_', ' ').title()}' deve ser um número inteiro positivo."
                    )
                    return False
        return True

    def calcular(self) -> None:
        """
        Realiza o cálculo do salário com base nos dados fornecidos,
        validando-os antes e exibindo o resultado ou erros na interface.
        """
        tipo = self.tipo_var.get()
        dados = self.coletar_dados()

        if not self.validar_campos(dados):
            return

        resultado = gerar_relatorio(dados, tipo)

        self.resultado_text.config(state='normal')
        self.resultado_text.delete(1.0, tk.END)
        self.resultado_text.insert(tk.END, resultado)
        self.resultado_text.config(state='disabled')


def executar() -> None:
    """
    Inicializa e executa a aplicação Tkinter da Calculadora de Salário.
    """
    root = tk.Tk()
    app = CalculadoraSalarioApp(root)
    root.mainloop()
