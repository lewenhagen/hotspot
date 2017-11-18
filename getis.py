#!/usr/bin/env python3

"""
Contains class for Local Getis-Ord*
"""

import numpy as np
import scipy.stats as st
import math
# from multiprocessing import Pool



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


    def get_neigbours(self, y, x):
        """
        Returns the neighbourhood from given x, y.
        Uses queen's case and modulus to get out of bounds features.
        """

        new_data = []
        m_sum = 0
        square_weight = 0
        j_count = 0
        start = self.raw_data[y, x]

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

        for local_y in new_data:
            m_sum += sum(local_y)

            for local_x in local_y:
                square_weight += self.weight**2

            j_count += len(local_y)

        return (m_sum, square_weight, j_count)



    def calculate(self):
        """
        Calculates the resulting matrix
        """

        for index, value in np.ndenumerate(self.raw_data):

            rows, cols = index

            m_sum, square_weight, j_count = self.get_neigbours(rows, cols)

            numerator = m_sum - (self.mean * j_count)
            S = math.sqrt( (self.square_sum / self.n) - (self.mean**2) )
            denominator = S * math.sqrt( ( (self.n * j_count) - square_weight**2) / self.n )

            self.gi_matrix[rows][cols] =  np.around(numerator / denominator, 2)



    def get_result(self):
        """
        Returns the result
        """
        return self.gi_matrix
