# CLASSE DO NÓ (objeto Musica)

class Musica:
    def __init__(self, codigo, titulo, artista, duracao):
        self.codigo = codigo
        self.titulo = titulo
        self.artista = artista
        self.duracao = duracao
        self.anterior = None
        self.proximo = None

    def __repr__(self):
        # transformar o objeto Musica em string legível sempre que o Python
        # precisar mostrá-lo. O código fica mais modular e evita reescrever
        # formatações em vários pontos.
        return f"[{self.codigo}] {self.titulo} - {self.artista} ({self.duracao}s)"


# CLASSE DA LISTA DUPLAMENTE ENCADEADA

class Playlist:
    def __init__(self):
        self.inicio = None
        self.fim = None

    # 1) ADICIONAR MÚSICA AO FINAL
    def adicionar_ao_final(self, musica):
        # Caso a playlist esteja vazia:
        if self.inicio is None:
            self.inicio = musica
            self.fim = musica
        # Caso a lista já possua uma música:
        else:
            self.fim.proximo = musica       # antigo fim aponta para frente
            musica.anterior = self.fim      # nova música aponta para trás
            self.fim = musica               # atualiza a posição de fim

    # 2) INSERIR MÚSICA ANTES DE UM CÓDIGO INFORMADO
    def buscar(self, codigo):
        atual = self.inicio
        while atual is not None:
            if atual.codigo == codigo:
                return atual
            atual = atual.proximo
        return None

    def inserir_antes_codigo(self, codigo, nova_musica):
        alvo = self.buscar(codigo)
        if alvo is None:
            print(f" [!] Código {codigo} não encontrado. Inserção cancelada")
            return False

        if alvo == self.inicio:
            # Inserção no início:
            nova_musica.proximo = self.inicio
            self.inicio.anterior = nova_musica
            self.inicio = nova_musica
        else:
            # Inserção no meio: ligar os 4 ponteiros:
            anterior = alvo.anterior
            anterior.proximo = nova_musica
            nova_musica.anterior = anterior
            nova_musica.proximo = alvo
            alvo.anterior = nova_musica
        return True

    # 3) INSERIR MÚSICA DEPOIS DE UM CÓDIGO INFORMADO
    def inserir_depois_codigo(self, codigo, nova_musica):
        alvo = self.buscar(codigo)
        if alvo is None:
            print(f"  [!] Código {codigo} não encontrado. Inserção cancelada.")
            return False

        if alvo == self.fim:
            # Inserção no fim: reusa a primeira função:
            self.adicionar_ao_final(nova_musica)
        else:
            proximo = alvo.proximo
            alvo.proximo = nova_musica
            nova_musica.anterior = alvo
            nova_musica.proximo = proximo
            proximo.anterior = nova_musica
        return True

    # 4) LISTAR DO INÍCIO AO FIM E DO FIM AO INÍCIO
    def listar_inicio_fim(self):
        atual = self.inicio
        if atual is None:
            print("  (lista vazia)")
            return
        while atual is not None:
            print(f"  {atual}")
            atual = atual.proximo

    def listar_fim_inicio(self):
        atual = self.fim           # CORRIGIDO: começa do fim!
        if atual is None:
            print("  (lista vazia)")
            return
        while atual is not None:
            print(f"  {atual}")
            atual = atual.anterior

    # 5) REMOVER MÚSICA PELO CÓDIGO
    def remover(self, codigo):
        alvo = self.buscar(codigo)
        if alvo is None:
            print(f"  [!] Código {codigo} não encontrado. Remoção cancelada.")
            return False

        # Caso 1: única música da lista:
        if self.inicio == self.fim:
            self.inicio = None
            self.fim = None
        # Caso 2: remover o primeiro:
        elif alvo == self.inicio:
            self.inicio = alvo.proximo
            self.inicio.anterior = None
        # Caso 3: remover o último:
        elif alvo == self.fim:
            self.fim = alvo.anterior
            self.fim.proximo = None
        # Caso 4: remover do meio:
        else:
            alvo.anterior.proximo = alvo.proximo
            alvo.proximo.anterior = alvo.anterior
        return True

    # 6) MOVER UMA MÚSICA EXISTENTE PARA O INÍCIO
    def mover_para_inicio(self, codigo):
        musica = self.buscar(codigo)
        if musica is None:
            print(f"  [!] Código {codigo} não encontrado. Movimentação cancelada.")
            return False

        # Se já é o primeiro, não move:
        if musica == self.inicio:
            return True

        # Caso não seja o primeiro, desconecta o nó do local atual:
        if musica == self.fim:
            # o penúltimo vira o último:
            self.fim = musica.anterior
            self.fim.proximo = None
        else:
            # tira do meio e religa os nós vizinhos:
            musica.anterior.proximo = musica.proximo
            musica.proximo.anterior = musica.anterior

        # Por último muda a posição da música:
        musica.anterior = None
        musica.proximo = self.inicio
        self.inicio.anterior = musica
        self.inicio = musica
        return True

    # 7) CALCULAR A DURAÇÃO TOTAL
    def calcular_total(self):
        total = 0
        atual = self.inicio
        while atual is not None:
            total += atual.duracao
            atual = atual.proximo
        return total


# FUNÇÕES AUXILIARES PARA O MENU

def ler_int(mensagem):
    #Lê um número inteiro do usuário, repetindo até digitar válido.
    while True:
        entrada = input(mensagem).strip()
        try:
            return int(entrada)
        except ValueError:
            print("  [!] Digite um número inteiro válido.")


def ler_musica():
    #Pede os dados de uma nova música ao usuário e devolve um objeto Musica.
    codigo = ler_int("  Código (int): ")
    titulo = input("  Título: ").strip()
    artista = input("  Artista: ").strip()
    duracao = ler_int("  Duração (segundos): ")
    return Musica(codigo, titulo, artista, duracao)


def formatar_tempo(segundos):
    #Converte 195s -> '3:15' para exibição amigável.
    m, s = divmod(segundos, 60)
    return f"{m}:{s:02d}"


# ---------------------------------------------------------------
# MENU INTERATIVO
# ---------------------------------------------------------------
def menu():
    playlist = Playlist()

    opcoes = {
        "1": ("Adicionar música ao final",                  "adicionar"),
        "2": ("Inserir música ANTES de um código",         "inserir_antes"),
        "3": ("Inserir música DEPOIS de um código",         "inserir_depois"),
        "4": ("Listar do início ao fim",                    "listar_if"),
        "5": ("Listar do fim ao início",                    "listar_fi"),
        "6": ("Buscar música pelo código",                  "buscar"),
        "7": ("Remover música pelo código",                "remover"),
        "8": ("Mover música para o início",                 "mover"),
        "9": ("Calcular duração total",                     "total"),
        "0": ("Sair",                                       "sair"),
    }

    while True:
        print("\n" + "=" * 55)
        print("        PLAYLIST EDITÁVEL - MENU INTERATIVO")
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
            print("\n-- Adicionar música ao final --")
            musica = ler_musica()
            playlist.adicionar_ao_final(musica)
            print(f"  -> Música adicionada: {musica}")

        elif acao == "inserir_antes":
            print("\n-- Inserir música ANTES de um código --")
            ref = ler_int("  Código de referência (inserir antes de): ")
            musica = ler_musica()
            ok = playlist.inserir_antes_codigo(ref, musica)
            if ok:
                print(f"  -> Música inserida antes de {ref}: {musica}")

        elif acao == "inserir_depois":
            print("\n-- Inserir música DEPOIS de um código --")
            ref = ler_int("  Código de referência (inserir depois de): ")
            musica = ler_musica()
            ok = playlist.inserir_depois_codigo(ref, musica)
            if ok:
                print(f"  -> Música inserida depois de {ref}: {musica}")

        elif acao == "listar_if":
            print("\n-- Playlist (início -> fim) --")
            playlist.listar_inicio_fim()

        elif acao == "listar_fi":
            print("\n-- Playlist (fim -> início) --")
            playlist.listar_fim_inicio()

        elif acao == "buscar":
            print("\n-- Buscar música pelo código --")
            codigo = ler_int("  Código: ")
            musica = playlist.buscar(codigo)
            if musica is None:
                print(f"  -> Código {codigo} não encontrado.")
            else:
                print(f"  -> Encontrada: {musica}")
                print(f"     anterior : {musica.anterior}")
                print(f"     proximo  : {musica.proximo}")

        elif acao == "remover":
            print("\n-- Remover música pelo código --")
            codigo = ler_int("  Código a remover: ")
            ok = playlist.remover(codigo)
            if ok:
                print(f"  -> Música {codigo} removida com sucesso.")

        elif acao == "mover":
            print("\n-- Mover música para o início --")
            codigo = ler_int("  Código a mover: ")
            ok = playlist.mover_para_inicio(codigo)
            if ok:
                print(f"  -> Música {codigo} movida para o início.")

        elif acao == "total":
            print("\n-- Duração total da playlist --")
            total = playlist.calcular_total()
            print(f"  -> Total: {total}s ({formatar_tempo(total)})")


# ---------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------
if __name__ == "__main__":
    menu()