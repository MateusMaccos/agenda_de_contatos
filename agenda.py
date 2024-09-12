class Agenda:
    def __init__(self):
        self.estaOnline = True
        self.contatos = []

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
