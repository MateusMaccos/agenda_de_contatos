import Pyro4


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Agenda:
    def __init__(self):
        self.estaOnline = True
        self.contatos = []
        self.nome = None
        self.outrasAgendas = []

    def atualizarAgenda(self):
        agendas = ["agenda1", "agenda2", "agenda3"]
        try:
            for agenda in agendas:
                if agenda != self.nome:
                    instanciaOutraAgenda = Pyro4.Proxy(
                        "PYRONAME:" + agenda + "@" + self.ip_sn + ":9090"
                    )
                    self.outrasAgendas.append(instanciaOutraAgenda)
        except Exception as e:
            print(e)

    def adicionarContato(self, contato):
        self.contatos.append(contato)

    def removerContato(self, contato):
        self.contatos.remove(contato)

    def consultarContato(self, nomeContato):
        for contato in self.contatos:
            if contato.nome == nomeContato:
                return contato

    def iniciar(self, nomeAgenda, ipSN, ipSV):
        daemon = Pyro4.Daemon(host=ipSV)
        self.nome = nomeAgenda
        self.ip_sn = ipSN
        try:
            ns = Pyro4.locateNS(host=ipSN, port=9090)
            uri = daemon.register(self)
            ns.register(nomeAgenda, uri)
            daemon.requestLoop()
        except Exception as e:
            print(e)
