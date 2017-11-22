#!/usr/bin/env python3

"""
Contains class for Local Gi*
"""

import numpy as np
import scipy.stats as st
import math
from multiprocessing import Process
from itertools import product
from multiprocessing import Pool

from joblib import Parallel, delayed



class Gi():
    """
    Class for Local Gi*
    """
    def __init__(self, data, distance=1, weight=1):
        """
        init method
        """
        self.original_data = data
        self.raw_data = np.matrix(data)
        self.distance = distance
        self.weight = weight
        self.n = self.raw_data.size
        self.mean = self.raw_data.mean()
        self.num_rows, self.row_len = self.raw_data.shape
        # print(np.square(self.raw_data))
        self.square_sum = (np.sum(np.square(self.raw_data)))
        self.gi_matrix = np.zeros(shape=(self.num_rows, self.row_len), dtype=float)

    def confidence_interval(self, conf=0.95):
        """
        Calculates the confidence interval for given data.
        Defaults at 95% confidence level.
        """
        mean = self.gi_matrix.mean()
        var = np.var(self.gi_matrix)
        std = math.sqrt(var)

        return st.norm.interval(conf, loc=mean, scale=std)

    # def getX(iter):



    def get_neigbours(self, y, x):
        """
        Returns the neighbourhood from given x, y.
        Uses queen's case and modulus to get out of bounds features.
        """
        new_data = []
        m_sum = 0
        square_weight = 0
        j_count = 0
        # start = self.raw_data[y, x]

        iterations = (self.distance * 2) + 1

        # new_data = [[] for _ in range(iterations)]
        for _ in range(iterations):
            new_data.append([])

        startY = (y - self.distance) % self.num_rows
        startX = (x - self.distance) % self.row_len

        counterY = 0

        while counterY < iterations:
            counterX = 0
            startX = (x - self.distance) % self.row_len
            while counterX < iterations:
                # print(round(self.raw_data[startY, startX], 2))
                new_data[counterY].append(self.raw_data[startY, startX])

                counterX += 1
                # startX += 1
                startX = (startX + 1) % self.row_len

            startY = (startY + 1) % self.num_rows
            counterY += 1

        for local_y in new_data:
            m_sum += sum(local_y)

            for local_x in local_y:
                square_weight += self.weight**2

            j_count += len(local_y)

        return (m_sum, square_weight, j_count)


    def get_neigbours2(self, y, x):
        """
        Returns the neighbourhood from given x, y.
        Uses queen's case and modulus to get out of bounds features.
        """
        new_data = []
        m_sum = 0
        square_weight = 0
        j_count = 0
        # start = self.raw_data[y, x]

        iterations = (self.distance * 2) + 1

        # new_data = [[] for _ in range(iterations)]
        # for _ in range(iterations):
        #     new_data.append([])

        startY = (y - self.distance) % self.num_rows
        startX = (x - self.distance) % self.row_len

        counterY = 0

        while counterY < iterations:
            counterX = 0
            startX = (x - self.distance) % self.row_len
            while counterX < iterations:
                # print(round(self.raw_data[startY, startX], 2))
                new_data.append(self.raw_data[startY, startX])

                counterX += 1
                # startX += 1
                startX = (startX + 1) % self.row_len

            startY = (startY + 1) % self.num_rows
            counterY += 1

        m_sum = sum(new_data)
        square_weight = (self.weight**2) * len(new_data)
        j_count = len(new_data)
        # for local_y in new_data:
        #     m_sum += sum(local_y)
        #
        #     for local_x in local_y:
        #         square_weight += self.weight**2
        #
        #     j_count += len(local_y)

        return (m_sum, square_weight, j_count)


    def get_neigbours_part(self, y, x):
        new_data = []

        iterations = self.distance + self.distance + 1

        for _ in range(iterations):
            new_data.append([])

        startY = (y - self.distance) % self.num_rows
        startX = (x - self.distance) % self.row_len

        counterY = 0

        while counterY < iterations:
            counterX = 0
            startX = (x - self.distance) % self.row_len
            while counterX < iterations:
                new_data[counterY].append(np.around(self.raw_data[startY, startX], 2))

                counterX += 1
                startX += 1
                startX = startX % self.row_len

            startY = (startY + 1) % self.num_rows
            counterY += 1
        return new_data
    #
    def get_neigbours_paralell(self, part):
        # print(part)
        # dataset = self.raw_data[y_axis]
        y, x = part
        new_data = []
        m_sum = 0
        square_weight = 0
        j_count = 0
        # start = self.raw_data[y, x]

        # iterations = self.distance + self.distance + 1
        #
        # for _ in range(iterations):
        #     new_data.append([])
        #
        # startY = (y - self.distance) % self.num_rows
        # startX = (x - self.distance) % self.row_len
        #
        # counterY = 0
        #
        # while counterY < iterations:
        #     counterX = 0
        #     startX = (x - self.distance) % self.row_len
        #     while counterX < iterations:
        #         new_data[counterY].append(np.around(self.raw_data[startY, startX], 2))
        #
        #         counterX += 1
        #         startX += 1
        #         startX = startX % self.row_len
        #
        #     startY = (startY + 1) % self.num_rows
        #     counterY += 1
        new_data = np.matrix(self.get_neigbours_part(y, x))
        # print(np.sum(new_data))
        m_sum = np.sum(new_data)
        square_weight = (self.weight**2) * new_data.size
        j_count = new_data.size
        # for local_y in new_data:
        #     m_sum += sum(local_y)
        #
        #     for local_x in local_y:
        #         square_weight += self.weight**2
        #
        #     j_count += len(local_y)

        numerator = m_sum - (self.mean * j_count)
        S = math.sqrt( (self.square_sum / self.n) - (self.mean**2) )
        denominator = S * math.sqrt( ( (self.n * j_count) - square_weight**2) / self.n )

        return np.around(numerator / denominator, 2)


    def my_gen(self):
        """
        Generator
        """
        for y in range(self.num_rows):
            for x in range(self.row_len):
                yield (y, x)



    def calculate_parallel(self):

        mygen = self.my_gen()

        # chunksize = 3
        # dataset = []
        #
        # for y in range(itersY):
        #     dataset.append([])
        #
        #     for x in range(itersX):
        #         dataset[y].append((y, x))
        #
        # # print(dataset)
        # #
        # counter = 0
        # with Pool(processes=5) as pool:
        #     pool.apply_async(self.get_neigbours_paralell, args=(next(mygen)))



        # print(next(mygen))
        # print(next(mygen))
        for _ in range(self.n):
            yx = next(mygen)
            self.gi_matrix[yx] = self.get_neigbours_paralell(yx)
        # self.gi_matrix[next(mygen)] = Parallel(itersX)(delayed(self.get_neigbours_paralell)(next(mygen2)) for _ in range(self.n))


    def calculate(self):
        """
        Calculates the resulting matrix
        """
        # print(self.raw_data)
        mygen = self.my_gen()

        for _ in range(self.n):

            rows, cols = next(mygen)

            m_sum, square_weight, j_count = self.get_neigbours2(rows, cols)

            numerator = m_sum - (self.mean * j_count)

            S = math.sqrt( (self.square_sum / self.n) - (self.mean**2) )
            denominator = S * math.sqrt( ( (self.n * j_count) - square_weight**2) / self.n )
            self.gi_matrix[rows][cols] =  numerator / denominator




    def clear_zscore(self, conf=0.05):
        """
        Clears all zscore out of bounds
        """
        confidence = 1 - conf
        low, high = self.confidence_interval(confidence)
        print("min:", low, "max", high)
        for index, value in np.ndenumerate(self.gi_matrix):
             if low < value < high:
                 self.gi_matrix[index] = 0.00



    def get_result(self):
        """
        Returns the result
        """
        return self.gi_matrix
