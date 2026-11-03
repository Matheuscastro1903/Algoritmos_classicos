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

import math
from collections import deque
from typing import Dict, List, Optional, Tuple


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
    self.vertices={}
    # O array principal de Listas de Adjacência (id -> lista de tuplas (Vertice Destino, Peso))
    self.Adj= {}

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

  def floyd_warshall(self,):
    """Executa o algoritmo de Floyd-Warshall utilizando a estrutura orientada a objetos.

    Retorna:
        - D: Dicionário 2D de menores distâncias (u_id -> v_id -> float)
        - Pi: Dicionário 2D de predecessores mapeando diretamente para objetos
        Vertice
    """
    nodos = list(self.vertices.keys())
    INF = math.inf

    # 1. Construção das Matrizes D^0 e Π^0 dinâmicas por ID dos Vértices
    D: Dict[any, Dict[any, float]] = {
        u: {v: INF for v in nodos} for u in nodos
    }
    Pi: Dict[any, Dict[any, Optional[Vertice]]] = {
        u: {v: None for v in nodos} for u in nodos
    }

    # Distância de um nó para ele mesmo é sempre zero
    for u in nodos:
      D[u][u] = 0.0

    # Preenchimento das arestas diretas a partir de self.Adj
    for u in nodos:
      for vertice_v, peso in self.Adj[u]:
        v = vertice_v.id
        if peso < D[u][v]:  # Trata arestas múltiplas mantendo o menor peso
          D[u][v] = float(peso)
          Pi[u][v] = self.vertices[u]

    # 2. Laços Tríplices de Programação Dinâmica Bottom-Up (k, i, j)
    for k in nodos:
      for i in nodos:
        for j in nodos:
          if D[i][k] < INF and D[k][j] < INF:
            if D[i][k] + D[k][j] < D[i][j]:
              D[i][j] = D[i][k] + D[k][j]
              # Na relaxação de Floyd-Warshall, o predecessor de j passa a ser
              # o predecessor de j vindo do caminho que passa por k
              Pi[i][j] = Pi[k][j]

    # 3. Verificação de Ciclos de Peso Negativo
    for v in nodos:
      if D[v][v] < 0:
        raise ValueError(
            f"Ciclo de peso negativo detectado envolvendo o vértice '{v}'."
        )

    return D, Pi

  def reconstruir_caminho(self,u_id,v_id,Pi,) :
    """Reconstrói o caminho mínimo da origem 'u_id' até o destino 'v_id'

    retornando a sequência exata de objetos Vertice.
    """
    if u_id not in self.vertices or v_id not in self.vertices:
      return []
    if u_id == v_id:
      return [self.vertices[u_id]]
    if Pi[u_id][v_id] is None:
      return []

    caminho = [self.vertices[v_id]]
    atual_id = v_id

    while atual_id != u_id:
      pred_vertice = Pi[u_id][atual_id]
      if pred_vertice is None:
        return []
      atual_id = pred_vertice.id
      caminho.append(pred_vertice)

    caminho.reverse()
    return caminho

  def imprimir_matrizes(
      self,
      D: Dict[any, Dict[any, float]],
      Pi: Dict[any, Dict[any, Optional[Vertice]]],
  ):
    """Exibe as matrizes D e Π formatadas no console."""
    nodos = list(self.vertices.keys())

    print("\n--- MATRIZ DE DISTÂNCIAS (D) ---")
    header = f"{'':>8}" + "".join([f"{str(v):>8}" for v in nodos])
    print(header)
    for u in nodos:
      linha = f"{str(u):>8}"
      for v in nodos:
        val = D[u][v]
        str_val = "inf" if val == math.inf else f"{val:.1f}"
        linha += f"{str_val:>8}"
      print(linha)

    print("\n--- MATRIZ DE PREDECESSORES (Π) ---")
    print(header)
    for u in nodos:
      linha = f"{str(u):>8}"
      for v in nodos:
        vert = Pi[u][v]
        str_val = f"V({vert.id})" if vert else "NIL"
        linha += f"{str_val:>8}"
      print(linha)


# ==============================================================================
# DEMONSTRAÇÃO DE USO E RECONSTRUÇÃO DE CAMINHOS
# ==============================================================================
if __name__ == "__main__":
    g = Grafo(direcionado=True)

    # Arestas do Grafo de Exemplo
    g.adicionar_aresta(0, 1, 3)
    g.adicionar_aresta(0, 3, 7)
    g.adicionar_aresta(1, 0, 8)
    g.adicionar_aresta(1, 2, 2)
    g.adicionar_aresta(2, 0, 5)
    g.adicionar_aresta(2, 3, 1)
    g.adicionar_aresta(3, 0, 2)

    # Execução do Algoritmo
    D, Pi = g.floyd_warshall()

    # Exibição Formatada
    g.imprimir_matrizes(D, Pi)

    # Consulta e Reconstrução de Caminhos
    print("\n--- RECONSTRUÇÃO DE CAMINHOS MINÍMOS ---")
    origem, destino = 1, 3
    caminho_objetos = g.reconstruir_caminho(origem, destino, Pi)
    custo = D[origem][destino]
    
    print(f"Caminho Mínimo de {origem} até {destino}:")
    print(f"  Objetos Vertice: {caminho_objetos}")
    print(f"  Sequência por ID: {' -> '.join([str(v.id) for v in caminho_objetos])}")
    print(f"  Custo Total: {custo}")