import numpy as np
import math
from simulation_output import *
import matplotlib.pyplot as plt
from population_Control import *
class Fitness_func_for_prob1:
    def __init__(self, depoteLocation = [0, 0], XYDemand = [[], [], []]):
        self.XYDemand = XYDemand
        self.depoteLocation = depoteLocation
        pass
    def evaluate_distance(self, state1 = [-25, 25], state2 = [20, 20]):
        return - (abs(state1[0] - state2[0]) + abs(state1[1] - state2[1]))
    def evaluate_eachPeople(self, people):
        vehicle = 1
        vehicles_last_position = [[self.depoteLocation[0], self.depoteLocation[1]]] * 6
        demand_vehicle_get = 0
        Fitness = 0
        index_gene = -1
        for gene in people:
            index_gene+=1
            while True:
                if demand_vehicle_get<=70:
                    Fitness = Fitness + self.evaluate_distance(vehicles_last_position[vehicle-1], [self.XYDemand[0][gene], self.XYDemand[1][gene]])
                    vehicles_last_position[vehicle-1] = [self.XYDemand[0][gene], self.XYDemand[1][gene]]
                    demand_vehicle_get = demand_vehicle_get + self.XYDemand[2][gene]
                    break
                else:
                    Fitness = Fitness + self.evaluate_distance(vehicles_last_position[vehicle-1], [self.depoteLocation[0], self.depoteLocation[1]])
                    vehicles_last_position[vehicle-1] = [self.depoteLocation[0], self.depoteLocation[1]]
                    demand_vehicle_get = 0
                    vehicle+=1
                    if vehicle == 7:
                        vehicle = 1
            if index_gene == len(people) - 1:
                Fitness = Fitness + self.evaluate_distance(vehicles_last_position[vehicle-1], [self.depoteLocation[0], self.depoteLocation[1]])
        return Fitness
    def evaluate_fitness(self, population = []):
        Fitnesses = []
        for people in population:
            Fitnesses.append(self.evaluate_eachPeople(people = people))
        self.Fitnesses = Fitnesses

    def update_mate_probs(self, fitnesses):
        mate_pop = []
        new_fitness = fitnesses.copy()
        new_fitness = [x+7000 for x in new_fitness]
        new_fitness = [x-min(new_fitness) for x in new_fitness]
        for i in range(len(fitnesses)):
            if np.sum(fitnesses)!=0:
                mate_pop.append(new_fitness[i]/np.sum(new_fitness))
            else:
                mate_pop.append(new_fitness[i])
        return mate_pop
    def draw_simulation(self, people, simulation_obj):
        for i in range(len(self.XYDemand[0][:])):
            simulation_obj.colored_specific_sq(self.XYDemand[0][i], self.XYDemand[1][i])
        vehicle = 1
        vehicles_last_position = [[self.depoteLocation[0], self.depoteLocation[1]]] * 6
        demand_vehicle_get = 0
        index_gene = -1
        # colors = np.random.randint(0, 255, (7, 3), dtype=np.int)
        colors = np.array([[0, 0, 128], 
                            [20, 215, 215], 
                            [128, 255, 128],
                            [128, 0, 0], 
                            [48, 130, 245], 
                            [180, 30, 145],
                            [75, 25, 230]])
        for gene in people:
            index_gene+=1
            while True:
                if demand_vehicle_get<=70:
                    simulation_obj.draw_arrow(x = [vehicles_last_position[vehicle-1][0], self.XYDemand[0][gene]], y = [vehicles_last_position[vehicle-1][1], self.XYDemand[1][gene]], color = colors[vehicle-1, :])
                    vehicles_last_position[vehicle-1] = [self.XYDemand[0][gene], self.XYDemand[1][gene]]
                    demand_vehicle_get = demand_vehicle_get + self.XYDemand[2][gene]
                    break
                else:
                    simulation_obj.draw_arrow(x = [vehicles_last_position[vehicle-1][0], self.depoteLocation[0]], y = [vehicles_last_position[vehicle-1][1], self.depoteLocation[1]], color = colors[vehicle-1, :])
                    vehicles_last_position[vehicle-1] = [self.depoteLocation[0], self.depoteLocation[1]]
                    demand_vehicle_get = 0
                    vehicle+=1
                    if vehicle == 7:
                        vehicle = 1
            if index_gene == len(people) - 1:
                simulation_obj.draw_arrow(x = [vehicles_last_position[vehicle-1][0], self.depoteLocation[0]], y = [vehicles_last_position[vehicle-1][1], self.depoteLocation[1]], color = colors[vehicle-1, :])




class Fitness_func_for_prob2:
    def __init__(self, depoteLocation = [0, 0], XYDemand = [[], [], []]):
        self.XYDemand = XYDemand
        self.depoteLocation = depoteLocation
        pass
    def evaluate_distance(self, state1 = [-25, 25], state2 = [20, 20]):
        return (abs(state1[0] - state2[0]) + abs(state1[1] - state2[1]))
    def evaluate_eachPeople(self, people):
        vehicle = 1
        vehicles_last_position = [[self.depoteLocation[0], self.depoteLocation[1]]] * 4
        all_distance = 0
        Fitness = 0
        fitness_distance = 0
        howmany_ = 0
        next_vehicle = False
        for gene in people:
            if vehicle <= 4:
                while True:
                    if not next_vehicle:
                        all_distance = all_distance + self.evaluate_distance(vehicles_last_position[vehicle-1], [self.XYDemand[0][gene], self.XYDemand[1][gene]])
                        if all_distance <= 200:
                            Fitness = Fitness + 1 - 2*self.evaluate_distance(vehicles_last_position[vehicle-1], [self.XYDemand[0][gene], self.XYDemand[1][gene]])/200
                        vehicles_last_position[vehicle-1] = [self.XYDemand[0][gene], self.XYDemand[1][gene]]

                        if all_distance + self.evaluate_distance(vehicles_last_position[vehicle-1], [self.depoteLocation[0], self.depoteLocation[1]]) > 200:
                            next_vehicle = True
                            all_distance = 0    
                        else:
                            break
                    else:
                        next_vehicle = False
                        vehicles_last_position[vehicle-1] = [self.depoteLocation[0], self.depoteLocation[1]]
                        all_distance = 0
                        vehicle+=1
                        if vehicle == 5:
                            break
            else:
                break
        return Fitness
    def evaluate_fitness(self, population = []):
        Fitnesses = []
        for people in population:
            Fitnesses.append(self.evaluate_eachPeople(people = people))
        self.Fitnesses = Fitnesses

    def update_mate_probs(self, fitnesses):
        mate_pop = []
        for i in range(len(fitnesses)):
            if np.sum(fitnesses)!=0:
                mate_pop.append(fitnesses[i]/np.sum(fitnesses))
            else:
                mate_pop.append(fitnesses[i])
        return mate_pop
    def draw_simulation(self, people, simulation_obj):
        for i in range(len(self.XYDemand[0][:])):
            simulation_obj.colored_specific_sq(self.XYDemand[0][i], self.XYDemand[1][i])
        vehicle = 1
        vehicles_last_position = [[self.depoteLocation[0], self.depoteLocation[1]]] * 4
        demand_vehicle_get = 0
        index_gene = -1
        # colors = np.random.randint(0, 255, (7, 3), dtype=np.int)
        colors = np.array([[0, 0, 128], 
                            [20, 215, 215], 
                            [128, 255, 128],
                            [128, 0, 0], 
                            [48, 130, 245], 
                            [180, 30, 145],
                            [75, 25, 230]])

        vehicle = 1
        vehicles_last_position = [[self.depoteLocation[0], self.depoteLocation[1]]] * 4
        all_distance = 0
        next_vehicle = False
        for gene in people:
            # print(vehicle)
            if vehicle <= 4:
                while True:
                    if not next_vehicle:
                        all_distance = all_distance + self.evaluate_distance(vehicles_last_position[vehicle-1], [self.XYDemand[0][gene], self.XYDemand[1][gene]])
                        if all_distance < 200:
                            simulation_obj.draw_arrow(x = [vehicles_last_position[vehicle-1][0], self.XYDemand[0][gene]], y = [vehicles_last_position[vehicle-1][1], self.XYDemand[1][gene]], color = colors[vehicle-1, :])
                            vehicles_last_position[vehicle-1] = [self.XYDemand[0][gene], self.XYDemand[1][gene]]
                        if all_distance + self.evaluate_distance(vehicles_last_position[vehicle-1], [self.depoteLocation[0], self.depoteLocation[1]]) > 200:
                            next_vehicle = True
                        else:
                            break
                    else:
                        simulation_obj.draw_arrow(x = [vehicles_last_position[vehicle-1][0], self.depoteLocation[0]], y = [vehicles_last_position[vehicle-1][1], self.depoteLocation[1]], color = colors[vehicle-1, :])
                        vehicles_last_position[vehicle-1] = [self.depoteLocation[0], self.depoteLocation[1]]
                        all_distance = 0
                        next_vehicle = False
                        vehicle+=1
                        break
            else:
                break




class Fitness_func_for_prob3:
    def __init__(self, depoteLocation = [0, 0], XYDemand = [[], [], []]):
        self.XYDemand = XYDemand
        self.depoteLocation = depoteLocation
        pass
    def evaluate_distance(self, state1 = [-25, 25], state2 = [20, 20]):
        return (abs(state1[0] - state2[0]) + abs(state1[1] - state2[1]))
    def evaluate_eachPeople(self, people):
        vehicle = 1
        vehicles_last_position = [[self.depoteLocation[0], self.depoteLocation[1]]] * 4
        all_distance = 0
        Fitness = 0
        fitness_distance = 0
        howmany_ = 0
        next_vehicle = False
        for gene in people:
            if vehicle <= 4:
                while True:
                    if not next_vehicle:
                        all_distance = all_distance + self.evaluate_distance(vehicles_last_position[vehicle-1], [self.XYDemand[0][gene], self.XYDemand[1][gene]])
                        if all_distance <= 200:
                            Fitness = Fitness + self.XYDemand[2] - 2*self.evaluate_distance(vehicles_last_position[vehicle-1], [self.XYDemand[0][gene], self.XYDemand[1][gene]])/200
                        vehicles_last_position[vehicle-1] = [self.XYDemand[0][gene], self.XYDemand[1][gene]]

                        if all_distance + self.evaluate_distance(vehicles_last_position[vehicle-1], [self.depoteLocation[0], self.depoteLocation[1]]) > 200:
                            next_vehicle = True
                            all_distance = 0    
                        else:
                            break
                    else:
                        next_vehicle = False
                        vehicles_last_position[vehicle-1] = [self.depoteLocation[0], self.depoteLocation[1]]
                        all_distance = 0
                        vehicle+=1
                        if vehicle == 5:
                            break
            else:
                break
        return Fitness
    def evaluate_fitness(self, population = []):
        Fitnesses = []
        for people in population:
            Fitnesses.append(self.evaluate_eachPeople(people = people))
        self.Fitnesses = Fitnesses

    def update_mate_probs(self, fitnesses):
        mate_pop = []
        for i in range(len(fitnesses)):
            if np.sum(fitnesses)!=0:
                mate_pop.append(fitnesses[i]/np.sum(fitnesses))
            else:
                mate_pop.append(fitnesses[i])
        return mate_pop
    def draw_simulation(self, people, simulation_obj):
        for i in range(len(self.XYDemand[0][:])):
            simulation_obj.colored_specific_sq(self.XYDemand[0][i], self.XYDemand[1][i])
        vehicle = 1
        vehicles_last_position = [[self.depoteLocation[0], self.depoteLocation[1]]] * 4
        demand_vehicle_get = 0
        index_gene = -1
        # colors = np.random.randint(0, 255, (7, 3), dtype=np.int)
        colors = np.array([[0, 0, 128], 
                            [20, 215, 215], 
                            [128, 255, 128],
                            [128, 0, 0], 
                            [48, 130, 245], 
                            [180, 30, 145],
                            [75, 25, 230]])

        vehicle = 1
        vehicles_last_position = [[self.depoteLocation[0], self.depoteLocation[1]]] * 4
        all_distance = 0
        next_vehicle = False
        for gene in people:
            # print(vehicle)
            if vehicle <= 4:
                while True:
                    if not next_vehicle:
                        all_distance = all_distance + self.evaluate_distance(vehicles_last_position[vehicle-1], [self.XYDemand[0][gene], self.XYDemand[1][gene]])
                        if all_distance < 200:
                            simulation_obj.draw_arrow(x = [vehicles_last_position[vehicle-1][0], self.XYDemand[0][gene]], y = [vehicles_last_position[vehicle-1][1], self.XYDemand[1][gene]], color = colors[vehicle-1, :])
                            vehicles_last_position[vehicle-1] = [self.XYDemand[0][gene], self.XYDemand[1][gene]]
                        if all_distance + self.evaluate_distance(vehicles_last_position[vehicle-1], [self.depoteLocation[0], self.depoteLocation[1]]) > 200:
                            next_vehicle = True
                        else:
                            break
                    else:
                        simulation_obj.draw_arrow(x = [vehicles_last_position[vehicle-1][0], self.depoteLocation[0]], y = [vehicles_last_position[vehicle-1][1], self.depoteLocation[1]], color = colors[vehicle-1, :])
                        vehicles_last_position[vehicle-1] = [self.depoteLocation[0], self.depoteLocation[1]]
                        all_distance = 0
                        next_vehicle = False
                        vehicle+=1
                        break
            else:
                break
