import sys
import itertools
from abc import ABC, abstractmethod

class Grafo(ABC):
    @abstractmethod
    def numero_de_vertices(self):
        pass

    @abstractmethod
    def numero_de_arestas(self):
        pass

    @abstractmethod
    def sequencia_de_graus(self):
        pass

    @abstractmethod
    def adicionar_aresta(self, u, v):
        pass

    @abstractmethod
    def remover_aresta(self, u, v):
        pass

    @abstractmethod
    def imprimir(self):
        pass

    #Aula 3 - Atividade 1
    @abstractmethod
    def is_simples(self):
        pass

    @abstractmethod
    def is_nulo(self):
        pass

    @abstractmethod
    def is_completo(self):
        pass

    #Aula 3 - Atividade 2
    @abstractmethod
    def get_vertices(self):
        pass
    
    @abstractmethod
    def get_arestas(self):
        pass

    @abstractmethod
    def is_subgrafo(self, outro_grafo):
        pass

    @abstractmethod
    def is_subgrafo_gerador(self, outro_grafo):
        pass

    @abstractmethod
    def is_subgrafo_induzido(self, outro_grafo):
        pass

    #Aula 3 - Atividade 3
    def _checa_mapeamento_preserva_adjacencia(self, grafo1, grafo2, mapping):
        """
        Verifica se uma dada correspondência (mapping) entre vértices preserva
        a estrutura de adjacência dos grafos.
        """
        # Itera sobre todos os pares possíveis de vértices no primeiro grafo
        arestas_1 = grafo1.get_arestas()
        arestas_2 = grafo2.get_arestas()

        for aresta in arestas_1:
            u1, v1 = aresta
            # Obtém os índices correspondentes no grafo 2
            u2 = mapping[u1]
            v2 = mapping[v1]

            # Verifica se a aresta (u1, v1) no grafo 1 tem uma aresta correspondente (u2, v2) no grafo 2
            if ((u2, v2) not in arestas_2) and ((v2, u2) not in arestas_2):
                return False

        # Se todos os pares preservam a adjacência, a correspondência é válida.
        return True

    def is_isomorfo(self, grafo):
        """
        Verifica se dois grafos são isomorfos usando força 
        bruta com poda por invariantes.
        """
        # --- ETAPA 1: PODA RÁPIDA COM INVARIANTES ---

        # 1. Invariante: Número de Vértices
        if (self.numero_de_vertices() != grafo.numero_de_vertices()):
            return False
                
        # 2. Invariante: Número de Arestas
        if (self.numero_de_arestas() != grafo.numero_de_arestas()):
            return False
                
        # 3. Invariante: Sequência de Graus
        if self.sequencia_de_graus() != grafo.sequencia_de_graus():
            return False

        # --- ETAPA 2: BUSCA EXAUSTIVA (FORÇA BRUTA) ---

        # Se os invariantes passaram, devemos testar as correspondências.
        vertices1 = list(self.get_vertices())
        vertices2 = list(grafo.get_vertices())

        # Gera todas as permutações dos vértices do grafo 2.
        #Ex. [1,2] -> (1,2), (2,1)
        # Cada permutação é uma potencial correspondência para os vértices do grafo 1.
        for p in itertools.permutations(vertices2):
            #Cria o mapeamento dos vértices do grafo 1 para o grafo 2
            #Ex. [A,B] e (1,2), (2,1) -> {A:1, B:2}, {A:2, B:1}
            mapping = dict(zip(vertices1, p))
    
                
            # Verifica se esta correspondência preserva a estrutura de arestas
            if self._checa_mapeamento_preserva_adjacencia(self, grafo, mapping):
                return True
                    
            # Se testou todas as permutações e nenhuma funcionou, eles não são isomorfos.
            return False



class GrafoDenso(Grafo):
    # Definição do grafo
    def __init__(self, num_vertices=None, labels=None):
        if labels:
            self.labels = labels
            self.num_vertices = len(labels)
            self.mapa_labels = {label: i for i, label in enumerate(labels)}
        elif num_vertices:
            self.num_vertices = num_vertices
            self.labels = [str(i) for i in range(num_vertices)]
            self.mapa_labels = {str(i): i for i in range(num_vertices)}
        else:
            print("Erro: Forneça 'num_vertices' ou uma lista de 'labels'.")
            sys.exit(1)

        # Cria a matriz de adjacência NxN preenchida com zeros
        self.matriz = [[0] * self.num_vertices for i in range(self.num_vertices)]
        
    
    def numero_de_vertices(self):
        # Retorna o número total de vértices no grafo.
        return self.num_vertices

    def numero_de_arestas(self):
        # Retorna o número total de arestas no grafo.
        count = 0
        for i in range(self.num_vertices):
            for j in range(i + 1, self.num_vertices):
                if self.matriz[i][j] != 0:
                    count += 1
        return count

    def sequencia_de_graus(self):
        # Retorna uma lista com os graus de todos os vértices.
        return sorted([sum(row) for row in self.matriz])


    def _obter_indice(self, vertice):
        if isinstance(vertice, str) and vertice in self.mapa_labels:
            return self.mapa_labels[vertice]
        elif isinstance(vertice, int) and 0 <= vertice < self.num_vertices:
            return vertice
        else:
            raise ValueError(f"Vértice '{vertice}' é inválido.")


    def adicionar_aresta(self, u, v):
        """
        Adiciona a aresta entre os vértices u e v.
        """
        try:
            idx_u = self._obter_indice(u)
            idx_v = self._obter_indice(v)

            self.matriz[idx_u][idx_v] = 1
            self.matriz[idx_v][idx_u] = 1

            print(f"Aresta adicionada entre {u} e {v}.")
        except ValueError as e:
            print(f"Erro ao adicionar aresta: {e}")


    def remover_aresta(self, u, v):
        """
        Remove a aresta entre os vértices u e v.
        """
        try:
            idx_u = self._obter_indice(u)
            idx_v = self._obter_indice(v)

            if self.matriz[idx_u][idx_v] == 0:
                print(f"Aresta entre {u} e {v} não existe.")
                return

            # Remove a aresta
            self.matriz[idx_u][idx_v] = 0
            self.matriz[idx_v][idx_u] = 0
            print(f"Aresta removida entre {u} e {v}.")
        
        except ValueError as e:
            print(f"Erro ao remover aresta: {e}")

    def imprimir(self):
        """Imprime a matriz de adjacência de forma legível."""
        print("\nMatriz de Adjacência:")
        # Imprime o cabeçalho das colunas
        header = "   " + "  ".join(self.labels)
        print(header)
        print("─" * len(header))

        # Imprime as linhas com seus respectivos rótulos
        for i, linha in enumerate(self.matriz):
            print(f"{self.labels[i]} |", "  ".join(map(str, linha)))
        print()


    #Aula 3 - Atividade 1
    def is_simples(self):
        #Percorre a matriz de adjacência para verificar se há laços 
        for i in range(self.num_vertices):
            if self.matriz[i][i] != 0:
                return False

        return True

    def is_nulo(self):
        if self.numero_de_arestas() == 0 and self.numero_de_vertices() > 0:
            return True
        return False


    def is_completo(self):
        if (self.is_simples()) and (
            self.numero_de_arestas() == (self.numero_de_vertices() *
                                         (self.numero_de_vertices() - 1)) // 2):
            return True
        return False    
    

    #Aula 3 - Atividade 2
    def get_vertices(self):
        return self.labels
    
    def get_arestas(self):
        arestas = []
        for i in range(self.num_vertices):
            for j in range(i + 1, self.num_vertices):
                if self.matriz[i][j] != 0:
                    arestas.append((self.labels[i], self.labels[j]))
        return arestas

    def is_subgrafo(self, outro_grafo):
        if not isinstance(outro_grafo, Grafo):
            raise TypeError("O grafo fornecido deve ser uma instância de Grafo.")

        # Verifica se todos os vértices do grafo atual estão no outro grafo
        for vertice in self.get_vertices():
            if vertice not in outro_grafo.get_vertices():
                return False

        for aresta in self.get_arestas():
            if aresta not in outro_grafo.get_arestas():
                return False
            
        #Compara se as arestas aparecem na mesma quantidade em ambos os grafos
        for aresta in self.get_arestas():
            if self.get_arestas().count(aresta) != outro_grafo.get_arestas().count(aresta):
                return False
            
        # Se todas as arestas e vértices estão presentes, é um subgrafo
        return True
    

    def is_subgrafo_gerador(self, outro_grafo):
        if not isinstance(outro_grafo, Grafo):
            raise TypeError("O grafo fornecido deve ser uma instância de Grafo.")

        if self.is_subgrafo(outro_grafo):
            if (all(vertice in self.get_vertices() for vertice in outro_grafo.get_vertices())):
                return True
            else:
                return False
        else:
            return False

    def is_subgrafo_induzido(self, outro_grafo):
        if not isinstance(outro_grafo, Grafo):
            raise TypeError("O grafo fornecido deve ser uma instância de Grafo.")

        if self.is_subgrafo(outro_grafo):
            lista_arestas = []
            #Filtra apenas as arestas que conectam os vértices do subgrafo
            for aresta in outro_grafo.get_arestas():
                if all(v in self.get_vertices() for v in aresta):
                    lista_arestas.append(aresta)

            for aresta in self.get_arestas():
                if aresta not in lista_arestas:
                    return False
                
            for aresta in outro_grafo.get_arestas():
                if aresta not in self.get_arestas():
                    return False
                
            return True
        else:
            return False
        


   






class GrafoEsparso(Grafo):
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

        # A lista de adjacências é um dicionário onde cada vértice
        # é uma chave e o valor é a lista de seus vizinhos.
        self.lista_adj = {vertice: [] for vertice in self.vertices}

  
    def numero_de_vertices(self):
        # Retorna o número total de vértices no grafo.
        return len(self.vertices)

    def numero_de_arestas(self):
        # Retorna o número total de arestas no grafo.
        return (sum([len(vizinhos) for vizinhos in self.lista_adj.values()]) // 2)


    def sequencia_de_graus(self):
        # Retorna uma lista com os graus de todos os vértices.
        return sorted([len(values) for values in self.lista_adj.values()])


    def _validar_vertice(self, vertice):
        """Método auxiliar para checar se um vértice existe no grafo."""
        if vertice not in self.lista_adj:
            raise ValueError(f"Vértice '{vertice}' não existe no grafo.")
        return True

    # (ii) Adição de arestas
    def adicionar_aresta(self, u, v):
        try:
            self._validar_vertice(u)
            self._validar_vertice(v)

            # Pode adicionar aresta duplicada ou laço (loop)
            self.lista_adj[u].append(v)
            self.lista_adj[v].append(u)
 
            print(f"Aresta adicionada entre {u} e {v}")
        except ValueError as e:
            print(f"Erro ao adicionar aresta: {e}")


    # (v) Remoção de arestas
    def remover_aresta(self, u, v, peso=None):
        """
        Se existir mais de uma, remove a primeira aresta entre os vértices u e v.
        """
        try:
            self._validar_vertice(u)
            self._validar_vertice(v)

            for index, ver in enumerate(self.lista_adj[u]):
                if v == ver:
                    del self.lista_adj[u][index]
                    print(f"Aresta removida entre {u} e {v}.")
                    break
            else:
                print(f"Aresta entre {u} e {v} não existe.")

            for index, ver in enumerate(self.lista_adj[v]):
                if u == ver:
                    del self.lista_adj[v][index]
                    print(f"Aresta removida entre {v} e {u}.")
                    break
            else:
                print(f"Aresta entre {u} e {v} não existe.")

        except ValueError as e:
            print(f"Erro ao remover aresta: {e}")


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

    #Atividade 1
    def is_simples(self):
        # Verifica se há laços (loops) na lista de adjacências
        for vertice, vizinhos in self.lista_adj.items():
            if vertice in vizinhos:
                return False
        # Verifica se há arestas duplicadas
        for vertice, vizinhos in self.lista_adj.items():
            if len(vizinhos) != len(set(vizinhos)):
                return False
        # Se não houver laços e arestas duplicadas, o grafo é simples
        return True

    def is_nulo(self):
        if self.numero_de_arestas() == 0 and self.numero_de_vertices() > 0:
            return True
        return False


    def is_completo(self):
        if (self.is_simples() and self.numero_de_arestas() == (self.numero_de_vertices() *
                                         (self.numero_de_vertices() - 1)) // 2):
            return True
        return False    
    
    #Atividade 2
    def get_vertices(self):
        return list(self.lista_adj.keys())
    
    def get_arestas(self):
        arestas = []
        for vertice, vizinhos in self.lista_adj.items():
            for vizinho in vizinhos:
                if (vizinho, vertice) not in arestas:
                    arestas.append((vertice, vizinho))
        return arestas
    
    def is_subgrafo(self, outro_grafo):
        if not isinstance(outro_grafo, Grafo):
            raise TypeError("O grafo fornecido deve ser uma instância de Grafo.")

        # Verifica se todos os vértices do grafo atual estão no outro grafo
        for vertice in self.get_vertices():
            if vertice not in outro_grafo.get_vertices():
                return False

        #Verifica se todas as arestas do grafo atual estão no outro grafo
        for aresta in self.get_arestas():
            if aresta not in outro_grafo.get_arestas():
                return False
            
        #Compara se as arestas aparecem na mesma quantidade em ambos os grafos
        for aresta in self.get_arestas():
            if self.get_arestas().count(aresta) != outro_grafo.get_arestas().count(aresta):
                return False

        # Se todas as arestas e vértices estão presentes, é um subgrafo
        return True

    def is_subgrafo_gerador(self, outro_grafo):
        if not isinstance(outro_grafo, Grafo):
            raise TypeError("O grafo fornecido deve ser uma instância de Grafo.")

        if self.is_subgrafo(outro_grafo):
            if (all(vertice in self.get_vertices() for vertice in outro_grafo.get_vertices())):
                return True
            else:
                return False
        else:
            return False

    def is_subgrafo_induzido(self, outro_grafo):
        if not isinstance(outro_grafo, Grafo):
            raise TypeError("O grafo fornecido deve ser uma instância de Grafo.")

        if self.is_subgrafo(outro_grafo):
            lista_arestas = []
            #Filtra apenas as arestas que conectam os vértices do subgrafo
            for aresta in outro_grafo.get_arestas():
                if all(v in self.get_vertices() for v in aresta):
                    lista_arestas.append(aresta)

            for aresta in self.get_arestas():
                if aresta not in lista_arestas:
                    return False
                
            for aresta in outro_grafo.get_arestas():
                if aresta not in self.get_arestas():
                    return False   
            return True
        else:
            return False




if __name__ == "__main__":
    
    vertices_labels = ['A', 'B', 'C', 'D', 'E']
    #g = GrafoDenso(labels=vertices_labels)
    g = GrafoDenso(labels=vertices_labels)
  
    g.adicionar_aresta('A', 'B')
    g.adicionar_aresta('B', 'C')
    g.adicionar_aresta('A', 'C')
    g.adicionar_aresta('C', 'D')
    g.adicionar_aresta('C', 'E')

    vertices_2_labels = ['1', '2', '3', '4', '5']
    g2 = GrafoEsparso(labels=vertices_2_labels)
    g2.adicionar_aresta('1', '2')
    g2.adicionar_aresta('3', '2')
    g2.adicionar_aresta('1', '3')
    g2.adicionar_aresta('3', '4')
    g2.adicionar_aresta('3', '5')


    if (g.is_isomorfo(g2)):
        print("Os grafos são isomorfos.")
    else:
        print("Os grafos não são isomorfos.")

    """
    g.imprimir()
    print(f"Número de vértices: {g.numero_de_vertices()}")
    print(f"Número de arestas: {g.numero_de_arestas()}")
    print(f"Sequência de graus: {g.sequencia_de_graus()}")
    print(f"É nulo: {g.is_nulo()}")
    print(f"É completo: {g.is_completo()}")
    print(f"É simples: {g.is_simples()}")
    print(f"G2  simples: {g2.is_simples()}")
    print(f"É subgrafo: {g2.is_subgrafo(g)}")  # Verifica se é subgrafo de si mesmo
    print(f"É subgrafo gerador: {g2.is_subgrafo_gerador(g)}")  # Verifica se é subgrafo de si mesmo
    print(f"É subgrafo induzido: {g2.is_subgrafo_induzido(g)}")  # Verifica se é subgrafo de si mesmo
    print(f"Vértices: {g.get_vertices()}")
    print(f"Arestas: {g.get_arestas()}")

    """


    """"

    vertices_labels = ['A', 'B', 'C', 'D', 'E']
    g = GrafoDenso(labels=vertices_labels)

    print("Grafo inicial criado.")
    g.imprimir()

    # (ii) Adição de arestas
    print("\n--- Adicionando arestas ---")
    g.adicionar_aresta('A', 'B')
    g.adicionar_aresta('A', 'C')
    g.adicionar_aresta('B', 'A')
    g.adicionar_aresta('B', 'E')
    g.adicionar_aresta('C', 'A')
    g.imprimir()
    g.remover_aresta('A', 'C')
    g.imprimir()

    print(g.numero_de_arestas())
  

    g = GrafoDenso(num_vertices=5)
    print("Grafo inicial criado.")
    g.imprimir()
    g.adicionar_aresta(1, 2)
    g.adicionar_aresta(1, 3)
    g.adicionar_aresta(0, 4)
    g.adicionar_aresta(1, 4)
    g.adicionar_aresta(2, 3)
    g.imprimir()
    print(g.numero_de_vertices())
    print(g.numero_de_arestas())
    print(g.sequencia_de_graus())

"""
