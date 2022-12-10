import numpy as np
import random

class Swap():
    def __init__(self):
        self.name = "Swap"
    def Mutate(self, Chromosome, Pm):
        random_shit = np.random.random()
        if random_shit < Pm:
            prob_size = len(Chromosome)
            genes = [np.random.randint(0, prob_size), np.random.randint(0, prob_size)]
            temp_value = Chromosome[genes[0]]
            Chromosome[genes[0]]=Chromosome[genes[1]]
            Chromosome[genes[1]] = temp_value
        return Chromosome


class Inversion():
    def __init__(self):
        self.name = "Inversion"
    def Mutate(self, Chromosome = [], Pm = 0.1):
        random_shit = np.random.random()
        if random_shit < Pm:
            prob_size = len(Chromosome)
            genes = sorted([np.random.randint(0, prob_size), np.random.randint(0, prob_size)])
            tempList = Chromosome[genes[0]:genes[1]]
            tempList.reverse()
            Chromosome[genes[0]:genes[1]] = tempList
        return Chromosome
class Scramble():
    def __init__(self):
        self.name = "Scramble"
    def Mutate(self, Chromosome = [], Pm = 0.1):
        random_shit = np.random.random()
        if random_shit < Pm:
            prob_size = len(Chromosome)
            genes = sorted([np.random.randint(0, prob_size), np.random.randint(0, prob_size)])
            tempList = Chromosome[genes[0]:genes[1]]
            random.shuffle(tempList)
            Chromosome[genes[0]:genes[1]] = tempList
        return Chromosome
