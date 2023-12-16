from beehive import *


def main(num_generations):
    hive = Hive()
    hive.getBees('Champ de pissenlits et de sauge des pres.xlsx')
    fitness_per_generation = []

    for gen in range(num_generations):
        hive.getSuperBees()
        if gen % 10 == 0:
            hive.add_mutation()
        fitness_list = hive.evolve_population()
        average_fitness = sum(fitness_list) / len(fitness_list)
        fitness_per_generation.append(average_fitness)

    hive.avg_fit_per_gen(num_generations, fitness_per_generation)
    hive.plot_best_bee_path()
    hive.create_genealogy_tree(min(5, num_generations))  # Use min to ensure it doesn't exceed the available generations

if __name__ == "__main__":
    num_generations = 10  # number of generations
    main(num_generations)