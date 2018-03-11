#!/usr/bin/env python3
"""
Main file for comparison
"""
# remove later
# import pandas as pd

# from scipy.stats import norm
import scipy.stats
# from numpy.linalg import eig
from sklearn.metrics import jaccard_similarity_score
from difflib import SequenceMatcher
from scipy.spatial.distance import pdist
from scipy.stats.stats import pearsonr
from scipy.spatial.distance import jaccard
import numpy as np

from math import*

def jaccard_similarity(x,y):

    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality/float(union_cardinality)

def jaccard_index(first_set, second_set):
    """ Computes jaccard index of two sets
        Arguments:
          first_set(set):
          second_set(set):
        Returns:
          index(float): Jaccard index between two sets; it is
            between 0.0 and 1.0
    """
    # If both sets are empty, jaccard index is defined to be 1
    index = 1.0
    if first_set or second_set:
        index = (float(len(first_set.intersection(second_set)))
                 / len(first_set.union(second_set)))

    return index

def square_rooted(x):

   return round(sqrt(sum([a*a for a in x])),3)

def cosine_similarity(x,y):

 numerator = sum(a*b for a,b in zip(x,y))
 denominator = square_rooted(x)*square_rooted(y)
 return round(numerator/float(denominator),3)

# get percent
#
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def get_percentage(file_a, file_b):
    """
    Returns the percentage of overlap
    """
    file_a = file_a.flatten()
    file_b = file_b.flatten()

    return(round(len(set(file_a)&set(file_b)) / float(len(set(file_a) | set(file_b))) * 100, 1))

def get_increase(old, new):
    """
    Return calculated increased percent
    """
    increase = new - old
    return (increase / old) * 100

def get_decrease(old, new):
    """
    Return calculated decreased percent
    """
    decrease = old - new
    return ((decrease / old) * 100) * -1



def manual_traverse_overlap(a, b):
    """
    Manually traverse the hotspots and find overlap
    Works on both increased and decreased values
    """
    num_rows, row_len = a.shape
    result = np.zeros(shape=(num_rows, row_len), dtype=float)


    for y_index, y_val in enumerate(a):
        for x_index, x_val in enumerate(y_val):
            old_nr = round(a[y_index][x_index], 1)
            new_nr = round(b[y_index][x_index], 1)

            if old_nr != 0.0 and new_nr != 0.0:
                if old_nr > 0.0 and new_nr > 0.0:
                    if old_nr > new_nr:
                        result[y_index][x_index] = get_decrease(old_nr, new_nr)
                    elif old_nr < new_nr:
                        result[y_index][x_index] = get_increase(old_nr, new_nr)
                    elif old_nr == new_nr:
                        result[y_index][x_index] = 0.0
                elif old_nr < 0.0 and new_nr < 0.0:
                    if old_nr > new_nr:
                        result[y_index][x_index] = get_increase(old_nr, new_nr)
                    elif old_nr < new_nr:
                        result[y_index][x_index] = get_decrease(old_nr, new_nr)
                    elif old_nr == new_nr:
                        result[y_index][x_index] = 0.0
                else:
                    result[y_index][x_index] = None
            elif old_nr == 0.0 and new_nr == 0.0:
                result[y_index][x_index] = None
            elif old_nr == 0.0 and new_nr != 0:
                result[y_index][x_index] = None
            elif new_nr == 0.0 and old_nr != 0:
                result[y_index][x_index] = None
    return result

def calculate_jaccard(file_a, file_b):
    """
    Sets up two matrices to be used for jaccard calculation
    calculates the jaccard index
    """
    # print(file_a)
    num_rows, row_len = file_a.shape
    # counter = 1
    j_matrix_left_all = np.zeros(shape=(num_rows, row_len), dtype=int)
    j_matrix_right_all = np.zeros(shape=(num_rows, row_len), dtype=int)
    j_matrix_left_hot = np.zeros(shape=(num_rows, row_len), dtype=int)
    j_matrix_right_hot = np.zeros(shape=(num_rows, row_len), dtype=int)
    j_matrix_left_cold = np.zeros(shape=(num_rows, row_len), dtype=int)
    j_matrix_right_cold = np.zeros(shape=(num_rows, row_len), dtype=int)

    for y_index, y_val in enumerate(file_a):
        for x_index, x_val in enumerate(y_val):
            # LEFT SET

            if file_a[y_index][x_index] != 0.0: # all
                j_matrix_left_all[y_index][x_index] = 1
                if file_a[y_index][x_index] > 0.0: # hotspot
                    j_matrix_left_hot[y_index][x_index] = 1

                if file_a[y_index][x_index] < 0.0: # coldspot
                    j_matrix_left_cold[y_index][x_index] = 1
                # else:
                #     j_matrix_left_cold[y_index][x_index] = 2

            # RIGHT SET
            if file_b[y_index][x_index] != 0.0: # all
                j_matrix_right_all[y_index][x_index] = 1
                if file_b[y_index][x_index] > 0.0: # hotspot
                    j_matrix_right_hot[y_index][x_index] = 1

                if file_b[y_index][x_index] < 0.0: # coldspot
                    j_matrix_right_cold[y_index][x_index] = 1
                # else:
                #     j_matrix_right_cold[y_index][x_index] = 3

    # print("left:")
    # print(j_matrix_left_hot)
    # print("right:")
    # print(j_matrix_right_hot)

    # j_left = np.array( [[0, 0, 1, 1, 1, 0, 0], [0, 0, 1, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0]]) # 33% per lista/rad 16 är när 33% (1) har samma och däri är det 50% som har samma
    # j_right = np.array([[0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0]])
    # left2 =  [1, 0, 0, 0, 0, 1, 0, 0, 0, 0]
    # right2 = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
    # print("Jaccard1:", (1 - jaccard(left2, right2)))
    # print("Cosine:", cosine_similarity(left2, right2))
    # print("Jaccard:", jaccard_similarity(left2, right2 ))
    # print("Pearson:", pearsonr(j_matrix_left_cold.flatten(), j_matrix_right_cold.flatten()))
    # print("jaccard2:", jaccard(j_matrix_left_cold.flatten(), j_matrix_right_cold.flatten()))
    #
    #
    # print(set(j_matrix_left_cold.flatten()).union(set(j_matrix_right_cold.flatten())))

    j_all = jaccard(j_matrix_left_all.flatten(), j_matrix_right_all.flatten())
    j_hot = jaccard(j_matrix_left_hot.flatten(), j_matrix_right_hot.flatten())
    j_cold = jaccard(j_matrix_left_cold.flatten(), j_matrix_right_cold.flatten())


    return {
        "similarity": {
            "all": round((1-j_all)*100, 1),
            "hot": round((1-j_hot)*100, 1),
            "cold": round((1-j_cold)*100, 1)
        },
        "unique": {
            "all": round((j_all)*100, 1),
            "hot": round((j_hot)*100, 1),
            "cold": round(j_cold*100, 1)
        }
    }

def compare(file_a, file_b):
    """
    Compare two hotspots
    """
    # max_value_a = round(file_a.max(), 1)
    # max_value_b = round(file_b.max(), 1)
    # use_max = max_value_a if max_value_a > max_value_b else max_value_b
    #
    # min_value_a = round(file_a.min(), 1)
    # min_value_b = round(file_b.min(), 1)
    # use_min = min_value_a if min_value_a > min_value_b else min_value_b
    #
    # print("MAX: ", use_max)
    # print("MIN: ", use_min)

    result = {
        "data": manual_traverse_overlap(file_a, file_b),
        "all_percentage": get_percentage(file_a, file_b),
        "jaccard": calculate_jaccard(file_a, file_b)
        # "z_max": use_max,
        # "z_min": use_min
    }

    return result
