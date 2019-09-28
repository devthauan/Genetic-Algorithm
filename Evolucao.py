import math
from Produto import Produto
import matplotlib.pyplot as plt
from random import *
from copy import deepcopy
# import das classes
from Individuo import Individuo
from GeneticOperators import GeneticOperators

# quantidade de produtos
tamanhoIndividuo = 50
volumeMaximoCaminhao = 3
tamanhoPopulacao = 100

#define o modo de criação de individuos

modo = "thauan" #OK
# modo = "daniel" #OK

evolucaoMetodo = "antiga"
# evolucaoMetodo = "novaComElite"

selecaoModo = "roleta" #OK
# selecaoModo = "torneio" #OK
k = 2

fitnessModo="punitiva" #OK
# fitnessModo="normal"

crossModo = "normal" #OK
# crossModo = "linear" #OK
crossProbabilidade = 0.7

# mutacaoModo = "uniforme"
mutacaoModo = "troca"
probabilidadeMutacao = 0.5
probabilidadeMutacaoGene = 0.3

solucao =[]
def criarProdutos():
    produtos = []
    for i in range(tamanhoIndividuo):
        produto = Produto("Produto " + str(i), uniform(0.0000700, 3), uniform(1, 10000))
        aux = deepcopy(produto)
        produtos.append(aux)
    return produtos


produtos = criarProdutos()


class Evolucao:

    def criarPopulacao(produtos):
        if (modo == "thauan"):
            return [Individuo.criarIndividuoThauan(produtos, tamanhoIndividuo, volumeMaximoCaminhao) for i in
                    range(tamanhoPopulacao)]
        elif (modo == "daniel"):
            return [Individuo.criarIndividuoDaniel(tamanhoIndividuo) for i in range(tamanhoPopulacao)]

    def verificarLimiteVolume(populacao, produtos):
        # verificando o volume dos produtos
        # ponto onde volume ultrapassa o limiete
        index = len(populacao)
        volume = [Individuo.calcularvolume(populacao[i], produtos) for i in range(len(populacao))]
        populacaoOrdenada = [x for _, x in sorted(zip(volume, populacao))]
        volumeOrdenado = [Individuo.calcularvolume(populacaoOrdenada[i], produtos) for i in range(len(populacaoOrdenada))]
        for i in range(len(populacaoOrdenada)):
            if (volumeOrdenado[i] > volumeMaximoCaminhao):
                index = i
                break
        populacao = populacaoOrdenada[:index]
        return populacao

    def evolucao(produtos):
        # média das populaçoes de N gerações
        resultados = []
        # maior fitness
        maiorFitness = []
        # menor fitness
        menorFitness = []
        # contador de geraçoes sem mudar a média
        contadorGeracao = 0
        # Cria a população
        populacao = Evolucao.criarPopulacao(produtos)
        # Calcula o fitness
        if (fitnessModo == "punitiva"):
            fitness = [Individuo.calcularFitnessPunitiva(populacao[i], produtos, volumeMaximoCaminhao) for i in
                       range(len(populacao))]
        elif (fitnessModo == "normal"):
            fitness = [Individuo.calcularFitness(populacao[i], produtos) for i in range(len(populacao))]
            populacao = Evolucao.verificarLimiteVolume(populacao, produtos)
            fitness = [Individuo.calcularFitness(populacao[i], produtos) for i in range(len(populacao))]
            if (len(populacao) == 0):
                print("População zerada")
                return 0
        geracao = 0
        contador = 0
        while (True):
            # seleciona individuos e faz crossover ate atingir  =~150% da população
            while (len(populacao) < (math.floor(tamanhoPopulacao * 0.5) + tamanhoPopulacao)):
                # seleciona 2 individuos
                if (selecaoModo == "roleta"):
                    individuo1 = GeneticOperators.selecaoRoleta(populacao, fitness)
                    individuo2 = GeneticOperators.selecaoRoleta(populacao, fitness)
                elif (selecaoModo == "torneio"):
                    individuo1 = GeneticOperators.selecaoTorneio(populacao, fitness, k, produtos, fitnessModo,
                                                                 volumeMaximoCaminhao)
                    individuo2 = GeneticOperators.selecaoTorneio(populacao, fitness, k, produtos, fitnessModo,
                                                                 volumeMaximoCaminhao)
                # Faz crossover
                if (crossModo == "normal"):
                    doisFilhos = GeneticOperators.crossover(individuo1, individuo2)
                elif (crossModo == "linear"):
                    doisFilhos = GeneticOperators.crossoverLinear(individuo1, individuo2, crossProbabilidade)
                # adiciona esses filhos a população
                populacao.append(doisFilhos[0])
                populacao.append(doisFilhos[1])
                # Calcula novamente o fitness porque a população cresceu
                if (fitnessModo == "punitiva"):
                    fitness = [Individuo.calcularFitnessPunitiva(populacao[i], produtos, volumeMaximoCaminhao) for i in
                               range(len(populacao))]
                elif (fitnessModo == "normal"):
                    fitness = [Individuo.calcularFitness(populacao[i], produtos) for i in range(len(populacao))]
                    populacao = Evolucao.verificarLimiteVolume(populacao, produtos)
                    fitness = [Individuo.calcularFitness(populacao[i], produtos) for i in range(len(populacao))]
                    if (len(populacao) == 0):
                        print("População zerada")
                        return 0
            # faz mutação
            if (mutacaoModo == "uniforme"):
                populacao = GeneticOperators.mutacaoUniforme(populacao, tamanhoIndividuo, probabilidadeMutacao,
                                                             probabilidadeMutacaoGene)
            elif (mutacaoModo == "troca"):
                populacao = GeneticOperators.mutacaoTroca(populacao, tamanhoIndividuo, probabilidadeMutacao)
            # rankeia novamente para verificar se chegou na solucao otima ou boa
            populacao = GeneticOperators.rankeamento(populacao, produtos, fitnessModo, volumeMaximoCaminhao)
            # pega a quantidade de individuos da populaçao original
            populacao = populacao[len(populacao) - tamanhoPopulacao:]
            # recalcula a fitness
            if (fitnessModo == "punitiva"):
                fitness = [Individuo.calcularFitnessPunitiva(populacao[i], produtos, volumeMaximoCaminhao) for i in
                           range(len(populacao))]
            elif (fitnessModo == "normal"):
                fitness = [Individuo.calcularFitness(populacao[i], produtos) for i in range(len(populacao))]
                populacao = Evolucao.verificarLimiteVolume(populacao, produtos)
                fitness = [Individuo.calcularFitness(populacao[i], produtos) for i in range(len(populacao))]
                if (len(populacao) == 0):
                    print("População zerada")
                    return 0
            # calcula a media da fitness dessa geração
            media = sum(fitness) / len(populacao)
            # adiciona essa media a resultados
            resultados.append(media)
            menorFitness.append(fitness[0])
            maiorFitness.append(fitness[len(fitness) - 1])
            if (len(resultados) >= 2):
                if (resultados[len(resultados) - 1] <= resultados[len(resultados) - 2]):
                    contadorGeracao += 1
                else:
                    contadorGeracao = 0
            # se durante 20 gerações nao aumentar a fitness, para
            if (contadorGeracao >= 20):
                break
            contador += 1
            # se durante 100 gerações não parar na restrição anterior para agora
            if (contador > 100):
                break
            geracao += 1
        plt.plot(resultados, label="Média", color="orange", linewidth=3)
        plt.plot(menorFitness, label="Mínimo", color="red", linewidth=2)
        plt.plot(maiorFitness, label="Máximo", color="green", linewidth=2)
        plt.legend(loc='upper left')
        plt.show()
        print("medias: ", resultados)
        print("Geração: ", geracao)
        if (fitnessModo == "punitiva"):
            print("Melhor fitness: ",
                  Individuo.calcularFitnessPunitiva(populacao[len(populacao) - 1], produtos, volumeMaximoCaminhao))
        elif (fitnessModo == "normal"):
            print("Melhor fitness: ", Individuo.calcularFitness(populacao[len(populacao) - 1], produtos))
        print("Volume do melhor: ", Individuo.calcularvolume(populacao[len(populacao) - 1], produtos))
        print("Volumes: ", [Individuo.calcularvolume(populacao[i], produtos) for i in range(len(populacao))])

    def evolucaoFilhos(produtos):
        # média das populaçoes de N gerações
        resultados = []
        # maximo
        maiorFitness = []
        # minimo
        menorFitness = []
        # contador de geraçoes sem mudar a média
        contadorGeracao = 0
        # Cria a população
        populacao = Evolucao.criarPopulacao(produtos)
        # Calcula o fitness
        if (fitnessModo == "punitiva"):
            fitness = [Individuo.calcularFitnessPunitiva(populacao[i], produtos, volumeMaximoCaminhao) for i in
                       range(len(populacao))]
        elif (fitnessModo == "normal"):
            fitness = [Individuo.calcularFitness(populacao[i], produtos) for i in range(len(populacao))]
            populacao = Evolucao.verificarLimiteVolume(populacao, produtos)
            if (len(populacao) == 0):
                print("População zerada")
                return 0
        geracao = 0
        contador = 0
        while (True):
            # cria uma nova populaçao
            novaPopulacao = []
            # seleciona individuos e faz crossover ate a nova população ter 90% da original
            while (len(novaPopulacao) < (math.floor(tamanhoPopulacao * 0.9))):
                # seleciona 2 individuos
                if (selecaoModo == "roleta"):
                    individuo1 = GeneticOperators.selecaoRoleta(populacao, fitness)
                    individuo2 = GeneticOperators.selecaoRoleta(populacao, fitness)
                elif (selecaoModo == "torneio"):
                    individuo1 = GeneticOperators.selecaoTorneio(populacao, fitness, k, produtos, fitnessModo,
                                                                 volumeMaximoCaminhao)
                    individuo2 = GeneticOperators.selecaoTorneio(populacao, fitness, k, produtos, fitnessModo,
                                                                 volumeMaximoCaminhao)
                # Faz crossover
                if (crossModo == "normal"):
                    doisFilhos = GeneticOperators.crossover(individuo1, individuo2)
                elif (crossModo == "linear"):
                    doisFilhos = GeneticOperators.crossoverLinear(individuo1, individuo2, crossProbabilidade)
                # adiciona esses filhos a população
                novaPopulacao.append(doisFilhos[0])
                novaPopulacao.append(doisFilhos[1])

            populacao = GeneticOperators.rankeamento(populacao, produtos, fitnessModo, volumeMaximoCaminhao)

            # faz mutação
            if (mutacaoModo == "uniforme"):
                novaPopulacao = GeneticOperators.mutacaoUniforme(novaPopulacao, tamanhoIndividuo, probabilidadeMutacao,
                                                                 probabilidadeMutacaoGene)
            elif (mutacaoModo == "troca"):
                novaPopulacao = GeneticOperators.mutacaoTroca(novaPopulacao, tamanhoIndividuo, probabilidadeMutacao)
            # elitismo de 10% da populaçao
            novaPopulacao.extend(populacao[math.floor(len(populacao) * 0.9):])
            # rankeia novamente para verificar se chegou na solucao otima ou boa
            novaPopulacao = GeneticOperators.rankeamento(novaPopulacao, produtos, fitnessModo, volumeMaximoCaminhao)
            # recalcula a fitness
            if (fitnessModo == "punitiva"):
                fitness = [Individuo.calcularFitnessPunitiva(novaPopulacao[i], produtos, volumeMaximoCaminhao) for i in
                           range(len(populacao))]
            elif (fitnessModo == "normal"):
                fitness = [Individuo.calcularFitness(novaPopulacao[i], produtos) for i in range(len(populacao))]
                populacao = Evolucao.verificarLimiteVolume(novaPopulacao, produtos)
                if (len(novaPopulacao) == 0):
                    print("Nova opulação zerada")
                    return 0
            novaPopulacao = novaPopulacao[:tamanhoPopulacao]
            # calcula a media da fitness dessa geração
            media = sum(fitness) / len(novaPopulacao)
            # adiciona essa media a resultados
            resultados.append(media)
            menorFitness.append(fitness[0])
            maiorFitness.append(fitness[len(fitness) - 1])
            if (len(resultados) >= 2):
                if (resultados[len(resultados) - 1] <= resultados[len(resultados) - 2]):
                    contadorGeracao += 1
                else:
                    contadorGeracao = 0
            # se durante 20 gerações nao aumentar a fitness, para
            if (contadorGeracao >= 20):
                break
            contador += 1
            # se durante 100 gerações não parar na restrição anterior para agora
            if (contador > 100):
                break
            geracao += 1
            populacao = novaPopulacao
        plt.plot(resultados, label="Média", color="orange", linewidth=3)
        plt.plot(menorFitness, label="Mínimo", color="red", linewidth=2)
        plt.plot(maiorFitness, label="Máximo", color="green", linewidth=2)
        plt.legend(loc='upper left')
        plt.show()
        print("medias: ", resultados)
        print("Geração: ", geracao)
        if (fitnessModo == "punitiva"):
            print("Melhor fitness: ",
                  Individuo.calcularFitnessPunitiva(novaPopulacao[len(novaPopulacao) - 1], produtos,
                                                    volumeMaximoCaminhao))
        elif (fitnessModo == "normal"):
            print("Melhor fitness: ", Individuo.calcularFitness(novaPopulacao[len(novaPopulacao) - 1], produtos))
        print("Volume do melhor: ", Individuo.calcularvolume(novaPopulacao[len(novaPopulacao) - 1], produtos))
        print("Volumes: ", [Individuo.calcularvolume(novaPopulacao[i], produtos) for i in range(len(novaPopulacao))])



for i in range(9):
    if(i == 0):
        modo = "daniel"
    elif(i == 1):
        evolucaoMetodo = "novaComElite"
    elif(i == 2):
        selecaoModo = "torneio"
        k = 2
    elif (i == 3):
        selecaoModo = "torneio"
        k = 10
    elif (i == 4):
        fitnessModo="normal"
    elif (i == 5):
        crossModo = "linear"
    elif (i == 6):
        mutacaoModo = "uniforme"
        probabilidadeMutacao = 0.5
        probabilidadeMutacaoGene = 0.3
    elif (i == 7):
        mutacaoModo = "uniforme"
        probabilidadeMutacao = 0.3
        probabilidadeMutacaoGene = 0.5
    if(evolucaoMetodo == "antiga"):
        Evolucao.evolucao(produtos)
    elif(evolucaoMetodo == "novaComElite"):
        Evolucao.evolucaoFilhos(produtos)
    print(i)
    # define o modo de criação de individuos
    modo = "thauan"
    evolucaoMetodo = "antiga"
    selecaoModo = "roleta"  # OK
    k = 2
    fitnessModo = "punitiva"
    crossModo = "normal"
    crossProbabilidade = 0.7
    mutacaoModo = "troca"
    probabilidadeMutacao = 0.5
    probabilidadeMutacaoGene = 0.3
