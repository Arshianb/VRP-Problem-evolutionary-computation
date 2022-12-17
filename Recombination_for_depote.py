import numpy as np


def Single_point_crossOver(S1, S2):
    Where = np.random.randint(len(S1))
    for i in range(len(S1)):
        if i >= Where:
            temp = S2[i]
            S2[i] = S1[i]
            S1[i] = temp
    return S1, S2

def Double_point_crossOver(S1, S2):
    TempWhere1 = np.random.randint(len(S1))
    TempWhere2 = np.random.randint(len(S1))
    Where1 = np.min([TempWhere1, TempWhere2])
    Where2 = np.max([TempWhere1, TempWhere2])
    for i in range(len(S1)):
        if i >= Where1 and i<=Where2:
            temp = S2[i]
            S2[i] = S1[i]
            S1[i] = temp
    return S1, S2

def Uniform_point_crossOver(S1, S2):
    for i in range(len(S1)):
        if np.random.random() > 0.5:
            temp = S2[i]
            S2[i] = S1[i]
            S1[i] = temp
    return S1, S2
