import numpy as np
import math
from simulation_output import *
import matplotlib.pyplot as plt
from population_Control import *
import copy

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
        # new_fitness = [x+7000 for x in new_fitness]
        new_fitness = [x-min(new_fitness) for x in new_fitness]
        for i in range(len(fitnesses)):
            if np.sum(fitnesses)!=0:
                mate_pop.append(new_fitness[i]/np.sum(new_fitness))
            else:
                mate_pop.append(new_fitness[i])
        return mate_pop
    def draw_simulation(self, people, simulation_obj):
        sum_depotes = []
        for i in self.XYDemand[2]:
            sum_depotes.append(i)
        for i in range(len(self.XYDemand[0][:])):
            simulation_obj.colored_specific_sq(self.XYDemand[0][i], self.XYDemand[1][i], self.XYDemand[2][i]/max(sum_depotes))
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
    def __init__(self, depoteLocation = [0, 0], XYDemand = [[], [], []], All_SortedDistances = [[]]):
        self.XYDemand = XYDemand
        self.depoteLocation = depoteLocation
        self.All_SortedDistances = All_SortedDistances
        pass
    def evaluate_distance(self, state1 = [-25, 25], state2 = [20, 20]):
        return (abs(state1[0] - state2[0]) + abs(state1[1] - state2[1]))
    def evaluate_eachPeople(self, people):
        vehicle = 1
        vehicles_last_position = [[self.depoteLocation[0], self.depoteLocation[1]]] * 4
        all_distance = 0
        Fitness = 0
        Temp_Fitness = 0
        fitness_distance = 0
        howmany_ = 0
        DistanceFromClossest = 0
        next_vehicle = False
        # All_SortedDistances = copy.deepcopy(self.All_SortedDistances)
        index = -1
        for gene in people:
            index +=1
            if vehicle <= 4:
                while True:
                    if not next_vehicle:
                        all_distance = all_distance + self.evaluate_distance(vehicles_last_position[vehicle-1], [self.XYDemand[0][gene], self.XYDemand[1][gene]])
                        if all_distance <= 200 and all_distance + self.evaluate_distance([self.XYDemand[0][gene], self.XYDemand[1][gene]], self.depoteLocation) < 200:
                            Temp_Fitness = Temp_Fitness + 1
                            if index > 0:
                                howFar = self.All_SortedDistances[people[index-1]].index(gene)
                                DistanceFromClossest =  DistanceFromClossest + howFar
                                # for indexx in range(len(All_SortedDistances)):
                                #     if indexx != gene:
                                #         All_SortedDistances[indexx].pop(All_SortedDistances[indexx].index(gene))
                            # else:
                            #     for indexx in range(len(All_SortedDistances)):
                            #         if indexx != gene:
                            #             All_SortedDistances[indexx].pop(All_SortedDistances[indexx].index(gene))
                        else:
                             all_distance = all_distance - self.evaluate_distance(vehicles_last_position[vehicle-1], [self.XYDemand[0][gene], self.XYDemand[1][gene]]) + self.evaluate_distance(vehicles_last_position[vehicle-1], self.depoteLocation)
                        vehicles_last_position[vehicle-1] = [self.XYDemand[0][gene], self.XYDemand[1][gene]]

                        if all_distance + self.evaluate_distance(vehicles_last_position[vehicle-1], [self.depoteLocation[0], self.depoteLocation[1]]) > 200:
                            next_vehicle = True
                            if Temp_Fitness != 0:
                                Fitness = Fitness + Temp_Fitness - DistanceFromClossest/100
                            DistanceFromClossest = 0
                                # exit()
                            all_distance = 0    
                            Temp_Fitness = 0
                        else:
                            break
                    else:
                        next_vehicle = False
                        vehicles_last_position[vehicle-1] = [self.depoteLocation[0], self.depoteLocation[1]]
                        all_distance = 0
                        DistanceFromClossest = 0
                        Temp_Fitness = 0
                        vehicle+=1
                        if vehicle == 5:
                            break
            else:
                break
        # del All_SortedDistances
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
        sum_depotes = []
        for i in self.XYDemand[2]:
            sum_depotes.append(i)
        for i in range(len(self.XYDemand[0][:])):
            simulation_obj.colored_specific_sq(self.XYDemand[0][i], self.XYDemand[1][i], self.XYDemand[2][i]/max(sum_depotes))
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
    def __init__(self, depoteLocation = [0, 0], XYDemand = [[], [], []], All_SortedDistances = [[]]):
        self.XYDemand = XYDemand
        self.new_Demand = []
        self.sum_depotes = []
        self.All_SortedDistances = All_SortedDistances
        for i in self.XYDemand[2]:
            self.sum_depotes.append(i)
        for i in range(len(self.XYDemand[2])):
            self.new_Demand.append((self.XYDemand[2][i] - min(self.sum_depotes))/(max(self.sum_depotes) - min(self.sum_depotes)))
        self.depoteLocation = depoteLocation
        pass
    def evaluate_distance(self, state1 = [-25, 25], state2 = [20, 20]):
        return (abs(state1[0] - state2[0]) + abs(state1[1] - state2[1]))
    def evaluate_eachPeople(self, people):
        vehicle = 1
        vehicles_last_position = [[self.depoteLocation[0], self.depoteLocation[1]]] * 4
        all_distance = 0
        Fitness = 0
        temp_Fitness = 0
        Fitness_count = 0
        howmany_ = 0
        DistanceFromClossest = 0
        next_vehicle = False
        index = -1
        for gene in people:
            index+=1
            if vehicle <= 4:
                while True:
                    if not next_vehicle:
                        all_distance = all_distance + self.evaluate_distance(vehicles_last_position[vehicle-1], [self.XYDemand[0][gene], self.XYDemand[1][gene]])
                        if all_distance <= 200 and all_distance + self.evaluate_distance([self.XYDemand[0][gene], self.XYDemand[1][gene]], self.depoteLocation) < 200:
                            temp_Fitness = temp_Fitness + 1 + self.new_Demand[gene]*2
                            Fitness_count = Fitness_count+1
                            if index > 0:
                                howFar = self.All_SortedDistances[people[index-1]].index(gene)
                                DistanceFromClossest =  DistanceFromClossest + howFar
                        else:
                            all_distance = all_distance - self.evaluate_distance(vehicles_last_position[vehicle-1], [self.XYDemand[0][gene], self.XYDemand[1][gene]]) + self.evaluate_distance(vehicles_last_position[vehicle-1], self.depoteLocation)
                        vehicles_last_position[vehicle-1] = [self.XYDemand[0][gene], self.XYDemand[1][gene]]

                        if all_distance + self.evaluate_distance(vehicles_last_position[vehicle-1], [self.depoteLocation[0], self.depoteLocation[1]]) > 200:
                            if Fitness_count != 0:
                                # print("Fitness_count - all_distance/(100*Fitness_count) = ", Fitness_count - all_distance/(100*Fitness_count))
                                # Fitness = Fitness + P * (temp_Fitness - (200 - all_distance)/(temp_Fitness)) + (1 - P) * (Fitness_count - (200 - all_distance)/(Fitness_count))
                                Fitness = Fitness + temp_Fitness - DistanceFromClossest/100
                                # print("Fitness = ", Fitness)
                            DistanceFromClossest = 0
                            Fitness_count = 0
                            temp_Fitness = 0
                            next_vehicle = True
                            all_distance = 0    
                        else:
                            break
                    else:
                        next_vehicle = False
                        vehicles_last_position[vehicle-1] = [self.depoteLocation[0], self.depoteLocation[1]]
                        all_distance = 0
                        Fitness_count = 0
                        DistanceFromClossest = 0
                        temp_Fitness = 0
                        vehicle+=1
                        if vehicle == 5:
                            break
            else:
                break
        # print("Fitness = ", Fitness)
        return Fitness
    def evaluate_fitness(self, population = [], P = 0):
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
            simulation_obj.colored_specific_sq(self.XYDemand[0][i], self.XYDemand[1][i], self.new_Demand[i])
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


class Fitness_func_for_prob4:
    def __init__(self, depoteLocation = [0, 0], XYDemand = [[], [], []], All_SortedDistances = [[]]):
        self.XYDemand = XYDemand
        self.depoteLocation = depoteLocation
        self.All_SortedDistances = All_SortedDistances
        pass
    def evaluate_distance(self, state1 = [-25, 25], state2 = [20, 20]):
        return (abs(state1[0] - state2[0]) + abs(state1[1] - state2[1]))
    def evaluate_eachPeople(self, people):
        vehicle = 1
        vehicles_last_position = [[self.depoteLocation[0], self.depoteLocation[1]]] * 150
        all_distance = 0
        Fitness = 0
        temp_Fitness = 0
        next_vehicle = False
        DistanceFromClossest = 0
        gen_index = -1
        index = -1
        for gene in people:
            index +=1
            gen_index+=1
            while True:
                # print(next_vehicle)
                if not next_vehicle:
                    all_distance_0 = all_distance
                    all_distance = all_distance + self.evaluate_distance(vehicles_last_position[vehicle-1], [self.XYDemand[0][gene], self.XYDemand[1][gene]])
                    if all_distance <= 200 and all_distance + self.evaluate_distance([self.XYDemand[0][gene], self.XYDemand[1][gene]], self.depoteLocation) < 200:
                        # temp_Fitness = temp_Fitness + 1
                        if index > 0:
                            howFar = self.All_SortedDistances[people[index-1]].index(gene)
                            DistanceFromClossest =  DistanceFromClossest + howFar
                    else:
                        all_distance = all_distance - self.evaluate_distance(vehicles_last_position[vehicle-1], [self.XYDemand[0][gene], self.XYDemand[1][gene]]) + self.evaluate_distance(vehicles_last_position[vehicle-1], self.depoteLocation)
                    vehicles_last_position[vehicle-1] = [self.XYDemand[0][gene], self.XYDemand[1][gene]]
                    # print(all_distance + self.evaluate_distance(vehicles_last_position[vehicle-1], [self.depoteLocation[0], self.depoteLocation[1]]))
                    if all_distance + self.evaluate_distance(vehicles_last_position[vehicle-1], [self.depoteLocation[0], self.depoteLocation[1]]) > 200:
                        # if all_distance_0 == 0:
                        #     temp_Fitness = temp_Fitness - 1
                        #     break
                        # if temp_Fitness != 0:
                        #     Fitness = Fitness + temp_Fitness - (200 - all_distance)/temp_Fitness
                        temp_Fitness = temp_Fitness + DistanceFromClossest/100
                        DistanceFromClossest = 0
                        next_vehicle = True
                        all_distance = 0    
                    else:
                        break
                    
                else:
                    next_vehicle = False
                    vehicles_last_position[vehicle-1] = [self.depoteLocation[0], self.depoteLocation[1]]
                    all_distance = 0
                    vehicle+=1
                    if gen_index == len(people)-1:
                        break
        # print(temp_Fitness/100)
        # print(vehicle)
        # print("--------------------")
        # # exit()
        Fitness = -temp_Fitness/100 - vehicle
                    
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
        sum_depotes = []
        for i in self.XYDemand[2]:
            sum_depotes.append(i)
        for i in range(len(self.XYDemand[0][:])):
            simulation_obj.colored_specific_sq(self.XYDemand[0][i], self.XYDemand[1][i], self.XYDemand[2][i]/max(sum_depotes))
        vehicle = 1
        vehicles_last_position = [[self.depoteLocation[0], self.depoteLocation[1]]] * 150
        demand_vehicle_get = 0
        index_gene = -1
        colors = np.random.randint(0, 255, (150, 3), dtype=np.int)
        # colors = np.array([[0, 0, 128], 
        #                     [20, 215, 215], 
        #                     [128, 255, 128],
        #                     [128, 0, 0], 
        #                     [48, 130, 245], 
        #                     [180, 30, 145],
        #                     [75, 25, 230],
        #                     [201, 174, 255],
        #                     [176, 228, 239],
        #                     [29, 230, 181],
        #                     [87, 122, 185],
        #                     [228, 179, 228],
        #                     [176, 228, 239],
        #                     [29, 230, 181],
        #                     [87, 122, 185],
        #                     [228, 179, 228]])

        vehicle = 1
        vehicles_last_position = [[self.depoteLocation[0], self.depoteLocation[1]]] * 150
        all_distance = 0
        next_vehicle = False
        for gene in people:
            # print(vehicle)
            if vehicle <= 4:
                while True:
                    if not next_vehicle:
                        all_distance = all_distance + self.evaluate_distance(vehicles_last_position[vehicle-1], [self.XYDemand[0][gene], self.XYDemand[1][gene]])
                        if all_distance < 200 and all_distance + self.evaluate_distance([self.XYDemand[0][gene], self.XYDemand[1][gene]], self.depoteLocation) < 200:
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
        gen_index = -1
        for gene in people:
            gen_index+=1
            while True:
                # print(next_vehicle)
                if not next_vehicle:
                    all_distance_0 = all_distance
                    break_it = False
                    break_it_after = False
                    all_distance = all_distance + self.evaluate_distance(vehicles_last_position[vehicle-1], [self.XYDemand[0][gene], self.XYDemand[1][gene]])
                    
                    # print(all_distance + self.evaluate_distance(vehicles_last_position[vehicle-1], [self.depoteLocation[0], self.depoteLocation[1]]))
                    if all_distance + self.evaluate_distance([self.XYDemand[0][gene], self.XYDemand[1][gene]], [self.depoteLocation[0], self.depoteLocation[1]]) > 200:
                        if all_distance_0 == 0:
                            break_it = True
                        next_vehicle = True
                        all_distance = 0    
                    else:
                        break_it_after = True
                    if break_it:
                        break
                    if all_distance <= 200 and not next_vehicle:
                        simulation_obj.draw_arrow(x = [vehicles_last_position[vehicle-1][0], self.XYDemand[0][gene]], y = [vehicles_last_position[vehicle-1][1], self.XYDemand[1][gene]], color = colors[vehicle-1, :])
                        vehicles_last_position[vehicle-1] = [self.XYDemand[0][gene], self.XYDemand[1][gene]]
                        if break_it_after:
                            break
                else:
                    next_vehicle = False
                    simulation_obj.draw_arrow(x = [vehicles_last_position[vehicle-1][0], self.depoteLocation[0]], y = [vehicles_last_position[vehicle-1][1], self.depoteLocation[1]], color = colors[vehicle-1, :])
                    vehicles_last_position[vehicle-1] = self.depoteLocation
                    all_distance = 0
                    vehicle+=1
                    if gen_index == len(people)-1:
                        break


class Fitness_func_for_prob5:
    def __init__(self, depoteLocation = [[0, 0], [0, 0], [0, 0]], XYDemand = [[], [], []], All_SortedDistances = [[]]):
        self.XYDemand = XYDemand
        self.depoteLocation = depoteLocation
        self.All_SortedDistances = All_SortedDistances
        pass
    def evaluate_distance(self, state1 = [-25, 25], state2 = [20, 20]):
        return - (abs(state1[0] - state2[0]) + abs(state1[1] - state2[1]))
    def evaluate_eachPeople(self, people):
        vehicle = 1
        vehicles_last_position = [self.depoteLocation[0], self.depoteLocation[1], self.depoteLocation[2]]
        demand_vehicle_get = 0
        Fitness = 0
        index_gene = -1
        DistanceFromClossest = 0
        vehicles_last_position_list = []
        vehicle_first_place = []
        for i in np.arange(len(people) - 11, len(people)):
            vehicles_last_position_list.append(vehicles_last_position[people[i]])
            vehicle_first_place.append(vehicles_last_position[people[i]])
        index = -1
        for gene in people:
            index +=1
            index_gene+=1
            if index_gene > len(self.XYDemand[0])-1:
                break 
            while True:
                if demand_vehicle_get<=100:
                    
                    if index > 0:
                        howFar = self.All_SortedDistances[people[index-1]].index(gene)
                        DistanceFromClossest =  DistanceFromClossest + howFar
                    Fitness = Fitness + self.evaluate_distance(vehicles_last_position_list[vehicle-1], [self.XYDemand[0][gene], self.XYDemand[1][gene]])
                    vehicles_last_position_list[vehicle-1] = [self.XYDemand[0][gene], self.XYDemand[1][gene]]
                    demand_vehicle_get = demand_vehicle_get + self.XYDemand[2][gene]
                    break
                else:
                    Fitness = Fitness + self.evaluate_distance(vehicles_last_position_list[vehicle-1], vehicle_first_place[vehicle-1]) - DistanceFromClossest/100
                    vehicles_last_position_list[vehicle-1] = vehicle_first_place[vehicle-1]
                    demand_vehicle_get = 0
                    DistanceFromClossest = 0
                    vehicle+=1
                    if vehicle == 12:
                        vehicle = 1
            if index_gene == len(people) - 11:
                Fitness = Fitness + self.evaluate_distance(vehicles_last_position[vehicle-1], vehicle_first_place[vehicle-1])
        return Fitness
    def evaluate_fitness(self, population = []):
        Fitnesses = []
        for people in population:
            Fitnesses.append(self.evaluate_eachPeople(people = people))
        self.Fitnesses = Fitnesses

    def update_mate_probs(self, fitnesses):
        mate_pop = []
        new_fitness = fitnesses.copy()
        new_fitness = [x+10000 for x in new_fitness]
        new_fitness = [x-min(new_fitness) for x in new_fitness]
        for i in range(len(fitnesses)):
            if np.sum(fitnesses)!=0:
                mate_pop.append(new_fitness[i]/np.sum(new_fitness))
            else:
                mate_pop.append(new_fitness[i])
        return mate_pop
    def draw_simulation(self, people, simulation_obj):
        sum_depotes = []
        for i in self.XYDemand[2]:
            sum_depotes.append(i)
        for i in range(len(self.XYDemand[0][:])):
            simulation_obj.colored_specific_sq(self.XYDemand[0][i], self.XYDemand[1][i], self.XYDemand[2][i]/max(sum_depotes))
        colors = np.array([[0, 0, 128], 
                            [20, 215, 215], 
                            [128, 255, 128],
                            [128, 0, 0], 
                            [48, 130, 245], 
                            [180, 30, 145],
                            [75, 25, 230],
                            [201, 174, 255],
                            [176, 228, 239],
                            [29, 230, 181],
                            [87, 122, 185],
                            [228, 179, 228],
                            [176, 228, 239],
                            [29, 230, 181],
                            [87, 122, 185],
                            [228, 179, 228]])

        vehicle = 1
        vehicles_last_position = [self.depoteLocation[0], self.depoteLocation[1], self.depoteLocation[2]]
        demand_vehicle_get = 0
        Fitness = 0
        index_gene = -1
        vehicles_last_position_list = []
        vehicle_first_place = []
        for i in np.arange(len(people) - 11, len(people)):
            vehicles_last_position_list.append(vehicles_last_position[people[i]-1])
            vehicle_first_place.append(vehicles_last_position[people[i]-1])
        for gene in people:
            index_gene+=1
            if index_gene > len(self.XYDemand[0])-1:
                break 
            while True:
                if demand_vehicle_get<=100:
                    # print(vehicle-1)
                    simulation_obj.draw_arrow(x = [vehicles_last_position_list[vehicle-1][0], self.XYDemand[0][gene]], y = [vehicles_last_position_list[vehicle-1][1], self.XYDemand[1][gene]], color = colors[vehicle-1, :])
                    vehicles_last_position_list[vehicle-1] = [self.XYDemand[0][gene], self.XYDemand[1][gene]]
                    demand_vehicle_get = demand_vehicle_get + self.XYDemand[2][gene]
                    break
                else:
                    Fitness = Fitness + self.evaluate_distance(vehicles_last_position_list[vehicle-1], vehicle_first_place[vehicle-1])
                    simulation_obj.draw_arrow(x = [vehicles_last_position_list[vehicle-1][0], vehicle_first_place[vehicle-1][0]], y = [vehicles_last_position_list[vehicle-1][1], vehicle_first_place[vehicle-1][1]], color = colors[vehicle-1, :])
                    vehicles_last_position_list[vehicle-1] = vehicle_first_place[vehicle-1]
                    demand_vehicle_get = 0
                    vehicle+=1
                    if vehicle == 12:
                        vehicle = 1
            if index_gene == len(people) - 12:
                simulation_obj.draw_arrow(x = [vehicles_last_position_list[vehicle-1][0], vehicle_first_place[vehicle-1][0]], y = [vehicles_last_position_list[vehicle-1][1], vehicle_first_place[vehicle-1][1]], color = colors[vehicle-1, :])


class Fitness_func_for_prob6:
    def __init__(self, depoteLocation = [[0, 0], [0, 0], [0, 0]], XYDemand = [[], [], []]):
        self.XYDemand = XYDemand
        self.depoteLocation = depoteLocation
        pass
    def evaluate_distance(self, state1 = [-25, 25], state2 = [20, 20]):
        return (abs(state1[0] - state2[0]) + abs(state1[1] - state2[1]))
    def evaluate_eachPeople(self, people):
        vehicle = 1
        vehicles_last_position = [self.depoteLocation[0], self.depoteLocation[1]]
        all_distance = 0
        Fitness = 0
        index_gene = -1
        vehicles_last_position_list = []
        vehicle_first_place = []
        for i in np.arange(len(people) - 7, len(people)):
            vehicles_last_position_list.append(vehicles_last_position[people[i]-1])
            vehicle_first_place.append(vehicles_last_position[people[i]-1])
        
        next_vehicle = False
        for gene in people:
            index_gene+=1
            if index_gene > len(self.XYDemand[0])-1:
                break 
            if vehicle <= 7:
                while True:
                    if not next_vehicle:
                        all_distance = all_distance + self.evaluate_distance(vehicles_last_position_list[vehicle-1], [self.XYDemand[0][gene], self.XYDemand[1][gene]])
                        if all_distance <= 250:
                            # Fitness = Fitness + 1 - 2*self.evaluate_distance(vehicles_last_position_list[vehicle-1], [self.XYDemand[0][gene], self.XYDemand[1][gene]])/250
                            Fitness = Fitness + 1
                        vehicles_last_position_list[vehicle-1] = [self.XYDemand[0][gene], self.XYDemand[1][gene]]

                        if all_distance + self.evaluate_distance(vehicles_last_position_list[vehicle-1], vehicle_first_place[vehicle-1]) > 250:
                            next_vehicle = True
                            all_distance = 0    
                        else:
                            break
                    else:
                        next_vehicle = False
                        vehicles_last_position_list[vehicle-1] = vehicle_first_place[vehicle-1]
                        all_distance = 0
                        vehicle+=1
                        if vehicle == 8:
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
        sum_depotes = []
        for i in self.XYDemand[2]:
            sum_depotes.append(i)
        for i in range(len(self.XYDemand[0][:])):
            simulation_obj.colored_specific_sq(self.XYDemand[0][i], self.XYDemand[1][i], self.XYDemand[2][i]/max(sum_depotes))
        colors = np.array([[0, 0, 128], 
                            [20, 215, 215], 
                            [128, 255, 128],
                            [128, 0, 0], 
                            [48, 130, 245], 
                            [180, 30, 145],
                            [75, 25, 230],
                            [201, 174, 255],
                            [176, 228, 239],
                            [29, 230, 181],
                            [87, 122, 185],
                            [228, 179, 228],
                            [176, 228, 239],
                            [29, 230, 181],
                            [87, 122, 185],
                            [228, 179, 228]])

        vehicle = 1
        all_distance = 0
        vehicles_last_position = [self.depoteLocation[0], self.depoteLocation[1]]
        demand_vehicle_get = 0
        Fitness = 0
        index_gene = -1
        vehicles_last_position_list = []
        vehicle_first_place = []
        for i in np.arange(len(people) - 7, len(people)):
            vehicles_last_position_list.append(vehicles_last_position[people[i]])
            vehicle_first_place.append(vehicles_last_position[people[i]])
        next_vehicle = False
        for gene in people:
            index_gene+=1
            if index_gene > len(self.XYDemand[0])-1:
                break 
            if vehicle <= 7:
                while True:
                    if not next_vehicle:
                        all_distance = all_distance + self.evaluate_distance(vehicles_last_position_list[vehicle-1], [self.XYDemand[0][gene], self.XYDemand[1][gene]])
                        if all_distance <= 250:
                            simulation_obj.draw_arrow(x = [vehicles_last_position_list[vehicle-1][0], self.XYDemand[0][gene]], y = [vehicles_last_position_list[vehicle-1][1], self.XYDemand[1][gene]], color = colors[vehicle-1, :])
                        vehicles_last_position_list[vehicle-1] = [self.XYDemand[0][gene], self.XYDemand[1][gene]]

                        if all_distance + self.evaluate_distance(vehicles_last_position_list[vehicle-1], vehicle_first_place[vehicle-1]) > 250:
                            next_vehicle = True
                            all_distance = 0    
                        else:
                            break
                    else:
                        simulation_obj.draw_arrow(x = [vehicles_last_position_list[vehicle-1][0], vehicle_first_place[vehicle-1][0]], y = [vehicles_last_position_list[vehicle-1][1], vehicle_first_place[vehicle-1][1]], color = colors[vehicle-1, :])
                        next_vehicle = False
                        vehicles_last_position_list[vehicle-1] = vehicle_first_place[vehicle-1]
                        all_distance = 0
                        vehicle+=1
                        if vehicle == 8:
                            break
            else:
                break

