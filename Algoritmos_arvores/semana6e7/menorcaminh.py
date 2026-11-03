from collections import deque
import heapq

class Vertice:
    def __init__(self, id):
        self.id = id
        self.cor =  'Branco'
        self.pi = None
        self.d = None #d nesse caso é de distância
        

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

    # ADIÇÃO parâmetro 'peso'
    def adicionar_aresta(self, u, v, peso):
            """Cria uma conexão ponderada saindo de 'u' e chegando em 'v'."""
            #verifica se realmente já foi adicionado
            self.adicionar_vertice(u)
            self.adicionar_vertice(v)
    
            #pega o valor das listas de adjacencia em reação ao id do vértice
            vertice_u = self.vertices[u]
            vertice_v = self.vertices[v]
    
            # ATUALIZAÇÃO A lista de adjacência agora guarda uma TUPLA (Objeto Destino, Peso)
            self.Adj[u].append((vertice_v, peso))
    
            #Se for Grafo Não Direcionado(caso do MST), faz a ligação reversa com o MESMO peso
            if not self.direcionado:
                self.Adj[v].append((vertice_u, peso))

    

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

    def relaxar(self, u, v, peso_uv):

        #função de recalculamento de distância

        #funciona do mesmo jeito que a comparação das interações no dijkstra

        # Se a distância atual até 'v' for maior do que o caminho vindo por 'u' + o peso da ponte

        if v.d > u.d + peso_uv:

            v.d = u.d + peso_uv  # Atualiza a distância para o novo recorde

            v.pi = u             # O pai de 'v' passa a ser 'u'



        
    def caminho_mais_curto_DAG(self, origem_id):
        # Gera a lista com os IDs na ordem do ordenamento topológico
        ordenamento = self.ordenamento_topologico()

        #Inicializa todos os vértices com infinito e sem pai
        for v_id in ordenamento:
            vertice = self.vertices[v_id]
            vertice.d = float('inf')
            vertice.pi = None

        #Resgata o objeto da origem e zera a sua distância
        vertice_origem = self.vertices[origem_id]
        vertice_origem.d = 0

        #relaxamento

        for v_id in ordenamento:
            vertice_u = self.vertices[v_id] # Este é o vértice de onde estamos saindo
            
            #'vertice_v' é o objeto destino e 'peso' é o custo da aresta
            for vertice_v, peso in self.Adj[v_id]:
                # Relaxamos a aresta entre o vértice atual (u) e o seu vizinho (v)
                self.relaxar(vertice_u, vertice_v, peso)


        resultado = []
        #.items retorna chave e valor
        #casa:'33'
        #por ter atualizado todos os valores de d para todos os vértices
        #chamamos .items do dicionário vértice para pegar o id do destino e o custo atualizado
        for destino_id, vertice_destino in self.vertices.items():
            resultado.append({
                'origem': origem_id,
                'destino': destino_id, #pega o id(sendo a chave) do objeto
                'custo': vertice_destino.d #.id pois vertice_destino é o objeto 
            })
            
        return resultado


    def dijkstra(self,origem_id):
        #reiniciando todos os vértices
        for v_id,vertice in self.vertices.items():
            vertice.d=float('Inf')
            vertice.pi=None

        origem = Grafo.vertices[origem_id]
        origem.d = 0

        # 3. Inicializando a Fila de Prioridade (Min-Heap)
    # A tupla DEVE ser (distância, id_do_vertice). O Python sempre usará o 
    # índice 0 da tupla como critério de ordenação para achar o "menor" valor.
        filaQprioridade = [(0, origem_id)] 

        while len(filaQprioridade) > 0:
            distancia_atual, u_id = heapq.heappop(filaQprioridade)
            vertice_u = self.vertices[u_id]

            #Ignora duplicatas desatualizadas)
            #Se extrairmos um caminho velho que já foi superado, apenas pulamos.
            if distancia_atual > vertice_u.d:
                continue

            # Espalhamento: Varre os vizinhos do vértice extraído
            for vertice_v, peso in self.Adj[u_id]:
                #distancia pré setada como infinita
                distancia_antiga = vertice_v.d
            
            
                self.relaxar(vertice_u, vertice_v, peso)

            #só será adicionado algo novo na fila se encontrar um novo melhor caminho,se nção add,então
            # uma hora acaba o código
            #o que impede de dar erro em duplicadas é primeiro comparar se o caminho real do vértice até o
                if vertice_v.d < distancia_antiga:
                # ...inserimos a NOVA distância e o ID na fila.
                    heapq.heappush(filaQprioridade, (vertice_v.d, vertice_v.id))



        resultado = []
        for destino_id, vertice_destino in self.vertices.items():
            if vertice_destino.d != float('inf'):
            
            # Reconstrói a rota caminhando pelos pais (de trás para frente)
                caminho = []
                atual = vertice_destino
                while atual is not None:
                    caminho.append(atual.id)
                    atual = atual.pi #vai pegando o pai de cada um
                caminho.reverse() # Inverte para Origem -> Destino

                resultado.append({
                    'origem': origem_id,
                    'destino': destino_id,
                    'custo': vertice_destino.d,
                    'rota': " -> ".join(caminho)
                })
            
        return resultado


    def bellman_ford(self, origem_id):
        #Inicialização identica aos outros
        for v_id, vertice in self.vertices.items():
            vertice.d = float('inf')
            vertice.pi = None

        self.vertices[origem_id].d = 0
        total_vertices = len(self.vertices)

        # FASE 2: Espalhamento Exaustivo (V-1 vezes)
        for _ in range(total_vertices - 1):
            for u_id, vizinhos in self.Adj.items():
                vertice_u = self.vertices[u_id]
                for vertice_v, peso in vizinhos:
                    self.relaxar(vertice_u, vertice_v, peso)

        # FASE 3: Detecção de Ciclos de Peso Negativo
        # Varremos todas as arestas uma última vez
        for u_id, vizinhos in self.Adj.items():
            vertice_u = self.vertices[u_id]
            for vertice_v, peso in vizinhos:
                # Se ainda é possível encontrar um caminho menor, existe um ciclo negativo
                if vertice_v.d > vertice_u.d + peso:
                    print("ERRO: O grafo contém um ciclo de peso negativo inalcançável!")
                    return False

        # FASE 4: Estrutura de Retorno (Idêntica ao Dijkstra)
        resultado = []
        for destino_id, vertice_destino in self.vertices.items():
            if vertice_destino.d != float('inf'):
                
                caminho = []
                atual = vertice_destino
                while atual is not None:
                    caminho.append(atual.id)
                    atual = atual.pi
                caminho.reverse()

                resultado.append({
                    'origem': origem_id,
                    'destino': destino_id,
                    'custo': vertice_destino.d,
                    'rota': " -> ".join(caminho)
                })
                
        return resultado

        
   
            

        


        


"""
CAMINHO_MAIS_CURTO_DAG(Grafo, origem):
1.  ordem_topologica = ORDENAMENTO_TOPOLOGICO(Grafo)
    
2.  Para cada vértice 'v' no Grafo:
        v.d = infinito
        v.pi = Nulo
        
3.  origem.d = 0
    
4.  Para cada vértice 'u' seguindo a 'ordem_topologica':
        Para cada vizinho 'v' na lista de adjacência de 'u':
            peso_uv = peso da aresta entre u e v
            RELAXAR(u, v, peso_uv)
"""


"""
Escolhemos o ponto de origem e mapeamos os seus vértices filhos. Posteriormente, 
escolheremos aquele que tem o menor caminho para iterar. A partir desse menor caminho, 
iremos verificar os filhos do vértice filho escolhido que tem o menor caminho em relação à origem. 
A partir disso, aplicaremos o relaxamento caso exista um caminho melhor. 



DIJKSTRA(Grafo, origem_id):
1.  Para cada vértice 'v' no Grafo:
        v.d = infinito
        v.pi = Nulo
        
2.  origem = Grafo.vertices[origem_id]
3.  origem.d = 0

4.  Crie uma Fila de Prioridade Q (Min-Heap)
5.  Insira todos os vértices do Grafo em Q, usando o atributo 'v.d' como chave de prioridade.

6.  Enquanto Q não estiver vazia:
7.      u = Extraia de Q o vértice com o menor valor de 'd'
        
8.      Para cada vizinho 'v' e 'peso' na lista de adjacência de 'u':
9.          Se 'v' ainda estiver em Q (ou seja, ainda não foi processado como raiz):
10.             distancia_antiga = v.d
                
11.             RELAXAR(u, v, peso)
                
12.             Se a distância mudou (v.d < distancia_antiga):
13.                 Atualize a posição de 'v' dentro da Fila de Prioridade Q

"""