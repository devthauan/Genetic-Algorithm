import numpy as np
from copy import deepcopy
from random import randint

class GeneticOperators:
    def __init__(self):
        pass

    # Sorts population by fitness
    def ranking(population):
        return  sorted(population, key=lambda x: x.fitness_value, reverse=True)

    # =============================================================================
    # Selection
    # =============================================================================
    # roulette wheel selection
    def roulette_wheel_selection(population):
        total_fitness = sum([population[i].fitness_value for i in range(len(population))])
        # Calculates the probability of each individual
        probability_vector = [population[i].fitness_value / total_fitness for i in range(len(population))]
        # Calculates a random number accourding to the probability of each individual
        chosen_individual_index = np.random.choice(len(population), p = probability_vector)
        return population[chosen_individual_index]
    

    # tournament selection
    def tournament_selection(population, k):
        # select K random numbers
        random_numbers = [randint(0, len(population) - 1) for i in range(k)]
        return GeneticOperators.ranking([population[random_numbers[i]] for i in range(len(random_numbers))])[0]

    # =============================================================================
    # Crossover
    # =============================================================================
    # Single Point Crossover 
    def single_point_crossover(first_parent, second_parent):
        # Select a random crossover point
        crossover_point = randint(1, first_parent.individual_size - 1)
        # Children initially receive a copy of its parents
        first_children = deepcopy(first_parent)
        second_children = deepcopy(second_parent)
        # Gets the individuals of each children
        first_children_individual = first_children.get_individual()
        second_children_individual = second_children.get_individual()
        # Changes the individuals
        aux = first_children_individual[crossover_point:]
        first_children_individual[crossover_point:] = second_children_individual[crossover_point:]
        second_children_individual[crossover_point:] = aux
        # Set the changed individuals back to the children
        first_children.set_individual(first_children_individual)
        second_children.set_individual(second_children_individual)
        return [first_children, second_children]

    # Uniform Crossover
    def uniform_crossover(first_parent, second_parent, crossover_probability = 0.5):
        first_children = deepcopy(first_parent)
        second_children = deepcopy(second_parent)
        # Gets the individuals of each children
        first_children_individual = first_children.get_individual()
        second_children_individual = second_children.get_individual()
        probability_vector = [crossover_probability, 1 - crossover_probability]
        for i in range(first_parent.individual_size):
            # Changes the chromosome of first_children with second_children according to the probability
            if (np.random.choice([1,0], p = probability_vector)):
                aux = first_children_individual[i]
                first_children_individual[i] = second_children_individual[i]
                second_children_individual[i] = aux
        # Set the changed individuals back to the children
        first_children.set_individual(first_children_individual)
        second_children.set_individual(second_children_individual)
        return [first_children, second_children]

    # =============================================================================
    # Mutation
    # =============================================================================
    # Bit Flip Mutation
    def bit_flip_mutation(population, mutation_probability = 0.4, chromosome_mutation_probability = 0.3):
        for i in range(population[0].individual_size):
            # Probability of mutation of an individual
            probability_vector = [mutation_probability, 1 - mutation_probability]
            if (np.random.choice([1,0], p = probability_vector)):
                # Gets the individuals of the population
                population_individual = population[i].get_individual()
                for j in range(len(population_individual)):
                    # Probability of mutation of the chromosome
                    probability_vector = [chromosome_mutation_probability, 1 - chromosome_mutation_probability]
                    if (np.random.choice([1,0], p = probability_vector)):
                        # Changes 1 to 0, or 0 to 1
                        population_individual[j] = 1 - population_individual[j]
                # Set the changed individual back to the population
                population[i].set_individual(population_individual)
        return population

    # Swap Mutation
    def swap_mutation(population, mutation_probability = 0.4):
        for i in range(population[0].individual_size):
            # Probability of mutation of an individual
            probability_vector = [mutation_probability, 1 - mutation_probability]
            # Gets the individuals of the population
            population_individual = population[i].get_individual()
            if (np.random.choice([1,0], p = probability_vector)):
                # Select two random chromosomes to swap locations
                first_position = randint(0, len(population_individual) - 1)
                second_position = randint(0, len(population_individual) - 1)
                aux = population_individual[first_position]
                population_individual[first_position] = population_individual[second_position]
                population_individual[second_position] = aux
            # Set the changed individual back to the population
            population[i].set_individual(population_individual)
        return population