import numpy as np
from population_Control import *
from Fitness import *
from Mutation import *
from Recombination import *
import csv
import os
import threading
import ast
import glob
import time
class genetic_alg(threading.Thread):
    def __init__(self, pop_control_obj, Fitness_func_for_prob1_obj, Selection, saved_folder, thread_name, HowMany_Thread):
        threading.Thread.__init__(self)
        pop_control_obj.creat_population_prob()
        self.pop = pop_control_obj.population
        Fitness_func_for_prob1_obj.evaluate_fitness(self.pop)
        self.cac_fitness = Fitness_func_for_prob1_obj.evaluate_eachPeople
        self.update_prob = Fitness_func_for_prob1_obj.update_mate_probs
        self.fitnesses = Fitness_func_for_prob1_obj.Fitnesses
        self.simulation = Fitness_func_for_prob1_obj.draw_simulation
        self.Selection = Selection
        self.destination_folder = saved_folder
        self.thread_name = thread_name
        self.HowMany_Thread = HowMany_Thread
        self.pop_size = len(self.pop)
        self.creat_folders()
    def sort_fitnessAndPop(self):
        self.fitnesses, self.pop = zip(*sorted(zip(self.fitnesses, self.pop)))
        self.fitnesses = list(self.fitnesses)
        self.pop = list(self.pop)
        self.pop = self.pop[::-1]
        self.fitnesses = self.fitnesses[::-1]
    def sort_fitnessAndPop_forChilderens(self, temp_fitness, temp_pop):
        temp_fitness, temp_pop = zip(*sorted(zip(temp_fitness, temp_pop)))
        temp_fitness = list(temp_fitness)
        temp_pop = list(temp_pop)
        temp_pop = temp_pop[::-1]
        temp_fitness = temp_fitness[::-1]
        return temp_fitness, temp_pop
    def FPS(self, mate_pop):
        try:
            selected = np.random.choice(self.pop_size, size=2, p=mate_pop)
        except:
            selected = np.random.choice(self.pop_size, size=2)
        # print(selected)
        parent_1 = self.pop[selected[0]].copy()
        parent_2 = self.pop[selected[1]].copy()
        return parent_1, parent_2
    def tournament(self, ):
        selected_P1 = np.random.choice(self.pop_size, size=2)
        selected_P2 = np.random.choice(self.pop_size, size=2)
        parent_11 = self.pop[selected_P1[0]].copy()
        parent_12 = self.pop[selected_P1[1]].copy()
        parent_21 = self.pop[selected_P2[0]].copy()
        parent_22 = self.pop[selected_P2[1]].copy()
        if self.cac_fitness(parent_11)>self.cac_fitness(parent_12):
            parent_1 = parent_11
        else:
            parent_1 = parent_12
        if self.cac_fitness(parent_21)>self.cac_fitness(parent_22):
            parent_2 = parent_21
        else:
            parent_2 = parent_22
        return parent_1, parent_2
    def creat_folders(self, ):
        if not os.path.exists(self.destination_folder):
            os.mkdir(self.destination_folder)
            os.mkdir("{}/images".format(self.destination_folder))
            os.mkdir("{}/best chromosome".format(self.destination_folder))
            os.mkdir("{}/threads connections".format(self.destination_folder))
        with open("{}/threads connections/{} Order.txt".format(self.destination_folder, self.thread_name), 'w') as f:
            f.write("in progressing")
            f.close()
        with open('{}/best chromosome/{}.csv'.format(self.destination_folder, self.thread_name), 'w', newline="") as file:
            writer = csv.writer(file)
            # writer.writerow([])
            file.close()
    def Cutting(self, temp_fitness, temp_population):
        
        for index in range(len(temp_fitness)):
            self.fitnesses.append(temp_fitness[index])
            self.pop.append(list(temp_population[index]))
        self.sort_fitnessAndPop()
        self.pop = self.pop[:self.pop_size]
        self.fitnesses = self.fitnesses[:self.pop_size]
    def Elitism(self, dived_into, temp_fitness, temp_population):
        while True:
            if self.pop_size - int(self.pop_size/dived_into) < len(temp_fitness):
                self.sort_fitnessAndPop()
                for i in range(len(self.fitnesses)):
                    if i >= int(len(self.fitnesses)/dived_into):
                        temp_fitness.append(self.fitnesses[i])
                        temp_population.append(self.pop[i])
                self.pop = self.pop[:int(len(self.pop)/dived_into)]
                self.fitnesses = self.fitnesses[:int(len(self.fitnesses)/dived_into)]
                mate_pop = self.update_prob(temp_fitness)
                try:
                    selected = np.random.choice(len(temp_population), size=self.pop_size-int(self.pop_size/dived_into), p=mate_pop)
                except:
                    selected = np.random.choice(len(temp_population), size=self.pop_size-int(self.pop_size/dived_into))

                temp_population = np.array(temp_population)
                temp_population = list(temp_population[selected])
                temp_fitness = np.array(temp_fitness)
                temp_fitness = list(temp_fitness[selected])
                for index in range(len(temp_fitness)):
                    self.fitnesses.append(temp_fitness[index])
                    self.pop.append(list(temp_population[index]))

                break
            else:
                dived_into-=1
    def RecombinationThreads(self):
        chromosomesThatShouldAppend = []
        FitnessesShouldAppend = []
        RandomChoice_chro = []
        RandomChoice_Fitness = []
        for file_name in glob.glob("{}/threads connections/*".format(self.destination_folder)):
            each_chromosomesThatShouldAppend = []
            each_FitnessesShouldAppend = []
            each_RandomChoice_chro = []
            each_RandomChoice_Fitness = []
            if "make connection" in file_name:
                thread_id = int( self.thread_name[self.thread_name.find("thread number")+len("thread number"):])
                if thread_id == self.HowMany_Thread-1:
                    next_thread = 0
                else:
                    next_thread = thread_id + 1
                if self.thread_name not in file_name and "thread number {}".format(next_thread) in file_name:
                    file = open(file_name)
                    csvreader = csv.reader(file)
                    row_num = 0
                    for row in csvreader:
                        row_num+=1
                        # each_RandomChoice_chro.append(ast.literal_eval(row[0]))
                        # each_RandomChoice_Fitness.append(float(row[1]))
                        # if row_num <= int(len(self.pop)/(8*(self.HowMany_Thread-1))):
                        if row_num <= int(len(self.pop)/(8)):
                            each_chromosomesThatShouldAppend.append(ast.literal_eval(row[0]))
                            each_FitnessesShouldAppend.append(float(row[1]))
                        else:
                            each_RandomChoice_chro.append(ast.literal_eval(row[0]))
                            each_RandomChoice_Fitness.append(float(row[1]))
       
                    mate_pop = self.update_prob(each_RandomChoice_Fitness)
                    try:
                        # selected = np.random.choice(len(each_RandomChoice_chro), size=math.ceil(len(self.pop)/(8*(self.HowMany_Thread-1))), p=mate_pop)
                        selected = np.random.choice(len(each_RandomChoice_chro), size=math.ceil(len(self.pop)/(8)), p=mate_pop)
                    except:            
                        selected = np.random.choice(len(each_RandomChoice_chro), size=math.ceil(len(self.pop)/(8)))

                    each_RandomChoice_chro = np.array(each_RandomChoice_chro)
                    each_RandomChoice_chro = list(each_RandomChoice_chro[selected])
                    each_RandomChoice_Fitness = np.array(each_RandomChoice_Fitness)
                    each_RandomChoice_Fitness = list(each_RandomChoice_Fitness[selected])
                    index = -1
                    for i in each_RandomChoice_chro:
                        index+=1
                        RandomChoice_chro.append(i)
                        RandomChoice_Fitness.append(each_RandomChoice_Fitness[index])
                    index = -1
                    for i in each_chromosomesThatShouldAppend:
                        index+=1
                        chromosomesThatShouldAppend.append(i)
                        FitnessesShouldAppend.append(each_FitnessesShouldAppend[index])

        self.pop = self.pop[:len(self.pop) - len(chromosomesThatShouldAppend) - len(RandomChoice_Fitness)]
        self.fitnesses = self.fitnesses[:len(self.fitnesses) - len(FitnessesShouldAppend) - len(RandomChoice_Fitness)]
        
        index = -1
        for chromosome in chromosomesThatShouldAppend:
            index+=1
            self.pop.append(chromosome)
            self.fitnesses.append(FitnessesShouldAppend[index])
        index = -1
        for chromosome in RandomChoice_chro:
            index+=1
            self.pop.append(list(chromosome))
            self.fitnesses.append(RandomChoice_Fitness[index])
    def run(self):
        iters = 0
        explore = True
        repetition_of_eq_fitnesses = 0
        repetition_of_not_eq_fitnesses = 0
        while (iters < 5000):
            iters +=1
            print(self.thread_name, " - iteration num = ", iters, ", best Fitness is = ", max(self.fitnesses), "explore = ", explore)
            mate_pop = self.update_prob(self.fitnesses)
            if iters < 500:
                Mutation_obj = Swap()
                Recombination_obj = Cycle1()
                Pm = 1
                explore = True
                dived_into = 4
                Pc = 1
            elif iters > 500 and iters < 1000:
                Recombination_obj = Cycle1()
                Mutation_obj = Swap()
                dived_into = 2
                # explore = False
                Pm = 0.8
                Pc = 1
            elif iters > 1000 and iters < 1500:
                Mutation_obj = Swap()
                Recombination_obj = Cycle1()
                # explore = False
                dived_into = 2
                Pm = 0.6
                Pc = 1
            elif iters > 1500 and iters < 2000:
                Mutation_obj = Swap()
                Recombination_obj = Cycle1()
                # explore = False
                dived_into = 2
                Pm = 0.4
                Pc = 1
            elif iters > 2000 and iters < 2500:
                Mutation_obj = Swap()
                Recombination_obj = Cycle1()
                Pm = 0.4
                # explore = False
                Pc = 1
            elif iters > 2500 and iters < 3000:
                Mutation_obj = Swap()
                Recombination_obj = Cycle1()
                # explore = False
                Pm = 1
                Pc = 1
            if iters == 1:
                simulation_obj = simulation()
                self.simulation(people = self.pop[self.fitnesses.index(max(self.fitnesses))][:], simulation_obj = simulation_obj)
                cv.imwrite("{}/images/{}_{}.png".format(self.destination_folder, self.thread_name,iters), simulation_obj.image)
            if iters%20 == 0:
                simulation_obj = simulation()
                self.simulation(people = self.pop[self.fitnesses.index(max(self.fitnesses))][:], simulation_obj = simulation_obj)
                cv.imwrite("{}/images/{}_{}.png".format(self.destination_folder, self.thread_name,iters), simulation_obj.image)
                self.sort_fitnessAndPop()
                with open('{}/threads connections/make connection with {}.csv'.format(self.destination_folder, self.thread_name), 'w',  newline="") as file:
                    writer = csv.writer(file)
                    for i in range(len(self.fitnesses)):
                        writer.writerow([self.pop[i], self.fitnesses[i]])
                    file.close()
                with open("{}/threads connections/{} Order.txt".format(self.destination_folder, self.thread_name), 'w') as f:
                    f.write("waiting".format(self.thread_name))
                    f.close()
                # time.sleep(2)
                while True:
                    with open("{}/threads connections/Main Thread Order.txt".format(self.destination_folder), "r") as f:
                        contents = f.read()
                        if "Wait" not in contents:
                            with open("{}/threads connections/{} Order.txt".format(self.destination_folder, self.thread_name), 'w') as f:
                                f.write("in progressing".format(self.thread_name))
                                f.close()
                            f.close()
                            self.RecombinationThreads()
                            break
                        f.close()
            
            with open('{}/best chromosome/{}.csv'.format(self.destination_folder, self.thread_name), 'a', newline="") as file:
                writer = csv.writer(file)
                writer.writerow([self.pop[self.fitnesses.index(max(self.fitnesses))], max(self.fitnesses), np.average(self.fitnesses)])
                file.close()
            if "Problem 1" in self.destination_folder:
                diffrence_Thereshold = 10
            elif "Problem 2" in self.destination_folder:
                diffrence_Thereshold = 1
            if abs(self.fitnesses[0] - np.average(self.fitnesses)) < diffrence_Thereshold and repetition_of_eq_fitnesses < 10:
                if iters < 500:
                    Mutation_obj = Inversion()
                repetition_of_eq_fitnesses+=1
                repetition_of_not_eq_fitnesses = 0
                if iters < 500:
                    Recombination_obj = Order()
                Pm = 1
            elif abs(self.fitnesses[0] - np.average(self.fitnesses)) < diffrence_Thereshold and repetition_of_eq_fitnesses >= 10:
                repetition_of_not_eq_fitnesses = 0
                if iters < 500:
                    Mutation_obj = Scramble()
                repetition_of_eq_fitnesses+=1
                if iters < 500:
                    Recombination_obj = CutAndCrossFill()
                else:
                    Recombination_obj = Order()
                Pm = 1
            else:
                Mutation_obj = Swap()
                Recombination_obj = Cycle1()
                # Pm = 1
                repetition_of_eq_fitnesses = 0
            # elif repetition_of_not_eq_fitnesses <= 10 and abs(self.fitnesses[0] - np.average(self.fitnesses)) > diffrence_Thereshold:
                
            #     if iters < 500:
            #         Mutation_obj = Inversion()
            #     repetition_of_eq_fitnesses = 0
            #     repetition_of_not_eq_fitnesses +=1
            #     if iters < 500:
            #         Recombination_obj = CutAndCrossFill()
            #     else:
            #         Recombination_obj = Order()
            #     Pm = 1
            # elif abs(self.fitnesses[0] - np.average(self.fitnesses)) > diffrence_Thereshold and repetition_of_not_eq_fitnesses > 10:
            #     # repetition_of_not_eq_fitnesses = 0
            #     Mutation_obj = Swap()
            #     Recombination_obj = Cycle1()
            #     # Pm = 1
            #     repetition_of_eq_fitnesses = 0
            temp_population = []
            temp_fitness = []
            for _ in range(self.pop_size):
                if np.random.random() < Pc:
                    if self.Selection == 0:
                        parent_1, parent_2 = self.tournament()
                    else:
                        parent_1, parent_2 = self.FPS(mate_pop)
                    
                    parent_1 = [x+1 for x in parent_1]
                    parent_2 = [x+1 for x in parent_2]
                    # child1, child2 = Recombination_obj.Recombination(parent_1, parent_2)
                    child1, child2 = Recombination_obj.Recombination(parent_1, parent_2)
                    # print(child1)
                    child1 = [x-1 for x in child1] 
                    child2 = [x-1 for x in child2] 
                    child1 = Mutation_obj.Mutate(child1, Pm)
                    child2 = Mutation_obj.Mutate(child2, Pm)
                    temp_population.append(child1)
                    temp_population.append(child2)
                    temp_fitness.append(self.cac_fitness(child1))
                    temp_fitness.append(self.cac_fitness(child2))
            dived_into = 6
            if explore:
                self.Elitism(dived_into, temp_fitness, temp_population)
            else:
                self.Cutting(temp_fitness, temp_population)