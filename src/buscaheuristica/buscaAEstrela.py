class BuscaAEstrela(object):

  def __init__(self, vertices):
    self.verticesAbertos = []
    self.verticesFechados = []
    self.vertices = vertices

  def baldiacaoExistente(self, antecessor, v_atual, v_final):
    '''
    Antecessor eh o dicionario que contem os vertices antecessores
    '''
    v_antecessor = antecessor[v_atual.chave]
    if not v_antecessor:
      return False
    aresta_antecessora = self.getAresta(v_antecessor, v_atual)
    aresta_atual = self.getAresta(v_atual, v_final)
    return aresta_antecessora.cor != aresta_atual.cor

  def reconstruirCaminho(self, v_antecessor, v_atual):
    caminho = [v_atual.chave]
    custo = v_atual.f_de_n
    chave_v_atual = v_atual.chave
    while v_antecessor[chave_v_atual]:
      chave_v_atual = v_antecessor[chave_v_atual].chave
      caminho.append(chave_v_atual)
    caminho.reverse() 
    return (caminho, custo)

  def getAllVerticesAdjacentes(self, vertice):
    v_adjacentes = []
    for aresta in vertice.arestas_adj:
      v_adjacentes.append(aresta.v_destino)
    return v_adjacentes

  def getAresta(self, v_inicio, v2_destino):
    for aresta in v_inicio.arestas_adj:
      if aresta.v_destino == v2_destino:
        return aresta

  def calcularDistanciaEntreVertices(self, v_atual, v_adj):
    return self.getAresta(v_atual, v_adj).distancia
  
  
  # Recupar o menor valor de vertice dentre os vertices abertos
  def recuperaMenorF(self):
    menor = self.verticesAbertos[0]
    for v in self.verticesAbertos:
      if v.f_de_n < menor.f_de_n:
        menor = v 
    return menor


  def buscaAEstrela(self, v_inicio, v_final, custo_baldeacao):
    # Inicia pelo primeiro vertice
    self.verticesAbertos.append(v_inicio)
    
    # Para cada vertice, eh salvo o seu antecessor que possui o melhor caminho,
    # caso ele tenha muitos caminhos, v_antecessor indicara o menor caminho
    v_antecessor = {}
    
    # Para cada vertice, a distancia do inicio ate o vertice atual
    distancia_ate_n = {}

    for v in self.vertices:
      v_antecessor[v.chave] = None
      distancia_ate_n[v.chave] = None

    distancia_ate_n[v_inicio.chave] = 0

    v_inicio.f_de_n = v_inicio.h_de_n

    while len(self.verticesAbertos) != 0:
        v_atual = self.recuperaMenorF()
        if v_atual == v_final:
            return self.reconstruirCaminho(v_antecessor, v_atual)

        # Ira remover o vertice atual do grupo de  vertices abertos
        self.verticesAbertos.remove(v_atual) 
        # Ira adicionar o vertice atual ao grupo de vertices fechados
        self.verticesFechados.append(v_atual) 

        for v_adj in self.getAllVerticesAdjacentes(v_atual):
            if v_adj in self.verticesFechados:
                continue

            if v_adj not in self.verticesAbertos:
                self.verticesAbertos.append(v_adj)
            
            # Distancia do vertice atual ate o seu vertice adjacente
            # Adiciona baldeacao, trafego
            baldeacao = 0 if self.baldiacaoExistente(v_antecessor, v_atual, v_adj) else custo_baldeacao
            trafego = self.getAresta(v_atual, v_adj).custo_trafego
            custo_adicional = trafego + baldeacao
            novo_g_de_n = distancia_ate_n[v_atual.chave] + self.calcularDistanciaEntreVertices(v_atual, v_adj) + custo_adicional
            
            # A distancia entre o inicio e o nó adjacente
            if distancia_ate_n[v_adj.chave]:                         
              if novo_g_de_n >= distancia_ate_n[v_adj.chave]:
                continue

            # Melhor caminho encontro até o momento atual                      
            v_antecessor[v_adj.chave] = v_atual
            distancia_ate_n[v_adj.chave] = novo_g_de_n
            # f(n) = g(n) + h(n)
            v_adj.f_de_n = distancia_ate_n[v_adj.chave] + v_adj.h_de_n

    return None

if __name__ == '__main__':
  from vertice import Vertice
  from aresta import Aresta
  import sys

  vertices = []
  # O segundo parametro de Vertice tem a função de 
  # guardar a distancia do no ate o destino final
  noE1 = Vertice('E1', 450) 
  vertices.append(noE1)
  noE2 = Vertice('E2', 302)
  vertices.append(noE2)
  noE3 = Vertice('E3', 659)
  vertices.append(noE3)
  noE4 = Vertice('E4', 48)
  vertices.append(noE4)
  noE5 = Vertice('E5', 446)
  vertices.append(noE5)
  noE6 = Vertice('E6', 132)
  vertices.append(noE6)
  noE7 = Vertice('E7', 278)
  vertices.append(noE7)
  noE8 = Vertice('E8', 720)
  vertices.append(noE8)
  noE9 = Vertice('E9', 15)
  vertices.append(noE9)
  noE10 = Vertice('E10', 605)
  vertices.append(noE10)
  noE11 = Vertice('E11', 200)
  vertices.append(noE11)
  noE12 = Vertice('E12', 192)
  vertices.append(noE12)
  noE13 = Vertice('E13', 168)
  vertices.append(noE13)
  noE14 = Vertice('E14', 37)
  vertices.append(noE14)

  custo_trafego_desta_aresta = 0

  noE1.add_aresta_adj(Aresta(noE2, 11, 'azul', custo_trafego_desta_aresta))

  noE2.add_aresta_adj(Aresta(noE1, 11, 'azul', custo_trafego_desta_aresta))
  noE2.add_aresta_adj(Aresta(noE3, 9, 'azul', custo_trafego_desta_aresta))
  noE2.add_aresta_adj(Aresta(noE9, 11, 'amarelo', custo_trafego_desta_aresta))
  noE2.add_aresta_adj(Aresta(noE10, 4, 'amarelo', custo_trafego_desta_aresta))

  noE3.add_aresta_adj(Aresta(noE2, 9, 'azul', custo_trafego_desta_aresta))
  noE3.add_aresta_adj(Aresta(noE4, 7, 'azul', custo_trafego_desta_aresta))
  noE3.add_aresta_adj(Aresta(noE9, 10, 'vermelho', custo_trafego_desta_aresta))
  noE3.add_aresta_adj(Aresta(noE13, 11, 'vermelho', custo_trafego_desta_aresta))
  
  noE4.add_aresta_adj(Aresta(noE3, 7, 'azul', custo_trafego_desta_aresta))
  noE4.add_aresta_adj(Aresta(noE5, 13, 'azul', custo_trafego_desta_aresta))
  noE4.add_aresta_adj(Aresta(noE8, 13, 'verde', custo_trafego_desta_aresta))
  noE4.add_aresta_adj(Aresta(noE13, 11, 'verde', custo_trafego_desta_aresta))

  noE5.add_aresta_adj(Aresta(noE4, 13, 'azul', custo_trafego_desta_aresta))
  noE5.add_aresta_adj(Aresta(noE6, 3, 'azul', custo_trafego_desta_aresta))
  noE5.add_aresta_adj(Aresta(noE7, 2, 'amarelo', custo_trafego_desta_aresta))
  noE5.add_aresta_adj(Aresta(noE8, 21, 'amarelo', custo_trafego_desta_aresta))

  noE8.add_aresta_adj(Aresta(noE5, 21, 'amarelo', custo_trafego_desta_aresta))
  noE8.add_aresta_adj(Aresta(noE4, 13, 'verde', custo_trafego_desta_aresta))
  noE8.add_aresta_adj(Aresta(noE9, 9, 'amarelo', custo_trafego_desta_aresta))
  noE8.add_aresta_adj(Aresta(noE12, 7, 'verde', custo_trafego_desta_aresta))

  noE9.add_aresta_adj(Aresta(noE2, 11, 'amarelo', custo_trafego_desta_aresta))
  noE9.add_aresta_adj(Aresta(noE3, 10, 'vermelho', custo_trafego_desta_aresta))
  noE9.add_aresta_adj(Aresta(noE8, 9, 'amarelo', custo_trafego_desta_aresta))
  noE9.add_aresta_adj(Aresta(noE11, 12, 'vermelho', custo_trafego_desta_aresta))

  noE10.add_aresta_adj(Aresta(noE2, 4, 'amarelo', custo_trafego_desta_aresta))

  noE11.add_aresta_adj(Aresta(noE9, 12, 'vermelho', custo_trafego_desta_aresta))

  noE12.add_aresta_adj(Aresta(noE8, 7, 'verde', custo_trafego_desta_aresta))

  noE13.add_aresta_adj(Aresta(noE3, 11, 'vermelho', custo_trafego_desta_aresta))
  noE13.add_aresta_adj(Aresta(noE4, 11, 'verde', custo_trafego_desta_aresta))
  noE13.add_aresta_adj(Aresta(noE14, 5, 'verde', custo_trafego_desta_aresta))
  
  noE14.add_aresta_adj(Aresta(noE13, 5, 'verde', custo_trafego_desta_aresta))

  custo_baldeacao = 2
  caminho, custo = BuscaAEstrela(vertices).buscaAEstrela(noE1, noE12, custo_baldeacao)
  print('O menor caminho é: {}\nCusto do menor caminho: {}'.format(' -> '.join(caminho), custo))

  '''
  Todo vertice contem:
    Label
    Distancia do vertice N ate o vertice Final
  
  Toda aresta contem:
    Cor - verificar baldeacao
    Distancia entre os vertices
    Quais sao os vertices
    Custo adicional previsto pelo Aprendizado de Maquina, referente ao trafego
  '''
