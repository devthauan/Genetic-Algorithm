from copy import deepcopy
from random import randint

class Individual:
    def __init__(self, name, individual_creation_method , products, fitness_method, individual_size, max_truck_volume):
        self.name = name
        self.individual_size = individual_size
        self.products = products
        self.max_truck_volume = max_truck_volume
        self.individual_creation_method = individual_creation_method
        self.individual =  self.create_individual()
        self.fitness_method = fitness_method
        self.fitness_value = self.calculate_fitness()
        self.volume = self.volume_calculation()

    
    def calculate_fitness(self):
        if(self.fitness_method == "profit_fitness"):
            fitness_value = self.profit_fitness()
        elif(self.fitness_method == "punitive_fitness"):
            fitness_value = self.punitive_fitness()
        return fitness_value
    
    def create_individual(self):
        if(self.individual_creation_method == "random_individuals"):
            individual = self.random_individuals() 
        elif(self.individual_creation_method == "individuals_that_fit"):
            individual = self.individuals_that_fit() 
        return individual


    def get_individual(self):
        return self.individual
    
    def set_individual(self, individual):
        self.individual = individual
        self.fitness_value = self.calculate_fitness()
        self.volume = self.volume_calculation()
        
    # Creates a random individual
    def random_individuals(self) -> list:
        return [randint(0,1) for i in range(self.individual_size)]


    # Creates and individual that fits in the truck
    def individuals_that_fit(self):
        all_products = deepcopy(self.products)  # Creates a copy of the products
        individual = [0] * self.individual_size # Creates an empty individual
        current_volume = 0
        while(True):
            # Select a random product index
            chossen_product_index = randint(0, len(all_products)-1)
            # checks if the individual with the addition of the selected product fits in the truck
            if current_volume + all_products[chossen_product_index].volume <= self.max_truck_volume:
                product_name = all_products[chossen_product_index].name
                # Gets the position of this product in the list "all_products"
                product_position = next((i for i, item in enumerate(self.products) if item.name == product_name), -1)
                individual[product_position] = 1
                current_volume += self.products[product_position].volume
                del(all_products[chossen_product_index]) # Deletes this product from the list of products
            else:
                break
        return individual
    

    # fitness function that calculates the profit
    def profit_fitness(self):
        value = 0
        for i in range(len(self.individual)):
            if (self.individual[i] == 1):
                value += self.products[i].value
        return value

    
    def volume_calculation(self):
        volume = 0
        for i in range(len(self.individual)):
            if (self.individual[i] == 1):
                volume += self.products[i].volume
        return volume


    # fitness que pune os individuos que passam o limite do caminhão
    def punitive_fitness(self):
        value = self.profit_fitness()
        volume = self.volume_calculation()
        if (volume > self.max_truck_volume):
            extra_load_percentage = (volume / self.max_truck_volume) -1
            value = value - (value * extra_load_percentage)
        return value