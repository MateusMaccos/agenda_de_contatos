import Pyro4


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Agenda:
    def __init__(self):
        self.estaOnline = True
        self.contatos = []
        self.nome = None

    def atualizarAgenda(self):
        pass

    def adicionarContato(self, contato):
        self.contatos.append(contato)

    def removerContato(self, contato):
        self.contatos.remove(contato)

    def consultarContato(self, nomeContato):
        for contato in self.contatos:
            if contato.nome == nomeContato:
                return contato

    def iniciar(self, nomeAgenda, ipNS, ipSV):
        daemon = Pyro4.Daemon(host=ipSV)
        self.nome = nomeAgenda
        try:
            ns = Pyro4.locateNS(host=ipNS, port=9090)
            uri = daemon.register(self)
            ns.register(nomeAgenda, uri)
            daemon.requestLoop()
        except Exception as e:
            print(e)
