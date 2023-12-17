import random
import math
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

class Bee:
    id_counter = 0

    def __init__(self):
        """
        Initialize a Bee object.

        Attributes:
        - flowers: List of flower coordinates representing the bee's path.
        - fitness: Fitness value of the bee's path.
        - hive: Hive coordinates.
        - parent1: Reference to the first parent bee during crossover.
        - parent2: Reference to the second parent bee during crossover.
        - id: Unique identifier for each bee.
        """
        self.flowers = []
        self.fitness = 0
        self.hive = (500, 500)
        self.parent1 = None
        self.parent2 = None
        self.id = Bee.id_counter
        Bee.id_counter += 1

    def get_flowers(self, file):
        """
        Read flower coordinates from an Excel file and assign them to the bee.

        Parameters:
        - file: Path to the Excel file containing flower coordinates.
        """
        df = pd.read_excel(file)
        flowers = list(zip(df['x'], df['y']))
        self.flowers = random.sample(flowers, len(flowers))

    def fly(self):
        """
        Calculate the fitness of the bee's path based on Euclidean distance between flowers.
        """
        self.flowers.insert(0, self.hive)  # Start from the hive
        for flower in range(len(self.flowers)):
            x1, y1 = self.flowers[flower]
            x2, y2 = self.flowers[(flower + 1) % len(self.flowers)]
            self.fitness += int(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2))

class Hive:
    def __init__(self):
        """
        Initialize a Hive object.

        Attributes:
        - beeFitness: Dictionary to store bee objects and their fitness values.
        - superBeesFitness: List to store the fitness values of the top bees.
        - child_list: List to store child bees during evolution.
        - parents_list: List to store parent bees during evolution.
        - super_bees: List to store the top bees in the population.
        - best_bee: Reference to the best bee in the population.
        """
        self.beeFitness = {}
        self.superBeesFitness = []
        self.child_list = []
        self.parents_list = []
        self.super_bees = []
        self.best_bee = None

    def getBees(self, file):
        """
        Generate bee objects, assign flowers, and calculate fitness for each bee.

        Parameters:
        - file: Path to the Excel file containing flower coordinates.
        """
        for i in range(100):
            bee = Bee()
            bee.get_flowers(file)
            bee.fly()
            self.beeFitness[bee] = bee.fitness

    def getSuperBees(self):
        """
        Select the top 50 bees based on fitness for further evolution.
        """
        sorted_by_fitness = dict(sorted(self.beeFitness.items(), key=lambda x: x[1]))
        self.super_bees = list(sorted_by_fitness.keys())[:50]
        self.superBeesFitness = list(sorted_by_fitness.values())[:50]

    def getChild(self, flowers, p1, p2):
        """
        Create child bee objects by combining flower lists of two parent bees.

        Parameters:
        - flowers: Tuple containing two flower lists for the child bees.
        - p1: First parent bee.
        - p2: Second parent bee.

        Returns:
        - Tuple containing two child bee objects.
        """
        child1 = Bee()
        child2 = Bee()
        child1.flowers = flowers[0]
        child2.flowers = flowers[1]
        child1.fly()
        child2.fly()
        child1.parent1 = p1
        child2.parent1 = p1
        child1.parent2 = p2
        child2.parent2 = p2
        return child1, child2

    def two_point_crossover(self, parent1, parent2):
        """
        Perform two-point crossover to create two child bees.

        Parameters:
        - parent1: First parent bee.
        - parent2: Second parent bee.

        Returns:
        - Tuple containing two child bee objects.
        """
        crossover_points = sorted(random.sample(range(1, len(parent1.flowers)), 2))
        start, end = crossover_points
        child1_flower_list = (
            parent1.flowers[:start] +
            [x for x in parent2.flowers if x not in parent1.flowers[:start]] +
            parent1.flowers[end:]
        )
        child2_flower_list = (
            parent2.flowers[:start] +
            [x for x in parent1.flowers if x not in parent2.flowers[:start]] +
            parent2.flowers[end:]
        )
        children = self.getChild((child1_flower_list, child2_flower_list), parent1, parent2)
        return children

    def evolve_population(self, crossover):
        """
        Evolve the population through crossover and mutation.

        Parameters:
        - crossover: Type of crossover ("classic" or "twopoint").

        Returns:
        - List of fitness values for the evolved population.
        """
        current_population = self.super_bees[:]
        best_bee = min(current_population, key=lambda x: x.fitness)
        if self.best_bee is None or best_bee.fitness < self.best_bee.fitness:
            self.best_bee = best_bee
        for i in range(25):
            parent1 = random.choice(current_population)
            current_population.remove(parent1)
            parent2 = random.choice(current_population)
            current_population.remove(parent2)
            if crossover == "classic":
                child1_flower_list = parent1.flowers[:math.floor(len(parent1.flowers) / 2)] + [x for x in parent2.flowers if x not in parent1.flowers[:math.floor(len(parent1.flowers) / 2)]]
                child2_flower_list = parent2.flowers[:math.floor(len(parent2.flowers) / 2)] + [x for x in parent1.flowers if x not in parent2.flowers[:math.floor(len(parent2.flowers) / 2)]]
                # Generate child bees using the new flower lists
                children = self.getChild((child1_flower_list, child2_flower_list), parent1, parent2)
            elif crossover == "twopoint":
                children = self.two_point_crossover(parent1, parent2)
            # Add the children to the next generation
            self.child_list.extend([children[0], children[1]])
        # Add the generation to the population
        self.super_bees += self.child_list
        self.child_list.clear()
        self.parents_list.clear()
        fitness_list = [bee.fitness for bee in self.super_bees]
        self.beeFitness = {}
        for bee in self.super_bees:
            self.beeFitness[bee] = bee.fitness
        return fitness_list

    def avg_fit_per_gen(self, x, y):
        """
        Plot the average fitness per generation.

        Parameters:
        - x: Number of generations.
        - y: List of average fitness values.
        """
        plt.plot(range(x), y)
        plt.xlabel('Generation')
        plt.ylabel('Average Fitness')
        plt.title('Average Fitness per Generation')
        plt.show()

    def swap_mutation(self):
        """
        Perform swap mutation on a randomly selected bee in the population.
        """
        current_population = self.super_bees
        bee = random.choice(current_population)
        i, j = random.sample(range(len(bee.flowers)), 2)
        bee.flowers[i], bee.flowers[j] = bee.flowers[j], bee.flowers[i]

    def reverse_mutation(self):
        """
        Perform reverse mutation on a randomly selected bee in the population.
        """
        current_population = self.super_bees
        bee = random.choice(current_population)
        i, j = sorted(random.sample(range(len(bee.flowers)), 2))
        bee.flowers[i:j+1] = reversed(bee.flowers[i:j+1])

    def add_mutation(self):
        """
        Apply either swap or reverse mutation randomly to the population.
        """
        mutation_type = random.choice(['swap', 'reverse'])
        if mutation_type == 'swap':
            self.swap_mutation()
        elif mutation_type == 'reverse':
            self.reverse_mutation()

    def plot_best_bee_path(self):
        """
        Plot the path of the best bee in the population.
        """
        x = [point[0] for point in self.best_bee.flowers]
        y = [point[1] for point in self.best_bee.flowers]

        plt.figure(figsize=(8, 8))
        plt.plot(x, y, marker='o', linestyle='-')
        plt.plot(*self.best_bee.hive, color='red', marker='o', label='Hive')
        plt.xlabel('X-coordinate')
        plt.ylabel('Y-coordinate')
        plt.title('Path of the Best Bee')
        plt.legend()
        plt.show()

    def create_genealogy_tree(self, num_generations):
        """
        Create a genealogy tree that represents the ancestry of the best bee using networkx & matplotlib.

        Parameters:
        - num_generations: Number of generations
        """
        graph = nx.DiGraph()
        best_bee_history = [self.best_bee]

        for generation in range(num_generations):
            current_bee = best_bee_history[-1]
            graph.add_node(current_bee.id, label=f"Bee {current_bee.id}", color="red")

            if current_bee.parent1:
                graph.add_edge(current_bee.parent1.id, current_bee.id)

            if current_bee.parent2:
                graph.add_edge(current_bee.parent2.id, current_bee.id)

            if current_bee.parent1:
                best_bee_history.append(current_bee.parent1)

            if current_bee.parent2:
                best_bee_history.append(current_bee.parent2)

        pos = nx.spring_layout(graph)
        # Set color for nodes based on the 'color' attribute
        node_colors = ["pink" if node == self.best_bee.id else "skyblue" for node in graph.nodes]
        labels = nx.get_edge_attributes(graph, 'label')
        nx.draw(graph, pos, with_labels=True, node_size=600, node_color=node_colors, font_size=10, font_color="black",
                font_weight="bold")
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
        plt.show()
