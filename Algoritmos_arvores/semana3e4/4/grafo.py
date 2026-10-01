from collections import deque


class Vertice:
    def __init__(self, id):
        self.id = id
        self.cor =  'BRANCO'
        self.pi = None
        self.d = None
        self.f = None

class Grafo:
    def __init__(self, direcionado=True):
        self.direcionado = direcionado

        #Armazena os objetos Vertice instanciados por chave e valor (id -> objeto Vertice)
        self.vertices = {} 
        # O array principal de Listas de Adjacência (id -> lista de objetos Vertice)
        #chave=id valor->lista de adjacencia do vértice
        self.Adj = {}      

    def adicionar_vertice(self, id):
        """Instancia e registra um vértice no grafo caso ele não exista."""
        if id not in self.vertices:
            novo_vertice = Vertice(id)
            #chave=id valor=instancia da classe
            self.vertices[id] = novo_vertice
            self.Adj[id] = [] # Cria a gaveta (lista vazia) para as futuras conexões

    def adicionar_aresta(self, u, v):
        """Cria uma conexão saindo de 'u' e chegando em 'v'."""
        #u e v serão os ids dos grafos
        
        #Garante que ambos os vértices existam fisicamente na memória
        #operação de adição só será concluida caso id não esteja já cadastrado
        self.adicionar_vertice(u)
        self.adicionar_vertice(v)

        #Resgata os objetos Vertice diretamente da memória
        vertice_u = self.vertices[u]
        vertice_v = self.vertices[v]

        #Insere o DESTINO na lista de adjacência da ORIGEM
        self.Adj[u].append(vertice_v)

        #Se for Grafo Não Direcionado, exige a ligação reversa obrigatória
        if not self.direcionado:
            self.Adj[v].append(vertice_u)

    

    def busca_em_largura(self, origem_id):
            """
            TROCA DE INTERAÇÃO SE DÁ A PARTIR DA LISTA FIFO

                  ATENÇÃO
                  - todo pai irá virar preto
                  - a origem nunca terá pai
                  - não existe escolha de melhor origem

                  Exemplo completo no final do documento
                  
            """
            
            
            for v_id, vertice in self.vertices.items():
                #preparando o terreno(garantindo que todos sejam brancos menos o vértice de origem) e que a distância
                #seja infinita e pi é None
                if v_id != origem_id:
                    
                    vertice.cor = 'Branco'
                vertice.d = float('inf') # Distância infinita
                vertice.pi = None

            #selecionando o vértice a partir do id da origem
            origem = self.vertices[origem_id]
            origem.cor = 'Cinza'
            origem.d = 0
            origem.pi = None

            #A FILA DE EXECUÇÃO (Q)
            # Usamos uma lista do Python atuando como Fila FIFO
            #First in first out,quem entrou primeiro irá sair primeiro
            Q = []
            Q.append(origem) # A fila nasce apenas com a origem

            #não podemos utilizar recursividade,se não a lista de vértices para ser processado iria embora toda vez que houvesse uma interação
            while len(Q) > 0:
                #pop remove e retorna para a varíavel o valor do índice passado
                u = Q.pop(0) 
                lista_adj = self.Adj[u.id]

                #v seria os vértices filhos
                for v in lista_adj:
                # Trava de segurança: só processa se for inédito (Branco)
                    if v.cor == 'Branco':
                        v.cor = 'Cinza'       # Marca como descoberto
                        v.d = u.d + 1         # A distância do filho é a do pai + 1 aresta
                        v.pi = u              # O pai deste vizinho v é o vértice u
            
                    #Adiciona na fila para que seus próprios vizinhos sejam lidos no futuro
                    Q.append(v)

                # Após esgotar o loop for (todos os vizinhos foram inspecionados), o pai finaliza
                u.cor = 'Preto'

    def dfs_principal(self):
        #PREPARAÇÃO DO TERRENO-->garantindo que todos os vértices sejam resetados por padrão
        for v_id, vertice in self.vertices.items():
            vertice.cor = 'Branco'
            vertice.pi = None
            vertice.d = None
            vertice.f = None
        
        #ciação de atributo da classe
        self.tempo = 0
        
        #loop para interar em todos os vértices
        for v_id, vertice in self.vertices.items():
            if vertice.cor == 'Branco':
                # Encontrou um nó intocado: aciona o motor para iniciar uma nova árvore
                self.dfs_visit(vertice)


    def dfs_visit(self, u):
        # 1. MARCAÇÃO DE DESCOBERTA (O mergulho no nó)
        self.tempo += 1          # O relógio avança
        u.d = self.tempo         #distancia do vértice seria o tempo atual
        u.cor = 'Cinza'          #transforma o nó que era Branco em Cinza
        
        #EXPLORAÇÃO PROFUNDA DOS VIZINHOS
        lista_adj = self.Adj[u.id]
        for v in lista_adj:
            #só irá ser explorado se a cor for branca
            if v.cor == 'Branco':
                v.pi = u  #seta o pai daquele vértice que estava na lista como u(vértice da interação)

                # Recursão: Mergulha imediatamente no vizinho antes de ler os outros
                self.dfs_visit(v)
                
        #Começo da volta da interação,
        u.cor = 'Preto'          # Nó totalmente processado
        self.tempo += 1          # O relógio avança para o fechamento
        #tempo seria a contagem de interação de ida=u.d
        # e a contagem de interação de volta=u.f
        u.f = self.tempo         #carimbo de finalização

    def ordenamento_topologico(self):
        #reseta os valores de todos os vértices
        for vertice in self.vertices.values():
            vertice.cor = 'Branco'
            vertice.pi = None
            
        self.tempo = 0
        
        #Utilizamos deque (double-ended queue) para garantir que a inserção 
        #no início (appendleft) custe O(1), mantendo o tempo linear total.
        self.lista_ordenada = deque()
        
        
        #pega apenas os valores dos dicionários
        for vertice in self.vertices.values():
            if vertice.cor == 'Branco':
                #puxa a função caso seja branco(não visitado ainda)
                self._dfs_visit_topologico(vertice)
                
        # Retorna a lista contendo apenas os IDs ordenados para facilitar a leitura
        return list(self.lista_ordenada)

    def _dfs_visit_topologico(self, u):
        #Descoberta do vértice==+1 de tempo
        self.tempo += 1
        u.d = self.tempo # define o tempo de descoberta como o tempo atual
        u.cor = 'Cinza' #seta o vértice como cinza pois está sendo processado
        
        #irá mergulahar nos vértices filhos do vértice escolhido
        for v in self.Adj[u.id]:
            #só irá fazer a recursão caso seja branco(ou seja nunca visitado)
            if v.cor == 'Branco':
                #seta o pai como o vértice atual da interação
                v.pi = u
                self._dfs_visit_topologico(v)
                
        # Finalização
        u.cor = 'Preto'
        self.tempo += 1 # adiciona +1 pelo tempo de volta
        u.f = self.tempo
        
        # A MÁGICA: No exato instante em que é finalizado, entra na cabeça da fila
        self.lista_ordenada.appendleft(u.id)


    def gerar_grafo_transposto(self):
        # 1. Aloca o novo grafo herdando a propriedade do original
        novo_grafo = Grafo(direcionado=self.direcionado)

        #primeiro add o vértice,posteriormente que seria as arestas
        #adicionando os vértices pelo id
        #se quiser pegar apenas a chave só usar o for normal
        for v_id in self.vertices:
            novo_grafo.adicionar_vertice(v_id)

        # 3. A Varredura de Inversão (Sua lógica com a sintaxe corrigida)
        for u_id, lista_vizinhos in self.Adj.items():
            for v in lista_vizinhos:
                # v é o objeto Vertice. Invertemos a injeção: (v.id -> u_id)
                novo_grafo.adicionar_aresta(v.id, u_id)

        return novo_grafo


    def componente_fortemente_conectado(self):
        #entender o objetivo e como implementar
        pass

                
            
        





# =====================================================================
# RASTREAMENTO VISUAL: BUSCA EM LARGURA (BFS)
# =====================================================================
"""
objetivo não é encontrar algo,mas sim ele atua como um radar mapeando a rede
"""


# Topologia Inicial:
#       [A]
#      /   \
#    [B]   [C]
#      \   /
#       [D]
#
# Legenda do Sistema de Cores: 
# (B) = Branco (Inexplorado)
# (C) = Cinza  (Na Fila, aguardando para expandir seus vizinhos)
# (P) = Preto  (Finalizado, todos os seus vizinhos já foram lidos)
#
# ---------------------------------------------------------------------
# PASSO 0: Inicialização (Origem = A)
# A origem 'A' é descoberta. Distância = 0.
# Fila : [A]
# Cores: A(C) | B(B), C(B), D(B)
#
# PASSO 1: Expansão do Nível 1
# Desenfileira [A]. Lê a lista Adj[A] -> encontra B e C (brancos).
# B e C ficam Cinzas, recebem distância 1, e entram na fila. 'A' vira Preto.
# Fila : [B, C]
# Cores: A(P) | B(C), C(C) | D(B)
#
# PASSO 2: Expansão do Nível 2 (Iniciando por B)
# Desenfileira [B]. Lê a lista Adj[B] -> encontra A (preto, ignora) e D (branco).
# D fica Cinza, recebe distância 2, e entra na fila. 'B' vira Preto.
# Fila : [C, D]
# Cores: A(P), B(P) | C(C), D(C)
#
# PASSO 3: Expansão do Nível 2 (Continuando por C)
# Desenfileira [C]. Lê a lista Adj[C] -> encontra A (preto) e D (cinza).
# Ignora ambos, pois nenhum é Branco. 'C' vira Preto.
# Fila : [D]
# Cores: A(P), B(P), C(P) | D(C)
#
# PASSO 4: Fechamento
# Desenfileira [D]. Vizinhos B e C já são Pretos. Ignora. 'D' vira Preto.
# Fila : [] (Vazia)
# Cores: A(P), B(P), C(P), D(P) -> Varredura Finalizada.




# =====================================================================


# =====================================================================
# RASTREAMENTO VISUAL: BUSCA EM PROFUNDIDADE (DFS)
# =====================================================================
# Topologia Inicial:
#       [A]
#      /   \
#    [B]   [C]
#      \   
#       [D]
#
# Legenda: 
# Vértice(Cor)[d/f] -> 'd' é Descoberta, 'f' é Finalização.
# Relógio Global (Tempo) inicia em 0.
#
# ---------------------------------------------------------------------
# PASSO 0: Inicialização
# Todos Brancos. Tempo = 0.
#
# PASSO 1: O Mergulho Inicial (Origem = A)
# Inicia em A. Tempo = 1. A vira Cinza e recebe d=1.
# Lê Adj[A] -> encontra B (Branco). O algoritmo NÃO enfileira, ele MERGULHA imediatamente em B.
# Pilha de Recursão: [A]
# Estado: A(C)[1/?]
#
# PASSO 2: Aprofundando em B
# Tempo = 2. B vira Cinza e recebe d=2.
# Lê Adj[B] -> encontra D (Branco). Mergulha imediatamente em D.
# Pilha de Recursão: [A -> B]
# Estado: A(C)[1/?], B(C)[2/?]
#
# PASSO 3: O Fundo do Poço (Beco sem saída em D)
# Tempo = 3. D vira Cinza e recebe d=3.
# Lê Adj[D] -> vazia (ou todos vizinhos já foram visitados). 
# D não tem para onde ir. Ele é finalizado (Preto). Tempo = 4. D recebe f=4.
# O algoritmo faz o BACKTRACK (volta para quem chamou D, que foi B).
# Pilha de Recursão: [A -> B] -> Volta!
# Estado: A(C)[1/?], B(C)[2/?], D(P)[3/4]
#
# PASSO 4: O Retorno a B
# O algoritmo volta a ler a Adj[B]. Todos os vizinhos de B já foram processados.
# B é finalizado (Preto). Tempo = 5. B recebe f=5.
# BACKTRACK para A.
# Pilha de Recursão: [A] -> Volta!
# Estado: A(C)[1/?], B(P)[2/5], D(P)[3/4]
#
# PASSO 5: A retoma sua lista e acha C
# A continua lendo Adj[A] e agora encontra C (Branco). Mergulha em C.
# Tempo = 6. C vira Cinza, recebe d=6.
# Lê Adj[C] -> vazia. C finaliza (Preto). Tempo = 7. C recebe f=7.
# Pilha de Recursão: [A -> C] -> Volta!
# Estado: A(C)[1/?], B(P)[2/5], D(P)[3/4], C(P)[6/7]
#
# PASSO 6: Fechamento Total
# A retoma sua lista. Nenhum vizinho Branco restante.
# A finaliza (Preto). Tempo = 8. A recebe f=8.
# Pilha de Recursão: Vazia.
# Resultado Final: A[1/8], B[2/5], C[6/7], D[3/4]
# =====================================================================


# =====================================================================
# RASTREAMENTO VISUAL: ORDENAMENTO TOPOLÓGICO
# =====================================================================
"""
Objetivo: Achatar o grafo em uma linha horizontal da esquerda para a 
direita, de modo que todas as setas de dependência apontem apenas 
para a direita.

Ordenamento topolótico irá ser feito em grafos DAG(Direcionados e aciclicos)

LEMA 22.11(CONDIÇÃO DE EXISTÊNCIA PARA GRAFO DIRECIONADO SER ORDENADO LINEARMENTE SE FOR ACICLICO,CASO CONTRÁRIO CAUSA CICLO 
A->B->C->A
)
- grafo direcionado só é aciclico se a busca em profundidade produzir nenhuma aresta preta(aresta de retorno)
se durante a varredura encontrar um vizinho cinza,então já passou por aquele vértice
vértice cinza é um ancestral que ainda está sendo processado
"""

# Topologia Inicial (Um mini-guia de se vestir):
#   [Calça]       [Camisa]
#       \           /   \
#        v         v     v
#       [Sapato] <~    [Gravata]
#
# Arestas Direcionadas:
# 1. Calça -> Sapato
# 2. Camisa -> Sapato
# 3. Camisa -> Gravata
#
# Legenda: Vértice(Cor)[Descoberta/Finalização]
# Estrutura Alvo: Lista Encadeada (inserção sempre na CABEÇA/INÍCIO)
#
# ---------------------------------------------------------------------
# PASSO 0: Inicialização
# Relógio = 0. Lista = Vazia [ ]
#
# PASSO 1: O Laço Principal escolhe um vértice Branco arbitrário (ex: Calça)
# Calça inicia (Cinza). Relógio = 1. d=1.
# Calça mergulha em Sapato (Branco). Relógio = 2. Sapato fica Cinza, d=2.
#
# PASSO 2: O Fundo do Poço para Sapato
# Sapato não tem setas saindo dele. Beco sem saída.
# Sapato encerra. Relógio = 3. f=3. Sapato vira Preto.
# MÁGICA DO ALGORITMO: No instante em que fica Preto, insere na Lista!
# Lista Atual: [Sapato]
#
# PASSO 3: O Retorno para Calça
# Backtrack para Calça. Ela não tem outros vizinhos.
# Calça encerra. Relógio = 4. f=4. Calça vira Preto.
# Insere na cabeça da Lista!
# Lista Atual: [Calça] -> [Sapato]
#
# PASSO 4: O Laço Principal continua e acha Camisa (Branco)
# Camisa inicia (Cinza). Relógio = 5. d=5.
# Camisa olha seus vizinhos: Sapato e Gravata.
# Vê Sapato: já é Preto (ignora, a precedência já está garantida).
# Vê Gravata: é Branco. Mergulha em Gravata! Relógio = 6. Gravata(Cinza), d=6.
#
# PASSO 5: O Fundo do Poço para Gravata
# Gravata não tem vizinhos. Encerra. Relógio = 7. f=7. Gravata vira Preto.
# Insere na cabeça da Lista!
# Lista Atual: [Gravata] -> [Calça] -> [Sapato]
#
# PASSO 6: O Retorno para Camisa e Fechamento
# Backtrack para Camisa. Não há mais vizinhos brancos.
# Camisa encerra. Relógio = 8. f=8. Camisa vira Preto.
# Insere na cabeça da Lista!
# Lista Atual: [Camisa] -> [Gravata] -> [Calça] -> [Sapato]
#
# RESULTADO FINAL DA LISTA:
# Camisa(f=8) -> Gravata(f=7) -> Calça(f=4) -> Sapato(f=3)
# =====================================================================

# =====================================================================
# RASTREAMENTO VISUAL: GRAFO TRANSPOSTO (G^T)
# =====================================================================
"""
Objetivo: Criar uma cópia espelhada do grafo original, onde o fluxo 
de todas as rodovias (arestas) é invertido fisicamente na memória.
"""

# ---------------------------------------------------------------------
# TOPOLOGIA ORIGINAL (G)
# ---------------------------------------------------------------------
# Vértices: A, B, C, D
# Arestas : 
# A -> B
# B -> C
# C -> A   (A, B e C formam um ciclo)
# C -> D   (D é uma rota de fuga isolada)
#
# Memória (Lista de Adjacência Original):
# Adj[A] = [B]
# Adj[B] = [C]
# Adj[C] = [A, D]
# Adj[D] = []
#
# ---------------------------------------------------------------------
# A MECÂNICA DE INVERSÃO
# ---------------------------------------------------------------------
# Passo 1: O algoritmo lê Adj[A]. Vê a aresta (A -> B).
#          Vai no novo grafo G^T e insere a aresta (B -> A).
#
# Passo 2: O algoritmo lê Adj[B]. Vê a aresta (B -> C).
#          Vai no novo grafo G^T e insere a aresta (C -> B).
#
# Passo 3: O algoritmo lê Adj[C]. Vê as arestas (C -> A) e (C -> D).
#          Vai no novo grafo G^T e insere (A -> C) e (D -> C).
#
# ---------------------------------------------------------------------
# TOPOLOGIA RESULTANTE (G^T)
# ---------------------------------------------------------------------
# Memória (Lista de Adjacência Transposta):
# Adj[A] = [C]
# Adj[B] = [A]
# Adj[C] = [B]
# Adj[D] = [C]
#
# O ciclo (A-B-C) agora gira no sentido inverso, mas continua sendo um ciclo.
# A rota de fuga (C -> D) virou uma barreira (D -> C).
# =====================================================================




# =====================================================================
# RASTREAMENTO VISUAL: COMPONENTES FORTEMENTE CONECTADAS
# =====================================================================
"""
Objetivo: Isolar sub-redes cíclicas (bairros onde todos chegam em todos)
usando duas rodadas de DFS separadas por uma inversão espacial.
"""

# TOPOLOGIA ORIGINAL G:
# [A] ----> [B] ----> [C]
#  ^         |         ^
#  \---------/         |
#                      v
#                     [D]
#
# Ciclos visíveis: (A, B) formam uma CFC. (C, D) formam outra CFC.
# Fluxo macro: A CFC(A,B) aponta para a CFC(C,D).
#
# ---------------------------------------------------------------------
# FASE 1: A Primeira DFS (Extraindo os tempos de finalização)
# O objetivo aqui é rodar a DFS normal apenas para carimbar o 'f' (tempo 
# de finalização) de cada nó.
#
# Roteiro da 1ª DFS (Iniciando por A):
# A(d=1) mergulha em B(d=2). B mergulha em C(d=3). C mergulha em D(d=4).
# D só tem seta para C (já cinza). D finaliza: f=5.
# Volta para C. C finaliza: f=6.
# Volta para B. A seta de B para A (já cinza). B finaliza: f=7.
# Volta para A. A finaliza: f=8.
#
# Tempos (f) extraídos: A(8), B(7), C(6), D(5)
# Ordem decrescente de 'f': [A, B, C, D]
#
# ---------------------------------------------------------------------
# FASE 2: A Inversão (Construção do Grafo Transposto G^T)
# Invertemos todas as setas. Os ciclos continuam girando, mas a "ponte"
# entre as componentes inverte. O que era (B -> C) vira (C -> B).
#
# TOPOLOGIA G^T:
# [A] <---- [B] <---- [C]
#  |         ^         |
#  \---------/         v
#                     [D]
#
# ---------------------------------------------------------------------
# FASE 3: A Segunda DFS (A Colheita das Ilhas)
# Rodamos uma DFS sobre G^T, OBRIGATORIAMENTE varrendo o laço principal
# na ordem DECRESCENTE dos tempos (f) calculados na FASE 1: [A, B, C, D]
#
# Passo 3.1: Inicia por 'A' (Maior f=8).
# 'A' mergulha em 'B'. 'B' aponta para 'A' (já visitado). 'B' finaliza.
# 'A' não tem mais vizinhos Brancos. 'A' finaliza.
# RESULTADO: A DFS esgotou. A árvore gerada é a 1ª COMPONENTE: {A, B}
# Magia: A recursão de 'A' não "vazou" para 'C' porque a seta (B->C) 
# foi invertida para (C->B) no Grafo Transposto!
#
# Passo 3.2: O laço testa 'B', mas 'B' já é Preto. Pula.
#
# Passo 3.3: Inicia por 'C' (Próximo maior f=6).
# 'C' aponta para 'B' (Preto, barreira intransponível!).
# 'C' mergulha em 'D'. 'D' aponta para 'C' (já visitado). 'D' finaliza.
# 'C' finaliza.
# RESULTADO: Nova árvore gerada. 2ª COMPONENTE: {C, D}
#
# RESULTADO FINAL: Duas ilhas isoladas -> {A, B} e {C, D}.
# =====================================================================



"""
STRONGLY_CONNECTED_COMPONENTS(G):
    # FASE 1: O Mapeamento
    # Custo: O(V + E)
    Executar DFS_PRINCIPAL(G) para computar os tempos de finalização u.f 
    para cada vértice u.
    
    # FASE 2: A Inversão
    # Custo: O(V + E)
    Computar o Grafo Transposto G_T.
    
    # FASE 3: A Varredura Restritiva
    # Custo: O(V + E)
    # Precisamos zerar as cores do novo grafo G_T para Brancas antes da busca.
    Executar DFS_PRINCIPAL_MODIFICADA(G_T) com uma única alteração no 
    laço principal:
        Em vez de selecionar os vértices aleatoriamente, o laço "Para cada 
        vértice u" DEVE testar os vértices na ordem estritamente DECRESCENTE
        dos tempos 'u.f' calculados na Fase 1.
        
    # FASE 4: O Resultado
    Cada "Floresta/Árvore" que nascer e morrer separadamente durante a 
    FASE 3 constitui uma Componente Fortemente Conectada isolada.

"""