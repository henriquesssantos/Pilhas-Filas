"""
================================================================
 EXERCÍCIO 4 - CONTROLE DE TURNOS DE UM JOGO
 Lista Circular Simplesmente Encadeada
================================================================

DIFERENÇAS-CHAVE em relação à lista simples comum:
  - O ÚLTIMO nó aponta para o PRIMEIRO (não para None/NULL)
  - A lista nunca "termina" naturalmente
  - NÃO PODE usar `while atual is not None` (loop infinito!)
  - Precisamos de um marcador `inicio` para saber quando demos a volta
  - Mantemos também `self.atual` (de quem é a vez)

PADRÃO DE PERCURSO SEGURO:
    atual = self.inicio
    while True:
        # processa atual
        atual = atual.proximo
        if atual == self.inicio:
            break
"""


# ---------------------------------------------------------------
# NÓ DA LISTA (classe Jogador)
# ---------------------------------------------------------------
class Jogador:
    """
    Representa um nó da lista circular.
    Equivalente à struct Jogador em C.

    Em C:     struct Jogador *prox;     // endereço
    Em Python: self.proximo            // referência
    """

    def __init__(self, identificador, nome):
        self.id = identificador         # int  - identificador único
        self.nome = nome                # str  - nome do jogador
        self.pontos = 0                 # int  - começa com 0 pontos
        self.proximo = None             # Jogador ou None (até fechar o ciclo)

    def __repr__(self):
        # Conveniência: transformar o objeto em string legível.
        return f"[{self.id}] {self.nome} - {self.pontos} pts"


# ---------------------------------------------------------------
# LISTA CIRCULAR (classe Jogo)
# ---------------------------------------------------------------
class Jogo:
    """
    Lista circular simplesmente encadeada de objetos Jogador.
    Mantém dois marcadores:
      - self.inicio -> primeiro jogador (cabeça da lista)
      - self.atual  -> jogador da vez (de quem é o turno)

    NÃO há marcador `fim`, porque o "último" é o nó cujo
    proximo == inicio. Em vez de guardá-lo, podemos procurá-lo
    percorrendo até achar esse nó.
    """

    def __init__(self):
        self.inicio = None
        self.atual = None

    # ---------------------------------------------------------
    # 1) ADICIONAR JOGADOR AO FINAL DO CICLO
    # ---------------------------------------------------------
    def adicionar_jogador(self, jogador):
        """
        Insere um novo jogador no fim do ciclo (logo antes do início).
        Casos:
          - Lista vazia: jogador vira o único, fecha ciclo sozinho
          - Lista com elementos: achar o "último" e religar
        """
        if self.inicio is None:
            # Lista vazia: o jogador aponta para SI MESMO
            self.inicio = jogador
            jogador.proximo = jogador
            self.atual = jogador          # começa sendo o da vez
        else:
            # Achar o "último" (o nó cujo proximo == inicio)
            ultimo = self.inicio
            while ultimo.proximo != self.inicio:
                ultimo = ultimo.proximo
            # Inserir o novo entre o último e o início
            ultimo.proximo = jogador
            jogador.proximo = self.inicio   # fecha o ciclo de volta

    # ---------------------------------------------------------
    # 2) LISTAR TODOS OS JOGADORES EXATAMENTE UMA VEZ
    # ---------------------------------------------------------
    def listar_jogadores(self):
        """
        Percurso circular com PARADA SEGURA: para quando voltar ao início.
        Mostra um marcador ao lado do jogador atual.
        """
        if self.inicio is None:
            print("  (sem jogadores)")
            return

        atual = self.inicio
        while True:
            marcador = "  <-- atual" if atual == self.atual else ""
            print(f"  {atual}{marcador}")
            atual = atual.proximo
            if atual == self.inicio:
                break       # demos a volta completa: PARAR!

    # ---------------------------------------------------------
    # 3) MOSTRAR O JOGADOR ATUAL
    # ---------------------------------------------------------
    def mostrar_atual(self):
        """Retorna o objeto Jogador da vez (ou None se vazio)."""
        if self.atual is None:
            print("  (sem jogadores)")
            return None
        print(f"  Atual: {self.atual}")
        return self.atual

    # ---------------------------------------------------------
    # 4) PASSAR O TURNO PARA O PRÓXIMO
    # ---------------------------------------------------------
    def passar_turno(self):
        """
        Avança o marcador `atual` para o próximo.
        Em lista circular, isso AUTOMATICAMENTE volta ao início
        quando saímos do último jogador.
        """
        if self.atual is None:
            print("  [!] Não há jogadores para passar o turno.")
            return False
        self.atual = self.atual.proximo
        return True

    # ---------------------------------------------------------
    # 5) REGISTRAR PONTOS PARA O JOGADOR ATUAL
    # ---------------------------------------------------------
    def registrar_pontos(self, pontos):
        """Soma `pontos` ao total do jogador atual."""
        if self.atual is None:
            print("  [!] Não há jogador atual.")
            return False
        self.atual.pontos += pontos
        print(f"  -> {self.atual.nome} agora tem {self.atual.pontos} pontos.")
        return True

    # ---------------------------------------------------------
    # 6) REMOVER JOGADOR PELO ID
    # ---------------------------------------------------------
    def remover_jogador(self, id_):
        """
        Remove o jogador cujo id == id_, sem quebrar o ciclo.

        Estratégia: como é lista SIMPLES (sem ponteiro `anterior`),
        precisamos achar o nó ANTERIOR ao alvo, percorrendo a partir
        do início. Depois, religamos anterior.proximo = alvo.proximo.

        Casos especiais:
          - Lista vazia                       -> False
          - ID não existe                     -> False
          - Único jogador (auto-apontado)     -> inicio = atual = None
          - Remover o primeiro (inicio)       -> achar último e refechar
          - Remover o jogador atual           -> mover `atual` para o próximo
        """
        if self.inicio is None:
            print(f"  [!] Lista vazia. Nada a remover.")
            return False

        # Buscar o alvo e seu anterior
        anterior = None
        atual = self.inicio
        while True:
            if atual.id == id_:
                break                       # encontrou
            anterior = atual
            atual = atual.proximo
            if atual == self.inicio:
                # demos a volta completa sem achar
                print(f"  [!] Jogador {id_} não encontrado.")
                return False

        alvo = atual

        # Caso 1: único jogador (aponta para si mesmo)
        if alvo.proximo == alvo:
            self.inicio = None
            self.atual = None
            print(f"  -> Removido {alvo}. Lista agora vazia.")
            return True

        # Caso 2: removendo o primeiro (inicio)
        elif alvo == self.inicio:
            # Achar o último (o nó cujo proximo == inicio)
            ultimo = self.inicio
            while ultimo.proximo != self.inicio:
                ultimo = ultimo.proximo
            # Último passa a apontar para o NOVO início
            ultimo.proximo = alvo.proximo
            self.inicio = alvo.proximo
            # Se estamos removendo o atual, mover para o próximo
            if self.atual == alvo:
                self.atual = self.inicio

        # Caso 3: removendo do meio (qualquer outro)
        else:
            anterior.proximo = alvo.proximo
            # Se estamos removendo o atual, mover para o próximo
            if self.atual == alvo:
                self.atual = alvo.proximo

        print(f"  -> Removido {alvo}.")
        return True

    # ---------------------------------------------------------
    # 7) VERIFICAR SE HÁ JOGADORES (ENCERRAR QUANDO VAZIO)
    # ---------------------------------------------------------
    def esta_vazia(self):
        """True se não há jogadores no ciclo."""
        return self.inicio is None


# ---------------------------------------------------------------
# TESTES OBRIGATÓRIOS DO EXERCÍCIO
# ---------------------------------------------------------------
def executar_testes():
    print("=" * 70)
    print(" EXERCÍCIO 4 - CONTROLE DE TURNOS (Lista Circular Simples) ")
    print("=" * 70)

    # ---------------------------------------------------------
    # TESTE 1: Lista vazia
    # ---------------------------------------------------------
    print("\n[1] Teste: lista vazia")
    jogo = Jogo()
    print("  -> está vazia?", jogo.esta_vazia())
    jogo.listar_jogadores()
    jogo.mostrar_atual()

    # ---------------------------------------------------------
    # TESTE 2: Um único jogador apontando para si mesmo
    # ---------------------------------------------------------
    print("\n[2] Teste: um único jogador (auto-apontado)")
    jogo.adicionar_jogador(Jogador(1, "Alice"))
    print(f"  inicio = {jogo.inicio}")
    print(f"  inicio.proximo == inicio? {jogo.inicio.proximo is jogo.inicio}")
    jogo.listar_jogadores()
    jogo.mostrar_atual()

    # ---------------------------------------------------------
    # TESTE 3: Adicionar mais jogadores
    # ---------------------------------------------------------
    print("\n[3] Adicionando mais jogadores (Bob, Carol, Dave)")
    jogo.adicionar_jogador(Jogador(2, "Bob"))
    jogo.adicionar_jogador(Jogador(3, "Carol"))
    jogo.adicionar_jogador(Jogador(4, "Dave"))
    print("  -> Listagem:")
    jogo.listar_jogadores()

    # ---------------------------------------------------------
    # TESTE 4: Executar mais turnos que a quantidade de jogadores
    # ---------------------------------------------------------
    print("\n[4] Executar 6 turnos (mais que os 4 jogadores) - valida o ciclo")
    for i in range(1, 7):
        print(f"  Turno {i}: atual = {jogo.atual.nome}")
        jogo.passar_turno()
    print("  -> Voltou naturalmente ao início. OK.")

    # ---------------------------------------------------------
    # TESTE 5: Registrar pontos ao longo de alguns turnos
    # ---------------------------------------------------------
    print("\n[5] Registrar pontos em 4 turnos")
    jogo.registrar_pontos(10)
    jogo.passar_turno()
    jogo.registrar_pontos(5)
    jogo.passar_turno()
    jogo.registrar_pontos(20)
    jogo.passar_turno()
    jogo.registrar_pontos(15)
    print("  -> Listagem final após pontuar:")
    jogo.listar_jogadores()

    # ---------------------------------------------------------
    # TESTE 6: Remover o primeiro (id=1)
    # ---------------------------------------------------------
    print("\n[6] Remover o PRIMEIRO jogador (id=1, Alice)")
    jogo.remover_jogador(1)
    print(f"  -> Novo início: {jogo.inicio}")
    print("  -> Listagem após remover o primeiro:")
    jogo.listar_jogadores()
    # valida que o ciclo continua íntegro:
    print(f"  -> ciclo íntegro? (último.proximo == inicio?)")
    ultimo = jogo.inicio
    while ultimo.proximo != jogo.inicio:
        ultimo = ultimo.proximo
    print(f"     último = {ultimo}, último.proximo = {ultimo.proximo}")

    # ---------------------------------------------------------
    # TESTE 7: Remover o último (precisamos achar quem é)
    # ---------------------------------------------------------
    print("\n[7] Remover o ÚLTIMO jogador")
    # achar o último
    ultimo = jogo.inicio
    while ultimo.proximo != jogo.inicio:
        ultimo = ultimo.proximo
    print(f"  -> Último identificado: {ultimo} (id={ultimo.id})")
    jogo.remover_jogador(ultimo.id)
    print("  -> Listagem após remover o último:")
    jogo.listar_jogadores()

    # ---------------------------------------------------------
    # TESTE 8: Remover o jogador ATUAL
    # ---------------------------------------------------------
    print("\n[8] Remover o jogador ATUAL")
    print(f"  -> Atual antes: {jogo.atual}")
    id_atual = jogo.atual.id
    jogo.remover_jogador(id_atual)
    print(f"  -> Atual depois: {jogo.atual}")
    print("  -> Listagem após remover o atual:")
    jogo.listar_jogadores()

    # ---------------------------------------------------------
    # TESTE 9: Remover todos até a lista ficar vazia
    # ---------------------------------------------------------
    print("\n[9] Remover todos os jogadores (até encerrar)")
    while not jogo.esta_vazia():
        # remove sempre o início
        id_remover = jogo.inicio.id
        jogo.remover_jogador(id_remover)
    print(f"  -> Lista vazia agora? {jogo.esta_vazia()}")
    jogo.listar_jogadores()
    jogo.mostrar_atual()

    # ---------------------------------------------------------
    # TESTE 10: Buscar/remover jogador inexistente
    # ---------------------------------------------------------
    print("\n[10] Remover jogador inexistente (id=999)")
    jogo.adicionar_jogador(Jogador(1, "Teste"))
    jogo.remover_jogador(999)
    jogo.listar_jogadores()

    print("\n" + "=" * 70)
    print(" FIM DOS TESTES ")
    print("=" * 70)


# ---------------------------------------------------------------
# EXECUÇÃO DIRETA
# ---------------------------------------------------------------
if __name__ == "__main__":
    executar_testes()
