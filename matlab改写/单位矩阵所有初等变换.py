import numpy as np
import itertools


def handle_array(order,array):
    length = len(order)
    for i in range(length):
        array[i][order[i] - 1] = 1
    return array

def get_all_matrice(degree):
    basic_num = list(range(1,degree+1))
    combinations = list(itertools.permutations(basic_num,degree))
    result_list = []
    for i in combinations:
        arr = np.zeros([degree,degree])
        arr = handle_array(i,arr)
        result_list.append(arr)
    return result_list



result = get_all_matrice(10)



# ======或是先生成全排列矩阵再进行处理
import numpy as np
from sympy.utilities.iterables import multiset_permutations
a = np.array([1,2,3,4,5,6,7,8,9])
combinations = []

for p in multiset_permutations(a):
    combinations.append(p)
combinations_arr = np.array(combinations)

# 或者用矩阵代替循环：
mp = multiset_permutations(a)
combinations = list(mp)
combinations_arr = np.array(combinations)
