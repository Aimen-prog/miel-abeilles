from beehive import *

def main(num_generations):
    # Create a Hive object
    hive = Hive()
    # Load bee data from the Excel file 'Champ de pissenlits et de sauge des pres.xlsx'
    hive.getBees('Champ de pissenlits et de sauge des pres.xlsx')
    # List to store average fitness per generation
    fitness_per_generation = []
    # Run the genetic algorithm for the specified number of generations
    for gen in range(num_generations):
        # Select the top bees for further evolution
        hive.getSuperBees()
        # Perform mutation every 10 generations
        if gen % 10 == 0:
            hive.add_mutation()
        # Evolve the population using two-point crossover
        fitness_list = hive.evolve_population("classic")
        # Calculate and store the average fitness for the generation
        average_fitness = sum(fitness_list) / len(fitness_list)
        fitness_per_generation.append(average_fitness)
    # Plot the average fitness per generation
    hive.avg_fit_per_gen(num_generations, fitness_per_generation)
    # Plot the path of the best bee in the final generation
    hive.plot_best_bee_path()
    # Create a genealogy tree that represents the ancestry of the best bee for a maximum of 5 generations
    hive.create_genealogy_tree(min(5, num_generations))

if __name__ == "__main__":
    num_generations = 50  # number of generations
    main(num_generations)
