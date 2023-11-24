import random
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
class Bee:
    def __init__(self):
        self.flowers = []
        self.fitness = 0
        self.hive = (500, 500)

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
        self.superBees = []
        self.child_list = []
        self.superBees_id = []

    def getBees(self, file):
        for i in range(100):
            bee = Bee()
            bee.get_flowers(file)
            bee.fly()
            self.beeFitness[bee] = bee.fitness


    def getSuperBees(self):
        sorted_by_fitness = dict(sorted(self.beeFitness.items(), key=lambda x: x[1]))
        self.superBees_id = list(sorted_by_fitness.keys())[:50]
        self.superBees = list(sorted_by_fitness.values())[:50]


### Creation des generations

    def getChild(self, flowers):
        child1 = Bee()
        child2 = Bee()
        child1.flowers = flowers[0]
        child2.flowers = flowers[1]
        child1.fly()
        child2.fly()
        return child1, child2

    def evolve_population(self):
        current_population = self.superBees_id[:]
        for i in range(25):
            parent1 = random.choice(current_population)
            current_population.remove(parent1)
            parent2 = random.choice(current_population)
            current_population.remove(parent2)
            child1_flower_list = parent1.flowers[:math.floor(len(parent1.flowers) / 2)] + [x for x in parent2.flowers if x not in parent1.flowers[:math.floor(len(parent1.flowers) / 2)]]
            child2_flower_list = parent2.flowers[:math.floor(len(parent2.flowers) / 2)] + [x for x in parent1.flowers if x not in parent2.flowers[:math.floor(len(parent2.flowers) / 2)]]
            # Generate child bees using the new flower lists
            children = self.getChild((child1_flower_list, child2_flower_list))
            # Add the children to the next generation
            self.child_list.extend([children[0], children[1]])
        #add the generation to the population
        self.superBees_id += self.child_list
        self.child_list.clear()
        fitness_list = [bee.fitness for bee in self.superBees_id]
        self.beeFitness = {}
        for bee in self.superBees_id:
            self.beeFitness[bee] = bee.fitness
        return fitness_list

    def avg_fit_per_gen(self, x, y):
        plt.plot(range(x), y)
        plt.xlabel('Generation')
        plt.ylabel('Average Fitness')
        plt.title('Average Fitness per Generation')
        plt.show()


    def add_mutation(self):
        current_population = self.superBees_id
        bee = random.choice(current_population)
        i = random.randint(0, len(bee.flowers) - 1)
        bee.flowers = bee.flowers[i:] + bee.flowers[:i]









