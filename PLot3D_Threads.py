import glob
import csv
import matplotlib.pyplot as plt
import ast
def Problem1_plot(Main_path = "Problem 1\\best chromosome"):
    X = []
    Y = []
    Z = []
    Z_avg = []
    for csv_File in glob.glob("{}/*".format(Main_path)):
        Csv = open(csv_File, "r")
        csv_row = csv.reader(Csv)
        row_num = 0
        for row in csv_row:
            row_num +=1
            # print(row)
            X.append(row_num)
            Y.append(int(csv_File[csv_File.find("number")+len("number"):csv_File.find(".csv")]))
            Z.append(float(row[1]))
            Z_avg.append(float(row[2]))

    
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.scatter3D(X, Y, Z, c='red', marker='o')
    ax.scatter3D(X, Y, Z_avg, c='blue', marker='o')
    ax.view_init(25, 152)
    ax.set_ylabel("Threads")
    ax.set_xlabel("Iterations")
    ax.set_zlabel("Best Fitness")
    ax.set_title("Problem 1\nOptimal total distance vehicles is = {}".format(Z[len(Z)-1]))
    
    # ax.set_title(Fitness_Func_string)
    # plt.savefig(c, dpi = 200)

    plt.show()

def evaluate_distance(state1 = [-25, 25], state2 = [20, 20]):
    return (abs(state1[0] - state2[0]) + abs(state1[1] - state2[1]))

def XYZ_(problem_txt = "Data/P2.txt"):
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
    return [X, Y, demand]
def Problem2_plot(Main_path = "Problem 1\\best chromosome"):
    X = []
    Y = []
    Z = []
    Z_avg = []
    Fitnesses = []
    for csv_File in glob.glob("{}/*".format(Main_path)):
        Csv = open(csv_File, "r")
        csv_row = csv.reader(Csv)
        row_num = 0
        index = 0
        whole = 0
        for row in csv_row:
            whole +=1
            # print(whole)
        Csv = open(csv_File, "r")
        csv_row = csv.reader(Csv)
        Fitness = 0
        for row in csv_row:
            # print(index)
            index +=1
            row_num +=1
            # print(row)
            X.append(row_num)
            Y.append(int(csv_File[csv_File.find("number")+len("number"):csv_File.find(".csv")]))
            Z.append(float(row[1]))
            XYDemand = XYZ_()
            Z_avg.append(float(row[2]))
            if index == whole:
                vehicle = 1
                vehicles_last_position = [[0, 13]] * 4
                all_distance = 0
                fitness_distance = 0
                howmany_ = 0
                next_vehicle = False
                for gene in ast.literal_eval(row[0]):
                    if vehicle <= 4:
                        while True:
                            if not next_vehicle:
                                all_distance = all_distance + evaluate_distance(vehicles_last_position[vehicle-1], [XYDemand[0][gene], XYDemand[1][gene]])
                                if all_distance <= 200:
                                    Fitness = Fitness + 1 
                                vehicles_last_position[vehicle-1] = [XYDemand[0][gene], XYDemand[1][gene]]

                                if all_distance + evaluate_distance(vehicles_last_position[vehicle-1], [0, 13]) > 200:
                                    next_vehicle = True
                                    all_distance = 0    
                                else:
                                    break
                            else:
                                next_vehicle = False
                                vehicles_last_position[vehicle-1] = [0, 13]
                                all_distance = 0
                                vehicle+=1
                                if vehicle == 5:
                                    break
                    else:
                        break
        Fitnesses.append(Fitness)
    
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.scatter3D(X, Y, Z, c='red', marker='o')
    ax.scatter3D(X, Y, Z_avg, c='blue', marker='o')
    ax.view_init(25, 152)
    ax.set_ylabel("Threads")
    ax.set_xlabel("Iterations")
    ax.set_zlabel("Best Fitness")
    ax.set_title("Problem 1\nMost served Customers is = {}".format(max(Fitnesses)))
    # ax.set_title(Fitness_Func_string)
    # plt.savefig(c, dpi = 200)

    plt.show()

    
Problem1_plot(Main_path = "Problem 1\\best chromosome")
# Problem2_plot(Main_path = "Problem 2\\best chromosome")