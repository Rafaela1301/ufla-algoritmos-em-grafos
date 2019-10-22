'''
Template de resposta em Python
GCC218 - 2019/02
Atividade: 
Grupo: Rafaela Custodio, 14, 201720376 
       Ruan Basilio, 14, 201720089
Data: 13/09/2019 
'''

'''
Escolha uma das 2 estruturas para implementar seus algoritmos
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
        Feita para armazenar informacoes do vertice nome, se ja foi visitado, pais
        tempo de descoberta e fechamento'''
class Vertice:
    nome = None
    marcado = None
    anterior = None
    tempoAbertura = None
    tempoFechamento = None

    def __init__(self, nome):
        self.marcado = False
        self.nome = nome
        self.anterior = []

'''Classe lista de adjacencia
        Classe da estrutura principal, possui um dicionario de vertices e uma lista propriamente dita
        o atributo tempo foi colocado aqui para ser global na estrutura toda
        por ser a classe principal, nela estao os metodos que adicionam vertices e arestas
        e metodos auxiliares para se obter as ligacoes de um vertice
        os metodos estao todos com nomes sugestivos'''
class ListaAdjacencia:
    listaAdj = None
    vertices = None
    tempo = None

    def __init__(self):
        self.listaAdj = {}
        self.vertices = {}
        self.tempo = 0
    
    def adicionaVertice(self, nome):
        if(nome in self.vertices):
            return "Item ja inserido"
        
        v = Vertice(nome)
        self.vertices[nome] = v
        self.listaAdj[nome] = Lista()

    def adicionaAresta(self, nomeV1, nomeV2):
        #Grafo direcionado
        self.listaAdj[nomeV1].adicionaVertice(nomeV2)

    '''Metodo para imprimir o grafo, apenas para debug'''
    def imprime(self):
        for elemento in self.listaAdj:
            print(str(elemento) + ": " + str(self.listaAdj[elemento]) + "\n")
    
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

'''Primeira abordagem
        Funcao da primeira abordagem do problema, foi utilizado nessa solucao busca em largura
        a ideia implementada foi na verificacao do caminho feito pelo grafo e em um vetor de "pais"
        que cada vertice possui, a busca em largura esta implementada nessa propria funcao
    '''
def abordagem1(grafo):
    vertices = grafo.vertices
    '''Inicio da busca em largura utilizando uma fila'''
    for chave in vertices:
        vertices[chave].marcado = False
        vertices[chave].anterior = []
    c = list(vertices.keys())[0]
    caminho = []
    flag = False
    caminho.append(c)
    fila = [c]
    while(len(fila) > 0):
        atual = fila.pop(0)
        vizinhos = grafo.getVizinhos(atual)
        if(vizinhos != []):
            for elemento in vizinhos:
                if(not vertices[elemento].marcado):
                    vertices[elemento].marcado = True
                    fila.append(elemento)
                    if(flag == False):
                        caminho.append(elemento)
                if(atual not in vertices[elemento].anterior):
                    vertices[elemento].anterior.append(atual)
        else:
            flag = True
            for chave in vertices:
                if(vertices[chave].marcado == False):
                    fila.append(chave)
                    #break'''
    '''Fim da busca em largura'''

    print("resultado 1: correspondente a abordagem 1")
    for elemento in vertices:
        if(len(vertices[elemento].anterior) == 1 and vertices[elemento].anterior[0] in caminho):
            print "O vertice %s domina o vertice %s" %(vertices[elemento].anterior[0], elemento)
            print "O vertice %s domina ele mesmo" %(elemento)
        elif(elemento in caminho):
            print "O vertice %s domina ele mesmo" %(elemento)
    print "\n"

'''Segunda abordagem
        Funcao da segunda abordagem do problema, nesta solucao foi utilizado busca em profundidade
        a ideia implementada foi em relacao ao caminho feito, os "pais" de um vertice e o tempo de
        fechamento dos ligantes do vertice em relacao vertice em si, a busca em profundidade esta implementada
        nessa propria funcao com uma funcao auxiliar que seria o "DFS-VISIT"'''
def abordagem2(grafo):
    vertices = grafo.vertices
    caminho = []
    verifica = False
    alcance = []
    '''Inicio da busca em profundidade'''
    for chave in vertices:
        vertices[chave].marcado = False
        vertices[chave].anterior = []
        vertices[chave].tempoAbertura = None
        vertices[chave].tempoFechamento = None
    for chave in vertices:
        if(not vertices[chave].marcado):
            if(verifica == False):
                '''Funcao auxiliar recursiva'''
                buscaProfundidadeRecursivo(grafo, vertices[chave], caminho)
                for i in caminho:
                    alcance.append(i)
                verifica = True
            else:
                buscaProfundidadeRecursivo(grafo, vertices[chave], caminho)
    '''Fim da busca em profundidade'''

    dominante = None
    print("resultado 2: correspondente a abordagem 2")
    for u in vertices:
        flag = True
        for v in vertices[u].anterior:
            if(v.tempoAbertura > vertices[u].tempoFechamento):
                flag = False
            if(v.tempoAbertura < vertices[u].tempoAbertura and v.tempoFechamento > vertices[u].tempoFechamento):
                dominante = v.nome
        if(vertices[u].nome in alcance):
            print "O vertice %s domina ele mesmo" %(u)
        if(flag == True and dominante != None and dominante in alcance):
            print "O vertice %s domina o vertice %s " %(dominante, u)
    print "\n"

'''Funcao auxiliar recursiva da busca em profundidade chamada pela abordagem 2'''
def buscaProfundidadeRecursivo(grafo, verticeAtual, caminho):
    caminho.append(verticeAtual.nome)
    grafo.tempo = grafo.tempo + 1
    verticeAtual.tempoAbertura = grafo.tempo
    verticeAtual.marcado = True
    for v in grafo.getVizinhos(verticeAtual.nome):
        grafo.vertices[v].anterior.append(verticeAtual)
        if(grafo.vertices[v].marcado == False):
            buscaProfundidadeRecursivo(grafo, grafo.vertices[v], caminho)
    grafo.tempo = grafo. tempo + 1
    verticeAtual.tempoFechamento = grafo.tempo

'''Funcao que extrai os valores do arquivo e cria o grafo atraves de uma lista de adjacencia'''
def leGrafo():
    grafo = ListaAdjacencia()
    f = open("ativ1_instance.txt")
    qtd = int(f.readline())
    for i in range (qtd):
        linha = f.readline()
        aux = linha.split(" ")
        tam = len(aux)
        grafo.adicionaVertice(aux[0].rstrip())
        for j in range (1, tam):
            if(aux[j] != '-'):
                grafo.adicionaAresta(aux[0], aux[j].rstrip())
    f.close()
    abordagem1(grafo)
    abordagem2(grafo)
      
leGrafo()
  