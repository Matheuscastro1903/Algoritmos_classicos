# ==============================================================================
# ALGORITMO DE FLOYD-WARSHALL EM PROGRAMAÇÃO ORIENTADA A OBJETOS (POO)
# ==============================================================================
# Contexto Acadêmico: Fundamentos de Problemas Computacionais II (UFRPE)
# Adaptado para a estrutura de classes Vertice e Grafo
# Autor: Matheus de Castro Pécora
#
# ------------------------------------------------------------------------------
# 1. PSEUDOCÓDIGO ADAPTADO PARA POO
# ------------------------------------------------------------------------------
#
# FLOYD_WARSHALL_POO(Grafo G):
# 1.  Vértices = G.vertices.keys()
# 2.  Inicializar Matriz D: D[u][v] = 0 se u == v, peso(u, v) se existe aresta, ∞ caso contrário
# 3.  Inicializar Matriz Π: Π[u][v] = objeto Vertice(u) se u ≠ v e D[u][v] < ∞, None caso contrário
# 4.  Para cada k em Vértices faça:
# 5.      Para cada i em Vértices faça:
# 6.          Para cada j em Vértices faça:
# 7.              se D[i][k] + D[k][j] < D[i][j] então:
# 8.                  D[i][j] = D[i][k] + D[k][j]
# 9.                  Π[i][j] = Π[k][j]  # O predecessor de j no caminho a partir de k
# 10. Para cada v em Vértices faça:
# 11.     se D[v][v] < 0 então:
# 12.         Lançar Exceção ("Ciclo de peso negativo detectado")
# 13. Retornar D, Π
#
# ------------------------------------------------------------------------------
# 2. REPRESENTAÇÃO DO GRAFO DE EXEMPLO (ASCII ART)
# ------------------------------------------------------------------------------
#
# Grafo Orientado Ponderado G = (V, E) com V = {0, 1, 2, 3}:
#
#         (3)
#     0 -------> 1
#    ^ |        / |
#   /  | (7)   /  |
# (2)  |   (8)/   | (2)
# /    v  <--/    v
# 3 <--- 2 <------
#   <---   (1)
#    (5) [aresta 2 -> 0]
#
# ------------------------------------------------------------------------------
# 3. PASSO A PASSO DA INTERAÇÃO (TRACE DAS MATRIZES D E Π POR ID)
# ------------------------------------------------------------------------------
#
# MATRIZES INICIAIS (k = 0 permitindo 0 intermediários):
# D^(0):
#         0      1      2      3
#   0 [ 0.0,   3.0,   inf,   7.0 ]
#   1 [ 8.0,   0.0,   2.0,   inf ]
#   2 [ 5.0,   inf,   0.0,   1.0 ]
#   3 [ 2.0,   inf,   inf,   0.0 ]
#
# Π^(0) (Armazena instâncias de Vertice):
#         0      1      2      3
#   0 [ None,   V(0),  None,  V(0) ]
#   1 [ V(1),   None,  V(1),  None ]
#   2 [ V(2),   None,  None,  V(2) ]
#   3 [ V(3),   None,  None,  None ]
#
# ------------------------------------------------------------------------------
# ITERAÇÃO k = 0 (Pivô: Vertice 0):
# Updates:
#   - D[1][3] = min(inf, D[1][0] + D[0][3] = 8 + 7 = 15) -> Π[1][3] = V(0)
#   - D[2][1] = min(inf, D[2][0] + D[0][1] = 5 + 3 = 8)  -> Π[2][1] = V(0)
#   - D[3][1] = min(inf, D[3][0] + D[0][1] = 2 + 3 = 5)  -> Π[3][1] = V(0)
#
# ------------------------------------------------------------------------------
# ITERAÇÃO k = 1 (Pivô: Vertice 1):
# Updates:
#   - D[0][2] = min(inf, D[0][1] + D[1][2] = 3 + 2 = 5)  -> Π[0][2] = V(1)
#   - D[3][2] = min(inf, D[3][1] + D[1][2] = 5 + 2 = 7)  -> Π[3][2] = V(1)
#
# ------------------------------------------------------------------------------
# ITERAÇÃO k = 2 (Pivô: Vertice 2):
# Updates:
#   - D[0][3] = min(7.0, D[0][2] + D[2][3] = 5 + 1 = 6)  -> Π[0][3] = V(2)
#   - D[1][0] = min(8.0, D[1][2] + D[2][0] = 2 + 5 = 7)  -> Π[1][0] = V(2)
#   - D[1][3] = min(15.0, D[1][2] + D[2][3] = 2 + 1 = 3) -> Π[1][3] = V(2)
#
# ------------------------------------------------------------------------------
# ITERAÇÃO k = 3 (Pivô: Vertice 3):
# Updates:
#   - D[1][0] = min(7.0, D[1][3] + D[3][0] = 3 + 2 = 5)  -> Π[1][0] = V(3)
#   - D[2][0] = min(5.0, D[2][3] + D[3][0] = 1 + 2 = 3)  -> Π[2][0] = V(3)
#   - D[2][1] = min(8.0, D[2][3] + D[3][1] = 1 + 5 = 6)  -> Π[2][1] = V(0)
#
# MATRIZ FINAL D:
#         0      1      2      3
#   0 [ 0.0,   3.0,   5.0,   6.0 ]
#   1 [ 5.0,   0.0,   2.0,   3.0 ]
#   2 [ 3.0,   6.0,   0.0,   1.0 ]
#   3 [ 2.0,   5.0,   7.0,   0.0 ]
#
# MATRIZ FINAL Π (Exibidos os IDs dos Vértices):
#         0      1      2      3
#   0 [ None,   V(0),  V(1),  V(2) ]
#   1 [ V(3),   None,  V(1),  V(2) ]
#   2 [ V(3),   V(0),  None,  V(2) ]
#   3 [ V(3),   V(0),  V(1),  None ]
# ==============================================================================

INF = float('inf')


class Vertice:

  def __init__(self, id):
    self.id = id
    self.cor = 'Branco'
    self.pi = None
    self.d = None
    self.f = None

  def __repr__(self) -> str:
    return f'Vertice({self.id})'


class Grafo:

  def __init__(self, direcionado=True):
    self.direcionado = direcionado

    # Armazena os objetos Vertice instanciados por chave e valor (id -> objeto Vertice)
    self.vertices = {}
    # O array principal de Listas de Adjacência (id -> lista de tuplas (Vertice Destino, Peso))
    self.Adj = {}

  def adicionar_vertice(self, id):
    """Instancia e registra um vértice no grafo caso ele não exista."""
    if id not in self.vertices:
      novo_vertice = Vertice(id)
      self.vertices[id] = novo_vertice
      self.Adj[id] = []  # Cria a gaveta (lista vazia) para as futuras conexões

  def adicionar_aresta(self, u, v, peso):
    """Cria uma conexão ponderada saindo de 'u' e chegando em 'v'."""
    self.adicionar_vertice(u)
    self.adicionar_vertice(v)

    vertice_u = self.vertices[u]
    vertice_v = self.vertices[v]

    # A lista de adjacência guarda uma TUPLA (Objeto Destino, Peso)
    self.Adj[u].append((vertice_v, peso))

    if not self.direcionado:
      self.Adj[v].append((vertice_u, peso))

  # ------------------------------------------------------------------
  # FLOYD-WARSHALL (programação dinâmica, todos os pares, Θ(V³))
  # ------------------------------------------------------------------

  def gerar_matriz_pesos_W(self):
    """
    Traduz a lista de adjacências (self.Adj) em uma Matriz W (n x n)
    para o algoritmo de Múltiplas Fontes.

    Retorna:
        W     -> matriz de pesos (n x n)
        ordem -> lista de IDs em ordem crescente (ordem[i] = id do índice i)
    """
    n = len(self.Adj)

    # Mapeamento interno ID -> índice (0..n-1), necessário para indexar a matriz
    mapa_indices = {}

    # Lista ordenada de IDs: ordem[i] devolve o ID correspondente ao índice i
    ordem = sorted(self.Adj)

    for i, v_id in enumerate(ordem):
        mapa_indices[v_id] = i

    # Inicializa a matriz W (n x n) preenchida com INF (ausência de aresta)
    W = []
    for _ in range(n):
        linha = []
        for _ in range(n):
            linha.append(INF)
        W.append(linha)

    # Regra 1: distância de um vértice a si mesmo = 0
    for i in range(n):
        W[i][i] = 0

    # Regra 2: preenche os custos das arestas existentes
    # self.Adj.items() devolve pares (id_origem, lista de (Vertice destino, peso))
    for u_id, vizinhos in self.Adj.items():
        idx_u = mapa_indices[u_id]
        for vertice_v, peso in vizinhos:
            idx_v = mapa_indices[vertice_v.id]
            # Proteção contra arestas paralelas: mantém o menor peso
            W[idx_u][idx_v] = min(W[idx_u][idx_v], peso)

    return W, ordem

  def floyd_warshall(self):
    """
    Calcula o menor caminho entre TODOS os pares de vértices.

    Retorna (D, Pi), ambos indexados por id:
      D[u][v]  -> peso do menor caminho de u até v (INF se v é inalcançável)
      Pi[u][v] -> predecessor de v no menor caminho que começa em u (None se u == v
                  ou se não há caminho)

    Levanta ValueError se o grafo contiver ciclo de peso negativo.
    """
    W, ordem = self.gerar_matriz_pesos_W()
    #lê a quantidade de vértices que tem
    n = len(ordem)

    # D^(0) = W (cópia: não alteramos W)
    #D vira uma cópia de W
    D = []
    for linha in W:
        D.append(linha[:])

    #constroi a matriz de predecessores colocando none em todos
    Pi = []
    for _ in range(n):
        linha = []
        for _ in range(n):
            linha.append(None)
        Pi.append(linha)



    for i in range(n):
      for j in range(n):
        #caso i seja diferente de j e a conexão for infinita então o pai de ij é i
        if i != j and W[i][j] < INF:
          Pi[i][j] = i


    # k PRECISA ser o laço mais externo: libera o vértice k como intermediário
    for k in range(n):
      for i in range(n):
        #caso não exista caminho entre i-->k
        if D[i][k] == INF:  # poda: sem caminho i -> k, o Caso B nunca ajuda
          continue
        for j in range(n):
          #caso não exista caminho entre k-->j
          if D[k][j] == INF:  # evita somar com infinito
            continue
          nova = D[i][k] + D[k][j]  # Caso B: passar por k
          #se o valor usando K for menor,entra no caso B
          #Caso contrário não entra no if,indo para o caso a(o que seria o else)
          if nova < D[i][j]:       
            D[i][j] = nova
            Pi[i][j] = Pi[k][j]  #herda o predecessor do trecho k ~> j

    # Ciclo negativo: algum vértice consegue chegar em si mesmo com custo < 0
    if any(D[i][i] < 0 for i in range(n)):
      raise ValueError("O grafo contém ciclo de peso negativo")

    # Converte índices em ids para o usuário não precisar conhecer a 'ordem'
    D_id = {}
    for i in range(n):
        id_i = ordem[i]
        linha_id = {}
        for j in range(n):
            id_j = ordem[j]
            linha_id[id_j] = D[i][j]
        D_id[id_i] = linha_id


    Pi_id = {}
    for i in range(n):
        id_i = ordem[i]
        linha_id = {}
        for j in range(n):
            id_j = ordem[j]
            pred = Pi[i][j]
            if pred is not None:
                linha_id[id_j] = ordem[pred]
            else:
                linha_id[id_j] = None
        Pi_id[id_i] = linha_id

    return D_id, Pi_id

  @staticmethod
  def reconstruir_caminho(Pi, u, v):
    """
    Reconstrói o menor caminho u -> v a partir da matriz de predecessores.
    Retorna a lista de ids [u, ..., v], ou None se não existe caminho.
    (Versão iterativa do PRINT-ALL-PAIRS-SHORTEST-PATH.)
    """
    if u == v:
      return [u]
    if Pi[u][v] is None:
      return None

    caminho = [v]
    atual = v
    while atual != u:
      atual = Pi[u][atual]
      caminho.append(atual)
    caminho.reverse()
    return caminho


if __name__ == '__main__':

  # ---------------------------------------------------------------
  # TESTE 1: grafo possível de executar (tem arestas negativas, mas NÃO tem ciclo negativo)
  # ---------------------------------------------------------------
  print('=== TESTE 1: grafo sem ciclo negativo ===')
  g1 = Grafo(direcionado=True)
  for u, v, w in [(1, 2, 3), (1, 3, 8), (1, 5, -4), (2, 4, 1), (2, 5, 7),
                  (3, 2, 4), (4, 1, 2), (4, 3, -5), (5, 4, 6)]:
    g1.adicionar_aresta(u, v, w)

  try:
    D, Pi = g1.floyd_warshall()
    for u in sorted(D):
      print(f'  de {u}:', [D[u][v] for v in sorted(D[u])])
    print('  Caminho 1 -> 3:', g1.reconstruir_caminho(Pi, 1, 3), '| custo:', D[1][3])
  except ValueError as erro:
    print('  Erro inesperado:', erro)

  # ---------------------------------------------------------------
  # TESTE 2: grafo com ciclo negativo (1 -> 2 -> 3 -> 1 soma -1)
  # ---------------------------------------------------------------
  print('\n=== TESTE 2: grafo com ciclo negativo ===')
  g2 = Grafo(direcionado=True)
  g2.adicionar_aresta(1, 2, 2)
  g2.adicionar_aresta(2, 3, -4)
  g2.adicionar_aresta(3, 1, 1)

  try:
    D, Pi = g2.floyd_warshall()
    print('  Erro: o ciclo negativo não foi detectado!')
  except ValueError as erro:
    print('  Ciclo negativo detectado corretamente:', erro)



# ==============================================================================
# EXPLICAÇÃO DETALHADA DO ALGORITMO DE FLOYD-WARSHALL
# ==============================================================================
#
# OBJETIVO:
#   Encontrar o menor caminho entre TODOS os pares de vértices (All-Pairs Shortest Path)
#   em um grafo ponderado (com suporte a arestas de peso negativo).
#
# COMPLEXIDADE:
#   - Tempo:  Θ(V³) por conta dos três laços aninhados (k, i, j).
#   - Espaço: Θ(V²) para armazenar as matrizes D (custos) e Pi (predecessores).
#
# PRINCIPIO DA PROGRAMAÇÃO DINÂMICA (SUBESTRUTURA ÓTIMA):
#   Qualquer sub-trecho de um menor caminho é, obrigatoriamente, também um menor caminho.
#   A cada iteração do laço externo 'k', liberamos o vértice 'k' como um possível
#   ponto intermediário na rota entre o vértice de origem 'i' e o de destino 'j'.
#
# RECORRÊNCIA E CASOS A vs B:
#   D^(k)[i][j] = min( D^(k-1)[i][j] , D^(k-1)[i][k] + D^(k-1)[k][j] )
#
#   - CASO A (D[i][j]): O menor caminho de i até j NÃO passa por k.
#     O código mantém o valor prévio de D[i][j] se a rota por k não for estritamente menor.
#   - CASO B (nova = D[i][k] + D[k][j]): O menor caminho de i até j PASSA por k.
#     Dividimos a rota em duas metades já otimizadas em etapas anteriores (i ~> k e k ~> j).
#
# POR QUE 'k' DEVE SER O LAÇO MAIS EXTERNO?
#   Para resolver o estado 'k', dependemos das soluções completas do estado 'k-1'.
#   Se 'k' ficasse no laço interno, tentaríamos calcular caminhos usando 'k' sem ter
#   otimizado previamente todas as sub-rotas entre (i ~> k) e (k ~> j).
#
# INICIALIZAÇÃO DA MATRIZ DE PREDECESSORES (Pi):
#   - Caso Base (antes do laço k):
#       if i != j and W[i][j] < INF:
#           Pi[i][j] = i   # Em um salto direto de i -> j, o predecessor de j é i.
#   - Atualização no Relaxamento:
#       Pi[i][j] = Pi[k][j]
#       Não fazemos Pi[i][j] = k pois o trecho de k até j pode conter múltiplos
#       intermediários (k ~> ... ~> j). Devemos herdar o predecessor imediato de j
#       na sub-rota que começou em k.
#
# PODAS DE SEGURANÇA E DESEMPENHO:
#   - if D[i][k] == INF: continue  -> Se i não alcança k, k não serve de ponte.
#   - if D[k][j] == INF: continue  -> Evita somar INF e previne loops inúteis.
#
# DETECÇÃO DE CICLO NEGATIVO:
#   if any(D[i][i] < 0 for i in range(n)): raise ValueError(...)
#   Se a distância de um vértice para ele mesmo ficar menor que zero, existe um
#   circuito fechado com soma de pesos negativa (caminho mínimo tende a -infinito).
#
# ==============================================================================
# RASTREIO PASSO A PASSO DA MATRIZ D (EXEMPLO COM 5 VÉRTICES: 0, 1, 2, 3, 4)
# ==============================================================================
#
# Grafo Inicial:
#   (0) ---2---> (1) ---3---> (2) ---1---> (3) ---4---> (4)
#    |                                                   ^
#    +-----------------------20--------------------------+
#   Aresta direta original (0 -> 2) tem peso 10.
#
# Matriz Inicial D^(0) (Apenas arestas diretas, sem intermediários):
#    i \ j |  0  |  1  |  2  |  3  |  4  |
#   -------+-----+-----+-----+-----+-----+
#      0   |  0  |  2  | 10  | INF | 20  |
#      1   | INF |  0  |  3  | INF | INF |
#      2   | INF | INF |  0  |  1  | INF |
#      3   | INF | INF | INF |  0  |  4  |
#      4   | INF | INF | INF | INF |  0  |
#
# Iteração k = 0: Nenhuma rota é encurtada passando por 0.
#
# Iteração k = 1 (Libera vértice 1 como intermediário):
#   - Teste (0 -> 2) via 1: D[0][1] + D[1][2] = 2 + 3 = 5 < 10 (Caso B vence).
#   Matriz D^(1): D[0][2] passa a ser 5.
#
# Iteração k = 2 (Libera vértice 2 como intermediário - Reutiliza sub-rota D[0][2]=5):
#   - Teste (0 -> 3) via 2: D[0][2] + D[2][3] = 5 + 1 = 6 < INF (Caso B vence).
#   - Teste (1 -> 3) via 2: D[1][2] + D[2][3] = 3 + 1 = 4 < INF (Caso B vence).
#   Matriz D^(2): D[0][3] passa a ser 6; D[1][3] passa a ser 4.
#
# Iteração k = 3 (Libera vértice 3 como intermediário - Reutiliza sub-rota D[0][3]=6):
#   - Teste (0 -> 4) via 3: D[0][3] + D[3][4] = 6 + 4 = 10 < 20 (Caso B vence o atalho de peso 20).
#   - Teste (1 -> 4) via 3: D[1][3] + D[3][4] = 4 + 4 = 8 < INF.
#   - Teste (2 -> 4) via 3: D[2][3] + D[3][4] = 1 + 4 = 5 < INF.
#   Matriz D^(3): D[0][4] vira 10; D[1][4] vira 8; D[2][4] vira 5.
#
# Iteração k = 4: Vértice 4 não tem saídas; matriz D final estabiliza em D^(3).
# ==============================================================================