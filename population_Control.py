from urllib.request import proxy_bypass
import numpy as np
import random
# from Fitness import *
class pop_control():
    def __init__(self, population_size, problem_txt = "P1.txt"):
        self.population_size = population_size
        X = []
        Y = []
        demand = []
        with open(problem_txt) as f:
            lines = f.readlines()
            for line in lines:
                cols = line.split(" ")
                if cols[0]!= 'number':
                    X.append(int(cols[1]))
                    Y.append(int(cols[2]))
                    demand.append(int(cols[3][:cols[3].find("\n")]))
        self.XYDemand = [X, Y, demand]

    def creat_population_prob(self):
        self.population = []
        for _ in range(self.population_size):
            chromosome = list(range(len(self.XYDemand[0])))
            random.shuffle(chromosome)
            self.population.append(chromosome)
class pop_control2():
    def __init__(self, population_size, problem_txt = "P2.txt"):
        self.population_size = population_size
        X = []
        Y = []
        demand = []
        with open(problem_txt) as f:
            lines = f.readlines()
            for line in lines:
                cols = line.split(" ")
                if cols[0]!= 'number':
                    X.append(int(cols[1]))
                    Y.append(int(cols[2]))
                    demand.append(int(cols[3][:cols[3].find("\n")]))
        self.XYDemand = [X, Y, demand]

    def creat_population_prob(self):
        self.population = []
        for _ in range(self.population_size):
            chromosome = list(range(len(self.XYDemand[0])))
            random.shuffle(chromosome)
            self.population.append(chromosome)