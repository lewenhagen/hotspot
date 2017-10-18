#!/usr/bin/env python3
import random as rm
"""
Module for LISA Statistics
"""
s_counter = 0

# test_data = []
#
# for y in range(24):
#     test_data.append([])
#     for x in range(7):
#         test_data[y].append(s_counter)
#         s_counter += 1
#
def print_data(data):
    print("[ 0   1   2   3   4   5   6]")
    for i, x in enumerate(data):
        print(i, x)

def get_neigbours(data, y, x, d):
    if y < len(data) and x < len(data[y]):
        start = data[y][x]
        new_data = []
        size_x = 7
        size_y = 24
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


    print_data(new_data)

# get_neigbours(test_data, 23, 0, 4)
