class AEstrela(object):

  def __init__(self, vertices):
    # lista de vertices ja calculados
    self._vertices_abertos = []
    # lista de vertices ainda nao calculados
    self._vertices_fechados = []
    self._vertices = vertices
    # Variavel ira decrescer o custo da aresta, caso o vertice destino possua um pT
    # Quanto maior este valor, maior chance de passar por um PT

  def reconstruitCaminho(self, v_antecessor, v_atual):
    caminho = [v_atual.chave]
    custo = v_atual.f_de_n
    chave_v_atual = v_atual.chave
    while v_antecessor[chave_v_atual]:
      chave_v_atual = v_antecessor[chave_v_atual].chave
      caminho.append(chave_v_atual)
    caminho.reverse() 
    return (caminho, custo)

  def getVerticesAdjacentes(self, vertice):
    v_adjacentes = []
    for aresta in vertice.arestas_adj:
      v_adjacentes.append(aresta.v_destino)
    return v_adjacentes

  def distanciaEntreVertices(self, v_atual, v_adj):
    return self.getAresta(v_atual, v_adj).distancia
  
  def getAresta(self, v_inicio, v2_destino):
    for aresta in v_inicio.arestas_adj:
      if aresta.v_destino == v2_destino:
        return aresta
  
  # Recupera o menor_f dentre os vertices em aberto
  def recuperaMenorF(self):
    menor = self._vertices_abertos[0]
    for v in self._vertices_abertos:
      if v.f_de_n < menor.f_de_n:
        menor = v 
    return menor

  def existeBaldiacao(self, antecessor, v_atual, v_final):
    '''
    Antecessor eh o dicionario que contem os vertices antecessores
    '''
    v_antecessor = antecessor[v_atual.chave]
    if not v_antecessor:
      return False
    aresta_antecessora = self.getAresta(v_antecessor, v_atual)
    aresta_atual = self.getAresta(v_atual, v_final)
    return aresta_antecessora.cor != aresta_atual.cor

  def aEstrela(self, v_inicio, v_final, custo_baldeacao):
    # Inicia pelo primeiro vertice
    self._vertices_abertos.append(v_inicio)
    
    # Para cada vertice, eh salvo o seu antecessor que possui o melhor caminho,
    # caso ele tenha muitos caminhos, v_antecessor indicara o menor caminho
    v_antecessor = {}
    
    # Para cada vertice, a distancia do inicio ate o vertice atual
    distancia_ate_n = {}

    # Preenche
    for v in self._vertices:
      v_antecessor[v.chave] = None
      distancia_ate_n[v.chave] = None

    # A distancia do inicio para o inicio eh zero
    distancia_ate_n[v_inicio.chave] = 0

    # Para o primeiro vertice, f(n) = g(n) + h(n) = 0 + h(n)
    v_inicio.f_de_n = v_inicio.h_de_n

    # Enquanto existir nos em aberto
    while len(self._vertices_abertos) != 0:
        v_atual = self.recuperaMenorF()
        if v_atual == v_final:
            return self.reconstruitCaminho(v_antecessor, v_atual) # Condicao de parada com sucesso!

        self._vertices_abertos.remove(v_atual) # Remove atual dos vertices abertos
        self._vertices_fechados.append(v_atual) # Adiciona atual aos vertices fechados

        for v_adj in self.getVerticesAdjacentes(v_atual):
            if v_adj in self._vertices_fechados:
                continue		# Ignora os vizinhos ja calculados

            if v_adj not in self._vertices_abertos: # Um vertice novo
                self._vertices_abertos.append(v_adj)
            
            # Distancia do vertice atual ate o seu vertice adjacente
            # Adiciona baldeacao, trafego
            baldeacao = 0 if self.existeBaldiacao(v_antecessor, v_atual, v_adj) else custo_baldeacao
            trafego = self.getAresta(v_atual, v_adj).custo_trafego
            custo_adicional = trafego + baldeacao
            novo_g_de_n = distancia_ate_n[v_atual.chave] + self.distanciaEntreVertices(v_atual, v_adj) + custo_adicional
            
            # Distancia do inicio ate o no adjacente
            if distancia_ate_n[v_adj.chave]:                         
              if novo_g_de_n >= distancia_ate_n[v_adj.chave]:
                continue		# Este nao eh o melhor caminho         

            # Melhor caminho ate agora                        
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
  # segundo parametro corresponde a distancia do No ate o destino Final(nesse caso E12)
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

  custo_trafego_desta_aresta = 0 # cada aresta possui seu custo

  noE1.add_aresta_adj(Aresta(noE2, 11, 'azul', custo_trafego_desta_aresta)) # azul

  noE2.add_aresta_adj(Aresta(noE1, 11, 'azul', custo_trafego_desta_aresta)) # azul
  noE2.add_aresta_adj(Aresta(noE3, 9, 'azul', custo_trafego_desta_aresta)) # azul
  noE2.add_aresta_adj(Aresta(noE9, 11, 'amarelo', custo_trafego_desta_aresta)) # amarelo
  noE2.add_aresta_adj(Aresta(noE10, 4, 'amarelo', custo_trafego_desta_aresta)) # amarelo

  noE3.add_aresta_adj(Aresta(noE2, 9, 'azul', custo_trafego_desta_aresta)) # azul
  noE3.add_aresta_adj(Aresta(noE4, 7, 'azul', custo_trafego_desta_aresta)) # azul
  noE3.add_aresta_adj(Aresta(noE9, 10, 'vermelho', custo_trafego_desta_aresta)) # vermelho
  noE3.add_aresta_adj(Aresta(noE13, 11, 'vermelho', custo_trafego_desta_aresta)) # vermelho
  
  noE4.add_aresta_adj(Aresta(noE3, 7, 'azul', custo_trafego_desta_aresta)) # azul
  noE4.add_aresta_adj(Aresta(noE5, 13, 'azul', custo_trafego_desta_aresta)) # azul
  noE4.add_aresta_adj(Aresta(noE8, 13, 'verde', custo_trafego_desta_aresta)) # verde
  noE4.add_aresta_adj(Aresta(noE13, 11, 'verde', custo_trafego_desta_aresta)) # verde

  noE5.add_aresta_adj(Aresta(noE4, 13, 'azul', custo_trafego_desta_aresta)) # azul
  noE5.add_aresta_adj(Aresta(noE6, 3, 'azul', custo_trafego_desta_aresta)) # azul
  noE5.add_aresta_adj(Aresta(noE7, 2, 'amarelo', custo_trafego_desta_aresta)) # amarelo
  noE5.add_aresta_adj(Aresta(noE8, 21, 'amarelo', custo_trafego_desta_aresta)) # amarelo

  noE8.add_aresta_adj(Aresta(noE5, 21, 'amarelo', custo_trafego_desta_aresta)) # amarelo
  noE8.add_aresta_adj(Aresta(noE4, 13, 'verde', custo_trafego_desta_aresta)) # verde
  noE8.add_aresta_adj(Aresta(noE9, 9, 'amarelo', custo_trafego_desta_aresta)) # amarelo
  noE8.add_aresta_adj(Aresta(noE12, 7, 'verde', custo_trafego_desta_aresta)) # verde

  noE9.add_aresta_adj(Aresta(noE2, 11, 'amarelo', custo_trafego_desta_aresta)) # amarelo
  noE9.add_aresta_adj(Aresta(noE3, 10, 'vermelho', custo_trafego_desta_aresta)) # vermelho
  noE9.add_aresta_adj(Aresta(noE8, 9, 'amarelo', custo_trafego_desta_aresta)) # amarelo
  noE9.add_aresta_adj(Aresta(noE11, 12, 'vermelho', custo_trafego_desta_aresta)) # vermelho

  noE10.add_aresta_adj(Aresta(noE2, 4, 'amarelo', custo_trafego_desta_aresta)) # amarelo

  noE11.add_aresta_adj(Aresta(noE9, 12, 'vermelho', custo_trafego_desta_aresta)) # vermelho

  noE12.add_aresta_adj(Aresta(noE8, 7, 'verde', custo_trafego_desta_aresta)) # verde

  noE13.add_aresta_adj(Aresta(noE3, 11, 'vermelho', custo_trafego_desta_aresta)) # vermelho
  noE13.add_aresta_adj(Aresta(noE4, 11, 'verde', custo_trafego_desta_aresta)) # verde
  noE13.add_aresta_adj(Aresta(noE14, 5, 'verde', custo_trafego_desta_aresta)) # verde
  
  noE14.add_aresta_adj(Aresta(noE13, 5, 'verde', custo_trafego_desta_aresta)) # verde

  custo_baldeacao = 2
  caminho, custo = AEstrela(vertices).aEstrela(noE1, noE12, custo_baldeacao)
  print('Menor Caminho: {}\nCusto: {}'.format(' -> '.join(caminho), custo))

  '''
  Para cada vertice:
    Label
    Distancia do vertice N ate o vertice Final
  
  Para aresta
    Cor - Para verificar baldeacao
    Distancia entre os vertices
    Quais sao os vertices
    Custo adicional previsto pelo Aprendizado de Maquina, referente ao trafego
  '''
