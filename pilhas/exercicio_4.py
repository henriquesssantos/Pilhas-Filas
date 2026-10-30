# CLASSE DO NÓ (objeto Chamado)

class Chamado:
    def __init__(self, protocolo, cliente, descricao):
        self.protocolo = protocolo
        self.cliente = cliente
        self.descricao = descricao
        self.proximo = None

    def __repr__(self):
        # transformar o objeto Chamado em string legível sempre que o Python
        # precisar mostrá-lo. O código fica mais modular e evita reescrever
        # formatações em vários pontos.
        return f"[{self.protocolo}] {self.cliente} - {self.descricao}"


# CLASSE DA FILA ENCADEADA

class Fila:
    def __init__(self):
        self.inicio = None   # primeiro chamado (sempre o próximo a sair)
        self.fim = None      # último chamado (o que chegou mais recentemente)

    # 1) CADASTRAR CHAMADO NO FINAL DA FILA (ENQUEUE)
    def enfileirar(self, chamado):
        # Caso a fila esteja vazia: o chamado é o primeiro e o último:
        if self.inicio is None:
            self.inicio = chamado
            self.fim = chamado
        # Caso a fila já possua chamados:
        else:
            # com o ponteiro fim não precisa percorrer: inserção em tempo constante
            self.fim.proximo = chamado      # antigo fim aponta para o novo
            self.fim = chamado              # atualiza a posição de fim

    # 2) CONSULTAR O PRÓXIMO CHAMADO SEM REMOVÊ-LO
    def consultar_proximo(self):
        # devolve o primeiro da fila (ou None se estiver vazia):
        return self.inicio

    # 3) ATENDER E RETIRAR O PRIMEIRO CHAMADO (DEQUEUE)
    def atender(self):
        # Tratamento de fila vazia durante a leitura:
        if self.inicio is None:
            return None
        removido = self.inicio
        # Remoção segura pelo início em tempo constante:
        self.inicio = removido.proximo
        # Caso a fila tenha esvaziado, o fim também volta a ser None:
        if self.inicio is None:
            self.fim = None
        return removido

    # 4) LISTAR DO INÍCIO AO FIM
    def listar(self):
        atual = self.inicio
        if atual is None:
            print("  (fila vazia)")
            return
        while atual is not None:
            print(f"  {atual}")
            atual = atual.proximo

    # 5) CONTAR OS CHAMADOS PENDENTES
    def contar(self):
        total = 0
        atual = self.inicio
        while atual is not None:
            total += 1
            atual = atual.proximo
        return total

    # 6) BUSCAR CHAMADO PELO PROTOCOLO (SEM ALTERAR A ORDEM)
    def buscar(self, protocolo):
        atual = self.inicio
        while atual is not None:
            if atual.protocolo == protocolo:
                return atual
            atual = atual.proximo
        return None


# FUNÇÕES AUXILIARES PARA O MENU

def ler_int(mensagem):
    #Lê um número inteiro do usuário, repetindo até digitar válido.
    while True:
        entrada = input(mensagem).strip()
        try:
            return int(entrada)
        except ValueError:
            print("  [!] Digite um número inteiro válido.")


def ler_chamado():
    #Pede os dados de um novo chamado ao usuário e devolve um objeto Chamado.
    protocolo = ler_int("  Protocolo (int): ")
    cliente = input("  Cliente: ").strip()
    descricao = input("  Descrição: ").strip()
    return Chamado(protocolo, cliente, descricao)


# ---------------------------------------------------------------
# MENU INTERATIVO
# ---------------------------------------------------------------
def menu():
    fila = Fila()

    opcoes = {
        "1": ("Cadastrar chamado (enqueue)",                "cadastrar"),
        "2": ("Consultar próximo chamado",                  "consultar"),
        "3": ("Atender primeiro chamado (dequeue)",         "atender"),
        "4": ("Listar do início ao fim",                    "listar"),
        "5": ("Contar chamados pendentes",                  "contar"),
        "6": ("Buscar chamado pelo protocolo",              "buscar"),
        "0": ("Sair",                                       "sair"),
    }

    while True:
        print("\n" + "=" * 55)
        print("        CENTRAL DE SUPORTE - MENU INTERATIVO")
        print("=" * 55)
        for chave, (descricao, _) in opcoes.items():
            print(f"  {chave}) {descricao}")
        print("=" * 55)

        escolha = input("Escolha uma opção: ").strip()

        if escolha == "0":
            print("Encerrando o programa. Até mais!")
            break

        if escolha not in opcoes:
            print("  [!] Opção inválida. Tente novamente.")
            continue

        acao = opcoes[escolha][1]

        # ---------- AÇÕES ----------
        if acao == "cadastrar":
            print("\n-- Cadastrar chamado no final da fila --")
            chamado = ler_chamado()
            fila.enfileirar(chamado)
            print(f"  -> Chamado cadastrado: {chamado}")

        elif acao == "consultar":
            print("\n-- Consultar o próximo chamado --")
            chamado = fila.consultar_proximo()
            if chamado is None:
                print("  [!] Não há chamados na fila.")
            else:
                print(f"  -> Próximo a ser atendido: {chamado}")

        elif acao == "atender":
            print("\n-- Atender o primeiro chamado --")
            chamado = fila.atender()
            if chamado is None:
                print("  [!] Não há chamados na fila.")
            else:
                print(f"  -> Chamado atendido: {chamado}")

        elif acao == "listar":
            print("\n-- Fila (início -> fim) --")
            fila.listar()

        elif acao == "contar":
            print("\n-- Chamados pendentes --")
            total = fila.contar()
            print(f"  -> Total: {total} chamado(s) pendente(s).")

        elif acao == "buscar":
            print("\n-- Buscar chamado pelo protocolo --")
            protocolo = ler_int("  Protocolo: ")
            chamado = fila.buscar(protocolo)
            if chamado is None:
                print(f"  -> Protocolo {protocolo} não encontrado.")
            else:
                print(f"  -> Encontrado: {chamado}")
                print(f"     proximo  : {chamado.proximo}")


# ---------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------
if __name__ == "__main__":
    menu()