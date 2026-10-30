# CLASSE DO NÓ (objeto Pedido)

class Pedido:
    def __init__(self, numero, produto, unidades_restantes):
        self.numero = numero
        self.produto = produto
        self.unidades_restantes = unidades_restantes
        self.proximo = None

    def __repr__(self):
        # transformar o objeto Pedido em string legível sempre que o Python
        # precisar mostrá-lo. O código fica mais modular e evita reescrever
        # formatações em vários pontos.
        return f"[{self.numero}] {self.produto} ({self.unidades_restantes} un. restantes)"


# CLASSE DA FILA CIRCULAR ENCADEADA

class FilaProducao:
    def __init__(self):
        self.inicio = None   # front da fila (próximo pedido a receber lote)
        self.fim = None      # último pedido (o proximo dele volta ao início)

    # 1) INSERIR PEDIDO NO FINAL DO CICLO
    def adicionar_ao_final(self, pedido):
        # Caso a fila esteja vazia: o pedido aponta para ele mesmo
        # (fila de um só) e ele já é o front:
        if self.inicio is None:
            self.inicio = pedido
            self.fim = pedido
            pedido.proximo = pedido          # único nó aponta para ele mesmo
        # Caso a fila já possua pedidos:
        else:
            # com o ponteiro fim não precisa percorrer: inserção em tempo constante
            self.fim.proximo = pedido        # antigo fim aponta para o novo
            pedido.proximo = self.inicio     # novo fim fecha o ciclo: fim -> início
            self.fim = pedido                # atualiza a posição de fim

    # 2) EXIBIR TODOS OS PEDIDOS EXATAMENTE UMA VEZ
    def listar(self):
        if self.inicio is None:
            print("  (fila vazia)")
            return
        # ATENÇÃO: em uma fila circular nunca aparece um None para parar
        # o laço (o fim aponta de volta para o início). Um while
        # "atual is not None" rodaria para sempre. A condição segura aqui é
        # percorrer até o FIM, imprimindo cada pedido exatamente uma vez:
        atual = self.inicio
        while True:
            if atual == self.inicio:
                print(f"  {atual}   <- front (próximo a processar)")
            else:
                print(f"  {atual}")
            if atual == self.fim:        # chegou no último: fecha a volta
                break
            atual = atual.proximo

    # 3) PROCESSAR UM LOTE CONFIGURÁVEL DO PRIMEIRO PEDIDO
    def processar_primeiro(self, lote):
        if self.inicio is None:
            print("  [!] Não há pedidos na fila. Processamento cancelado.")
            return False
        if lote <= 0:
            print("  [!] O lote precisa ser maior que zero. Processamento cancelado.")
            return False
        if self.inicio.unidades_restantes == 0:
            print("  [!] O pedido do front já está concluído. Remova os concluídos antes de processar.")
            return False

        pedido = self.inicio
        # o lote é limitado: se ele for maior que as unidades restantes,
        # processa apenas o que falta (o pedido conclui no mesmo ciclo):
        if lote >= pedido.unidades_restantes:
            processadas = pedido.unidades_restantes
        else:
            processadas = lote
        pedido.unidades_restantes -= processadas

        if pedido.unidades_restantes == 0:
            print(f"  -> {pedido} processou {processadas} unidade(s): PEDIDO CONCLUÍDO!")
        else:
            print(f"  -> {pedido} processou {processadas} unidade(s) neste ciclo.")
        return True

    # 4) REMOVER PEDIDOS CONCLUÍDOS
    def remover_concluidos(self):
        if self.inicio is None:
            print("  [!] Não há pedidos na fila. Remoção cancelada.")
            return False

        removidos = []
        # Repete a varredura até uma volta completa não achar mais nenhum
        # pedido concluído. A remoção do primeiro nó circular é o caso
        # delicado: antes de tirar o início, o fim precisa ser religado ao
        # novo início, ou o ciclo quebra e a fila se perde:
        while True:
            if self.inicio is None:      # a fila terminou: nada mais a remover
                break

            # procura um pedido concluído em uma volta completa
            # (parada segura: de volta ao início, sem depender de None):
            alvo = None
            anterior = self.fim          # quem precede o início é o próprio fim
            atual = self.inicio
            while True:
                if atual.unidades_restantes == 0:
                    alvo = atual
                    break
                anterior = atual
                atual = atual.proximo
                if atual == self.inicio: # deu a volta completa: nada concluído
                    break

            if alvo is None:
                break                    # só restam pedidos ativos: fim da remoção

            # Caso 1: único pedido da fila: a fila termina vazia:
            if alvo == self.inicio and alvo == self.fim:
                self.inicio = None
                self.fim = None
            # Caso 2: remover o primeiro nó circular (alteração segura do início!):
            elif alvo == self.inicio:
                novo_inicio = alvo.proximo
                self.fim.proximo = novo_inicio   # LIGAÇÃO ESSENCIAL: fim -> novo início
                self.inicio = novo_inicio
            # Caso 3: remover o último: o penúltimo fecha o ciclo:
            elif alvo == self.fim:
                anterior.proximo = self.inicio
                self.fim = anterior
            # Caso 4: remover do meio: o anterior "pula" o removido:
            else:
                anterior.proximo = alvo.proximo

            removidos.append(alvo)
            print(f"  -> Pedido concluído removido da fila: {alvo}")

        if not removidos:
            print("  -> Nenhum pedido concluído na fila. Nada foi removido.")
            return False
        return True

    # 5) MOVER O FRONT PARA O PRÓXIMO PEDIDO ATIVO
    def mover_front(self):
        if self.inicio is None:
            print("  [!] Não há pedidos na fila. Movimentação cancelada.")
            return False
        # o front só gira se for um pedido ativo: pedido concluído não volta
        # ao final, ele precisa SAIR da fila (remoção dos concluídos):
        if self.inicio.unidades_restantes == 0:
            print("  [!] O pedido do front já está concluído. Remova os concluídos antes de mover o front.")
            return False

        # Mudança do front SEM reconstruir a fila: em uma fila circular basta
        # girar os dois ponteiros. O pedido parcial do início volta ao final
        # e o próximo pedido se torna o novo front:
        self.fim = self.inicio
        self.inicio = self.inicio.proximo
        print(f"  -> Front movido sem reconstruir a fila. Novo front: {self.inicio}")
        return True

    # 6) EXECUTAR ATÉ CONCLUIR TODOS OS PEDIDOS
    def executar_ate_concluir(self, lote):
        if self.inicio is None:
            print("  [!] Não há pedidos na fila. Execução cancelada.")
            return False
        if lote <= 0:
            print("  [!] O lote precisa ser maior que zero. Execução cancelada.")
            return False

        print(f"\n  Lote de processamento: {lote} unidade(s) por ciclo.")
        ciclo = 0
        # A fila circular não tem None no final para parar um laço de percurso
        # (por isso o listar usa a volta completa como parada). Aqui a parada
        # é outra: cada ciclo processa o front, e o pedido ou conclui e SAI
        # da fila, ou fica parcial e VOLTA ao final. Como todo ciclo processa
        # pelo menos 1 unidade, mais cedo ou mais tarde a fila termina vazia:
        while self.inicio is not None:
            ciclo += 1
            print(f"\n  --- Ciclo {ciclo} ---")
            # o pedido do front recebe uma quantidade limitada de processamento:
            self.processar_primeiro(lote)
            # concluído deixa a fila; parcial volta ao final:
            if self.inicio is not None and self.inicio.unidades_restantes == 0:
                self.remover_concluidos()
            elif self.inicio is not None:
                self.mover_front()

        print(f"\n  -> Execução finalizada em {ciclo} ciclo(s). Todos os pedidos foram concluídos!")
        return True

    # 7) CONTAR OS PEDIDOS DA FILA
    def contar_pedidos(self):
        quantidade = 0
        if self.inicio is None:
            return quantidade
        atual = self.inicio
        while True:
            quantidade += 1
            if atual == self.fim:        # mesma parada segura do listar
                break
            atual = atual.proximo
        return quantidade

    # 8) SOMAR AS UNIDADES RESTANTES DE TODA A FILA
    def calcular_unidades_restantes(self):
        unidades = 0
        if self.inicio is None:
            return unidades
        atual = self.inicio
        while True:
            unidades += atual.unidades_restantes
            if atual == self.fim:        # soma uma única volta, sem repetir
                break
            atual = atual.proximo
        return unidades


# FUNÇÕES AUXILIARES PARA O MENU

def ler_int(mensagem):
    #Lê um número inteiro do usuário, repetindo até digitar válido.
    while True:
        entrada = input(mensagem).strip()
        try:
            return int(entrada)
        except ValueError:
            print("  [!] Digite um número inteiro válido.")


def ler_pedido():
    #Pede os dados de um novo pedido ao usuário e devolve um objeto Pedido.
    numero = ler_int("  Número (int): ")
    produto = input("  Produto: ").strip()
    while True:
        unidades = ler_int("  Unidades restantes: ")
        if unidades > 0:
            break
        print("  [!] As unidades precisam ser maiores que zero.")
    return Pedido(numero, produto, unidades)


# ---------------------------------------------------------------
# MENU INTERATIVO
# ---------------------------------------------------------------
def menu():
    fila = FilaProducao()

    opcoes = {
        "1": ("Inserir pedido no final do ciclo",            "adicionar"),
        "2": ("Exibir todos os pedidos exatamente uma vez",  "listar"),
        "3": ("Processar um lote do primeiro pedido",        "processar"),
        "4": ("Remover pedidos concluídos",                  "remover_concluidos"),
        "5": ("Mover o front para o próximo pedido ativo",   "mover_front"),
        "6": ("Executar até concluir todos os pedidos",      "executar"),
        "7": ("Resumo da fila (pedidos e unidades)",         "resumo"),
        "0": ("Sair",                                        "sair"),
    }

    while True:
        print("\n" + "=" * 55)
        print("        FILA CIRCULAR DE PEDIDOS - MENU INTERATIVO")
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
            print("\n-- Inserir pedido no final do ciclo --")
            pedido = ler_pedido()
            fila.adicionar_ao_final(pedido)
            print(f"  -> Pedido adicionado: {pedido}")

        elif acao == "listar":
            print("\n-- Fila de produção (uma volta completa) --")
            fila.listar()

        elif acao == "processar":
            print("\n-- Processar um lote do primeiro pedido --")
            lote = ler_int("  Tamanho do lote (unidades): ")
            fila.processar_primeiro(lote)

        elif acao == "remover_concluidos":
            print("\n-- Remover pedidos concluídos --")
            fila.remover_concluidos()

        elif acao == "mover_front":
            print("\n-- Mover o front para o próximo pedido ativo --")
            fila.mover_front()

        elif acao == "executar":
            print("\n-- Executar até concluir todos os pedidos --")
            lote = ler_int("  Tamanho do lote por ciclo (unidades): ")
            fila.executar_ate_concluir(lote)

        elif acao == "resumo":
            print("\n-- Resumo da fila de produção --")
            print(f"  -> Pedidos na fila: {fila.contar_pedidos()}")
            print(f"  -> Unidades restantes a processar: {fila.calcular_unidades_restantes()}")


# ---------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------
if __name__ == "__main__":
    menu()