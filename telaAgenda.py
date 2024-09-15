import tkinter as tk
from tkinter import ttk, messagebox
import Pyro4
import threading
from agenda import Agenda


class TelaAgenda:
    def __init__(self, tela, menu, voltar_inicio):
        self.tela = tela
        self.menu = menu
        self.voltar_inicio = voltar_inicio

        self.menu.destroy()
        self.tela.title("Cadastrar agenda")
        self.frame_agenda = tk.Frame(self.tela)
        self.frame_agenda.pack()

        self.lbl_nome_agenda = tk.Label(self.frame_agenda, text="Nome da Agenda")
        self.lbl_nome_agenda.pack(pady=5)

        self.entrada_nome_agenda = ttk.Entry(self.frame_agenda)
        self.entrada_nome_agenda.pack(pady=5)

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

    def iniciar_agenda(self, nome_sv, ip_sn, ip_agenda):
        self.instancia_sv_mensagens = Agenda()
        t_sv = threading.Thread(
            target=self.instancia_sv_mensagens.iniciar,
            args=(nome_sv, ip_sn, ip_agenda),
            daemon=True,
        )
        t_sv.start()

    def tela_agenda_iniciada(self):
        self.tela.title("Agenda iniciada")
        ip_sn = self.entrada_ip_sn.get().strip()
        ip_agenda = self.entrada_ip_agenda.get().strip()
        nome_agenda = self.entrada_nome_agenda.get()
        try:
            Pyro4.locateNS(host=ip_sn, port=9090)
            self.iniciar_agenda(nome_agenda, ip_sn, ip_agenda)
            self.frame_agenda.destroy()

            self.frame_agenda_iniciada = tk.Frame(self.tela)
            self.frame_agenda_iniciada.pack()

            self.lbl_texto = tk.Label(
                self.frame_agenda_iniciada, text="Agenda iniciada"
            )
            self.lbl_texto.pack(pady=10)

            self.lbl_ip_agenda = tk.Label(
                self.frame_agenda_iniciada, text=f"IP: {ip_agenda}"
            )
            self.lbl_ip_agenda.pack(pady=10)

            self.lbl_nome_sv = tk.Label(
                self.frame_agenda_iniciada, text=f"Nome: {nome_agenda}"
            )
            self.lbl_nome_sv.pack(pady=10)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao localizar o servidor de nomes: {e}")
