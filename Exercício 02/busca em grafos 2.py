'''
GCC218 - 2019/02
Atividade: Segundo exercicio de implementacao
Grupo: Liliana Sabato Teodoro, 14, 201810021
       Rafaela Custodio, 14, 201720376 
       Ruan Basilio, 14, 201720089
Data: 28/09/2019 
'''

'''Classe auxiliar de uma lista para a lista de adjacencia'''
class Lista:
    inicio = None
    fim = None
    
    def adicionaVertice(self, nome):
        if(self.inicio == None):
            self.inicio = Noh(nome)
            self.fim = self.inicio
            return

        novo = Noh(nome)
        self.fim.proximo = novo
        self.fim = novo

'''Classe auxiliar a classe lista para armazenar um no'''
class Noh:
    nome = None
    proximo = None
    relacao = None
    def __init__(self, nome):
        self.nome = nome

'''Classe vertice
        Feita para armazenar informacoes do vertice nome, se ja foi visitado, pai,
        o numero de identificacao do vertice (usado na DFS) e o menor numero de vertices 
        que se atinge com zero ou mais arestas aqui chamado de low'''
class Vertice:
    nome = None
    marcado = None
    anterior = None
    low = None
    num = None

    def __init__(self, nome):
        self.marcado = False
        self.nome = nome

'''Classe lista de adjacencia
        Classe da estrutura principal, possui um dicionario de vertices e uma lista propriamente dita
        o atributo counter foi colocado aqui para ser global na estrutura toda
        por ser a classe principal, nela estao os metodos que adicionam vertices e arestas
        e metodos auxiliares para se obter as ligacoes de um vertice
        os metodos estao todos com nomes sugestivos'''
class ListaAdjacencia:
    listaAdj = None
    vertices = None
    counter = None

    def __init__(self):
        self.listaAdj = {}
        self.vertices = {}
        self.counter = 0
    
    def adicionaVertice(self, nome):
        if(nome in self.vertices):
            return "Item ja inserido"
        
        v = Vertice(nome)
        self.vertices[nome] = v
        self.listaAdj[nome] = Lista()

    def adicionaAresta(self, nomeV1, nomeV2):
        #Grafo direcionado
        self.listaAdj[nomeV1].adicionaVertice(nomeV2)
        #Grafo nao direcionada
        self.listaAdj[nomeV2].adicionaVertice(nomeV1)

    '''Metodo para imprimir o grafo, apenas para debug'''
    def imprime(self):
        for elemento in self.listaAdj:
            print(str(elemento) + ": " + str(self.getVizinhos(elemento)) + "\n")
    
    def saoVizinhos(self, v1, v2):
        if(v1 not in self.listaAdj):
            return False
        if(v2 not in self.listaAdj):
            return False
        if(v2 not in self.listaAdj[v1]):
            return False
        return True

    def getVizinhos(self, v):
        vizinhos = []
        listaVizinhos = self.listaAdj[v]
        viz = listaVizinhos.inicio
        while(viz != None):
            vizinhos.append(viz.nome)
            viz = viz.proximo
        return vizinhos

'''Exercicio 3
        Funcao de resolucao do problema 3, utilizando busca em profundidade"'''
def exercicio3(grafo):
    vertices = grafo.vertices
    cameras = []
    '''Inicio da busca em profundidade'''
    for chave in vertices:
        vertices[chave].marcado = False
        vertices[chave].anterior = None
    for chave in vertices:
        if(not vertices[chave].marcado):
            '''Funcao auxiliar recursiva'''
            buscaProfundidadeRecursivo(grafo, vertices[chave], cameras)
    '''Fim da busca em profundidade'''

    '''Exibindo as cameras encontradas, esse esquema de print funcionou no python 2.7.15+.'''
    print len(cameras),
    print "camera(s) encontrada(s):", 
    for cam in cameras:
        print cam,
    
    '''Outro esquema de print'''
    #print (str (len(cameras)) + " camera(s) encontrada(s) ")
    #for cam in cameras:
    #    print cam

'''Funcao auxiliar recursiva da busca em profundidade, onde coloca em uma lista os pontos em que devem estar as cameras'''
def buscaProfundidadeRecursivo(grafo, verticeAtual, cameras):
    verticeAtual.marcado = True
    grafo.counter+=1
    verticeAtual.low = verticeAtual.num = grafo.counter
    for v in grafo.getVizinhos(verticeAtual.nome):
        if(grafo.vertices[v].marcado == False):
            grafo.vertices[v].anterior = verticeAtual
            buscaProfundidadeRecursivo(grafo, grafo.vertices[v], cameras)
            if(grafo.vertices[v].low >= verticeAtual.num):
                if(verticeAtual.nome not in cameras):
                    cameras.append(verticeAtual.nome)
            verticeAtual.low = min(grafo.vertices[v].low, verticeAtual.low)
        else:
            if(verticeAtual.anterior != v):
                verticeAtual.low = min(verticeAtual.low, grafo.vertices[v].low)

'''Funcao que extrai os valores do arquivo e cria o grafo atraves de uma lista de adjacencia'''
def leGrafo():
    grafo = ListaAdjacencia()
    f = open("grafo.txt")
    qtdVertice = int(f.readline())
    for i in range (qtdVertice):
        linha = f.readline()
        aux = linha.split(" ")
        grafo.adicionaVertice(aux[0].rstrip())
    qtdAresta = int(f.readline())
    for i in range (qtdAresta):
        linha = f.readline()
        aux = linha.split(" ")
        grafo.adicionaAresta(aux[0].rstrip(), aux[1].rstrip())
    f.close()

    exercicio3(grafo)
      
leGrafo()
  