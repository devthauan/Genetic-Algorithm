from random import *
from copy import *
from Individuo import  Individuo
import numpy
import matplotlib.pyplot as plt

class GeneticOperators:
    def __init__(self, nome, tipo):
        self.nome = nome
        self.tipo = tipo

    #rankeia a populaçao pela fitness
    def rankeamento(populacao, produtos, fitnessModo, volumeMaximoCaminhao):
        if(fitnessModo =="punitiva"):
            fitness = [Individuo.calcularFitnessPunitiva(populacao[i], produtos, volumeMaximoCaminhao) for i in range(len(populacao))]
        elif(fitnessModo == "normal"):
            fitness = [Individuo.calcularFitness(populacao[i], produtos) for i in range(len(populacao))]
        #ordena a populaçao pela fitness
        populacao = [x for _, x in sorted(zip(fitness, populacao))]
        return populacao

    #SELEÇÃO------------------------------------------------------------------------------------------------------------

    # seleção por roleta
    def selecaoRoleta(populacao, fitness):
        possibilidades = sum(fitness)
        # calcula a probabilidade de cada individuo
        vetorposibility = [fitness[i] / possibilidades for i in range(len(populacao))]
        # organiza isso num vetor com uma faixa referente a sua porcentagem
        # for i in range(1, len(vetorposibility)):
        #     vetorposibility[i] += vetorposibility[i - 1]
        vetorposibility = list(numpy.cumsum(vetorposibility))
        # gera um numero aleatorio
        aleatorio = uniform(0, 1)
        # verifica qual faixa esse numero aleatorio caiu e pega o individuo
        for i in range(len(vetorposibility)):
            if (aleatorio <= vetorposibility[i]):
                escolhido = populacao[i]
                break
        return escolhido

    # seleção por torenio
    def selecaoTorneio(populacao, fitness, k, produtos,  fitnessModo, volumeMaximoCaminhao):
        # individuos aleatorios, tamanho k
        vetor = []
        for i in range(k):
            # valores aleatorios
            aleatorio = randint(0, len(populacao) - 1)
            vetor.append(populacao[aleatorio])
        # ordena esse vetor
        vetor = GeneticOperators.rankeamento(vetor, produtos, fitnessModo, volumeMaximoCaminhao)
        # pega o melhor desse subconjunto K pego aleatoriamente e retorna
        return vetor[len(vetor) - 1]

    # CROSSOVER --------------------------------------------------------------------------------------------------------

    # crossover normal
    def crossover(pai1, pai2):
        # cria um valor aleatorio para dividir o individuo
        valorDeCorte = randint(1, len(pai1) - 1)
        filho1 = deepcopy(pai1)
        filho2 = deepcopy(pai2)
        # filho 1 parte pai 1, parte pai 2
        filho1[valorDeCorte:] = pai2[valorDeCorte:]
        # filho 2 parte pai2, parte pai 1
        filho2[valorDeCorte:] = pai1[valorDeCorte:]
        return [filho1, filho2]

    # cross over unifore pegando celula a celula controlando a probablidade da moeda
    def crossoverLinear(pai1, pai2, probabilidade = 0.5):
        for i in range(len(pai1)):
            filho1 = deepcopy(pai1)
            filho2 = deepcopy(pai2)
            vetorDecisao = [probabilidade, 1 - probabilidade]
            escolha = uniform(0, 1)
            # muda os genes do pai1 com pai2 de acordo com a probabilidade
            if (escolha <= vetorDecisao[0]):
                aux = filho1[i]
                filho1[i] = filho2[i]
                filho2[i] = aux
        return [filho1, filho2]

    #MUTAÇÂO -----------------------------------------------------------------------------------------------------------

    def mutacaoUniforme(populacao, tamanhoIndividuo, probabilidadeMutacao = 0.4, probabilidadeMutacaoGene = 0.3):
        for i in range(len(populacao)):
            # Probabilidade de mutar ou não
            vetorDecisao = [probabilidadeMutacao, 1 - probabilidadeMutacao]
            escolha = uniform(0, 1)
            # entra no IF se for mutar
            if (escolha <= vetorDecisao[0]):
                for j in range(tamanhoIndividuo):
                    # probabilidade de mutar o gene
                    vetorDecisaoGene = [probabilidadeMutacaoGene, 1 - probabilidadeMutacaoGene]
                    escolhaGene = uniform(0, 1)
                    # entra no IF se for mutar
                    if (escolhaGene <= vetorDecisaoGene[0]):
                        if (populacao[i][j] == 1):
                            populacao[i][j] = 0
                        else:
                            populacao[i][j] = 1
        return populacao

    # mutação por troca
    def mutacaoTroca(populacao, tamanhoIndividuo, probabilidadeMutacao = 0.4):
        for i in range(len(populacao)):
            # Probabilidade de mutar ou não
            vetorDecisao = [probabilidadeMutacao, 1 - probabilidadeMutacao]
            escolha = uniform(0, 1)
            # entra no IF se for mutar
            if (escolha <= vetorDecisao[0]):
                # troca 2 genes de lugar entre si
                posicao1 = randint(0, tamanhoIndividuo - 1)
                posicao2 = randint(0, tamanhoIndividuo - 1)
                aux = populacao[i][posicao1]
                populacao[i][posicao1] = populacao[i][posicao2]
                populacao[i][posicao2] = aux
        return populacao