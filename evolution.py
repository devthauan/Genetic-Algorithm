import math
from products import Product
import matplotlib.pyplot as plt
from random import randint
from random import uniform
from copy import deepcopy
from individuals import Individual
from genetic_operators import GeneticOperators


class Evolution:

    # Function that drops individuals that doesn't fit the truck
    def extra_load_drop_individuals(population):
        # Sorts population by volume
        population = sorted(population, key=lambda x: x.volume, reverse=False)
        # Get the index of the sorted population where the volume of the individual doesn't fit the truck
        try:
            index = [index for index, individual in enumerate(population) if individual.volume > individual.max_truck_volume][0]
            population = population[:index]
        except:
            pass
        return population
    
    
    def expand_population(population, porcentage_new_elements, population_size, selection_method, k, crossover_method, crossover_probability):
        new_population = []
        # Selection until  =~150% total population
        for _ in range(int((population_size * porcentage_new_elements) / 2)):
            
            # Select two individuals according to the selection method chosen
            if (selection_method == "roulette wheel"):
                fisrt_individual = GeneticOperators.roulette_wheel_selection(population)
                second_individual = GeneticOperators.roulette_wheel_selection(population)
            elif (selection_method == "tournament"):
                fisrt_individual = GeneticOperators.tournament_selection(population, k)
                second_individual = GeneticOperators.tournament_selection(population, k)
                
            # Crossover according to the selection method chosen
            if (crossover_method == "single_point_crossover"):
                new_children = GeneticOperators.single_point_crossover(fisrt_individual, second_individual)
            elif (crossover_method == "uniform_crossover"):
                new_children = GeneticOperators.uniform_crossover(fisrt_individual, second_individual, crossover_probability)
                
            # Adds the new children to the population
            new_population.append(new_children[0])
            new_population.append(new_children[1])
        return new_population
    


    def evolution(population, population_size, selection_method, crossover_probability, k, crossover_method, mutation_method, mutation_probability, chromosome_mutation_probability, evolution_method):
        # Average fitness value for each generation
        population_average_fitness = [0]*1
       # Highest fitness value for each generation
        highest_fitness_per_generation = []
        # Lowest fitness value for each generation
        lowest_fitness_per_generation = []
        # Contador de geraçoes sem mudar a média
        generation_count = 0
        generation = 0
        counter = 0
        while (True):
            # Drops individuals that doesn't fit in the truck
            population = Evolution.extra_load_drop_individuals(population)
            
            if(evolution_method == "ancestral"):
                new_population = Evolution.expand_population(population, 0.5, population_size, selection_method, k, crossover_method, crossover_probability)
                new_population = new_population + population
                
            elif(evolution_method == "elite"):
                new_population = Evolution.expand_population(population, 0.9, population_size, selection_method, k, crossover_method, crossover_probability)
                
            
            # Mutates
            if (mutation_method == "bit_flip_mutation"):
                new_population = GeneticOperators.bit_flip_mutation(new_population, mutation_probability, chromosome_mutation_probability)
            elif (mutation_method == "swap_mutation"):
                new_population = GeneticOperators.swap_mutation(new_population, mutation_probability)
            
            if(evolution_method == "ancestral"):
                # Drops individuals that doesn't fit in the truck
                new_population = Evolution.extra_load_drop_individuals(new_population)
                # Ranks the population by fitness value
                new_population = GeneticOperators.ranking(new_population)
                # Takes the best individuals until original population size is restored and deletes the rest
                population = new_population[:population_size]
                
            elif(evolution_method == "elite"):
                # Drops individuals that doesn't fit in the truck
                new_population = Evolution.extra_load_drop_individuals(new_population)
                # Ranks the population by fitness value
                population = GeneticOperators.ranking(population)
                # Joins the new population with the 10% of the best individuals from the past population (elite) 
                new_population.extend(population[:int(len(population) * 0.1)])
                # Ranks the population by fitness value
                population = GeneticOperators.ranking(new_population)
            
            
            
            # Calculates some information about the population to improve upon next
            population_average_fitness.append( sum([population[i].fitness_value for i in range(len(population))]) / len(population) )            
            lowest_fitness_per_generation.append(population[-1].fitness_value)
            highest_fitness_per_generation.append(population[0].fitness_value)
            
            # Checks if the population average fitness improved
            if (population_average_fitness[-1] <= population_average_fitness[-2]):
                generation_count += 1
            else:
                generation_count = 0
            # Stops if the population doesn't improve during 20 generations
            if (generation_count >= 20):
                break
            counter += 1
            # Stops after 100 generations
            if (counter > 100):
                break
            generation += 1
        best_result = GeneticOperators.ranking(population)[0]
        plt.figure(figsize=(12,8))  
        plt.plot(population_average_fitness[1:], label="Average fitness_value", color="orange", linewidth=3)
        plt.plot(lowest_fitness_per_generation, label="Lowest fitness_value", color="red", linewidth=2)
        plt.plot(highest_fitness_per_generation, label="Highest fitness_value", color="green", linewidth=2)
        plt.legend(loc='upper left')
        plt.show()
        print("Generations required: ", generation)
        return best_result, population_average_fitness[1:], lowest_fitness_per_generation, highest_fitness_per_generation