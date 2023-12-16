import random
import math
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx


class Bee:
    id_counter = 0
    def __init__(self):
        self.flowers = []
        self.fitness = 0
        self.hive = (500, 500)
        self.parent1 = None
        self.parent2 = None
        self.id = Bee.id_counter
        Bee.id_counter += 1

    def get_flowers(self, file):
        df = pd.read_excel(file)
        flowers = list(zip(df['x'], df['y']))
        self.flowers = random.sample(flowers, len(flowers))

    def fly(self):
        self.flowers.insert(0, self.hive) #start from the hive
        for flower in range(len(self.flowers)):
            x1, y1 = self.flowers[flower]
            x2, y2 = self.flowers[(flower + 1) % len(self.flowers)]
            self.fitness += int(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2))

class Hive:
    def __init__(self):
        self.beeFitness = {}
        self.superBeesFitness = []
        self.child_list = []
        self.parents_list = []
        self.super_bees = []
        self.best_bee = None

    def getBees(self, file):
        for i in range(100):
            bee = Bee()
            bee.get_flowers(file)
            bee.fly()
            self.beeFitness[bee] = bee.fitness


    def getSuperBees(self):
        sorted_by_fitness = dict(sorted(self.beeFitness.items(), key=lambda x: x[1]))
        self.super_bees = list(sorted_by_fitness.keys())[:50]
        self.superBeesFitness = list(sorted_by_fitness.values())[:50]


### Creation des generations

    def getChild(self, flowers, p1, p2):
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

    def evolve_population(self):
        current_population = self.super_bees[:]
        best_bee = min(current_population, key=lambda x: x.fitness)
        if self.best_bee is None or best_bee.fitness < self.best_bee.fitness:
            self.best_bee = best_bee
        for i in range(25):
            parent1 = random.choice(current_population)
            current_population.remove(parent1)
            parent2 = random.choice(current_population)
            current_population.remove(parent2)
            child1_flower_list = parent1.flowers[:math.floor(len(parent1.flowers) / 2)] + [x for x in parent2.flowers if x not in parent1.flowers[:math.floor(len(parent1.flowers) / 2)]]
            child2_flower_list = parent2.flowers[:math.floor(len(parent2.flowers) / 2)] + [x for x in parent1.flowers if x not in parent2.flowers[:math.floor(len(parent2.flowers) / 2)]]
            # Generate child bees using the new flower lists
            children = self.getChild((child1_flower_list, child2_flower_list), parent1, parent2)
            # Add the children to the next generation
            self.child_list.extend([children[0], children[1]])
        #add the generation to the population
        self.super_bees += self.child_list
        self.child_list.clear()
        self.parents_list.clear()
        fitness_list = [bee.fitness for bee in self.super_bees]
        self.beeFitness = {}
        for bee in self.super_bees:
            self.beeFitness[bee] = bee.fitness
        return fitness_list

    def avg_fit_per_gen(self, x, y):
        plt.plot(range(x), y)
        plt.xlabel('Generation')
        plt.ylabel('Average Fitness')
        plt.title('Average Fitness per Generation')
        plt.show()


    def swap_mutation(self):
        current_population = self.super_bees
        bee = random.choice(current_population)
        i, j = random.sample(range(len(bee.flowers)), 2)
        bee.flowers[i], bee.flowers[j] = bee.flowers[j], bee.flowers[i]

    def reverse_mutation(self):
        current_population = self.super_bees
        bee = random.choice(current_population)
        i, j = sorted(random.sample(range(len(bee.flowers)), 2))
        bee.flowers[i:j+1] = reversed(bee.flowers[i:j+1])

    def add_mutation(self):
        mutation_type = random.choice(['swap', 'reverse'])
        if mutation_type == 'swap':
            self.swap_mutation()
        elif mutation_type == 'reverse':
            self.reverse_mutation()

    def plot_best_bee_path(self):
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

    # def create_genealogy_tree(self):
    #     graph = nx.DiGraph()
    #     current_bee = self.best_bee
    #     tmp = [current_bee]
    #     while tmp:
    #         current_bee = tmp[0]
    #         graph.add_node(current_bee.id, label=f"Bee {current_bee.id}", color="red")
    #         if current_bee.parent1:
    #             graph.add_edge(current_bee.parent1.id, current_bee.id)
    #
    #         if current_bee.parent2:
    #             graph.add_edge(current_bee.parent2.id, current_bee.id)
    #
    #         tmp = tmp[1:]
    #         if current_bee.parent1:
    #             tmp.append(current_bee.parent1)
    #         if current_bee.parent2:
    #             tmp.append(current_bee.parent2)
    #     pos = nx.spring_layout(graph)
    #     # Set color for nodes based on the 'color' attribute
    #     node_colors = ["pink" if node == self.best_bee.id else "skyblue" for node in graph.nodes]
    #     labels = nx.get_edge_attributes(graph, 'label')
    #     nx.draw(graph, pos, with_labels=True, node_size=600, node_color=node_colors, font_size=10, font_color="black",
    #             font_weight="bold")
    #     nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    #     plt.show()





    def create_genealogy_tree(self, num_generations):
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





