'''A lista circular é a mesma coisa que a lista simples, com uma única diferença:
o último nó não aponta para None — ele aponta de volta para o primeiro.'''

# CLASSE DO NÓ (objeto Jogador)

class Jogador:
    def __init__(self, identificador, nome):
        self.id = identificador
        self.nome = nome
        self.pontos = 0
        self.proximo = None

    def __repr__(self):
        # transformar o objeto Jogador em string legível sempre que o Python
        # precisar mostrá-lo. O código fica mais modular e evita reescrever
        # formatações em vários pontos.
        return f"[{self.id}] {self.nome} ({self.pontos} pts)"


# CLASSE DA LISTA CIRCULAR SIMPLESMENTE ENCADEADA

class Jogo:
    def __init__(self):
        self.inicio = None   # primeiro jogador do círculo
        self.fim = None      # último jogador (o proximo dele volta ao início)
        self.atual = None    # jogador que está com o turno agora

    # 1) ADICIONAR JOGADOR AO FINAL DO CÍRCULO
    def adicionar_ao_final(self, jogador):
        # Caso o círculo esteja vazio: o jogador aponta para ele mesmo
        # (círculo de um só) e ele já começa com o turno:
        if self.inicio is None:
            self.inicio = jogador
            self.fim = jogador
            self.atual = jogador
            jogador.proximo = jogador        # único nó aponta para ele mesmo
        # Caso o círculo já possua jogadores:
        else:
            self.fim.proximo = jogador       # antigo fim aponta para o novo
            jogador.proximo = self.inicio    # novo fim aponta de volta para o primeiro
            self.fim = jogador               # atualiza a posição de fim

    # 2) LISTAR TODOS OS JOGADORES EXATAMENTE UMA VEZ
    def listar(self):
        if self.inicio is None:
            print("  (círculo vazio)")
            return
        # ATENÇÃO: em uma lista circular nunca aparece um None para parar
        # o laço (o último nó aponta de volta para o primeiro). Um while
        # "atual is not None" rodaria para sempre — é o desafio do enunciado.
        # A condição segura aqui é percorrer até o FIM, imprimindo cada
        # jogador exatamente uma vez:
        atual = self.inicio
        while True:
            if atual == self.atual:
                print(f"  {atual}   <- jogador atual")
            else:
                print(f"  {atual}")
            if atual == self.fim:        # chegou no último: fecha a volta
                break
            atual = atual.proximo

    # 3) MOSTRAR O JOGADOR ATUAL
    def jogador_atual(self):
        # Devolve quem está com o turno agora (None se não houver jogadores):
        return self.atual

    # 4) PASSAR O TURNO PARA O PRÓXIMO
    def passar_turno(self):
        if self.inicio is None:
            print("  [!] Não há jogadores no jogo. Passagem de turno cancelada.")
            return False
        self.atual = self.atual.proximo   # depois do último vem o primeiro de novo
        return True

    # 5) REGISTRAR PONTOS PARA O JOGADOR ATUAL
    def registrar_pontos(self, pontos):
        if self.inicio is None:
            print("  [!] Não há jogadores no jogo. Pontuação cancelada.")
            return False
        self.atual.pontos += pontos
        return True

    # 6) REMOVER UM JOGADOR PELO IDENTIFICADOR
    def buscar(self, identificador):
        # Percorre o círculo comparando o ID. Como não existe None no final,
        # a parada segura é quando o ponteiro volta para o início:
        if self.inicio is None:
            return None
        atual = self.inicio
        while True:
            if atual.id == identificador:
                return atual
            atual = atual.proximo
            if atual == self.inicio:     # deu a volta completa: ID não existe
                return None

    def remover(self, identificador):
        alvo = self.buscar(identificador)
        if alvo is None:
            print(f"  [!] Identificador {identificador} não encontrado. Remoção cancelada.")
            return False

        proximo = alvo.proximo           # guarda quem vem depois do removido
                                         # (em círculo, o próximo do fim é o início)

        # Caso 1: único jogador do círculo:
        if self.inicio == self.fim:
            self.inicio = None
            self.fim = None
            self.atual = None
        # Caso 2: remover o primeiro:
        elif alvo == self.inicio:
            self.fim.proximo = proximo       # último aponta para o novo primeiro
            self.inicio = proximo
        # Caso 3: remover o último:
        elif alvo == self.fim:
            anterior = self.inicio
            while anterior.proximo != alvo:  # localiza o penúltimo
                anterior = anterior.proximo
            anterior.proximo = self.inicio   # penúltimo fecha o círculo
            self.fim = anterior              # penúltimo vira o último
        # Caso 4: remover do meio:
        else:
            anterior = self.inicio
            while anterior.proximo != alvo:  # localiza o nó anterior
                anterior = anterior.proximo
            anterior.proximo = proximo       # o anterior "pula" o removido

        # Se o jogador removido estava com o turno, passa para o próximo dele:
        if self.atual == alvo:
            self.atual = proximo
        return True

    # 7) CONTAR OS JOGADORES E VERIFICAR O FIM DE JOGO
    def contar_jogadores(self):
        # Percorre o círculo contando os jogadores ainda ativos:
        if self.inicio is None:
            return 0
        total = 0
        atual = self.inicio
        while True:
            total += 1
            if atual == self.fim:        # mesma parada segura do listar
                break
            atual = atual.proximo
        return total

    def jogo_terminou(self):
        # o jogo se encerra quando o círculo fica sem nenhum jogador:
        return self.inicio is None


# FUNÇÕES AUXILIARES PARA O MENU

def ler_int(mensagem):
    #Lê um número inteiro do usuário, repetindo até digitar válido.
    while True:
        entrada = input(mensagem).strip()
        try:
            return int(entrada)
        except ValueError:
            print("  [!] Digite um número inteiro válido.")


def ler_jogador():
    #Pede os dados de um novo jogador ao usuário e devolve um objeto Jogador.
    identificador = ler_int("  Identificador (int): ")
    nome = input("  Nome: ").strip()
    return Jogador(identificador, nome)   # pontos começa em 0, como no enunciado


# ---------------------------------------------------------------
# MENU INTERATIVO
# ---------------------------------------------------------------
def menu():
    jogo = Jogo()

    opcoes = {
        "1": ("Adicionar jogador ao final do círculo",      "adicionar"),
        "2": ("Listar todos os jogadores (uma volta)",      "listar"),
        "3": ("Mostrar o jogador atual",                    "atual"),
        "4": ("Passar o turno para o próximo",              "passar_turno"),
        "5": ("Registrar pontos para o jogador atual",      "pontuar"),
        "6": ("Remover jogador pelo identificador",         "remover"),
        "7": ("Verificar estado do jogo",                   "estado"),
        "0": ("Sair",                                       "sair"),
    }

    while True:
        print("\n" + "=" * 55)
        print("        CONTROLE DE TURNOS DE UM JOGO - MENU INTERATIVO")
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
        if acao == "adicionar":
            print("\n-- Adicionar jogador ao final do círculo --")
            jogador = ler_jogador()
            jogo.adicionar_ao_final(jogador)
            print(f"  -> Jogador adicionado: {jogador}")

        elif acao == "listar":
            print("\n-- Jogadores do círculo (exatamente uma volta) --")
            jogo.listar()

        elif acao == "atual":
            print("\n-- Jogador atual --")
            jogador = jogo.jogador_atual()
            if jogador is None:
                print("  [!] Não há jogadores no jogo.")
            else:
                print(f"  -> Jogador atual: {jogador}")

        elif acao == "passar_turno":
            print("\n-- Passar o turno para o próximo --")
            ok = jogo.passar_turno()
            if ok:
                print(f"  -> Turno passado. Jogador atual: {jogo.jogador_atual()}")

        elif acao == "pontuar":
            print("\n-- Registrar pontos para o jogador atual --")
            jogador = jogo.jogador_atual()
            if jogador is None:
                print("  [!] Não há jogadores no jogo. Pontuação cancelada.")
            else:
                print(f"  -> Jogador atual: {jogador}")
                pontos = ler_int("  Pontos a registrar: ")
                jogo.registrar_pontos(pontos)
                print(f"  -> {jogador.nome} agora tem {jogador.pontos} ponto(s).")

        elif acao == "remover":
            print("\n-- Remover jogador pelo identificador --")
            identificador = ler_int("  Identificador a remover: ")
            ok = jogo.remover(identificador)
            if ok:
                print(f"  -> Jogador {identificador} removido com sucesso.")
                if jogo.jogo_terminou():
                    print("  -> Fim de jogo! Não há mais jogadores no círculo.")

        elif acao == "estado":
            print("\n-- Estado do jogo --")
            if jogo.jogo_terminou():
                print("  -> Fim de jogo! Não há mais jogadores no círculo.")
            else:
                total = jogo.contar_jogadores()
                print(f"  -> Jogo em andamento: {total} jogador(es) no círculo.")
                print(f"     Jogador atual: {jogo.jogador_atual()}")


# ---------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------
if __name__ == "__main__":
    menu()

