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

    return(len(set(file_a)&set(file_b)) / float(len(set(file_a) | set(file_b))) * 100)

def compare(file_a, file_b):
    """
    Compare two hotspots
    """

    print("Percentage: {}".format(get_percentage(file_a, file_b)) )
    # print(np.allclose(file_a, file_b))
    # a = np.matrix(file_a)
    # b = np.matrix(file_b)
    # x = norm(eig(file_a) - eig(file_b))
    # y = norm.pdf(file_a - file_b)
    # file_a.drop(file_a.head(1).index, inplace=True)


    # get -1, 0 and 1
    # y = np.sign(file_a - file_b)
    # print(y)

    # get nr of elements are the same
    # print((file_a == file_b).sum())
    # ELLER
    # print(np.count_nonzero(file_a == file_b))

    # does not work for matrices (yet)
    # print(similar(file_a, file_b))
