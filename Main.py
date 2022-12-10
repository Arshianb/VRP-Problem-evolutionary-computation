import numpy as np
from population_Control import *
from Fitness import *
from Mutation import *
from Recombination import *
from EvolutionaryAlg import *
import glob
import time

HowManyThread = 6
Threads = []
Output_Folder = "Problem 2"
for Thread in range(HowManyThread):
    if Thread%2 == 0:
        Selection = 0
    else:
        Selection = 1
    # Selection = 0
    pop_control_obj = pop_control2(150, "Data/P2.txt")
    Threads.append(genetic_alg(pop_control_obj,  Fitness_func_for_prob2([0, 13], pop_control_obj.XYDemand), Selection, Output_Folder, "thread number {}".format(Thread), HowManyThread))

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
            
            
            
