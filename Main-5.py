import numpy as np
from population_Control import *
from Fitness import *
from Mutation import *
from Recombination import *
from EvolutionaryAlg_5 import *
import glob
import time


HowManyThread = 3
Threads = []
Output_Folder = "Problem 5"
for Thread in range(HowManyThread):
    # if Thread%2 == 0:
    #     Selection = 0
    # else:
    #     Selection = 1
    Selection = 1
    pop_control_obj = pop_control5(100, "Data/P5.txt")
    Threads.append(genetic_alg(pop_control_obj,  Fitness_func_for_prob5([[31, 6], [-31, 7], [25, -10]], pop_control_obj.XYDemand), Selection, Output_Folder, "thread number {}".format(Thread), HowManyThread))

with open("{}/threads connections/Main Thread Order.txt".format(Output_Folder), "w") as f:
     f.write("Wait")
     f.close()
for Threads_id in range(HowManyThread):
    Threads[Threads_id].start()

for big_itation in range(50):
    while True:
        how_many_wait = 0
        for file_name in glob.glob("{}/threads connections/*".format(Output_Folder)):
            if "Order" in file_name:
                with open(file_name, "r") as f:
                    contents = f.read()
                    if "waiting" in contents:
                        how_many_wait+=1
                    f.close()
        if how_many_wait==HowManyThread:
            with open("{}/threads connections/Main Thread Order.txt".format(Output_Folder), "w") as f:
                f.write("Go Threads")
                f.close()
            time.sleep(3)
            with open("{}/threads connections/Main Thread Order.txt".format(Output_Folder), "w") as f:
                f.write("Wait")
                f.close()
            break
            
            
            
