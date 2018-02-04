#!/usr/bin/env python3
"""
Main file for comparison
"""
# remove later
import pandas as pd

from scipy.stats import norm
from numpy.linalg import eig
import numpy as np

def print_data(data):
    """
    Pretty print matrix in terminal
    """
    print(pd.DataFrame(data))

def compare(file_a, file_b):
    """
    Compare two hotspots
    """
    # a = np.matrix(file_a)
    # b = np.matrix(file_b)
    # x = norm(eig(file_a) - eig(file_b))
    y = norm.pdf(file_a - file_b)
    # file_a.drop(file_a.head(1).index, inplace=True)
    print(y)
