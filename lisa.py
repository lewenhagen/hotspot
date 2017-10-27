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
    # print(raw_data)
    n = raw_data.size
    mean = raw_data.mean()
    num_rows, row_len = raw_data.shape
    # print("num_rows:", num_rows)
    # print("row_len", row_len)

    raw_total = raw_data.sum()

    distance = 3
    # dist_y = distance
    # dist_x = distance
    weight = 1
    # square_sum = (raw_data*raw_data).sum()
    square_sum = (np.sum(np.square(raw_data)))

    j_counts_matrix = np.zeros(shape=(num_rows, row_len), dtype=object)
    gi_matrix = np.zeros(shape=(num_rows, row_len), dtype=object)

    # for index, value in np.ndenumerate(raw_data):
    #     i, j = index
    for rows in range(num_rows):
        for cols in range(row_len):
            # print(raw_data[rows])
            # print(cols)
            # print(i, j)

            # min_y = -1
            # max_y = -1
            # min_x = -1
            # max_x = -1


            if (cols - distance) < 0:
                min_x = 0
            else:
                min_x = cols - distance

            if (cols + distance) > row_len:
                max_x = row_len
            else:
                max_x = cols + distance

            if (rows - distance) < 0:
                min_y = 0
            else:
                min_y = rows - distance

            if (rows + distance) > num_rows:
                max_y = num_rows
            else:
                max_y = rows + distance

            # print("col-min:", min_x)
            # print("col-max:", max_x)
            # print("row-min:", min_y)
            # print("row-max:", max_y)


            # local_temp = get_neigbours_inbound(raw_data, i, j, min_y, max_y, min_x, max_x, distance)
            # print("Local:temp", local_temp)
            # local_temp = get_neigbours(matrix, i, j, distance)
            # print_data(local_temp)

            m_sum = 0
            square_weight = 0
            j_count = 0


            for trow in range(min_y, max_y):
                # print(raw_data[trow, min_x:max_x])
                # print(raw_data[trow, min_x:max_x].sum())
            
                m_sum += raw_data[trow, min_x:max_x+1].sum()
                # print(m_sum)

                # print(raw_data[trow, min_x:max_x])
                print(range(min_x, max_x))
                for tcol in range(min_x, max_x):
                    # print(tcol)
                    # print(raw_data[trow][tcol])
                    square_weight += (weight * weight)
                    print(square_weight)

                j_count += (max_x - min_x)
                # print(j_count)
                # print("col-max", max_x)
                # print("col-min", min_x)

            # for local_y in local_temp:
            #     m_sum += sum(local_y)
            #
            #     for local_x in local_y:
            #         square_weight += weight**2
            #
            #     j_count += max(local_y) - min(local_y) + 1
            # print("j_count:", j_count)
                j_counts_matrix[rows][cols] = j_count

            # print("j_count: ", j_count)
            # print(j_counts_matrix[i][j])
            # print("m_sum:", m_sum)
            numerator = m_sum - (mean * j_counts_matrix[rows][cols])

            S = math.sqrt( (square_sum / n) - (mean**2) )
            denominator = S * math.sqrt( ( (n * j_counts_matrix[rows][cols]) - square_weight**2) / n )

            gi_matrix[rows][cols] = numerator / denominator
            # print("numerator", numerator)
            # print("denominator", denominator)


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

    # print_data(j_counts_matrix)
    # return gi_matrix

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
# print_data(calculate_from_matrix(test_matrix))
print_data(calculate_from_matrix(test_matrix))



# get_neigbours(test_data, 23, 0, 4)
