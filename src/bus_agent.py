
from buscaheuristica.buscaAEstrela import BuscaAEstrela
from buscaheuristica.vertice import Vertice
from buscaheuristica.aresta import Aresta
from gerarRotas import GerarRotas

QTD_VERTICES = 15
VELOCIDADE_MEDIA_ONIBUS = 60

def contrucaoDoGrafo(inicio, fim, dia, hora, fluxo, 
                    listaDePontosAdjs, dictRotas):

    gerador = GerarRotas(listaDePontosAdjs)
    matrizDeRotas = gerador.gerar_rotas()

    vertices = []

    for index in range(QTD_VERTICES):
        vertices.append(Vertice('E' + str(index + 1), 
                                matrizDeRotas[index][fim - 1].distancia))
    
    for i in range(QTD_VERTICES):
        for j in range(QTD_VERTICES):
            if [i, j] in listaDePontosAdjs \
               or [j, i] in listaDePontosAdjs:

                adj = vertices[j]
                rota_cor = ""
                adicional_trafego = VELOCIDADE_MEDIA_ONIBUS * (matrizDeRotas[i][j].prever(dia, hora, fluxo)/60)

                if i in dictRotas["vermelho"] \
                    and j in dictRotas["vermelho"]:

                    rota_cor = "vermelho"

                elif i in dictRotas["azul"] \
                     and j in dictRotas["azul"]:
                    
                    rota_cor = "vermelho"

                elif i in dictRotas["roxo"] \
                    and j in dictRotas["roxo"]:
                    
                    rota_cor = "roxo"

                elif i in dictRotas["rosa"] \
                    and j in dictRotas["rosa"]:
                    
                    rota_cor = "rosa"

                vertices[i].add_aresta_adj(Aresta(vertices[j], matrizDeRotas[i][j].distancia,
                                           rota_cor, adicional_trafego))

    return vertices

if __name__ == "__main__":
    import sys

    inicio = int(sys.argv[1])
    fim = int(sys.argv[2])
    dia = 1
    hora = 14
    fluxo = 10

    listaDePontosAdjs = [[0, 1], [1, 3], [3, 8], 
                        [8, 9], [9, 10], [10, 12], 
                        [12, 13], [13, 11], [11, 14], 
                        [14, 4], [4, 2], [2, 7], 
                        [6, 7], [6, 5], [5, 4], 
                        [3, 7], [11, 7], [7, 10]]

    dictRotas = {"vermelho" : [0, 1, 3, 7],
                  "azul" : [3, 8, 9, 10, 11, 12, 13],
                  "roxo" : [4, 6, 7, 11, 14],
                  "rosa" : [2, 4, 5, 6, 7]}

    vertices = contrucaoDoGrafo(inicio, fim, dia, hora, fluxo,
                              listaDePontosAdjs, dictRotas)
    
    caminho, custo = BuscaAEstrela(vertices).buscaAEstrela(vertices[inicio - 1], vertices[fim - 1], 15)
    print('O menor caminho é: {}'.format(' -> '.join(caminho)))