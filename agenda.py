import Pyro4
from contato import Contato


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Agenda:
    def __init__(self):
        self.estaOnline = True
        self.contatos = [
            Contato("Mateus", "85996417275"),
            Contato("Jorge", "85996417275"),
            Contato("Pedro", "85996417275"),
            Contato("Joao", "85996417275"),
            Contato("Picolo", "85996417275"),
            Contato("Heitor", "85996417275"),
            Contato("Guilherme", "85996417275"),
            Contato("Josias", "85996417275"),
        ]
        self.nome = None
        self.agendasConectadas = []
        self.ip_sn = None

    # 192.168.1.11
    def conectarAgendas(self):
        agendas = ["agenda1", "agenda2", "agenda3"]
        for agenda in agendas:
            if agenda != self.nome:
                try:
                    destino_uri = self.ns.lookup(agenda)
                    instanciaOutraAgenda = Pyro4.Proxy(destino_uri)
                    self.agendasConectadas.append(instanciaOutraAgenda)
                    print(f"Registrou pelo servidor de nomes: {agenda}")
                    instanciaOutraAgenda.adicionarOutraAgenda(self.nome)
                except Exception as e:
                    print(e)
        print(len(self.agendasConectadas))

    def adicionarOutraAgenda(self,outraAgenda):
        print(f"Registrou por outra agenda: {outraAgenda}")
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
            agenda.limparContatos()
            agenda.atualizarContatosPorLista(self.retornarListaDeContatos())
    
    def atualizarContatosPorLista(self,lista):
        for contato in lista:
            self.contatos.append(Contato(contato[0],contato[1]))

    def mudarStatus(self):
        if self.estaOnline == True:
            self.estaOnline = False
        else:
            if len(self.agendasConectadas) != 0:
                for agenda in self.agendasConectadas:
                    if agenda.estaOnline:
                        self.contatos.clear()
                        for contato in agenda.retornarListaDeContatos():
                            contatoAtualizado = Contato(contato[0], contato[1])
                            self.contatos.append(contatoAtualizado)

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
            print(e)
