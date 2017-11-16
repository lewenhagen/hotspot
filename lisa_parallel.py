#!/usr/bin/env python3

import numpy as np
import math
import pandas as pd
import scipy.stats as st
from scipy import mean as sci_mean

from getis import Gi

import time
from multiprocessing import Pool

from confidence_interval import conf_interval as conf

"""
Module for LISA Statistics
"""

# Set variables for printing in terminal
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def print_data(data):
    """
    Pretty print matrix in terminal
    """
    print(pd.DataFrame(data))


# def get_neigbours(data, y, x, d, w):
#     """
#     Calculates the neighbourhood, with modulus
#     """
#     new_data = []
#     m_sum = 0
#     square_weight = 0
#     j_count = 0
#     start = data[y, x]
#     size_y, size_x = data.shape
#
#     iterations = d+d+1
#
#     for _ in range(iterations):
#         new_data.append([])
#
#     startY = (y - d) % size_y
#     startX = (x - d) % size_x
#
#     counterY = 0
#
#     while counterY < iterations:
#         counterX = 0
#         startX = (x - d) % size_x
#         while counterX < iterations:
#             new_data[counterY].append(np.around(data[startY, startX], 2))
#
#             counterX += 1
#             startX += 1
#             startX = startX % size_x
#
#         startY = (startY + 1) % size_y
#         counterY += 1
#
#     for local_y in new_data:
#         m_sum += sum(local_y)
#
#         for local_x in local_y:
#             square_weight += w * w
#
#         j_count += len(local_y)
#
#     return {"sum": m_sum, "square_weight": square_weight, "j_count": j_count}
#
#
#
#
#
# def calculate_from_matrix(matrix):
#     """
#     Creates a matrix based on Local Getis and Ord*, (Local Gi*)
#     """
#     start_time = time.time()
#     # Initialization of variables
#     raw_data = np.matrix(matrix)
#     n = raw_data.size
#     mean = raw_data.mean()
#     num_rows, row_len = raw_data.shape
#     # raw_total = raw_data.sum
#     distance = 1
#     weight = 1
#     square_sum = (np.sum(np.square(raw_data)))
#     gi_matrix = np.zeros(shape=(num_rows, row_len), dtype=float)
#
#     pool = Pool()
#
#     for index, value in np.ndenumerate(raw_data):
#
#         rows, cols = index
#
#
#         result = pool.map(get_neigbours, [raw_data, rows, cols, distance, weight])
#
#         m_sum = result["sum"]
#         square_weight = result["square_weight"]
#         j_count = result["j_count"]
#
#         numerator = m_sum - (mean * j_count)
#         S = math.sqrt( (square_sum / n) - (mean**2) )
#         denominator = S * math.sqrt( ( (n * j_count) - square_weight**2) / n )
#
#         res = np.around(numerator / denominator, 2)
#
#         gi_matrix[rows][cols] =  res
#
#     pool.close()
#     pool.join()
#     result = {
#         "getis": gi_matrix,
#         "conf_levels": {
#                 "0.90": conf(gi_matrix, 0.90),
#                 "0.95": conf(gi_matrix, 0.95),
#                 "0.99": conf(gi_matrix, 0.99)
#                 }
#     }
#     print("--- %s seconds ---" % (time.time() - start_time))
#     return result
# Verify correctness of function calculateGiScoreMatrix with example on page 165 in Chainey and
# Ratcliffe's book "GIS and Crime Mapping"
test_matrix = [
    [1,1,1,5,0,0,0,1,0,0,0,0,0,0,3,2], # 14
    [0,3,0,0,6,1,0,1,1,0,0,0,0,0,1,3], # 16
    [5,0,0,0,0,1,9,5,0,0,3,0,0,1,0,1], # 25
    [1,4,0,2,0,5,0,0,0,1,1,0,0,0,0,2], # 16
    [1,0,2,3,0,3,6,0,1,2,0,0,0,1,5,0], # 24
    [3,5,0,4,0,0,0,2,1,2,1,1,0,0,1,0], # 20
    [0,0,1,1,8,1,6,6,2,2,0,1,0,1,2,0], # 31
    [0,2,2,2,4,6,12,9,2,2,3,6,2,0,0,2], # 54
    [0,0,3,8,5,1,2,1,1,1,5,0,0,0,2,2], # 31
    [1,2,4,2,1,0,1,0,1,3,0,0,2,3,0,2], # 22
    [4,4,1,0,0,1,1,1,0,2,1,4,2,1,6,4], # 32
    [1,1,0,0,0,0,0,0,1,4,5,2,2,6,1,0], # 23
    [0,0,0,2,0,0,1,0,2,6,1,3,0,4,0,0], # 19
    [1,1,0,0,0,0,0,0,0,2,0,0,13,0,0,0], # 17
    [0,0,0,1,1,0,0,0,1,4,6,0,2,0,0,0], # 15
    [0,8,2,6,0,0,0,4,3,1,4,7,0,0,0,0] # 35
]

real_test_matrix = [
[68.572, 71.866, 71.911, 78.126, 82.657, 141.275, 165.821],
[80.385, 79.612, 89.549, 92.047, 94.857, 159.282, 168.846],
[86.896, 93.582, 108.077, 89.076, 101.59, 149.312, 156.221],
[73.538, 78.552, 86.831, 97.91, 100.007, 147.114, 153.528],
[69.443, 74.08, 71.814, 81.423, 78.1, 134.274, 129.818],
[63.695, 64.989, 66.831, 69.081, 73.186, 114.87, 119.69],
[70.75, 63.488, 64.787, 75.097, 70.565, 97.81, 108.351],
[80.639, 81.515, 80.949, 83.846, 85.698, 93.955, 103.041],
[109.591, 101.17, 108.573, 106.283, 98.825, 93.999, 89.262],
[116.722, 124.726, 125.856, 122.164, 125.148, 99.987, 92.35],
[140.347, 137.358, 146.882, 136.935, 148.832, 105.246, 91.31],
[138.219, 149.48, 166.032, 160.447, 152.609, 115.059, 94.244],
[155.778, 166.675, 186.683, 169.972, 163.171, 115.02, 97.114],
[155.336, 179.119, 188.886, 171.733, 176.499, 131.112, 105.069],
[175.254, 174.099, 187.675, 167.274, 181.207, 140.252, 99.5],
[160.248, 163.302, 166.443, 171.123, 183.708, 166.698, 102.936],
[164.03, 169.833, 164.555, 165.164, 196.36, 184.065, 107.679],
[153.958, 159.319, 185.984, 176.55, 217.531, 224.336, 106.408],
[139.409, 150.137, 163.719, 158.959, 231.541, 230.345, 101.416],
[122.482, 134.157, 145.391, 144.396, 219.715, 235.422, 89.188],
[95.862, 120.507, 133.847, 122.315, 207.273, 207.102, 79.282],
[83.362, 83.89, 96.499, 102.739, 182.843, 212.987, 78.457],
[76.42, 70.432, 86.595, 92.142, 169.206, 203.029, 71.066],
[105.538, 84.411, 117.781, 85.257, 175.185, 192.827, 91.749]

]
# Totalt: 394
# print_data(calculate_from_matrix(real_test_matrix)["getis"])
start_time = time.time()
gi = Gi(real_test_matrix)
gi.calculate()
print_data(gi.get_result())
print(gi.confidence_interval(0.97))
print("--- %s seconds ---" % (time.time() - start_time))
