class Vertice:
    def __init__(self, id):
        self.id = id

    def __repr__(self) -> str:
        return f'Vertice({self.id})'


class Grafo:
    def __init__(self, direcionado=True):
        self.direcionado = direcionado
        self.vertices = {}
        self.Adj = {}

    def adicionar_vertice(self, id):
        if id not in self.vertices:
            self.vertices[id] = Vertice(id)
            self.Adj[id] = []

    def adicionar_aresta(self, u, v, peso=1):
        self.adicionar_vertice(u)
        self.adicionar_vertice(v)
        vertice_u = self.vertices[u]
        vertice_v = self.vertices[v]

        self.Adj[u].append((vertice_v, peso))
        if not self.direcionado:
            self.Adj[v].append((vertice_u, peso))

    # ------------------------------------------------------------------
    # WARSHALL: FECHO TRANSITIVO (Matriz Booleana de Alcançabilidade, Θ(V³))
    # ------------------------------------------------------------------
    def existe_caminho_warshall(self):
        """
        Retorna uma matriz booleana T indexada por IDs de vértices, onde:
            T[u][v] == True  -> Existe ao menos 1 caminho de u até v
            T[u][v] == False -> v é inalcançável a partir de u
        """
        ordem = sorted(self.Adj)
        n = len(ordem)
        mapa_indices = {v_id: i for i, v_id in enumerate(ordem)}

        # 1. INICIALIZAÇÃO DA MATRIZ BOOLEANA T (n x n)
        # Preenche inteiramente com False (sem caminhos conhecidos)
        T = [[False] * n for _ in range(n)]

        # Regra 1: Todo vértice alcança a si mesmo (caminho de comprimento 0)
        for i in range(n):
            T[i][i] = True

        # Regra 2: Arestas diretas existentes passam a ser True
        for u_id, vizinhos in self.Adj.items():
            idx_u = mapa_indices[u_id]
            for vertice_v, _ in vizinhos:
                idx_v = mapa_indices[vertice_v.id]
                T[idx_u][idx_v] = True

        # 2. ALGORITMO DE WARSHALL COM LÓGICA BOOLEANA
        for k in range(n):
            for i in range(n):
                # PODA DE DESEMPENHO: Se i não alcança k, (T[i][k] AND T[k][j]) sempre será False
                if not T[i][k]:
                    continue

                for j in range(n):
                    # CASO A: T[i][j] (Caminho antigo sem k)
                    # CASO B: T[i][k] and T[k][j] (Caminho passando por k)
                    #
                    # Como o 'if not T[i][k]' acima garante que T[i][k] é True,
                    # a expressão: T[i][j] or (T[i][k] and T[k][j])
                    # simplifica para: T[i][j] or T[k][j]
                    T[i][j] = T[i][j] or (T[i][k] and T[k][j])

        # 3. MAPEAMENTO DE VOLTA PARA OS IDS ORIGINAIS
        T_id = {}
        for i in range(n):
            id_i = ordem[i]
            linha_id = {}
            for j in range(n):
                id_j = ordem[j]
                linha_id[id_j] = T[i][j]
            T_id[id_i] = linha_id

        return T_id


if __name__ == '__main__':
    g = Grafo(direcionado=True)

    # 1 -> 2 -> 3 -> 4  e um nó isolado 5
    g.adicionar_aresta(1, 2)
    g.adicionar_aresta(2, 3)
    g.adicionar_aresta(3, 4)
    g.adicionar_vertice(5)

    T = g.existe_caminho_warshall()

    print("=== MATRIZ DE ALCANÇABILIDADE (True/False) ===")
    vertices = sorted(T.keys())
    print("Origem \\ Destino", vertices)
    for u in vertices:
        linha = [1 if T[u][v] else 0 for v in vertices]
        print(f"  Vertice {u}:    ", linha)