# CLASSE DO NÓ (objeto Simbolo)

class Simbolo:
    def __init__(self, caractere, posicao):
        self.caractere = caractere
        self.posicao = posicao
        self.proximo = None

    def __repr__(self):
        # transformar o objeto Simbolo em string legível sempre que o Python
        # precisar mostrá-lo. O código fica mais modular e evita reescrever
        # formatações em vários pontos.
        return f"'{self.caractere}' (posição {self.posicao})"


# CLASSE DA PILHA ENCADEADA

class Pilha:
    def __init__(self):
        self.topo = None   # símbolo do topo (None significa pilha vazia)

    # 1) EMPILHAR UM SÍMBOLO (PUSH)
    def empilhar(self, caractere, posicao):
        novo = Simbolo(caractere, posicao)
        # Caso a pilha esteja vazia: o novo símbolo vira o topo:
        if self.topo is None:
            self.topo = novo
        # Caso a pilha já possua símbolos: o novo entra na frente do topo:
        else:
            novo.proximo = self.topo        # novo aponta para o antigo topo
            self.topo = novo                # atualiza a posição de topo

    # 2) CONSULTAR O TOPO SEM REMOVER (PEEK)
    def consultar_topo(self):
        # devolve o nó do topo para comparação (ou None se estiver vazia):
        return self.topo

    # 3) DESEMPILHAR O TOPO (POP)
    def desempilhar(self):
        # se a pilha estiver vazia, não há o que remover:
        if self.topo is None:
            return None
        removido = self.topo
        self.topo = removido.proximo        # topo desce para o próximo nó
        return removido

    # 4) VERIFICAR SE A PILHA ESTÁ VAZIA
    def esta_vazia(self):
        return self.topo is None

    # 5) MOSTRAR O CONTEÚDO DA PILHA (DO TOPO PARA A BASE)
    def listar(self):
        if self.topo is None:
            print("  (pilha vazia)")
            return
        atual = self.topo
        while atual is not None:
            print(f"  {atual}")
            atual = atual.proximo

    def conteudo(self):
        #Devolve o conteúdo da pilha em uma linha, do topo para a base.
        itens = []
        atual = self.topo
        while atual is not None:
            itens.append(f"'{atual.caractere}'")
            atual = atual.proximo
        return " ".join(itens) if itens else "(vazia)"

    # 6) LIMPAR A PILHA (LIMPEZA DOS NÓS AO FINALIZAR)
    def limpar(self):
        while self.topo is not None:
            self.desempilhar()      # reusa o pop até a pilha esvaziar


# FUNÇÕES AUXILIARES PARA O MENU

def ler_expressao():
    #Pede a expressão textual ao usuário, repetindo até digitar algo.
    while True:
        expressao = input("  Expressão: ").strip()
        if expressao != "":
            return expressao
        print("  [!] Nenhuma expressão informada. Tente novamente.")


def validar_expressao(expressao, pilha, passo_a_passo=False):
    #Percorre a expressão caractere a caractere: empilha as aberturas e, nos
    #fechamentos, consulta e remove o topo. A expressão só é válida se não
    #ocorrer erro e a pilha terminar vazia.
    aberturas = "([{"
    fechamentos = ")]}"
    pares = {")": "(", "]": "[", "}": "{"}   # cada fechamento aponta para a abertura que o combina

    for indice in range(len(expressao)):
        caractere = expressao[indice]
        posicao = indice + 1     # posições contadas a partir de 1, como em editores

        # abertura: empilha o símbolo junto com a posição dele:
        if caractere in aberturas:
            pilha.empilhar(caractere, posicao)
            if passo_a_passo:
                print(f"  push '{caractere}' (posição {posicao})  -> pilha: {pilha.conteudo()}")

        # fechamento: consulta o topo antes de remover:
        elif caractere in fechamentos:
            topo = pilha.consultar_topo()

            # Tratamento de pilha vazia durante a leitura:
            if topo is None:
                print(f"  -> Expressão INVÁLIDA! Primeiro erro na posição {posicao}: "
                      f"fechamento '{caractere}' sem abertura correspondente (pilha vazia).")
                return False

            if topo.caractere != pares[caractere]:
                print(f"  -> Expressão INVÁLIDA! Primeiro erro na posição {posicao}: "
                      f"fechamento '{caractere}' não combina com '{topo.caractere}' "
                      f"(aberto na posição {topo.posicao}).")
                return False

            par = pilha.desempilhar()
            if passo_a_passo:
                print(f"  pop  '{par.caractere}' (posição {par.posicao})  -> pilha: {pilha.conteudo()}")

    # ao final, a pilha precisa estar vazia:
    if not pilha.esta_vazia():
        print("  -> Expressão INVÁLIDA! A expressão terminou, mas a pilha não ficou vazia.")
        print("     Abertura(s) sem fechamento (do topo para a base):")
        pilha.listar()
        return False

    print("  -> Expressão VÁLIDA! Todos os delimitadores combinaram.")
    return True


# ---------------------------------------------------------------
# MENU INTERATIVO
# ---------------------------------------------------------------
def menu():
    pilha = Pilha()

    opcoes = {
        "1": ("Validar expressão",                          "validar"),
        "2": ("Simular passo a passo (push/pop e pilha)",   "simular"),
        "3": ("Mostrar pilha atual (topo -> base)",         "listar"),
        "0": ("Sair",                                       "sair"),
    }

    while True:
        print("\n" + "=" * 55)
        print("        VALIDADOR DE EXPRESSÕES - MENU INTERATIVO")
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
        if acao == "validar":
            print("\n-- Validar expressão --")
            expressao = ler_expressao()
            validar_expressao(expressao, pilha)
            # Garantia de que a pilha termina vazia (limpeza dos nós):
            pilha.limpar()
            print(f"  -> Pilha ao finalizar: {pilha.conteudo()}")

        elif acao == "simular":
            print("\n-- Simular passo a passo (push/pop e pilha) --")
            expressao = ler_expressao()
            validar_expressao(expressao, pilha, passo_a_passo=True)
            # Garantia de que a pilha termina vazia (limpeza dos nós):
            pilha.limpar()
            print(f"  -> Pilha ao finalizar: {pilha.conteudo()}")

        elif acao == "listar":
            print("\n-- Pilha atual (topo -> base) --")
            pilha.listar()


# ---------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------
if __name__ == "__main__":
    menu()