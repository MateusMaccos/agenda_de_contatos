import Pyro4
import tkinter as tk
from tkinter import ttk, messagebox
from constantes import agendas
import Pyro4.errors


class TelaCliente:
    def __init__(self, tela, menu, voltar_inicio):
        self.tela = tela
        self.menu = menu
        self.voltar_inicio = voltar_inicio
        self.ip_sn = None
        self.contatosDaAgenda = []

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

    def telaAdicionarContato(self):
        self.tela_cadastro = tk.Tk()
        self.tela_cadastro.title("Adicionar Contato")
        self.tela_cadastro.geometry("500x300")
        self.tela_cadastro.iconbitmap("images/icone.ico")
        self.tela_cadastro.tk.call("source", "azure.tcl")
        self.tela_cadastro.tk.call("set_theme", "dark")

        self.frame_cadastro = tk.Frame(self.tela_cadastro)
        self.frame_cadastro.pack()

        self.lbl_texto_nome = tk.Label(self.frame_cadastro, text="Nome do Contato")
        self.lbl_texto_nome.pack(pady=5)

        self.entrada_nome_contato = ttk.Entry(self.frame_cadastro)
        self.entrada_nome_contato.pack(pady=5, padx=10)

        self.lbl_texto_telefone = tk.Label(
            self.frame_cadastro, text="Telefone do Contato"
        )
        self.lbl_texto_telefone.pack(pady=5)

        self.entrada_telefone_contato = ttk.Entry(self.frame_cadastro)
        self.entrada_telefone_contato.pack(pady=5, padx=10)

        self.botao_adicionar = ttk.Button(
            self.frame_cadastro,
            text="Adicionar contato",
            style="Accent.TButton",
            command=self.adicionarContato,
        )
        self.botao_adicionar.pack(pady=10)

    def contatoEstaNaAgenda(self, nomeContato):
        for contato in self.agenda.retornarListaDeContatos():
            if nomeContato == contato[0]:
                return True
        return False

    def adicionarContato(self):
        nome_contato = self.entrada_nome_contato.get().strip()
        telefone_contato = self.entrada_telefone_contato.get().strip()
        if self.contatoEstaNaAgenda(nomeContato=nome_contato):
            messagebox.showwarning("Atenção", "Esse contato já existe na agenda!")
        else:
            try:
                self.entrada_nome_contato.delete(0, tk.END)
                self.entrada_telefone_contato.delete(0, tk.END)
                self.agenda.adicionarContato([nome_contato, telefone_contato])
                self.lb_usuarios.insert(tk.END, nome_contato)
            except Exception as e:
                messagebox.showerror(
                    "Erro", f"Não foi possível adicionar esse contato: {e}"
                )

    def telaAtualizarContato(self):
        try:
            selecao = self.lb_usuarios.curselection()[0]
            contatoSelecionado = self.lb_usuarios.get(selecao)

            self.tela_atualizacao = tk.Tk()
            self.tela_atualizacao.title("Atualizar Contato")
            self.tela_atualizacao.geometry("500x300")
            self.tela_atualizacao.iconbitmap("images/icone.ico")
            self.tela_atualizacao.tk.call("source", "azure.tcl")
            self.tela_atualizacao.tk.call("set_theme", "dark")

            self.frame_cadastro = tk.Frame(self.tela_atualizacao)
            self.frame_cadastro.pack()

            self.lbl_texto_nome = tk.Label(self.frame_cadastro, text="Nome do Contato")
            self.lbl_texto_nome.pack(pady=5)

            self.entrada_nome_contato = ttk.Entry(self.frame_cadastro)
            self.entrada_nome_contato.insert(0, contatoSelecionado)
            self.entrada_nome_contato.pack(pady=5, padx=10)

            self.lbl_texto_telefone = tk.Label(
                self.frame_cadastro, text="Telefone do Contato"
            )
            self.lbl_texto_telefone.pack(pady=5)

            self.entrada_telefone_contato = ttk.Entry(self.frame_cadastro)
            telefone = self.agenda.consultarContato(contatoSelecionado)[1]
            self.entrada_telefone_contato.insert(0, telefone)
            self.entrada_telefone_contato.pack(pady=5, padx=10)

            self.botao_adicionar = ttk.Button(
                self.frame_cadastro,
                text="Atualizar contato",
                style="Accent.TButton",
                command=lambda: self.atualizarContato(
                    contatoSelecionado,
                    [
                        self.entrada_nome_contato.get(),
                        self.entrada_telefone_contato.get(),
                    ],
                ),
            )
            self.botao_adicionar.pack(pady=10)
        except IndexError:
            messagebox.showwarning("Atenção", "Escolha um contato!")
        except Exception as e:
            messagebox.showerror("Erro", f"{e}")

    def atualizarContato(self, contatoSelecionado, dadosAtualizados):
        for contato in self.agenda.retornarListaDeContatos():
            if contato[0] == dadosAtualizados[0]:
                messagebox.showwarning("Aviso", "Um contato com esse nome já existe!")
                return
        self.agenda.atualizarContato(contatoSelecionado, dadosAtualizados)
        messagebox.showinfo("Atualização de contato", "O contato foi atualizado!")
        self.tela_atualizacao.destroy()

    def removerContato(self):
        try:
            selecao = self.lb_usuarios.curselection()[0]
            contatoSelecionado = self.lb_usuarios.get(selecao)
            self.agenda.removerContato(contatoSelecionado)
            self.lb_usuarios.delete(tk.ANCHOR)
        except ValueError:
            messagebox.showerror("Error", "O contato não está na lista!")
        except IndexError:
            messagebox.showwarning("Atenção", "Escolha um contato!")
        except Exception as e:
            messagebox.showerror(
                "Erro", f"Não foi possível apagar esse contato! {str(e)}"
            )

    def atualizarContatos(self):
        pesquisa = self.entrada_pesquisa.get()
        self.atualizarAgendaConectada()
        try:
            if (
                not self.compararAgenda(
                    self.contatosDaAgenda, self.agenda.retornarListaDeContatos()
                )
                or pesquisa
            ):
                self.lb_usuarios.delete(0, tk.END)
                self.contatosDaAgenda.clear()
                for contato in self.agenda.retornarListaDeContatos():
                    nome_contato = str(contato[0]).lower()
                    if not pesquisa or pesquisa.lower() in nome_contato:
                        self.lb_usuarios.insert(tk.END, contato[0])
                        self.contatosDaAgenda.append(contato)
        except:
            self.lb_usuarios.delete(0, tk.END)
            self.contatosDaAgenda.clear()

        self.frame_caixa_usuarios.after(1000, self.atualizarContatos)

    def compararAgenda(self, agendaLocal, agendaConectada):
        agendaLocal.sort()
        agendaConectada.sort()
        if agendaLocal == agendaConectada:
            return True
        else:
            return False

    def conectarAoServidorDeNomes(self):
        try:
            self.sn = Pyro4.locateNS(host=self.ip_sn)
            return True
        except Pyro4.errors.NamingError:
            messagebox.showerror("Erro", f"Não foi possível achar o servidor de nomes")
            return False

    def conectarNaAgenda(self, agenda):
        try:
            return Pyro4.Proxy("PYRONAME:" + agenda + "@" + self.ip_sn + ":9090")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível conectar a agenda:{e}")

    def verificarStatusAgenda(self, instanciaDaAgenda):
        try:
            status = instanciaDaAgenda.getStatus()
            return status
        except:
            return False

    def iniciar(self):
        self.ip_sn = self.entrada_ip_sn.get().strip()
        seConectou = self.conectarAoServidorDeNomes()
        for agenda in agendas:
            instanciaDaAgenda = self.conectarNaAgenda(agenda)
            if seConectou:
                if self.verificarStatusAgenda(instanciaDaAgenda):
                    self.agenda = instanciaDaAgenda
                    self.criarInterface(self.frame_criar_cliente)
                    return
        messagebox.showwarning("Aviso", "Nenhuma agenda online!")

    def verificandoAgendaOnline(self):
        if not self.verificarStatusAgenda(self.agenda) or not self.verificar_conexao():
            for agenda in agendas:
                try:
                    instanciaDaAgenda = self.conectarNaAgenda(agenda)
                    if self.verificarStatusAgenda(instanciaDaAgenda):
                        self.agenda = instanciaDaAgenda
                        break
                except:
                    continue
            if instanciaDaAgenda != self.agenda:
                messagebox.showwarning("Aviso", "Nenhuma agenda online!")
        self.frame_caixa_usuarios.after(1000, self.verificandoAgendaOnline)

    def verificar_conexao(self):
        try:
            self.agenda._pyroBind()
            return True
        except Pyro4.errors.CommunicationError:
            print("Conexão perdida, tentando reconectar...")
            return False
        except Pyro4.errors.NamingError:
            return False
        except Exception:
            return False

    def atualizarAgendaConectada(self):
        try:
            self.agenda.getNome()
            self.lbl_agenda_atual.config(
                text=f"Agenda conectada: {self.agenda.getNome()}"
            )
        except Pyro4.errors.ConnectionClosedError:
            self.lbl_agenda_atual.config(text="Conexão perdida")
        except Exception as e:
            self.lbl_agenda_atual.config(text=f"Erro: {str(e)}")

    def criarInterface(self, frameAnterior):
        frameAnterior.destroy()
        self.tela.title(f"Agenda de Contatos")
        self.tela.geometry("500x500")
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

        self.frame_caixa_usuarios = tk.Frame(self.frame_contatos)
        self.frame_caixa_usuarios.pack(fill=tk.BOTH, expand=True)

        self.lb_usuarios = tk.Listbox(self.frame_caixa_usuarios, width=50, height=10)
        self.lb_usuarios.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        for contato in self.agenda.retornarListaDeContatos():
            self.lb_usuarios.insert(tk.END, contato[0])
            self.contatosDaAgenda.append(contato)

        # Adiciona a barra de rolagem se necessário
        scrollbar = tk.Scrollbar(
            self.frame_caixa_usuarios,
            orient=tk.VERTICAL,
            command=self.lb_usuarios.yview,
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.lb_usuarios.config(yscrollcommand=scrollbar.set)

        frame_botoes = tk.Frame(self.frame_contatos)
        frame_botoes.pack()

        self.botao_atualizar = ttk.Button(
            frame_botoes,
            text="Consultar Contato",
            style="Accent.TButton",
            command=self.telaAtualizarContato,
        )
        self.botao_atualizar.pack(pady=10)

        self.pesquisa = ttk.LabelFrame(
            self.frame_cliente, text="Pesquise por um contato", padding=(10, 10)
        )
        self.pesquisa.pack(pady=5)

        self.entrada_pesquisa = ttk.Entry(self.pesquisa)
        self.entrada_pesquisa.pack(pady=5)
        self.lbl_agenda_atual = ttk.Label()
        self.atualizarAgendaConectada()
        self.lbl_agenda_atual.pack(pady=5)

        self.atualizarContatos()
        self.verificandoAgendaOnline()
