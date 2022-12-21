from urllib.request import proxy_bypass
import numpy as np
import random
# from Fitness import *

def evaluate_distance(state1 = [-25, 25], state2 = [20, 20]):
    return (abs(state1[0] - state2[0]) + abs(state1[1] - state2[1]))
    
def SortEachchro(X = [], Y = []):
    All_Sorted = []
    for index in range(len(X)):
        EachSorted = []
        Gens_index = []
        x_g = X[index]
        y_g = Y[index]
        for indexx in range(len(X)):
            if index != indexx:
                EachSorted.append(evaluate_distance([X[indexx], Y[indexx]], [x_g, y_g]))
                Gens_index.append(indexx)
        EachSorted, Gens_index = zip(*sorted(zip(EachSorted, Gens_index)))
        # print(EachSorted)
        # print(Gens_index)
        # exit()
        All_Sorted.append(list(Gens_index))
    return All_Sorted
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
        self.All_SortedDistances = SortEachchro(X, Y)

    def creat_population_prob(self):
        self.population = []
        for _ in range(self.population_size):
            chromosome = list(range(len(self.XYDemand[0])))
            random.shuffle(chromosome)
            self.population.append(chromosome)


class pop_control5():
    def __init__(self, population_size, problem_txt = "P5.txt", number_of_vehicles = 5):
        self.numOFVeh = number_of_vehicles
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
        self.All_SortedDistances = SortEachchro(X, Y)

    def creat_population_prob(self):
        self.population = []
        for _ in range(self.population_size):
            chromosome = list(range(len(self.XYDemand[0])))
            random.shuffle(chromosome)
            for i in range(11):
                chromosome.append(np.random.randint(0,3))
            self.population.append(chromosome)



class pop_control6():
    def __init__(self, population_size, problem_txt = "P5.txt", number_of_vehicles = 5):
        self.numOFVeh = number_of_vehicles
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
            for i in range(7):
                chromosome.append(np.random.randint(0,2))
            self.population.append(chromosome)