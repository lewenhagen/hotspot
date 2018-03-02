#!/usr/bin/env python3
"""
Main file for comparison
"""
# remove later
# import pandas as pd

# from scipy.stats import norm
# from numpy.linalg import eig
from sklearn.metrics import jaccard_similarity_score
import numpy as np

from math import*

def jaccard_similarity(x,y):

 intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
 union_cardinality = len(set.union(*[set(x), set(y)]))
 return intersection_cardinality/float(union_cardinality)

# get percent
# from difflib import SequenceMatcher
#
# def similar(a, b):
#     return SequenceMatcher(None, a, b).ratio()

def get_percentage(file_a, file_b):
    """
    Returns the percentage of overlap
    """
    file_a = file_a.flatten()
    file_b = file_b.flatten()

    return(round(len(set(file_a)&set(file_b)) / float(len(set(file_a) | set(file_b))) * 100, 3))

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
    num_rows, row_len = file_a.shape
    j_matrix_left = []#np.zeros(shape=(num_rows, row_len), dtype=int)
    j_matrix_right = []#np.zeros(shape=(num_rows, row_len), dtype=int)

    for y_index, y_val in enumerate(file_a):
        for x_index, x_val in enumerate(y_val):
            if file_a[y_index][x_index] > 0.0 or file_a[y_index][x_index] < 0.0:
                j_matrix_left.append(1)#[y_index][x_index] = 1
            else:
                j_matrix_left.append(0)
            if file_b[y_index][x_index] > 0.0 or file_b[y_index][x_index] < 0.0:
                j_matrix_right.append(1)#[y_index][x_index] = 1
            else:
                j_matrix_right.append(0)
    # print("left:")
    # print(j_matrix_left)
    #
    # print("right:")
    # print(j_matrix_right)

    # j_matrix_left =  [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # j_matrix_right = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # print(set(j_matrix_left.flatten()).intersection(j_matrix_right.flatten()))
    # print(set(j_matrix_left.flatten()).union(j_matrix_right.flatten()))



    return round(jaccard_similarity(j_matrix_left, j_matrix_right), 3)

def compare(file_a, file_b):
    """
    Compare two hotspots
    """
    result = {
        "data": manual_traverse_overlap(file_a, file_b),
        "all_percentage": get_percentage(file_a, file_b),
        "jaccard": calculate_jaccard(file_a, file_b)
    }


    # print("Percentage same values: {}".format(get_percentage(file_a, file_b)))

    # print(np.allclose(file_a, file_b))
    # get -1, 0 and 1
    # y = np.sign(file_a - file_b)
    # print(y)
    return result
    # a = np.matrix(file_a)
    # b = np.matrix(file_b)
    # x = norm(eig(file_a) - eig(file_b))
    # y = norm.pdf(file_a - file_b)
    # file_a.drop(file_a.head(1).index, inplace=True)



    # get nr of elements are the same
    # print((file_a == file_b).sum())
    # ELLER
    # print(np.count_nonzero(file_a == file_b))

    # does not work for matrices (yet)
    # print(similar(file_a, file_b))
