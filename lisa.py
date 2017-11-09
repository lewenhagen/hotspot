#!/usr/bin/env python3
# import pysal
# from pysal.esda.getisord import G_Local
# from pysal.weights.Distance import DistanceBand
import random as rm
import numpy as np
import math
import pandas as pd
import scipy.stats as st
from scipy import mean as sci_mean
# import scikits.bootstrap as bootstrap
# import scipy as sp
# from pandas import DataFrame
"""
Module for LISA Statistics
"""


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def print_data(data):
    print(pd.DataFrame(data))


def get_neigbours(data, y, x, d, w):
    """
    Calculates the neighbourhood, with modulus
    """
    new_data = []
    m_sum = 0
    square_weight = 0
    j_count = 0
    start = data[y, x]
    size_y, size_x = data.shape

    iterations = d+d+1

    for _ in range(iterations):
        new_data.append([])

    startY = (y - d) % size_y
    startX = (x - d) % size_x

    counterY = 0

    while counterY < iterations:
        counterX = 0
        startX = (x - d) % size_x
        while counterX < iterations:
            new_data[counterY].append(np.around(data[startY, startX], 2))

            counterX += 1
            startX += 1
            startX = startX % size_x

        startY = (startY + 1) % size_y
        counterY += 1
    # print("HERE:", new_data)
    for local_y in new_data:
        m_sum += sum(local_y)

        for local_x in local_y:
            square_weight += w * w

        j_count += len(local_y)

    return {"sum": m_sum, "square_weight": square_weight, "j_count": j_count}



def get_neigbours_inbound(data, rows, cols, distance, w, n_rows, r_len):
    """
    Calculates the neighbourhood, inbound
    """
    row_len, num_rows = data.shape
    m_sum = 0
    square_weight = 0
    j_count = 0

    min_x = 0 if (cols - distance) < 0 else (cols - distance)
    max_x = row_len if (cols + distance) > row_len else (cols + distance)

    min_y = 0 if (rows - distance) < 0 else (rows - distance)
    max_y = num_rows if (rows + distance) > num_rows else (rows + distance)

    if max_y < row_len and max_y > 0:
        max_y += 1

    if max_x < num_rows and max_x > 0:
        max_x += 1

    for trow in range(min_y, max_y):
        m_sum += data[trow, min_x:max_x].sum()

        for tcol in range(min_x, max_x):
            square_weight += (w * w)

        j_count += (max_x - min_x)

    return {"sum": m_sum, "square_weight": square_weight, "j_count": j_count}




def conf(data, confidence=0.95):
    mean = data.mean()

    var = np.var(data) # variance

    std=math.sqrt(var)

    return st.norm.interval(confidence, loc=mean, scale=std)




def calculate_from_matrix(matrix):
    # print("HERE:")
    # print(pd.DataFrame(st.zscore(matrix, axis=None, ddof=3)))
    """
    Creates a matrix based on Local Getis and Ord*, (Local Gi*)
    """
    # Initialization of variables
    raw_data = np.matrix(matrix)
    n = raw_data.size
    mean = raw_data.mean()
    num_rows, row_len = raw_data.shape
    # raw_total = raw_data.sum
    distance = 1
    weight = 1
    square_sum = (np.sum(np.square(raw_data))) # sum(map(sum, matrix))
    gi_matrix = np.zeros(shape=(num_rows, row_len), dtype=float)

    for index, value in np.ndenumerate(raw_data):

        rows, cols = index
        # print("rows:", rows)
        # print("cols:", cols)
        result = get_neigbours(raw_data, rows, cols, distance, weight)
        # result = get_neigbours_inbound(raw_data, rows, cols, distance, weight, num_rows, row_len)
        # print(result)
        m_sum = result["sum"]
        square_weight = result["square_weight"]
        j_count = result["j_count"]

        numerator = m_sum - (mean * j_count)
        S = math.sqrt( (square_sum / n) - (mean**2) )
        denominator = S * math.sqrt( ( (n * j_count) - square_weight**2) / n )

        res = np.around(numerator / denominator, 2)
        # print(rows, cols, st.norm.cdf(0.1))
        gi_matrix[rows][cols] =  res #if res != 0 else 0

    # print_data(raw_data)
    # print_data(gi_matrix)

    # print(gi_matrix)

    # print(pd.DataFrame(st.norm.pdf(gi_matrix)))

    # print(st.norm.ppf(gi_matrix))
    # sigma = np.std(gi_matrix)
    # s_mean = np.mean(gi_matrix)
    # # print(st.norm.interval(0.95, loc=s_mean, scale=sigma))
    # test = 1 - 4 * 0.05
    #
    # level = 1 - 256 * (0.05)
    # print(level)
    # print("90%")
    # print(conf(gi_matrix, 0.90))
    # print("95%")
    # print(conf(gi_matrix, 0.95))
    # print("99%")
    # print(conf(gi_matrix, 0.99))
    # print("99.99%")
    # print(conf(gi_matrix, 0.9999))
    result = {
        "getis": gi_matrix,
        "conf_levels": {
                "0.90": conf(gi_matrix, 0.90),
                "0.95": conf(gi_matrix, 0.95),
                "0.99": conf(gi_matrix, 0.99)
                }
    }
    # print(mean_confidence_interval(gi_matrix))
    # print( bootstrap.ci(data=gi_matrix, statfunction=sci_mean, alpha=0.05) )
    # print(confIntMean(gi_matrix.flatten()))
    # print(st.t.interval(0.95, len(gi_matrix)-1, loc=np.mean(gi_matrix), scale=st.sem(gi_matrix)))

    return result

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
# Totalt: 394
# print_data(calculate_from_matrix(test_matrix))
