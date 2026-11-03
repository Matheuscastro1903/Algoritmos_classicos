from collections import deque


class Vertice:
    def __init__(self, id):
        self.id = id
        self.cor =  'Branco'
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



    def gerar_matriz_pesos_W(self):
        """
        Traduz a lista de adjacências (self.Adj) em uma Matriz W (n x n) 
        para o algoritmo de Múltiplas Fontes.
        """
        n = len(self.vertices)
        
        # Cria um mapeamento de ID do vértice para um índice numérico (0 até n-1)
        # Necessário pois matrizes operam com índices sequenciais rígidos.
        mapa_indices = {v_id: i for i, v_id in enumerate(sorted(self.vertices))}
        
        # Inicializa a matriz W de tamanho n x n preenchida com infinito (ausência de aresta)
        W = [[float('inf')] * n for _ in range(n)]
        
        # Regra 1: A distância de um vértice para ele mesmo é rigorosamente 0
        for i in range(n):
            W[i][i] = 0
            
        # Regra 2: Preenche os custos das arestas existentes
        for u_id, vizinhos in self.Adj.items():
            idx_u = mapa_indices[u_id]
            for vertice_v, peso in vizinhos:
                idx_v = mapa_indices[vertice_v.id]
                
                # Regra de proteção: Se houver arestas paralelas, mantemos a de menor peso
                W[idx_u][idx_v] = min(W[idx_u][idx_v], peso)
                
        return W, mapa_indices

    def extend_shortest_paths(self, L, W):
        """
        Gera uma nova matriz de distâncias (L_linha) cruzando as distâncias 
        já conhecidas (L) com os pesos originais do grafo (W).
        Custo Operacional: Θ(n^3)
        """
        n = len(L)
        
        # Linha 2: Cria a nova matriz L' preenchida inteiramente com infinito
        L_linha = [[float('inf')] * n for _ in range(n)]
        
        # Linhas 3 e 4: Seleciona a Origem (i) e o Destino (j)
        for i in range(n):
            for j in range(n):
                
                # Linha 6: Testa todos os vértices intermediários (k) como escalas
                for k in range(n):
                    
                    # Linha 7: A Equação de Recorrência
                    # L_linha[i][j] guarda o melhor recorde descoberto até agora
                    # L[i][k] + W[k][j] é a tentativa de rota passando por 'k'
                    nova_rota = L[i][k] + W[k][j]
                    
                    if nova_rota < L_linha[i][j]:
                        L_linha[i][j] = nova_rota
                        
        return L_linha


    def faster_all_pairs_shortest_paths(self):
        """
        Calcula o caminho mais curto entre todos os pares de vértices 
        utilizando Programação Dinâmica com Exponenciação Sucessiva.
        Custo Operacional: Θ(V^3 lg V)
        """
        # 1. Extrai a planta baixa estática (W) e o tradutor de IDs
        W, mapa_indices = self.gerar_matriz_pesos_W()
        n = len(W)
        
        # 2. Inicializa a memória dinâmica (L) com as conexões diretas (1 aresta)
        L = W
        m = 1
        
        # 3. O motor de dobragem logarítmica
        # O limite n - 1 representa o maior caminho simples possível no grafo
        while m < n - 1:
            # Cruza a matriz com ela mesma para dobrar o raio de busca
            L = self.extend_shortest_paths(L, L)
            m = 2 * m
            
        return L, mapa_indices



# ==============================================================================
# BATERIA DE TESTES - CAMINHOS MAIS CURTOS COM MÚLTIPLAS FONTES (AULA 08)
# ==============================================================================

def executar_testes_multiplas_fontes():
    print("="*65)
    print("TESTE: FASTER-ALL-PAIRS-SHORTEST-PATHS (Múltiplas Fontes)")
    print("="*65)
    
    # 1. Instanciando o Grafo Direcionado
    g_multi = Grafo(direcionado=True)
    
    # 2. Inserindo as arestas exatas do Slide 26 da Aula 08
    # O formato é (Origem, Destino, Peso)
    arestas_slide_26 = [
        (1, 2, 3), (1, 3, 8), (1, 5, -4),
        (2, 4, 1), (2, 5, 7),
        (3, 2, 4),
        (4, 1, 2), (4, 3, -5),
        (5, 4, 6)
    ]
    
    # Adaptação para suportar o peso na adição.
    # Certifique-se de que a sua função 'adicionar_aresta' esteja aceitando o 3º parâmetro
    # e guardando-o na lista de adjacência, ex: self.Adj[u].append((vertice_v, peso))
    for origem, destino, peso in arestas_slide_26:
        g_multi.adicionar_aresta(origem, destino, peso)
        
    print(f"Grafo construído com {len(g_multi.vertices)} vértices (Cenário do Slide 26).")
    
    # 3. Execução do Motor de Exponenciação Sucessiva
    print("\n--- EXECUTANDO O ALGORITMO (DOBRAGEM LOGARÍTMICA) ---")
    try:
        # Chama a função que implementamos no Módulo 5
        L_final, mapa_indices = g_multi.faster_all_pairs_shortest_paths()
        
        # 4. Formatação e Impressão Visual da Matriz de Distâncias
        print("\nMatriz Final de Distâncias D (ou L^(4)):")
        
        # Inverte o mapa de índices para imprimir os IDs originais corretamente nas colunas
        mapa_reverso = {indice: v_id for v_id, indice in mapa_indices.items()}
        n = len(L_final)
        
        # Imprime o cabeçalho das colunas
        cabecalho = "      " + "".join([f"[{mapa_reverso[j]}]   " for j in range(n)])
        print(cabecalho)
        
        # Imprime cada linha com o respectivo ID do vértice
        for i in range(n):
            linha_formatada = f"[{mapa_reverso[i]}] | "
            for j in range(n):
                valor = L_final[i][j]
                if valor == float('inf'):
                    linha_formatada += "  ∞   "
                else:
                    linha_formatada += f"{valor:>3}   "
            print(linha_formatada)
            
        print("\nSUCESSO: Compare os valores impressos acima com o Slide 26!")
        print("Os resultados da primeira linha devem ser: 0, 1, -3, 2, -4")
        
    except AttributeError as e:
        print(f"\nERRO DE INTEGRAÇÃO: {e}")
        print("Certifique-se de que as funções 'gerar_matriz_pesos_W', 'extend_shortest_paths' e 'faster_all_pairs_shortest_paths' foram inseridas dentro da classe Grafo.")

# Substitua a chamada no bloco main para testar apenas as Múltiplas Fontes
if __name__ == "__main__":
    executar_testes_multiplas_fontes()



"""
EXTEND-SHORTEST-PATHS(L, W)
1  n = L.rows
2  let L' = (l'_{ij}) be a new n × n matrix
3  for i = 1 to n
4      for j = 1 to n
5          l'_{ij} = ∞
6          for k = 1 to n
7              l'_{ij} = min(l'_{ij}, l_{ik} + w_{kj})
8  return L'

"""

# =====================================================================
# OBJETIVO: Calcular o melhor caminho do vértice 1 (Origem i) 
# para o vértice 3 (Destino j). 
# A variável 'k' representa as CIDADES INTERMEDIÁRIAS (Escalas).
# =====================================================================
# Estamos na linha 7 do pseudocódigo. O laço 'k' testará todas as 
# conexões possíveis para fechar a viagem.

# k = 1 (Usando a própria origem como escala)
# Custo = L[1][1] (Custo zero) + W[1][3] (Voo direto de 1 para 3)
# l'_{13} = min(∞, 0 + 8) = 8. (Novo recorde salvo: 8)

# k = 2 (Fazendo escala na cidade 2)
# Custo = L[1][2] (Custo guardado para chegar em 2) + W[2][3] (Voo 2->3)
# Digamos que L[1][2] custe 3 e W[2][3] custe -4. Total = -1.
# l'_{13} = min(8, 3 + -4) = -1. (Novo recorde salvo: -1)

# k = 3 (Usando o próprio destino como escala)
# Custo = L[1][3] (Custo guardado) + W[3][3] (Custo zero)
# l'_{13} = min(-1, 8 + 0) = -1. (O recorde de -1 é mantido)

# RESULTADO FINAL DO LAÇO k: 
# A célula L'[1][3] recebe definitivamente o valor -1, pois a rede 
# descobriu que fazer a escala em k=2 é matematicamente o melhor atalho.
# =====================================================================


"""
FASTER-ALL-PAIRS-SHORTEST-PATHS(W)
1  n = W.rows
2  L = W
3  m = 1
4  while m < n - 1
5      L = EXTEND-SHORTEST-PATHS(L, L)
6      m = 2 * m
7  return L
"""

