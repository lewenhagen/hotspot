#!/usr/bin/env python3
"""
Main file for comparison
"""
# remove later
import pandas as pd

from scipy.stats import norm
from numpy.linalg import eig
import numpy as np
# get percent
# from difflib import SequenceMatcher
#
# def similar(a, b):
#     return SequenceMatcher(None, a, b).ratio()



def print_data(data):
    """
    Pretty print matrix in terminal
    """
    print(pd.DataFrame(data))

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

def manual_traverse(a, b):
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
                if old_nr < 0.0 and new_nr < 0.0:
                    if old_nr > new_nr:
                        result[y_index][x_index] = get_increase(old_nr, new_nr)
                    elif old_nr < new_nr:
                        result[y_index][x_index] = get_decrease(old_nr, new_nr)
                    elif old_nr == new_nr:
                        result[y_index][x_index] = 0.0
            elif old_nr == 0.0 and new_nr != 0.0:
                result[y_index][x_index] = new_nr * 100
            elif old_nr != 0.0 and new_nr == 0.0:
                result[y_index][x_index] = old_nr * 100
            elif old_nr == 0.0 and new_nr == 0.0:
                result[y_index][x_index] = None
    return result



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



def compare(file_a, file_b, overlap):
    """
    Compare two hotspots
    """
    if overlap:
        result = {
            "data": manual_traverse_overlap(file_a, file_b),
            "all_percentage": get_percentage(file_a, file_b)
        }
    else:
        result = {
            "data": np.sign(file_a - file_b),#manual_traverse(file_a, file_b),
            "all_percentage": get_percentage(file_a, file_b)
        }

    # print("Percentage same values: {}".format(get_percentage(file_a, file_b)))

    # print(np.allclose(file_a, file_b))
    # get -1, 0 and 1
    y = np.sign(file_a - file_b)
    print(y)
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
