
class Vertice:
    def __init__(self, id):
        self.id = id
        self.key= float('inf')  #infinito do python
        self.pi=None

class Grafo:
    # Para MST, o padrão deve ser Não Direcionado (direcionado=False)
    def __init__(self, direcionado=False):
        self.direcionado = direcionado
        self.vertices = {} 
        self.Adj = {}      

    def adicionar_vertice(self, id):
        """Instancia e registra um vértice no grafo caso ele não exista."""
        if id not in self.vertices:
            novo_vertice = Vertice(id)
            self.vertices[id] = novo_vertice
            self.Adj[id] = [] 

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



"""
O objetivo do conjunto disjunto é atuar no algorito de kruskal 

conjunto disjunto atua como detector de ciclo



"""
class DisjointSet:
    def __init__(self):
        # Dicionários para mapear cada vértice ao seu respectivo 'pai' e 'rank'
        self.pai = {}
        self.rank = {}

    def make_set(self, vertice):
        """
        Cria um novo conjunto contendo apenas o vértice passado.
        Ele começa apontando para si mesmo (é o próprio representante).

        todos os vértice serão iniciados tendo os próprios como representantes
        e todos iniciando com rank 0

        """

        
        #chave=vértice
        #valor=vértice
        self.pai[vertice] = vertice
        #todo mundo começa com o mesmo rank
        self.rank[vertice] = 0

    def find_set(self, vertice):
        """
        Encontra o representante (raiz) do conjunto que contém o vértice.
        Aplica a heurística de Compressão de Percurso.
        """
        # Se o vértice não é o próprio pai, ele não é a raiz.
        #só não entrará nesse if se o valor de self.pa[vertice] for igual ou seja quando for o pai dele mesmo(pai supremo)
        if self.pai[vertice] != vertice:
            # Busca recursiva: encontra a raiz verdadeira e já atualiza 
            # o ponteiro do vértice atual DIRETAMENTE para essa raiz.
            #existe essa chamada recursiva pelo fato de pode ser dessa forma a-->b-->c
            #então a recursividade vai ser até o valor do self.pai[vertice] for o valor do vértice correto
            # essa atribuição de valor seria apenas para confirmação se todos estão corretos
            
            self.pai[vertice] = self.find_set(self.pai[vertice])
        
        return self.pai[vertice]

    """
================================================================================
VISUALIZAÇÃO DA RECURSÃO: COMPRESSÃO DE PERCURSO (PATH COMPRESSION)
================================================================================
Cenário: Imagine que, após várias fusões, temos uma árvore longa formando uma 
linha reta. O nó 'a' é o chefe supremo (raiz).

Estado inicial do dicionário:
self.pai = {'a': 'a', 'b': 'a', 'c': 'b', 'd': 'c'}

Estrutura visual antes da busca:
[a] (Chefe supremo, pai dele mesmo)
 |
[b] (Aponta para a)
 |
[c] (Aponta para b)
 |
[d] (Aponta para c)

O algoritmo aciona: ds.find_set('d')

--------------------------------------------------------------------------------
FASE 1: A IDA (Mergulhando na recursão até achar o chefe)
--------------------------------------------------------------------------------
O código executa a linha: self.pai[vertice] = self.find_set(self.pai[vertice])

1. find_set('d')
   - O pai de 'd' é 'c'. Como 'c' != 'd', a execução PAUSA e aciona:
   --> find_set('c')

2. find_set('c')
   - O pai de 'c' é 'b'. Como 'b' != 'c', a execução PAUSA e aciona:
   --> find_set('b')

3. find_set('b')
   - O pai de 'b' é 'a'. Como 'a' != 'b', a execução PAUSA e aciona:
   --> find_set('a')

4. find_set('a')
   - O pai de 'a' é 'a'. Condição satisfeita (a == a)! 
   - A recursão para de descer e RETORNA o valor 'a' para quem a chamou.

--------------------------------------------------------------------------------
FASE 2: A VOLTA (Desempilhando e Achatando a Árvore)
--------------------------------------------------------------------------------
Agora a resposta ('a') sobe pela pilha, resolvendo as execuções que estavam 
pausadas. É AQUI que ocorre a atribuição: self.pai[vertice] = 'a'

1. Voltando para find_set('b'):
   - A pausa termina. Ele recebe 'a'.
   - Atualiza: self.pai['b'] = 'a' (Já estava assim, então apenas confirma).
   - Retorna 'a' para a função de cima.

2. Voltando para find_set('c'):
   - A pausa termina. Ele recebe 'a'.
   - Atualiza: self.pai['c'] = 'a' (MÁGICA: 'c' abandona 'b' e aponta para 'a').
   - Retorna 'a' para a função de cima.

3. Voltando para find_set('d'):
   - A pausa termina. Ele recebe 'a'.
   - Atualiza: self.pai['d'] = 'a' (MÁGICA: 'd' abandona 'c' e aponta para 'a').
   - A função principal termina e entrega o resultado final: 'a'.

--------------------------------------------------------------------------------
O RESULTADO (O Achatamento)
--------------------------------------------------------------------------------
Estado do dicionário após a execução:
self.pai = {'a': 'a', 'b': 'a', 'c': 'a', 'd': 'a'}

Estrutura visual após a busca:
      [a]
     / | \
   [b][c][d]

Graças à recursão, se no próximo passo o Kruskal perguntar quem é o pai de 'd' 
ou de 'c', o código responderá em tempo O(1), sem precisar mergulhar novamente.
================================================================================
"""

    def union(self, u, v):
        """
        Une os conjuntos dinâmicos que contêm u e v.
        Utiliza a heurística de União por Rank para manter a árvore balanceada.
        """
        """
        Objtetivo de chamar a função findset é encontrar quem é o representante(pai) daquele vértice
        """
        raiz_u = self.find_set(u)
        raiz_v = self.find_set(v)

        #Se já possuem a mesma raiz, estão no mesmo conjunto (evita ciclo).
        if raiz_u == raiz_v:
            return

        # Heurística: União por Rank
        # A árvore menor (menor rank) é anexada à raiz da árvore maior.
        if self.rank[raiz_u] > self.rank[raiz_v]:
            self.pai[raiz_v] = raiz_u
        elif self.rank[raiz_u] < self.rank[raiz_v]:
            self.pai[raiz_u] = raiz_v
        else:
            # Se der empate, escolhemos uma como raiz e incrementamos seu rank
            self.pai[raiz_v] = raiz_u
            self.rank[raiz_u] += 1

"""
================================================================================
    O ALGORITMO DE KRUSKAL 
================================================================================
O Kruskal apenas ordena as arestas e usa a nossa classe DisjointSet para
tomar as decisões sem precisar olhar para o grafo inteiro toda hora.
"""

def mst_kruskal(grafo):
    """
    Recebe uma instância da sua classe Grafo e retorna a lista 
    de arestas que formam a Árvore Geradora Mínima.

    objetivo da MST é gerar um subconjunto aciclico que possua todos os vértices e que a o peso total das 
    arestas sejam os menores possíveis
    """
    mst = []
    ds = DisjointSet() 
    
    # 1.MAKE-SET: Inicializa a floresta usando as chaves (IDs) do dicionário
    for id_vertice in grafo.vertices:
        ds.make_set(id_vertice)
        
    #Varrendo a lista de Adjacência
    #arestas serve para guardar peso,u,v
    arestas = []
    #arestas vistas serve para guardar em conjunto quais arestas já foi passado
    arestas_vistas = set() 
    
    for u in grafo.Adj:
        # lista de adjacência agora devolve o Objeto e o Peso
        for obj_v, peso in grafo.Adj[u]:
            v = obj_v.id  
            
            #como é não direcionado,ordena-se o id para ser possível registrar apenas uma vez
            assinatura_aresta = tuple(sorted([u, v])) 
            
            if assinatura_aresta not in arestas_vistas:
                arestas_vistas.add(assinatura_aresta) #como é conjunto,só irá ter um de cada tipo

                # Guarda a tupla no formato prático para o sort: (peso, u, v)
                arestas.append((peso, u, v))
                
    #Ordena todas as arestas do mapa pelo peso 
    arestas.sort(key=lambda x: x[0])
    
    #ESTRATÉGIA GULOSA
    for peso, u, v in arestas:
        # Verifica no Conjunto Disjunto se eles já pertencem à mesma árvore
        #se não pertencerem então
        if ds.find_set(u) != ds.find_set(v):
            mst.append((u, v, peso))  # Contrata a aresta
            ds.union(u, v)            # Funde as duas árvores na memória
            
    return mst

def mst_prim(grafo, id_raiz):
    
    
    
    for v in grafo.vertices.values():
        v.key = float('inf')  #infinito do python
        v.pi = None
        
    raiz = grafo.vertices[id_raiz] #aponta para o objeto raiz escolhido
    raiz.key = 0 #zera a contagem do key da raiz
    
    
    filaQ = list(grafo.vertices.values())


    mst=[]
    # 3. O Loop Principal (Linhas 6 a 11)
    while len(filaQ) > 0:
        
        
        #Varre a lista, encontra o objeto vértice com o menor atributo 'key'
        #: lambda entrada : o_que_ela_devolve
        #"Extraia o mínimo da filaQ, mas baseie a sua decisão 
        # matemática exclusivamente no atributo 'key' de cada vértice".
        u = min(filaQ, key=lambda vertice: vertice.key)
        
        # Remove fisicamente o vértice u da filaQ, pois ele agora entrou na MST
        filaQ.remove(u)

        #ATUALIZAÇÃO DA LISTA QUE MOSTRA CAMINHO
        #para garantir que não terá none,raiz como tupla
        #objetivo é mostrar vértice pai,filho e peso
        if u.pi is not None:
            mst.append((u.pi.id, u.id, u.key))
        
        # A sua lista de adjacência guarda tuplas (objeto_destino, peso)
        #dicionário de listas
        #irá pegar apenas a lista em relação ao id do vértice

        #ATUALIZAÇÃO DOS VALORES DOS VIZINHIS
        for vizinho_v, peso_aresta in grafo.Adj[u.id]:
            
           
            # Se o vizinho ainda está aguardando na fila E a conexão com o vértice da vez for mais curta
            #dps o while pegará o menor valor de key atualizado e repetirá o processo,atualizando os valores de key
            if vizinho_v in filaQ and peso_aresta < vizinho_v.key:
                
                vizinho_v.pi = u           #Atualiza o pai
                vizinho_v.key = peso_aresta  #Atualiza o custo em relação ao pai


    
            
    return mst


# ==============================================================================
# BATERIA DE TESTES - GRAFOS, CONJUNTOS DISJUNTOS, KRUSKAL E PRIM
# ==============================================================================

def executar_testes():
    # 1. Instanciando o Grafo (Não direcionado para MST)
    print("--- INICIANDO CONSTRUÇÃO DO GRAFO ---")
    g = Grafo(direcionado=False)

    # 2. Inserindo as arestas (Os vértices são criados automaticamente pela sua função)
    # Arestas baseadas no clássico exemplo do Cormen
    arestas_teste = [
        ('a', 'b', 4), ('a', 'h', 8),
        ('b', 'c', 8), ('b', 'h', 11),
        ('c', 'd', 7), ('c', 'f', 4), ('c', 'i', 2),
        ('d', 'e', 9), ('d', 'f', 14),
        ('e', 'f', 10),
        ('f', 'g', 2),
        ('g', 'h', 1), ('g', 'i', 6),
        ('h', 'i', 7)
    ]

    for origem, destino, peso in arestas_teste:
        g.adicionar_aresta(origem, destino, peso)
        
    print(f"Grafo construído com {len(g.vertices)} vértices.\n")

    # 3. Teste do Algoritmo de Kruskal
    print("--- EXECUTANDO MST-KRUSKAL ---")
    resultado_kruskal = mst_kruskal(g)
    custo_total_kruskal = 0
    
    for u, v, peso in resultado_kruskal:
        print(f"Aresta adicionada: {u} -- {v} (Peso: {peso})")
        custo_total_kruskal += peso
        
    print(f">> Custo Total da MST (Kruskal): {custo_total_kruskal}\n")

    # 4. Teste do Algoritmo de Prim
    print("--- EXECUTANDO MST-PRIM ---")
    raiz_escolhida = 'a'
    print(f"Raiz inicial escolhida: '{raiz_escolhida}'")
    
    resultado_prim = mst_prim(g, raiz_escolhida)
    custo_total_prim = 0
    
    for pai, filho, peso in resultado_prim:
        print(f"Aresta conectada: {pai} -> {filho} (Peso: {peso})")
        custo_total_prim += peso
        
    print(f">> Custo Total da MST (Prim): {custo_total_prim}\n")

    # 5. Validação de Integridade
    print("--- VALIDAÇÃO FINAL ---")
    if custo_total_kruskal == custo_total_prim == 37:
        print("SUCESSO: Ambos os algoritmos encontraram a MST ótima (Custo 37).")
    else:
        print("ALERTA: Divergência nos resultados. Verifique a lógica de extração.")

# Executa a bateria
if __name__ == "__main__":
    executar_testes()      
    


"""
MST-PRIM(G, w, r)
1  for each u ∈ G.V                   // Para cada vértice u no grafo G
2      u.key = ∞                      // Inicializa o peso de conexão com infinito
3      u.pi = NIL                     // Inicializa o predecessor como nulo
4  r.key = 0                          // A raiz r ganha peso 0 para ser a primeira a sair
5  Q = G.V                            // Coloca todos os vértices na Fila de Prioridade Q
6  while Q ≠ ∅                        // Enquanto a fila não estiver vazia
7      u = EXTRACT-MIN(Q)             // Extrai o vértice u com a menor 'key'
8      for each v ∈ G.Adj[u]          // Para cada vizinho v do vértice u extraído
9          if v ∈ Q and w(u, v) < v.key // Se v ainda está na fila E a aresta oferece um custo menor
10             v.pi = u               // Atualiza o pai de v para ser u
11             v.key = w(u, v)        // Atualiza a key de v com o peso dessa nova aresta
"""


# =====================================================================
# REPRESENTAÇÃO VISUAL: CONJUNTOS DISJUNTOS E COMPRESSÃO
# =====================================================================

"""
Conjunto disjuntos serve para entender se u e v estão na mesma árvore ou não
"""

# 1. MAKE-SET (O Início)
# Cada vértice nasce isolado. Ele é o seu próprio representante (pai).
# Rank (altura) de todos é 0.
#
#   [a]      [b]      [c]      [d]

# 2. UNION(a, b) e UNION(c, d)
# O algoritmo elege um para ser o pai do outro.
#
#   [a] (Rank 1)       [c] (Rank 1)
#    |                  |
#   [b] (Rank 0)       [d] (Rank 0)

# 3. UNION(a, c) (União por Rank)
# Como ambos têm Rank 1, há um empate. Escolhemos [a] como chefe supremo,
# e o Rank de [a] sobe para 2.
#
#         [a] (Rank 2)
#        /   \
#      [b]   [c] (Rank 1)
#             |
#            [d]

# 4. FIND-SET(d) (A Mágica da Compressão de Percurso)
# O algoritmo procura o chefe de [d]. Ele sobe para [c], depois para [a].
# Ao voltar da busca, ele ACHATA a árvore, ligando [d] DIRETAMENTE a [a].
#
#         [a] (Rank 2)
#        / | \
#      [b][c][d]
#
# Futuras buscas por [d] agora custarão tempo O(1)!
# =====================================================================


"""
MAKE-SET(x)
1  x.p = x
2  x.rank = 0

FIND-SET(x)
1  if x ≠ x.p
2      x.p = FIND-SET(x.p)  // A chamada recursiva achata o caminho
3  return x.p

UNION(x, y)
1  LINK(FIND-SET(x), FIND-SET(y))

LINK(x, y)
1  if x.rank > y.rank
2      y.p = x
3  elseif x.rank < y.rank
4      x.p = y
5  else
6      y.p = x
7      x.rank = x.rank + 1




A Autonomia (MAKE-SET): No começo, a cidade a aponta para a (self.pai['a'] = 'a'), e 
a cidade b aponta para b. Cada vértice é o chefe supremo de si mesmo.

A Fusão (UNION): Quando unimos a e b, o código simplesmente subordina um ao outro. 
Ele faz o b apontar para o a (self.pai['b'] = 'a').

O Rastreador (FIND-SET): Como o algoritmo tem certeza se a cidade c e a 
cidade d já fazem parte da mesma árvore? Ele pega a cidade c e vai subindo o dicionário de pais até 
achar o nó raiz (aquele que é pai de si mesmo). Depois, faz o mesmo rastreio para d.

O Veredito: Se a raiz final de c for exatamente a mesma raiz final de d, o código conclui: "Eles pertencem ao mesmo conjunto".


"""

"""
================================================================================
RASTREAMENTO DE MEMÓRIA: KRUSKAL + CONJUNTOS DISJUNTOS (DISJOINT SETS)
================================================================================
Imagine um grafo com quatro vértices (a, b, c, d) e as seguintes arestas já 
ordenadas do menor para o maior peso pelo Kruskal: 
1. (a,b) com peso 1
2. (c,d) com peso 2
3. (b,c) com peso 3
4. (a,d) com peso 4

--------------------------------------------------------------------------------
Passo 0: A Inicialização (O Início da Floresta)
--------------------------------------------------------------------------------
O algoritmo roda o MAKE-SET para cada vértice. Cada cidade é um conjunto 
isolado e chefe de si mesma.

Estado da Memória:
pai  = {'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd'}
rank = {'a': 0,   'b': 0,   'c': 0,   'd': 0}


--------------------------------------------------------------------------------
Passo 1: Avaliando a Aresta (a,b) com peso 1
--------------------------------------------------------------------------------
O Kruskal pergunta à estrutura se pode ligar 'a' e 'b'.
- FIND-SET('a') retorna 'a'.
- FIND-SET('b') retorna 'b'.
Decisão: Chefes diferentes. Não há ciclo. A aresta é ACEITA na MST.
Ação: UNION('a', 'b').
União por Rank: Ambos têm rank 0 (empate). Escolhemos 'a' como chefe, 
subordinamos 'b' e aumentamos o rank de 'a'.

Estado Atualizado:
pai  = {'a': 'a', 'b': 'a', 'c': 'c', 'd': 'd'}  # b agora aponta para a
rank = {'a': 1,   'b': 0,   'c': 0,   'd': 0}


--------------------------------------------------------------------------------
Passo 2: Avaliando a Aresta (c,d) com peso 2
--------------------------------------------------------------------------------
O Kruskal testa a aresta entre 'c' e 'd'.
- FIND-SET('c') retorna 'c'.
- FIND-SET('d') retorna 'd'.
Decisão: Chefes diferentes. Não há ciclo. A aresta é ACEITA na MST.
Ação: UNION('c', 'd').
União por Rank: Ambos têm rank 0 (empate). 'c' vira chefe, 'd' é subordinado.

Estado Atualizado:
pai  = {'a': 'a', 'b': 'a', 'c': 'c', 'd': 'c'}  # d agora aponta para c
rank = {'a': 1,   'b': 0,   'c': 1,   'd': 0}


--------------------------------------------------------------------------------
Passo 3: Avaliando a Aresta (b,c) com peso 3 (Fusão de Grandes Árvores)
--------------------------------------------------------------------------------
O Kruskal tenta ligar 'b' e 'c'.
- FIND-SET('b') vê que o pai de 'b' é 'a'. Retorna 'a'.
- FIND-SET('c') retorna 'c'.
Decisão: Chefes supremos diferentes ('a' e 'c'). A aresta é ACEITA na MST.
Ação: UNION('a', 'c').
União por Rank: Ambos têm rank 1 (empate). 'a' é escolhido como chefe absoluto. 
O pai de 'c' passa a ser 'a', e o rank de 'a' sobe para 2.

Estado Atualizado:
pai  = {'a': 'a', 'b': 'a', 'c': 'a', 'd': 'c'}
rank = {'a': 2,   'b': 0,   'c': 1,   'd': 0}
Nota: A árvore tem três níveis agora: a -> c -> d


--------------------------------------------------------------------------------
Passo 4: Avaliando a Aresta (a,d) com peso 4 (Compressão de Percurso)
--------------------------------------------------------------------------------
O Kruskal tenta ligar 'a' e 'd'.
- FIND-SET('a') retorna 'a'.
- FIND-SET('d') entra em recursão: O pai de 'd' é 'c'. O pai de 'c' é 'a'. Retorna 'a'.
Decisão: Chefes supremos IDÊNTICOS ('a' e 'a'). A aresta criaria um ciclo. REJEITADA.
Ação (Efeito Colateral): A Mágica da Compressão.
Como o FIND-SET teve que subir de d -> c -> a, ele achata a árvore antes de terminar,
atualizando o dicionário para fazer 'd' apontar DIRETAMENTE para 'a'.

Estado Final (Otimizado):
pai  = {'a': 'a', 'b': 'a', 'c': 'a', 'd': 'a'}  # Todos apontam DIRETAMENTE para a raiz
rank = {'a': 2,   'b': 0,   'c': 1,   'd': 0}
================================================================================
"""