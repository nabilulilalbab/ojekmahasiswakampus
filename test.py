import math 



def calculateCost(km : float) -> float :
    cost = 0
    constCost = 8500
    if km <= 4 :
        cost = 8500
    else :
        kmdinamis = km - 4
        cost = (kmdinamis * 2000) + constCost
    return cost
