import tkinter as tk
from tkinter import ttk, messagebox
import Pyro4
import threading

import Pyro4.errors
from agenda import Agenda


class TelaAgenda:
    def __init__(self, tela, menu, voltar_inicio):
        self.tela = tela
        self.menu = menu
        self.voltar_inicio = voltar_inicio
        self.nome_agenda = None
        self.ip_sn = None

        self.menu.destroy()
        self.tela.title("Cadastrar agenda")
        self.frame_agenda = tk.Frame(self.tela)
        self.frame_agenda.pack()

        self.lbl_nome_agenda = tk.Label(self.frame_agenda, text="Nome da Agenda")
        self.lbl_nome_agenda.pack(pady=5)

        opcoes = ["", "agenda1", "agenda2", "agenda3"]

        self.nome_agenda_selecionado = tk.StringVar(value=opcoes[0])

        self.dropdown_nome_agenda = ttk.OptionMenu(
            self.frame_agenda, self.nome_agenda_selecionado, *opcoes
        )
        self.dropdown_nome_agenda.pack(pady=15)

        self.lbl_texto_ip_agenda = tk.Label(self.frame_agenda, text="IP da Agenda:")
        self.lbl_texto_ip_agenda.pack(pady=5)

        self.entrada_ip_agenda = ttk.Entry(self.frame_agenda)
        self.entrada_ip_agenda.pack(pady=5)

        self.lbl_texto_ip_sn = tk.Label(
            self.frame_agenda, text="IP do Servidor de Nomes:"
        )
        self.lbl_texto_ip_sn.pack(pady=5)

        self.entrada_ip_sn = ttk.Entry(self.frame_agenda)
        self.entrada_ip_sn.pack(pady=5)

        self.botao_iniciar = ttk.Button(
            self.frame_agenda,
            text="Iniciar Agenda",
            style="Accent.TButton",
            command=self.tela_agenda_iniciada,
        )
        self.botao_iniciar.pack(pady=10)

        self.botao_voltar = ttk.Button(
            self.frame_agenda,
            text="Voltar",
            command=lambda: self.voltar_inicio(self.frame_agenda),
        )
        self.botao_voltar.pack(pady=5)

    def verifica_existencia_agenda(self, nome_agenda):
        try:
            ns = Pyro4.locateNS(host=self.ip_sn, port=9090)
            ns.lookup(nome_agenda)
            messagebox.showwarning("Aviso", f"Essa agenda já foi criada!")
            return True
        except Pyro4.errors.NamingError:
            return False
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao localizar o servidor de nomes: {e}")
            return True

    def iniciar_agenda(self, nome_agenda, ip_agenda):
        self.instancia_agenda = Agenda()
        t_sv = threading.Thread(
            target=self.instancia_agenda.iniciar,
            args=(nome_agenda, self.ip_sn, ip_agenda),
            daemon=True,
        )
        t_sv.start()

        t_sv.join(timeout=1)

        if self.instancia_agenda.erroAoIniciar:
            messagebox.showerror("Erro na Agenda", f"Ocorreu um erro: {erro}")

    def tela_agenda_iniciada(self):

        self.ip_sn = self.entrada_ip_sn.get().strip()
        ip_agenda = self.entrada_ip_agenda.get().strip()
        self.nome_agenda = self.nome_agenda_selecionado.get()

        if not self.verifica_existencia_agenda(self.nome_agenda):
            self.tela.title("Agenda iniciada")
            self.iniciar_agenda(self.nome_agenda, ip_agenda)
            self.frame_agenda.destroy()
            self.tela.protocol(name="WM_DELETE_WINDOW", func=self.fechar_janela)
            self.frame_agenda_iniciada = tk.Frame(self.tela)
            self.frame_agenda_iniciada.pack()

            self.info = ttk.LabelFrame(
                self.frame_agenda_iniciada,
                text="Informações",
                padding=(10, 10),
            )
            self.info.pack(pady=10)

            self.lbl_ip_agenda = tk.Label(self.info, text=f"IP: {ip_agenda}")
            self.lbl_ip_agenda.pack(pady=10)

            self.lbl_nome_agenda = tk.Label(self.info, text=f"Nome: {self.nome_agenda}")
            self.lbl_nome_agenda.pack(pady=10)

            self.lbl_contatos = tk.Label(self.frame_agenda_iniciada, text="Contatos")
            self.lbl_contatos.pack(side=tk.TOP)

            self.frame_caixa_contatos = tk.Frame(self.frame_agenda_iniciada)
            self.frame_caixa_contatos.pack(fill=tk.BOTH, expand=True)

            self.lb_contatos = tk.Listbox(
                self.frame_caixa_contatos, width=50, height=10
            )
            self.lb_contatos.pack(
                side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10
            )

            # Adiciona a barra de rolagem se necessário
            scrollbar = tk.Scrollbar(
                self.frame_caixa_contatos,
                orient=tk.VERTICAL,
                command=self.lb_contatos.yview,
            )
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.lb_contatos.config(yscrollcommand=scrollbar.set)

            self.frame_switch = tk.Frame(self.frame_agenda_iniciada)
            self.frame_switch.pack()

            self.statusSwitch = tk.BooleanVar()
            self.statusSwitch.set(self.instancia_agenda.getStatus())

            self.switch = ttk.Checkbutton(
                self.frame_switch,
                text="Ativada" if self.instancia_agenda.getStatus() else "Desativada",
                style="Switch.TCheckbutton",
                command=self.atualizarSwitch,
                variable=self.statusSwitch,
            )
            self.switch.pack()

            self.carregarContatosDaAgenda()

    def atualizarSwitch(self):
        self.instancia_agenda.mudarStatus()
        self.statusSwitch.set(self.instancia_agenda.getStatus())
        self.switch.config(
            text="Ativada" if self.instancia_agenda.getStatus() else "Desativada"
        )

    def carregarContatosDaAgenda(self):
        self.frame_caixa_contatos.after(200, self.carregarContatosDaAgenda)
        if self.lb_contatos.size() != 0:
            self.lb_contatos.delete(0, tk.END)
        for usuario in self.instancia_agenda.retornarListaDeContatos():
            self.lb_contatos.insert(0, f"{usuario[0]} - {usuario[1]}")

    def fechar_janela(self):
        self.tela.destroy()
        name_server = Pyro4.locateNS()

        name_server.remove(self.nome_agenda)
