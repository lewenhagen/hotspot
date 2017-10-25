#!/usr/bin/env python3
import pysal
from pysal.esda.getisord import G_Local
from pysal.weights.Distance import DistanceBand
import random as rm
import numpy as np
import math
"""
Module for LISA Statistics
"""

#
def print_data(data):
    # print("[ 0   1   2   3   4   5   6]")
    # for i, x in enumerate(data):
    #     print(i, np.around(x.astype(np.double), 2))
    for index, value in np.ndenumerate(data):
        print(index, value)

def get_neigbours(data, y, x, d):
    if y < len(data) and x < len(data[y]):
        start = data[y][x]
        new_data = []
        size_x = len(data[0])
        size_y = len(data)

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
                new_data[counterY].append(data[startY][startX])

                counterX += 1
                startX += 1
                startX = startX % size_x

            startY = (startY + 1) % size_y
            counterY += 1

    else:
        print("x or y is out of range")


    # print_data(new_data)
    return new_data



def get_neigbours_inbound(data, y, x, min_y, max_y, min_x, max_x, d):
    # print("here:", data[:3, :3])
    print("min_y:", min_y)
    print("max_y:", max_y)
    print("min_x:", min_x)
    print("max_x:", max_x)

    return data[min_y:max_y, min_x:max_x]


def calculate_from_matrix(matrix):
    """
    calculates awesome stuff
    """
    # Initialization of variables
    raw_data = np.matrix(matrix)
    n = raw_data.size
    mean = raw_data.mean()
    num_rows, row_len = raw_data.shape
    raw_total = raw_data.sum()

    distance = 1
    weight = 1
    square_sum = np.sum(raw_data**2)

    j_counts_matrix = np.zeros(shape=(num_rows, row_len), dtype=object)
    gi_matrix = np.zeros(shape=(num_rows, row_len), dtype=object)

    for index, value in np.ndenumerate(raw_data):
        i, j = index

        min_y = -1
        max_y = -1
        min_x = -1
        max_x = -1


        if (j - distance) < 1:
            min_x = 1
        else:
            min_x = j - distance

        if (j + distance) > row_len:
            max_x = row_len
        else:
            max_x = j + distance

        if (i - distance) < 1:
            min_y = 1
        else:
            min_y = i - distance

        if (i + distance) > num_rows:
            max_y = num_rows
        else:
            max_y = i + distance


        # local_temp = get_neigbours_inbound(raw_data, i, j, min_y, max_y, min_x, max_x, distance)
        # print("Local:temp", local_temp)
        # local_temp = get_neigbours(matrix, i, j, distance)
        # print_data(local_temp)

        square_weight = 0
        j_count = 0
        m_sum = 0

        for trow in raw_data[min_y:max_y]:
            m_sum += sum(raw_data[trow, min_x:max_x])
            for tcol in raw_data[min_x:max_x]:
                square_weight += weight**2
            j_count += (max_x - min_x + 1)
        # for local_y in local_temp:
        #     m_sum += sum(local_y)
        #
        #     for local_x in local_y:
        #         square_weight += weight**2
        #
        #     j_count += max(local_y) - min(local_y) + 1

        j_counts_matrix[i][j] = j_count
        numerator = m_sum - (mean * j_counts_matrix[i][j])
        S = math.sqrt( (square_sum / n) - (mean**2) )
        denominator = S * math.sqrt( ( (n * j_counts_matrix[i][j]) - square_weight**2) / n )
        gi_matrix[i][j] = numerator / denominator



    # for i, y_val in enumerate(matrix):
    #     for j, x_val in enumerate(y_val):
    #         local_temp = get_neigbours(matrix, i, j, distance)
    #         # print_data(local_temp)
    #
    #         square_weight = 0
    #         j_count = 0
    #         m_sum = 0
    #         for local_y in local_temp:
    #             m_sum += sum(local_y)
    #
    #             for local_x in local_y:
    #                 square_weight += pow(weight, 2)
    #
    #             j_count += max(local_y) - min(local_y) + 1
    #
    #         j_counts_matrix[i][j] = j_count
    #         numerator = m_sum - (mean * j_counts_matrix[i][j])
    #         S = math.sqrt( (square_sum / n) - (pow(mean, 2)) )
    #         denominator = S * math.sqrt( ( (n * j_counts_matrix[i][j]) - pow(square_weight, 2)) / n )
    #         gi_matrix[i][j] = round(numerator / denominator, 2)
    #         # print(gi_matrix[i][j])
    return gi_matrix
    # print_data(gi_matrix)
    # print("raw_data:", raw_data)
    # print("n:", n)
    # print("mean:", mean)
    # print("row_len:", row_len)
    # print("num_rows:", num_rows)


    # for y in t_map:
    #     for x in y:
    #         print(x)

    # lg = G_Local(y, dist_w)
    # lg.n
# s_counter = 0

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
print_data(calculate_from_matrix(test_matrix))




# get_neigbours(test_data, 23, 0, 4)
