from distutils.command.clean import clean
import numpy as np
import math
import random

def Give_Me_next_gene(chromosome, index):
    if index < len(chromosome):
        return chromosome[index]
    else:
        return chromosome[index - len(chromosome)]
class CutAndCrossFill():
    def __init__(self):
        self.name = "CutAndCrossFill"
        pass
    def Recombination(self, parent1, parent2):
        CuterPoint = np.random.randint(0, len(parent1))
        # CuterPoint = 3
        child1 = parent1[:CuterPoint]
        child2 = parent2[:CuterPoint]
        for i in np.arange(CuterPoint, len(parent1)):
            
            index_Parent2 = 0
            index_Parent1 = 0
            break_it_1 = False
            break_it_2 = False
            while True:
                fromparent2 = Give_Me_next_gene(parent2, index_Parent2+i)
                fromparent1 = Give_Me_next_gene(parent1, index_Parent1+i)
                if fromparent2 not in child1 and not break_it_1:
                    child1.append(fromparent2)
                    break_it_1 = True
                else:
                    index_Parent2+=1
                if fromparent1 not in child2 and not break_it_2:
                    child2.append(fromparent1)
                    break_it_2 = True
                else:
                    index_Parent1+=1
                if break_it_2 and break_it_1:
                    break
                if index_Parent2 > len(parent1) or index_Parent2 > len(parent1):
                    raise Exception("Something went wrong in CutAndCrossFill")
        return child1, child2
class Order():
    def __init__(self):
        self.name = "Order"
        pass
    def Recombination(self, parent1, parent2):
        # CuterPoint = sorted([np.random.randint(0, len(parent1)), np.random.randint(0, len(parent1))])
        CuterPoint = sorted([3, 6])
        CuterPoint[1] = CuterPoint[1]+1
        # CuterPoint = 
        child1_ToControle = parent1[CuterPoint[0]:CuterPoint[1]]
        child2_ToControle = parent2[CuterPoint[0]:CuterPoint[1]]
        child1 = parent1.copy()
        child2 = parent2.copy()
        listed_genes1 = list(np.arange(CuterPoint[1], len(parent1)))
        listed_genes2 = list(range(CuterPoint[0]))
        listed_genes = listed_genes1 + listed_genes2
        for i in listed_genes:
            index_Parent2 = 0
            index_Parent1 = 0
            break_it_1 = False
            break_it_2 = False
            while True:
                fromparent2 = Give_Me_next_gene(parent2, index_Parent2+i)
                fromparent1 = Give_Me_next_gene(parent1, index_Parent1+i)
                if fromparent2 not in child1_ToControle and not break_it_1:
                    child1[i] = fromparent2
                    child1_ToControle.append(fromparent2)
                    break_it_1 = True
                elif fromparent2 in child1_ToControle:
                    index_Parent2+=1
                if fromparent1 not in child2_ToControle and not break_it_2:
                    child2[i] = fromparent1
                    break_it_2 = True
                    child2_ToControle.append(fromparent1)
                elif fromparent1 in child2_ToControle:
                    index_Parent1+=1
                if break_it_2 and break_it_1:
                    break
        return child1, child2
class Cycle1():
    def __init__(self):
        self.name = "Cycle"
        pass
    def fillNoneWithSwappedValue(self, arr1 ,arr2 ,final1 ,final2 ):
        for a in range(0,arr1.__len__()):
            if final1[a] == None:
                final1[a] = arr2[a]
            if final2[a] == None:
                final2[a] = arr1[a]
        return final1,final2
    def indexOf(self, arr,x):
        for a in range(0,arr.__len__()):
            if arr[a] == x:
                return a
        return -1

    def Recombination(self, parent1, parent2 ):
        offspring1 = [None] * parent1.__len__()
        offspring2 = [None] * parent2.__len__()
        size1 = 1
        size2 = 1

        initalSelected = parent1[0]
        offspring1[0] = parent1[0]
        latestUpdated2 = parent2[0]
        check = 1

        while size1 < parent1.__len__() or size2 < parent2.__len__():
            if latestUpdated2 == initalSelected:
                index2 = self.indexOf(parent2,latestUpdated2)
                offspring2[index2] = parent2[index2]
                ans1,ans2 = self.fillNoneWithSwappedValue(parent1, parent2, offspring1, offspring2)
                offspring1 = ans1
                offspring2 = ans2
                size1 = parent1.__len__()
                size2 = parent2.__len__()
                check = 0
            else:
                index2 = self.indexOf(parent2,latestUpdated2)
                offspring2[index2] = parent2[index2]
                size2 += 1
                index1 = self.indexOf(parent1,parent2[index2])
                offspring1[index1] = parent1[index1]
                size1 += 1
                latestUpdated2 = parent2[index1]
        if check:
            index2 = self.indexOf(parent2, latestUpdated2)
            offspring2[index2] = parent2[index2]
        return offspring1,offspring2
class Cycle2():
    def __init__(self):
        self.name = "Cycle"
        pass
    def indexOf(self, arr,x):
        for a in range(0,arr.__len__()):
            if arr[a] == x:
                return a
        return -1

    def findUnusedIndexValues(self, parent,offspring):
        res = list()
        for a in parent:
            if self.indexOf(offspring,a) == -1:
                res.append(a)
        return res
    def Recombination(self, parent1, parent2 ):
        offspring1 = [None] * parent1.__len__()
        offspring2 = [None] * parent2.__len__()
        i1 = 0
        i2 = 0
        initalSelected = parent1[0]
        offspring1[i1] = parent2[0]
        i1 += 1
        # latestUpdated2 = parent2[0]
        check = 1

        while i1 < parent1.__len__() and i2 < parent2.__len__():
            index1 = self.indexOf(parent1,offspring1[i1-1])
            index1 = self.indexOf(parent1,parent2[index1])
            latestUpdated2 = parent2[index1]
            if latestUpdated2 == initalSelected:
                offspring2[i2] = latestUpdated2
                i2 += 1
                # print("cycle detected")
                check = 0
                res1 = self.findUnusedIndexValues(parent1,offspring1)
                res2 = self.findUnusedIndexValues(parent2,offspring2)
                # print(res1,res2)
                ans1,ans2 = self.Recombination(res1, res2)
                offspring1[i1:] = ans1
                offspring2[i2:] = ans2
                check = 0
                break
            else:
                offspring2[i2] = parent2[index1]
                i2 += 1
                index1 = self.indexOf(parent1,offspring2[i2-1])
                offspring1[i1] = parent2[index1]
                i1 += 1
        if check:
            index1 = self.indexOf(parent1, offspring1[i1 - 1])
            index1 = self.indexOf(parent1, parent2[index1])
            latestUpdated2 = parent2[index1]
            offspring2[i2] = latestUpdated2
            i2 += 1
        return offspring1,offspring2
                            
class edge_CrossOver_Operator():
    def __init__(self):
        self.name = "edge_CrossOver_Operator"
        pass
    # def choice():
    def clean_lists(self, value):
        for i in range(len(self.neighbors)):
            if value in self.neighbors[i]:
                self.neighbors[i].pop(self.neighbors[i].index(value))
    def indices(self, lst, item):
        return [i for i, x in enumerate(lst) if x == item]
    def next_choices(self, value):
        temp_lens = []
        for i in self.neighbors[self.values.index(value)]:
            temp_lens.append(len(self.neighbors[self.values.index(i)]))
        if len(temp_lens) != 0:
            temp_duplicated_indexes = self.indices(temp_lens, min(temp_lens))
            for temp_duplicated_indexe in temp_duplicated_indexes:
                # print(self.duplicated_indexes[self.neighbors[self.values.index(value)][temp_duplicated_indexe]-1])
                if self.duplicated_indexes[self.neighbors[self.values.index(value)][temp_duplicated_indexe]-1] != "":
                    return self.neighbors[self.values.index(value)][temp_duplicated_indexe]
            return self.neighbors[self.values.index(value)][temp_lens.index(min(temp_lens))]
        else:
            # if len(self.not_empy_lists)==0:
            not_empy_lists = []
            index = -1
            for i in self.neighbors:
                index+=1
                if len(i) != 0:
                    not_empy_lists.append(index)
            delete_it = random.choice(not_empy_lists)
            temp_value_ = self.neighbors[delete_it]
            return random.choice(temp_value_)

    def Recombination(self, parent1, parent2):
        neighbors = []
        values = []
        child = []
        duplicated_indexes = []
        for i in range(len(parent1)):
            neighbor = []
            values.append(i+1)
            index = parent2.index(i+1)
            neighbor.append(Give_Me_next_gene(parent2, index-1))
            neighbor.append(Give_Me_next_gene(parent2, index+1))
            index = parent1.index(i+1)
            neighbor.append(Give_Me_next_gene(parent1, index-1))
            neighbor.append(Give_Me_next_gene(parent1, index+1))
            neighbors.append(list(set(neighbor)))
            if len(set(neighbor)) != len(neighbor):
                for c in neighbor:
                    temp_duplicated_indexes = self.indices(neighbor, c)
                    if len(temp_duplicated_indexes)>1:
                        duplicated_indexes.append(neighbor[temp_duplicated_indexes[0]])
                        break
            else:
                duplicated_indexes.append("")
        self.duplicated_indexes = duplicated_indexes
        self.neighbors = neighbors
        self.values = values
        # first_value_to_start = np.random.choice(len(values))+1
        first_value_to_start = 1

        child.append(first_value_to_start)  
        while True:
            self.clean_lists(value=child[-1])
            value = self.next_choices(child[-1])
            child.append(value)
            if len(child) == len(parent1):
                break
            # print(self.neighbors)
        return parent1, child

