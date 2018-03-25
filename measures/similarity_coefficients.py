#/usr/bin/env python3
"""
Main file for different similarity coefficients
"""

import numpy as np
from math import sqrt

def setup_data(left, right):
    """
    Sets up data. left and right should be numpy arrays.
    Returns four variables.
    """
    true_false = 0
    false_true = 0
    false_false = 0
    true_true = 0

    if len(left) == len(right):
        for index, val in enumerate(left):
            if left[index] == 1 and right[index] == 0: # true false
                true_false += 1
            elif left[index] == 0 and right[index] == 1: # false true
                false_true += 1
            elif left[index] == 0 and right[index] == 0: # false false
                false_false += 1
            elif left[index] == 1 and right[index] == 1: # true true
                true_true += 1

            elif left[index] == -1 and right[index] == 0: # true false
                true_false += 1
            elif left[index] == 0 and right[index] == -1: # false true
                false_true += 1
            elif left[index] == -1 and right[index] == -1: # true true
                true_true += 1

    return (true_true, true_false, false_true)



def jaccard(left, right):
    """
    Calculates Jaccard Similarity Index
    """
    a, b, c = setup_data(left, right)

    return a / (a + b + c)



def s_dice(left, right):
    """
    Calculates Sørensen-Dice Index
    """
    a, b, c = setup_data(left, right)

    return 2*a / ((2*a) + b + c)



def kulczynski(left, right):
    """
    Calculates Kulczynski Index
    """
    a, b, c = setup_data(left, right)

    return 0.5 * ( (a / (a + b)) + (a / (a + c)) )



def ochai(left, right):
    """
    Calculates Ochai Index
    """
    a, b, c = setup_data(left, right)

    return a / sqrt( (a + b) * (a + c) )


if __name__ == "__main__":
    unique_left =  [1, 0, 1, 0, 0, 1, 0, 0, 0, 0]
    unique_right = [0, 0, 0, 0, 0, 0, 1, 0, 0, 1]

    identical_left =  [1, 0, 1, 0, 0, 1, 0, 0, 0, 0]
    identical_right = [1, 0, 1, 0, 0, 1, 0, 0, 0, 0]

    partial_left =  [0, 0, 1, 0, 0, 1, 0, 0, 1, 0] # 3 / 5 = 6 / 10 = 60 / 100
    partial_right = [1, 0, 1, 0, 0, 1, 1, 0, 1, 0]

    print("Jaccard unique:", jaccard(unique_left, unique_right))
    print("Jaccard identical:", jaccard(identical_left, identical_right))
    print("Jaccard partial:", jaccard(partial_left, partial_right))

    print("Sorensen-Dice unique:", s_dice(unique_left, unique_right))
    print("Sorensen-Dice identical:", s_dice(identical_left, identical_right))
    print("Sorensen-Dice partial:", s_dice(partial_left, partial_right))

    print("Kulczynski unique:", kulczynski(unique_left, unique_right))
    print("Kulczynski identical:", kulczynski(identical_left, identical_right))
    print("Kulczynski partial:", kulczynski(partial_left, partial_right))

    print("Ochai unique:", ochai(unique_left, unique_right))
    print("Ochai identical:", ochai(identical_left, identical_right))
    print("Ochai partial:", ochai(partial_left, partial_right))
