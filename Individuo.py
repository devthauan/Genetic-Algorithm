from random import *
from copy import *
import numpy as np

class Individuo:
    def __init__(self, produtos, volume, valorFitness ,tamanhoIndividuo):
        self.produtos = produtos
        self.volume = volume
        self.valorFitness = valorFitness
        self.tamanhoIndividuo = tamanhoIndividuo

    #cria individuo aleatorio
    def criarIndividuoDaniel(tamanhoIndividuo):
        return [randint(0,1) for i in range(tamanhoIndividuo)]

    #cria um individuo "enviesado" que não passa o limite do carminhão
    def criarIndividuoThauan(produtos,tamanhoIndividuo,volumeMaximoCaminhao):
        #uma copia dos meus produtos
        produtoAuxiliar = deepcopy(produtos)
        #individuo zerado
        individuo = np.zeros(tamanhoIndividuo).tolist()
        volumeAtual = 0
        while(True):
            #escolhe um produto aleatorio
            escolhido = randint(0,len(produtoAuxiliar)-1)
            #se couber no caminhao pegue
            if volumeAtual + produtoAuxiliar[escolhido].volume <= volumeMaximoCaminhao:
                nomeProduto = produtoAuxiliar[escolhido].nome
                #percorre o vetor de produtos originais achando a posição que esse produto escolhido está e o pegando
                for i in range(len(produtos)):
                    if(produtos[i].nome == nomeProduto):
                        individuo[i] = 1
                volumeAtual += produtoAuxiliar[escolhido].volume
                del(produtoAuxiliar[escolhido])
            else:
                break
        return individuo

    # fitness que considera apenas o lucro
    def calcularFitness(individuo, produtos):
        valor = 0
        for i in range(len(individuo)):
            if (individuo[i] == 1):
                valor += produtos[i].valor
        return valor

    # fitness que pune os individuos que passam o limite do caminhão
    def calcularFitnessPunitiva(individuo, produtos, volumeMaximoCaminhao):
        valor = 0
        volume = 0
        for i in range(len(individuo)):
            if (individuo[i] == 1):
                valor += produtos[i].valor
                volume += produtos[i].volume
        if (volume > volumeMaximoCaminhao):
            porcentagemPassada = (1 - (volume / volumeMaximoCaminhao)) * (-1)
            valor = valor - (valor * porcentagemPassada)
        return valor

    def calcularvolume(individuo, produtos):
        volume = 0
        for i in range(len(individuo)):
            if (individuo[i] == 1):
                volume += produtos[i].volume
        return volume