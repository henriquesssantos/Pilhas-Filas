# CLASSE DO NÓ (objeto Ponto)

class Ponto:
    def __init__(self, codigo, setor, intervalo_min):
        self.codigo = codigo
        self.setor = setor
        self.intervalo_min = intervalo_min
        self.inspecionado = False
        self.proximo = None

    def __repr__(self):
        # transformar o objeto Ponto em string legível sempre que o Python
        # precisar mostrá-lo. O código fica mais modular e evita reescrever
        # formatações em vários pontos.
        return f"[{self.codigo}] {self.setor} ({self.intervalo_min} min)"


# CLASSE DA LISTA CIRCULAR SIMPLESMENTE ENCADEADA

class Rota:
    def __init__(self):
        self.inicio = None   # primeiro ponto da rota
        self.fim = None      # último ponto (o proximo dele volta ao início)
        self.atual = None    # ponto onde a inspeção está agora

    # 1) ADICIONAR UM PONTO AO FINAL DA ROTA
    def adicionar_ao_final(self, ponto):
        # Caso a rota esteja vazia: o ponto aponta para ele mesmo
        # (rota de um só) e ele já é o ponto atual da inspeção:
        if self.inicio is None:
            self.inicio = ponto
            self.fim = ponto
            self.atual = ponto
            ponto.proximo = ponto            # único nó aponta para ele mesmo
        # Caso a rota já possua pontos:
        else:
            # com o ponteiro fim não precisa percorrer: inserção em tempo constante
            self.fim.proximo = ponto         # antigo fim aponta para o novo
            ponto.proximo = self.inicio      # novo fim aponta de volta para o primeiro
            self.fim = ponto                 # atualiza a posição de fim

    # 2) INSERIR UM PONTO DEPOIS DE UM CÓDIGO INFORMADO
    def buscar(self, codigo):
        # Percorre a rota comparando o código. Como não existe None no final,
        # a parada segura é quando o ponteiro volta para o início:
        if self.inicio is None:
            return None
        atual = self.inicio
        while True:
            if atual.codigo == codigo:
                return atual
            atual = atual.proximo
            if atual == self.inicio:     # deu a volta completa: código não existe
                return None

    def inserir_depois_codigo(self, codigo, novo_ponto):
        alvo = self.buscar(codigo)
        if alvo is None:
            print(f"  [!] Código {codigo} não encontrado. Inserção cancelada.")
            return False

        if alvo == self.fim:
            # Inserção no fim: reusa a primeira função:
            self.adicionar_ao_final(novo_ponto)
        else:
            # Inserção no meio: liga o novo ponto entre o alvo e o próximo,
            # sem romper o ciclo:
            proximo = alvo.proximo
            alvo.proximo = novo_ponto
            novo_ponto.proximo = proximo
        return True

    # 3) LISTAR UMA VOLTA COMPLETA
    def listar(self):
        if self.inicio is None:
            print("  (rota vazia)")
            return
        # ATENÇÃO: em uma lista circular nunca aparece um None para parar
        # o laço (o último nó aponta de volta para o primeiro). Um while
        # "atual is not None" rodaria para sempre. A condição segura aqui é
        # percorrer até o FIM, imprimindo cada ponto exatamente uma vez:
        atual = self.inicio
        while True:
            situacao = "inspecionado" if atual.inspecionado else "pendente"
            if atual == self.atual:
                print(f"  {atual} [{situacao}]   <- ponto atual")
            else:
                print(f"  {atual} [{situacao}]")
            if atual == self.fim:        # chegou no último: fecha a volta
                break
            atual = atual.proximo

    # 4) AVANÇAR PARA O PRÓXIMO PONTO DA INSPEÇÃO
    def avancar(self):
        if self.inicio is None:
            print("  [!] Não há pontos na rota. Avanço cancelado.")
            return False
        self.atual = self.atual.proximo   # depois do último volta para o primeiro
        return True

    # 5) MARCAR O PONTO ATUAL COMO INSPECIONADO
    def marcar_inspecionado(self):
        if self.inicio is None:
            print("  [!] Não há pontos na rota. Marcação cancelada.")
            return False
        self.atual.inspecionado = True
        return True

    # 6) REMOVER UM PONTO DA ROTA
    def remover(self, codigo):
        alvo = self.buscar(codigo)
        if alvo is None:
            print(f"  [!] Código {codigo} não encontrado. Remoção cancelada.")
            return False

        proximo = alvo.proximo           # guarda quem vem depois do removido
                                         # (na rota, o próximo do fim é o início)

        # Caso 1: único ponto da rota:
        if self.inicio == self.fim:
            self.inicio = None
            self.fim = None
            self.atual = None
        # Caso 2: remover o início (alteração segura do início!):
        elif alvo == self.inicio:
            self.fim.proximo = proximo       # LIGAÇÃO ESSENCIAL: fim -> novo início
            self.inicio = proximo
        # Caso 3: remover o fim:
        elif alvo == self.fim:
            anterior = self.inicio
            while anterior.proximo != alvo:  # localiza o penúltimo
                anterior = anterior.proximo
            anterior.proximo = self.inicio   # penúltimo fecha o ciclo
            self.fim = anterior              # penúltimo vira o último
        # Caso 4: remover do meio:
        else:
            anterior = self.inicio
            while anterior.proximo != alvo:  # localiza o nó anterior
                anterior = anterior.proximo
            anterior.proximo = proximo       # o anterior "pula" o removido

        # Se o ponto removido era o atual, a inspeção segue do próximo dele:
        if self.atual == alvo:
            self.atual = proximo
        return True

    # 7) CALCULAR O TEMPO TOTAL DE UMA VOLTA
    def calcular_tempo_total(self):
        total = 0
        if self.inicio is None:
            return total
        atual = self.inicio
        while True:
            total += atual.intervalo_min
            if atual == self.fim:        # conta uma única volta, sem repetir
                break
            atual = atual.proximo
        return total

    # 8) REINICIAR OS ESTADOS PARA UMA NOVA RODADA
    def reiniciar_estados(self):
        if self.inicio is None:
            print("  [!] Não há pontos na rota. Reinício cancelado.")
            return False
        # percorre uma única volta desmarcando cada ponto:
        atual = self.inicio
        while True:
            atual.inspecionado = False
            if atual == self.fim:        # mesma parada segura do listar
                break
            atual = atual.proximo
        return True


# FUNÇÕES AUXILIARES PARA O MENU

def ler_int(mensagem):
    #Lê um número inteiro do usuário, repetindo até digitar válido.
    while True:
        entrada = input(mensagem).strip()
        try:
            return int(entrada)
        except ValueError:
            print("  [!] Digite um número inteiro válido.")


def ler_ponto():
    #Pede os dados de um novo ponto ao usuário e devolve um objeto Ponto.
    codigo = ler_int("  Código (int): ")
    setor = input("  Setor: ").strip()
    intervalo_min = ler_int("  Intervalo (minutos): ")
    return Ponto(codigo, setor, intervalo_min)   # inspecionado começa em False


def formatar_minutos(minutos):
    #Converte 150min -> '2:30' para exibição amigável.
    h, m = divmod(minutos, 60)
    return f"{h}:{m:02d}"


# ---------------------------------------------------------------
# MENU INTERATIVO
# ---------------------------------------------------------------
def menu():
    rota = Rota()

    opcoes = {
        "1": ("Adicionar ponto ao final da rota",           "adicionar"),
        "2": ("Inserir ponto DEPOIS de um código",          "inserir_depois"),
        "3": ("Listar uma volta completa",                  "listar"),
        "4": ("Avançar para o próximo ponto",               "avancar"),
        "5": ("Marcar ponto atual como inspecionado",       "marcar"),
        "6": ("Remover ponto pelo código",                  "remover"),
        "7": ("Calcular tempo total de uma volta",          "tempo"),
        "8": ("Reiniciar estados para nova rodada",         "reiniciar"),
        "0": ("Sair",                                       "sair"),
    }

    while True:
        print("\n" + "=" * 55)
        print("        ROTA DE INSPEÇÃO INDUSTRIAL - MENU INTERATIVO")
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
            print("\n-- Adicionar ponto ao final da rota --")
            ponto = ler_ponto()
            rota.adicionar_ao_final(ponto)
            print(f"  -> Ponto adicionado: {ponto}")

        elif acao == "inserir_depois":
            print("\n-- Inserir ponto DEPOIS de um código --")
            ref = ler_int("  Código de referência (inserir depois de): ")
            ponto = ler_ponto()
            ok = rota.inserir_depois_codigo(ref, ponto)
            if ok:
                print(f"  -> Ponto inserido depois de {ref}: {ponto}")

        elif acao == "listar":
            print("\n-- Rota (uma volta completa) --")
            rota.listar()

        elif acao == "avancar":
            print("\n-- Avançar para o próximo ponto --")
            ok = rota.avancar()
            if ok:
                print(f"  -> Avanço feito. Ponto atual: {rota.atual}")

        elif acao == "marcar":
            print("\n-- Marcar ponto atual como inspecionado --")
            ok = rota.marcar_inspecionado()
            if ok:
                print(f"  -> Ponto marcado como inspecionado: {rota.atual}")

        elif acao == "remover":
            print("\n-- Remover ponto pelo código --")
            codigo = ler_int("  Código a remover: ")
            ok = rota.remover(codigo)
            if ok:
                print(f"  -> Ponto {codigo} removido com sucesso.")

        elif acao == "tempo":
            print("\n-- Tempo total de uma volta --")
            total = rota.calcular_tempo_total()
            print(f"  -> Total: {total} min ({formatar_minutos(total)}h)")

        elif acao == "reiniciar":
            print("\n-- Reiniciar estados para uma nova rodada --")
            ok = rota.reiniciar_estados()
            if ok:
                print("  -> Estados reiniciados! Todos os pontos voltam a ficar pendentes.")


# ---------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------
if __name__ == "__main__":
    menu()