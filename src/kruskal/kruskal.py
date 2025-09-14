import sys

class GrafoEsparsoPonderado():
    """
    Implementa as operações básicas de um grafo não orientado
    usando uma LISTA DE ADJACÊNCIAS (implementada com um dicionário).
    """
    # (i) Definição do grafo
    def __init__(self, num_vertices=None, labels=None):

        if labels:
            self.vertices = labels
        elif num_vertices:
            self.vertices = [str(i) for i in range(num_vertices)]
        else:
            print("Erro: Forneça 'num_vertices' ou uma lista de 'labels'.")
            sys.exit(1)

        self.lista_adj = {vertice: [] for vertice in self.vertices}


    # (ii) Adição de arestas
    def adicionar_aresta(self, u, v, peso=1):
        try:
            self._validar_vertice(u)
            self._validar_vertice(v)

            # Pode adicionar aresta duplicada ou laço (loop)
            self.lista_adj[u].append((v, peso))
            self.lista_adj[v].append((u, peso))
 
            print(f"Aresta adicionada entre {u} e {v}")
        except ValueError as e:
            print(f"Erro ao adicionar aresta: {e}")

    def get_vertices(self):
        return list(self.lista_adj.keys())
    
    def get_arestas(self):
        arestas = []
        for vertice, vizinhos in self.lista_adj.items():
            for vizinho, peso in vizinhos:
                if (vizinho, vertice, peso) not in arestas:
                    arestas.append((vertice, vizinho, peso))
        return arestas
    
    def _validar_vertice(self, vertice):
        """Método auxiliar para checar se um vértice existe no grafo."""
        if vertice not in self.lista_adj:
            raise ValueError(f"Vértice '{vertice}' não existe no grafo.")
        return True
    
    def imprimir(self):
        """Imprime a lista de adjacências de forma legível."""
        print("\nLista de Adjacências:")
        if not self.lista_adj:
            print("{}")
            return
        for vertice, vizinhos in self.lista_adj.items():
            # Junta a lista de vizinhos em uma string para impressão
            saida = [vizinho for vizinho in vizinhos]             
            print(f"  {vertice} -> [ {saida} ]")
        print()

class BuscaUniaoSimples():

    def __init__(self, vertices):
        """
        Cada vértice começa como seu próprio "pai" (em seu próprio conjunto).
        """
        self.parent = {v: v for v in vertices}
        print(self.parent)

    def find(self, v):
        """
        Encontra a raiz do conjunto ao qual 'v' pertence.
        Faz isso simplesmente seguindo os ponteiros de "pai" até o topo
        """
        root = v
        while self.parent[root] != root:
            root = self.parent[root]
        return root

    def union(self, u, v):
        """
        Une os conjuntos de 'u' e 'v' de forma arbitrária.
        """
        root_u = self.find(u)
        root_v = self.find(v)

        # Se não estiverem no mesmo conjunto, une os dois
        if root_u != root_v:
            # Simplesmente faz a raiz de um apontar para a raiz do outro
            self.parent[root_v] = root_u
            return True
        return False

class BuscaUniaoSimples():

    def __init__(self, vertices):
        """
        Cada vértice começa como seu próprio "pai" (em seu próprio conjunto).
        """
        self.parent = {v: v for v in vertices}
        print(self.parent)

    def find(self, v):
        """
        Encontra a raiz do conjunto ao qual 'v' pertence.
        Faz isso simplesmente seguindo os ponteiros de "pai" até o topo
        """
        root = ''
        return root

    def union(self, u, v):
        """
        Une os conjuntos de 'u' e 'v' de forma arbitrária.
        """
        root_u = self.find(u)
        root_v = self.find(v)

        # Se não estiverem no mesmo conjunto, une os dois


def kruskal(grafo:GrafoEsparsoPonderado):

    # 1. Ordena as arestas pelo peso
   

    # 2. Inicializa a estrutura BuscaUniaoSimples
    uf = BuscaUniaoSimples(grafo.get_vertices())

    minimum_spanning_tree = []
    total_weight = 0
        
    # 3. Itera sobre as arestas ordenadas
    for u, v, weight in sorted_edges:
        # 4. Se adicionar a aresta não formar um ciclo...
        #    (ou seja, se u e v estiverem em conjuntos diferentes)
        if :
            # ...une os conjuntos e adiciona a aresta à árvore.

            
    return minimum_spanning_tree, total_weight
 

if __name__ == "__main__":
    vertices_exemplo = ['A', 'B', 'C', 'D', 'E']
    grafo = GrafoEsparsoPonderado(labels=vertices_exemplo)
    grafo.adicionar_aresta('A', 'B', 3)
    grafo.adicionar_aresta('A', 'D', 1)
    grafo.adicionar_aresta('B', 'C', 5)
    grafo.adicionar_aresta('B', 'D', 4)
    grafo.adicionar_aresta('C', 'E', 2)
    grafo.adicionar_aresta('D', 'E', 6)
    grafo.imprimir()
 

    agm, custo = kruskal(grafo)
    
    print("\nArestas da Árvore Geradora Mínima:")
    for u, v, weight in agm:
        print(f"  - De {u} para {v} com custo {weight}")
            
    print(f"\nCusto Total da Árvore Geradora Mínima: {custo}")

