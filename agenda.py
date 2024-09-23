import Pyro4
from contato import Contato
from constantes import agendas


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Agenda:
    def __init__(self):
        self.estaOnline = True
        self.contatos = []
        self.nome = None
        self.agendasConectadas = []
        self.ip_sn = None
        self.erroAoIniciar = None

    def getStatus(self):
        return self.estaOnline

    def conectarAgendas(self):
        for agenda in agendas:
            if agenda != self.nome:
                try:
                    destino_uri = self.ns.lookup(agenda)
                    instanciaOutraAgenda = Pyro4.Proxy(destino_uri)
                    self.agendasConectadas.append(instanciaOutraAgenda)
                    instanciaOutraAgenda.adicionarOutraAgenda(self.nome)
                    self.limparContatos()
                    self.atualizarContatosPorLista(
                        instanciaOutraAgenda.retornarListaDeContatos()
                    )
                except Exception as e:
                    continue

    def adicionarOutraAgenda(self, outraAgenda):
        destino_uri = self.ns.lookup(outraAgenda)
        instanciaOutraAgenda = Pyro4.Proxy(destino_uri)
        self.agendasConectadas.append(instanciaOutraAgenda)

    def retornarListaDeContatos(self):
        listaDeStrings = []
        for contato in self.contatos:
            listaDeStrings.append([contato.nome, contato.telefone])
        return listaDeStrings

    def adicionarContato(self, dadosContato):
        self.contatos.append(Contato(dadosContato[0], dadosContato[1]))
        self.atualizarNasOutrasAgendas()

    def limparContatos(self):
        self.contatos.clear()

    def removerContato(self, nomeContato):
        for contato in self.contatos:
            if contato.nome == nomeContato:
                self.contatos.remove(contato)
                self.atualizarNasOutrasAgendas()

    def consultarContato(self, nomeContato):
        for contato in self.contatos:
            if contato.nome == nomeContato:
                return [contato.nome, contato.telefone]

    def atualizarContato(self, nomeContato, dadosAtualizados):
        for contato in self.contatos:
            if contato.nome == nomeContato:
                contato.alterarNome(dadosAtualizados[0])
                contato.alterarTelefone(dadosAtualizados[1])
                self.atualizarNasOutrasAgendas()

    def atualizarNasOutrasAgendas(self):
        for agenda in self.agendasConectadas:
            if agenda.getStatus():
                agenda.limparContatos()
                agenda.atualizarContatosPorLista(self.retornarListaDeContatos())

    def atualizarContatosPorLista(self, lista):
        for contato in lista:
            self.contatos.append(Contato(contato[0], contato[1]))

    def mudarStatus(self):
        if self.estaOnline == True:
            self.estaOnline = False
        else:
            self.estaOnline = True
            if len(self.agendasConectadas) != 0:
                for agenda in self.agendasConectadas:
                    if agenda.getStatus():
                        self.contatos.clear()
                        self.atualizarContatosPorLista(agenda.retornarListaDeContatos())

    def getNome(self):
        return self.nome

    def iniciar(self, nomeAgenda, ipSN, ipAgenda):
        daemon = Pyro4.Daemon(host=ipAgenda)
        self.nome = nomeAgenda
        self.ip_sn = ipSN
        try:
            self.ns = Pyro4.locateNS(host=self.ip_sn, port=9090)
            uri = daemon.register(self)
            self.ns.register(nomeAgenda, uri)
            self.conectarAgendas()
            daemon.requestLoop()
        except Exception as e:
            self.erroAoIniciar = e
