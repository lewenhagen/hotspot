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
    # for i in range(len(data)):
    #     # print(data[i])
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
    distance = 3
    weight = 1
    square_sum = (np.sum(np.square(raw_data)))
    j_counts_matrix = np.zeros(shape=(num_rows, row_len), dtype=object)
    gi_matrix = np.zeros(shape=(num_rows, row_len), dtype=object)

    for index, value in np.ndenumerate(raw_data):
        rows, cols = index
    # for rows in range(num_rows):
    #     for cols in range(row_len):
        ########################################################################
        min_x = 0 if (cols - distance) < 0 else (cols - distance)
        max_x = row_len if (cols + distance) > row_len else (cols + distance)

        min_y = 0 if (rows - distance) < 0 else (rows - distance)
        max_y = num_rows if (rows + distance) > num_rows else (rows + distance)
        ########################################################################

        # local_temp = get_neigbours_inbound(raw_data, i, j, min_y, max_y, min_x, max_x, distance)
        # print("Local:temp", local_temp)
        # local_temp = get_neigbours(matrix, i, j, distance)
        # print_data(local_temp)

        m_sum = 0
        square_weight = 0
        j_count = 0

        if max_y != row_len and max_y != 0:
            max_y += 1

        if max_x != num_rows and max_x != 0:
            max_x += 1

        for trow in range(min_y, max_y):
            m_sum += raw_data[trow, min_x:max_x].sum()

            for tcol in range(min_x, max_x):
                square_weight += (weight * weight)

            j_count += (max_x - min_x)

        # for local_y in local_temp:
        #     m_sum += sum(local_y)
        #
        #     for local_x in local_y:
        #         square_weight += weight**2
        #
        #     j_count += max(local_y) - min(local_y) + 1
        # print("j_count:", j_count)
            j_counts_matrix[rows][cols] = j_count


        numerator = m_sum - (mean * j_counts_matrix[rows][cols])
        S = math.sqrt( (square_sum / n) - (mean**2) )
        denominator = S * math.sqrt( ( (n * j_counts_matrix[rows][cols]) - square_weight**2) / n )

        gi_matrix[rows][cols] = np.around(numerator / denominator, 2)



    return gi_matrix


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
