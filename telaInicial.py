import tkinter as tk
from tkinter import ttk
from telaServidorDeNomes import TelaServidorDeNomes
from telaAgenda import TelaAgenda
from telaCliente import TelaCliente

class TelaInicial:
    def __init__(self):
        self.tela = tk.Tk()
        self.tela.title("Menu Principal")
        self.tela.geometry("500x400")
        self.tela.tk.call("source", "azure.tcl")
        self.tela.tk.call("set_theme", "dark")
        self.menu()
        self.tela.mainloop()

    def menu(self):
        self.menu_frame = tk.Frame(self.tela)
        self.menu_frame.pack()
        self.tela.title("Menu Principal")

        self.lbl_texto_principal = tk.Label(
            self.menu_frame, text="Aplicativo de Agenda"
        )
        self.lbl_texto_principal.pack(pady=20)

        self.botao_sn = ttk.Button(
            self.menu_frame,
            text="Servidor de Nomes",
            style="Accent.TButton",
            command=lambda: TelaServidorDeNomes(
                tela=self.tela,
                tela_inicial=self.menu_frame,
                voltar_inicio=self.voltar_inicio,
            ).tela_sn_iniciar(),
        )
        self.botao_sn.pack(pady=(10, 10))

        self.botao_agenda = ttk.Button(
            self.menu_frame,
            text="Criar Agenda",
            style="Accent.TButton",
            command=lambda: TelaAgenda(
                tela=self.tela,
                menu=self.menu_frame,
                voltar_inicio=self.voltar_inicio,
            ),
        )
        self.botao_agenda.pack(pady=10)

        self.botao_cliente = ttk.Button(
            self.menu_frame,
            text="Criar Cliente",
            style="Accent.TButton",
            command=lambda: TelaCliente(
                tela=self.tela,
                menu=self.menu_frame,
                voltar_inicio=self.voltar_inicio,
            ),
        )
        self.botao_cliente.pack(pady=10)

    def voltar_inicio(self, frame):
        frame.destroy()
        self.menu()


if __name__ == "__main__":
    TelaInicial()
