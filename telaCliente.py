import Pyro4
import tkinter as tk
from tkinter import ttk,messagebox
class TelaCliente:
    def __init__(self, tela, menu, voltar_inicio):
        self.tela = tela
        self.menu = menu
        self.voltar_inicio = voltar_inicio
        self.ip_sn = None
        
        self.menu.destroy()
        self.tela.title("Criar Cliente")
        self.frame_criar_cliente = tk.Frame(self.tela)
        self.frame_criar_cliente.pack()

        self.lbl_texto_ip_sn = tk.Label(
            self.frame_criar_cliente, text="IP do Servidor de Nomes:"
        )
        self.lbl_texto_ip_sn.pack(pady=5)

        self.entrada_ip_sn = ttk.Entry(self.frame_criar_cliente)
        self.entrada_ip_sn.pack(pady=5)

        self.botao_iniciar = ttk.Button(
            self.frame_criar_cliente,
            text="Iniciar Cliente",
            style="Accent.TButton",
            command=self.iniciar,
        )
        self.botao_iniciar.pack(pady=10)

        self.botao_voltar = ttk.Button(
            self.frame_criar_cliente,
            text="Voltar",
            command=lambda: self.voltar_inicio(self.frame_criar_cliente),
        )
        self.botao_voltar.pack(pady=5)

    def iniciar(self):
        self.ip_sn = self.entrada_ip_sn.get()

        agenda="agenda1"
        self.tela.title(f"Agenda de Contatos")

        self.frame_criar_cliente.destroy()

        try:
            self.agenda = Pyro4.Proxy(
                "PYRONAME:" + agenda + "@" + self.ip_sn + ":9090"
            )

            self.frame_cliente = tk.Frame()
            self.frame_cliente.pack()
            self.cabecalho = tk.Frame(self.frame_cliente)
            self.cabecalho.pack()

            self.botao_adicionar = ttk.Button(
                self.cabecalho,
                text="Adicionar contato",
                style="Accent.TButton",
                command=self.telaAdicionarContato,
            )
            self.botao_adicionar.pack(pady=10, side=tk.LEFT)

            self.frame_apagar = tk.Frame(self.cabecalho)
            self.frame_apagar.pack(side=tk.RIGHT)

            self.botao_adicionar = ttk.Button(
                self.frame_apagar,
                text="Apagar Contato",
                command=self.removerContato,
            )
            self.botao_adicionar.pack(pady=10, side=tk.RIGHT)

            self.lbl_texto = tk.Label(self.cabecalho, text="Contatos")
            self.lbl_texto.pack(pady=10, padx=50, side=tk.RIGHT)

            self.frame_contatos = tk.Frame(self.frame_cliente)
            self.frame_contatos.pack()

            frame_caixa_usuarios = tk.Frame(self.frame_contatos)
            frame_caixa_usuarios.pack(fill=tk.BOTH, expand=True)

            self.lb_usuarios = tk.Listbox(frame_caixa_usuarios, width=50, height=10)
            self.lb_usuarios.pack(
                side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5
            )

            for contato in self.agenda.retornarListaDeContatos():
                self.lb_usuarios.insert(0, contato[0])
            
            # Adiciona a barra de rolagem se necessário
            scrollbar = tk.Scrollbar(
                frame_caixa_usuarios, orient=tk.VERTICAL, command=self.lb_usuarios.yview
            )
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.lb_usuarios.config(yscrollcommand=scrollbar.set)

        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível conectar ao servidor:{e}")

    def telaAdicionarContato(self):
        pass
    def removerContato(self):
        pass