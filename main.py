# -*- coding: utf-8 -*-
import time
import math
import random
random.seed(10)
import itertools
import pandas as pd
from copy import deepcopy
from random import randint
from random import uniform
from products import Product
from evolution import Evolution
import matplotlib.pyplot as plt
from individuals import Individual
from genetic_operators import GeneticOperators
"""
Titulo: Otimização de carga de caminhão.
Problema: Existe um caminhão com uma determinada metragem cubica de espaço disponível para preenchimento com produtos.
Esses produtos possuem uma metragem cubica que ocupam e o seu valor. O objetivo é colocar dentro do caminhão produtos de forma
com que se consiga o maior valor possível em produtos.

Solução 1: Através da utilização de algoritmos genéticos, chegar numa solução ótima para o problema proposto.
Passos:
    Primeiramente foi criado um vetor de produtos aleatórios com um volume e valor.
    Em seguida foi criado uma população de indivíduos. Indivíduos são possíveis soluções para o problema. Nesse caso, um indivíduo é
    um vetor com 1s e 0s, onde o valor 1 indica que o produto referente aquela posição está presente naquele indivíduo e 0 não está.
    Sendo assim, um indivíduo é uma lista de quais produtos vão estar dentro do caminhão, ou seja, uma possível solução para o problema.
    
    Seguindo a ideia de algoritmo genético foi criada uma população de individuos. Essa população foi avaliada de acordo com uma função fitness,
    que nesse caso é um somatório dos valores dos produtos presentes no indivíduo.
    Essa população de indivíduos foi submetida aos passos da evolução segundo a lógica de algoritmos genéticos, passando pela seleção, crossover e mutação.
    Diversas gerações foram criadas e evoluidas até que se atinja um critério de parada.
    
    Foi implementado um par de algoritmos para cada fase da evolução, tendo até mais de uma forma de criação de indivíduos, método de evolução,
    forma de cálculo da fitness, forma de seleção, etc.
    
Solução 2: Força bruta. 
Passos:
    Considerando a mesma ideia de individuo apresentadona primeira solução, foi utilizado força bruta para testar todas as 
    combinações possíveis de produtos e foi pega aquela com o maior valor possível respeitando o limite de volume cúbico do caminhão.
"""


# =============================================================================
# Setting variables
# =============================================================================
individual_size = 30
max_truck_volume = 36
population_size = 100

individuals_creating_method = "random_individuals"
# individuals_creating_method = "individuals_that_fit"

evolution_method = "ancestral"
# evolution_method = "elite"

selection_method = "roulette wheel"
# selection_method = "tournament"
k = 2

fitness_method = "punitive_fitness"
# fitness_method = "profit_fitness"

crossover_method = "single_point_crossover"
# crossover_method = "uniform_crossover"
crossover_probability = 0.7

mutation_method = "bit_flip_mutation"
# mutation_method = "swap_mutation"
mutation_probability = 0.5
chromosome_mutation_probability = 0.3

# Creating products
products = [Product("product " + str(i), uniform(0.00007, 3), uniform(1, 10_000)) for i in range(individual_size)]


start = time.time()
# Creating population
population = [Individual("individual " + str(i), individuals_creating_method, products, fitness_method, individual_size, max_truck_volume) for i in range(population_size)]
# Evolution
best_result, population_average_fitness, lowest_fitness_per_generation, highest_fitness_per_generation = Evolution.evolution(population, population_size, selection_method, crossover_probability, k, crossover_method, mutation_method, mutation_probability, chromosome_mutation_probability, evolution_method)
end = time.time()
print(f""""Best result:
      fitness: {best_result.fitness_value}
      volume: {best_result.volume}
      time: {end-start}\n""")

# =============================================================================
# Brute Force
# =============================================================================
def fitness_and_volume_calculation(individual, products):
    value = 0
    volume = 0
    for i in range(len(individual)):
        if (individual[i] == 1):
            value += products[i].value
            volume += products[i].volume
    return [value, volume]

start = time.time()

best_fitness_brute_force = 0
best_individual_brute_force = []
# Calculates the fitness and volume for each possible individual and saves the best one
for individual in itertools.product([0, 1], repeat=30):
    fitness_value, volume = fitness_and_volume_calculation(individual, products)
    if(fitness_value > best_fitness_brute_force and volume <= max_truck_volume):
        best_fitness_brute_force = fitness_value
        best_individual_brute_force = individual

best_result_brute_force_fitness_value, best_result_brute_force_volume = fitness_and_volume_calculation(best_individual_brute_force, products)
end = time.time()
print(f""""Best result brute_force:
      fitness: {best_result_brute_force_fitness_value}
      volume: {best_result_brute_force_volume}
      time: {end-start}\n""")

print(f"Quantidade de individuos analisados: {1073741824:_}".replace("_", "."))

# =============================================================================
# Results
# =============================================================================
"""
"Best result Brute Force:
      fitness: 124015.39152913929
      volume: 34.962080685703256
      time: 8305.587522268295 # 2.3H
      """
"""
Best result Genetic Algorithm:
Generations required:  78
"Best result:
      fitness: 124015.39152913929
      volume: 34.962080685703256
      time: 10.28027892112732 # 10s
      """