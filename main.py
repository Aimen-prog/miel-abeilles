from beehive import *

def main(num_generations):
    hive = Hive()
    hive.getBees('/home/cherif/Bureau/abeilles/Champ de pissenlits et de sauge des pres.xlsx')
    fitness_per_generation = []
    for gen in range(num_generations):
        hive.getSuperBees()
        # if gen % 10 == 0:
        #     hive.add_mutation()
        fitness_list = hive.evolve_population()
        average_fitness = sum(fitness_list) / len(fitness_list)
        fitness_per_generation.append(average_fitness)
    hive.avg_fit_per_gen(num_generations, fitness_per_generation)


if __name__ == "__main__":
    num_generations = 100  # number of generations
    main(num_generations)