#/usr/bin/env python3
"""
Main file for different metrics
"""

import numpy as np

def jaccard(left, right):
    """
    Calculates Jaccard Similarity Index
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

    # print("p:", true_true)
    # print("q:", true_false)
    # print("r:", false_true)
    # print("s:", false_false)

    return true_true / (true_false + false_true + true_true)
