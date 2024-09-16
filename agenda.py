import Pyro4


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Agenda:
    def __init__(self):
        self.estaOnline = True
        self.contatos = []
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
                except Exception as e:
                    print(e)
        print(len(self.agendasConectadas))

    def adicionarContato(self, contato):
        self.contatos.append(contato)

    def removerContato(self, contato):
        self.contatos.remove(contato)

    def consultarContato(self, nomeContato):
        for contato in self.contatos:
            if contato.nome == nomeContato:
                return contato

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
