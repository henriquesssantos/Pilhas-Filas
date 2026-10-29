"""
================================================================
EXERCÍCIO 2 - PLAYLIST EDITÁVEL (Lista Duplamente Encadeada)
================================================================
Estruturas de Dados | Listas duplas e circulares

Diferenças-chave em relação à lista simples:
  - Cada nó tem DOIS ponteiros: self.anterior e self.proximo
  - Mantemos dois marcadores: self.inicio e self.fim
  - Podemos navegar nas duas direções (início -> fim e fim -> início)
  - Regra de coerência: A.proximo == B  <=>  B.anterior == A

Autor: <seu nome>
================================================================
"""


# ---------------------------------------------------------------
# NÓ DA LISTA (classe Musica)
# ---------------------------------------------------------------
class Musica:
    """
    Representa um nó da lista duplamente encadeada.
    Em C teríamos: struct Musica *ant, *prox;
    Em Python usamos: self.anterior, self.proximo (referências para outros objetos Musica)
    """

    def __init__(self, codigo, titulo, artista, duracao):
        self.codigo = codigo        # int  - identificador único
        self.titulo = titulo        # str  - nome da música
        self.artista = artista      # str  - nome do artista
        self.duracao = duracao      # int  - duração em SEGUNDOS
        self.anterior = None        # Musica ou None  (equivalente ao *ant em C)
        self.proximo = None         # Musica ou None  (equivalente ao *prox em C)

    def __repr__(self):
        return f"[{self.codigo}] {self.titulo} - {self.artista} ({self.duracao}s)"
    


# ---------------------------------------------------------------
# LISTA DUPLAMENTE ENCADEADA (classe Playlist)
# ---------------------------------------------------------------
class Playlist:
    """
    Lista duplamente encadeada de objetos Musica.
    Mantém dois marcadores:
      - self.inicio  -> primeiro nó (None se vazia)
      - self.fim     -> último  nó (None se vazia)
    """

    def __init__(self):
        self.inicio = None
        self.fim = None

    # ---------------------------------------------------------
    # 1) ADICIONAR MÚSICA AO FINAL
    # ---------------------------------------------------------
    def adicionar_ao_final(self, musica):
        """
        Insere um novo nó no fim da lista.
        Casos: lista vazia  |  lista com elementos
        """
        if self.inicio is None:
            # Lista vazia: a nova música é início E fim
            self.inicio = musica
            self.fim = musica
        else:
            # Liga a nova música DEPOIS do fim atual
            self.fim.proximo = musica      # antigo fim aponta para frente
            musica.anterior = self.fim     # nova música aponta para trás
            self.fim = musica             # atualiza o marcador fim

    # ---------------------------------------------------------
    # 5) BUSCAR MÚSICA PELO CÓDIGO  (usado pelos métodos 2, 3, 6, 7)
    # ---------------------------------------------------------
    def buscar(self, codigo):
        """
        Percorre do início ao fim procurando o código.
        Retorna o nó Musica ou None se não existir.
        """
        atual = self.inicio
        while atual is not None:
            if atual.codigo == codigo:
                return atual
            atual = atual.proximo
        return None

    # ---------------------------------------------------------
    # 2) INSERIR UMA MÚSICA ANTES DE UM CÓDIGO INFORMADO
    # ---------------------------------------------------------
    def inserir_antes_de(self, codigo_ref, nova_musica):
        """
        Insere nova_musica imediatamente ANTES do nó cujo codigo == codigo_ref.
        Casos especiais:
          - codigo_ref não existe  -> retorna False
          - codigo_ref é o início  -> nova_musica vira o novo início
        """
        alvo = self.buscar(codigo_ref)
        if alvo is None:
            print(f"  [!] Código {codigo_ref} não encontrado. Inserção cancelada.")
            return False

        if alvo == self.inicio:
            # Inserção no início: nova música aponta para o início atual
            nova_musica.proximo = self.inicio
            self.inicio.anterior = nova_musica
            self.inicio = nova_musica
        else:
            # Inserção no meio: ligar 4 ponteiros
            anterior = alvo.anterior
            # lado esquerdo: anterior -> nova -> alvo
            anterior.proximo = nova_musica
            nova_musica.anterior = anterior
            # lado direito: nova -> alvo
            nova_musica.proximo = alvo
            alvo.anterior = nova_musica
        return True

    # ---------------------------------------------------------
    # 3) INSERIR UMA MÚSICA DEPOIS DE UM CÓDIGO INFORMADO
    # ---------------------------------------------------------
    def inserir_depois_de(self, codigo_ref, nova_musica):
        """
        Insere nova_musica imediatamente DEPOIS do nó cujo codigo == codigo_ref.
        Caso codigo_ref seja o fim, delega para adicionar_ao_final (atualiza self.fim).
        """
        alvo = self.buscar(codigo_ref)
        if alvo is None:
            print(f"  [!] Código {codigo_ref} não encontrado. Inserção cancelada.")
            return False

        if alvo == self.fim:
            # Inserção no fim: reusa o método 1 para atualizar self.fim corretamente
            self.adicionar_ao_final(nova_musica)
        else:
            # Inserção no meio: ligar 4 ponteiros
            proximo = alvo.proximo
            # lado esquerdo: alvo -> nova -> proximo
            alvo.proximo = nova_musica
            nova_musica.anterior = alvo
            # lado direito: nova -> proximo
            nova_musica.proximo = proximo
            proximo.anterior = nova_musica
        return True

    # ---------------------------------------------------------
    # 4) LISTAR DO INÍCIO AO FIM  e  DO FIM AO INÍCIO
    # ---------------------------------------------------------
    def listar_inicio_fim(self):
        """Percorre usando self.proximo, do início ao fim."""
        atual = self.inicio
        if atual is None:
            print("  (lista vazia)")
            return
        while atual is not None:
            print(f"  {atual}")
            atual = atual.proximo

    def listar_fim_inicio(self):
        """Percorre usando self.anterior, do fim ao início. ( Só é possível em lista dupla! )"""
        atual = self.fim
        if atual is None:
            print("  (lista vazia)")
            return
        while atual is not None:
            print(f"  {atual}")
            atual = atual.anterior

    # ---------------------------------------------------------
    # 6) REMOVER UMA MÚSICA PELO CÓDIGO
    # ---------------------------------------------------------
    def remover(self, codigo):
        """
        Remove o nó cujo codigo == codigo.
        Casos especiais:
          - código não existe       -> False
          - único elemento da lista -> inicio = fim = None
          - remover o primeiro      -> atualiza self.inicio
          - remover o último        -> atualiza self.fim
          - remover do meio         -> liga anterior.proximo = proximo
        """
        alvo = self.buscar(codigo)
        if alvo is None:
            print(f"  [!] Código {codigo} não encontrado. Remoção cancelada.")
            return False

        # Caso 1: único elemento da lista
        if self.inicio == self.fim:
            self.inicio = None
            self.fim = None

        # Caso 2: remover o primeiro
        elif alvo == self.inicio:
            self.inicio = alvo.proximo
            self.inicio.anterior = None

        # Caso 3: remover o último
        elif alvo == self.fim:
            self.fim = alvo.anterior
            self.fim.proximo = None

        # Caso 4: remover do meio
        else:
            alvo.anterior.proximo = alvo.proximo
            alvo.proximo.anterior = alvo.anterior

        # (Opcional) limpa os ponteiros do nó removido
        alvo.anterior = None
        alvo.proximo = None
        return True

    # ---------------------------------------------------------
    # 7) MOVER UMA MÚSICA EXISTENTE PARA O INÍCIO
    # ---------------------------------------------------------
    def mover_para_inicio(self, codigo):
        """
        Reposiciona um nó já existente para o início da lista,
        SEM criar/destruir o objeto (apenas religa ponteiros).
        Etapas:
          1. Buscar o nó
          2. Se já é o início, nada a fazer
          3. Desconectar do local atual (trata fim e meio)
          4. Inserir no início
        """
        musica = self.buscar(codigo)
        if musica is None:
            print(f"  [!] Código {codigo} não encontrado. Movimentação cancelada.")
            return False

        # Se já é o primeiro, não precisa mover
        if musica == self.inicio:
            return True

        # Etapa 3: desconectar do local atual
        if musica == self.fim:
            # Tira do fim: o penúltimo vira o novo fim
            self.fim = musica.anterior
            self.fim.proximo = None
        else:
            # Tira do meio: religa os vizinhos
            musica.anterior.proximo = musica.proximo
            musica.proximo.anterior = musica.anterior

        # Etapa 4: coloca no início
        musica.anterior = None
        musica.proximo = self.inicio
        self.inicio.anterior = musica
        self.inicio = musica
        return True

    # ---------------------------------------------------------
    # 8) CALCULAR A DURAÇÃO TOTAL
    # ---------------------------------------------------------
    def duracao_total(self):
        """Soma a duração de todas as músicas (em segundos)."""
        total = 0
        atual = self.inicio
        while atual is not None:
            total += atual.duracao
            atual = atual.proximo
        return total


# ---------------------------------------------------------------
# TESTES OBRIGATÓRIOS DO EXERCÍCIO
# ---------------------------------------------------------------
def formatar_tempo(segundos):
    """Converte 195s -> '3:15' para exibição amigável."""
    m, s = divmod(segundos, 60)
    return f"{m}:{s:02d}"


def executar_testes():
    print("=" * 70)
    print(" EXERCÍCIO 2 - PLAYLIST EDITÁVEL (Lista Duplamente Encadeada) ")
    print("=" * 70)

    p = Playlist()

    # ---------------------------------------------------------
    # 1) Adicionar músicas ao final
    # ---------------------------------------------------------
    print("\n[1] Adicionar 3 músicas ao final")
    p.adicionar_ao_final(Musica(1, "Bohemian Rhapsody",  "Queen",         354))
    p.adicionar_ao_final(Musica(2, "Smells Like Teen Spirit", "Nirvana",  301))
    p.adicionar_ao_final(Musica(3, "Imagine",           "John Lennon",   183))

    print("\n  -> Listar início -> fim:")
    p.listar_inicio_fim()
    print("\n  -> Listar fim -> início:")
    p.listar_fim_inicio()
    print(f"\n  -> Duração total: {p.duracao_total()}s ({formatar_tempo(p.duracao_total())})")

    # ---------------------------------------------------------
    # 2) Inserir ANTES da primeira música  (código 1)
    # ---------------------------------------------------------
    print("\n[2] Inserir ANTES da primeira música (código 1)")
    p.inserir_antes_de(1, Musica(10, "Stairway to Heaven", "Led Zeppelin", 482))
    print("  -> Listar início -> fim:")
    p.listar_inicio_fim()

    # ---------------------------------------------------------
    # 3) Inserir DEPOIS da última música  (código 3)
    # ---------------------------------------------------------
    print("\n[3] Inserir DEPOIS da última música (código 3)")
    p.inserir_depois_de(3, Musica(20, "Hotel California", "Eagles", 391))
    print("  -> Listar início -> fim:")
    p.listar_inicio_fim()

    # ---------------------------------------------------------
    # 4) Pesquisar código inexistente
    # ---------------------------------------------------------
    print("\n[4] Pesquisar código inexistente (999)")
    resultado = p.buscar(999)
    print(f"  -> Resultado da busca: {resultado}")
    if resultado is None:
        print("  -> OK: retorna None conforme esperado.")

    # ---------------------------------------------------------
    # 5) Remover duas músicas consecutivas (códigos 2 e 3)
    # ---------------------------------------------------------
    print("\n[5] Remover duas músicas consecutivas (códigos 2 e 3)")
    print("  -> Removendo código 2...")
    p.remover(2)
    print("  -> Removendo código 3 (vizinho do anterior)...")
    p.remover(3)
    print("  -> Listar início -> fim:")
    p.listar_inicio_fim()
    print("\n  -> Listar fim -> início (valida coerência dos ponteiros):")
    p.listar_fim_inicio()

    # ---------------------------------------------------------
    # 6) Mover a primeira música para o início
    #     (deve permanecer no início, sem alterar a ordem)
    # ---------------------------------------------------------
    print("\n[6] Mover a primeira música (código 10) para o início")
    p.mover_para_inicio(10)
    print("  -> Listar início -> fim:")
    p.listar_inicio_fim()

    # Teste extra: mover uma do meio para o início
    print("\n  -> Teste extra: mover código 20 (que estava no fim) para o início")
    p.mover_para_inicio(20)
    print("  -> Listar início -> fim:")
    p.listar_inicio_fim()
    print("\n  -> Listar fim -> início:")
    p.listar_fim_inicio()

    # ---------------------------------------------------------
    # 7) Remover a ÚNICA música da lista
    # ---------------------------------------------------------
    print("\n[7] Remover a única música da lista")
    p_unica = Playlist()
    p_unica.adicionar_ao_final(Musica(100, "One", "U2", 271))
    print("  -> Antes da remoção:")
    p_unica.listar_inicio_fim()
    print(f"     inicio={p_unica.inicio}, fim={p_unica.fim}")
    p_unica.remover(100)
    print("  -> Depois da remoção:")
    p_unica.listar_inicio_fim()
    print(f"     inicio={p_unica.inicio}, fim={p_unica.fim}")
    print("  -> OK: lista voltou a ficar vazia (inicio = fim = None).")

    # ---------------------------------------------------------
    # 8) Duração total final da playlist principal
    # ---------------------------------------------------------
    print("\n[8] Duração total da playlist principal ao final dos testes")
    total = p.duracao_total()
    print(f"  -> Total: {total}s ({formatar_tempo(total)})")
    print("  -> Listagem final:")
    p.listar_inicio_fim()

    print("\n" + "=" * 70)
    print(" FIM DOS TESTES ")
    print("=" * 70)


# ---------------------------------------------------------------
# Execução direta: roda os testes quando o arquivo é chamado
# ---------------------------------------------------------------
if __name__ == "__main__":
    executar_testes()
