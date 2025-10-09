import numpy as np

def sum(a:list[int], b:list[int]) -> list[int]:
    primary_ist = np.array(a)
    secondary_list = np.array(b)
    return primary_ist + secondary_list
