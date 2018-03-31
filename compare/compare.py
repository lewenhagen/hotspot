#!/usr/bin/env python3
"""
Main file for Comparison class
"""
# remove later
# import pandas as pd


# from scipy.stats import norm
import scipy.stats
import numpy as np
# from numpy.linalg import eig
from math import*
from sklearn.metrics import jaccard_similarity_score
from difflib import SequenceMatcher
from scipy.spatial.distance import pdist
from scipy.stats.stats import pearsonr
from scipy.spatial.distance import jaccard
from scipy.spatial.distance import hamming
from scipy.spatial.distance import kulsinski

from measures import similarity_coefficients as sc


class Compare():
    """
    Class for comparison
    Holds all data
    """
    def __init__(self, left_map, right_map):
        """
        Init method
        """
        self.num_rows, self.row_len = left_map.shape
        self.left_map = left_map
        self.right_map = right_map
        self.overlap_matrix = np.zeros(shape=(self.num_rows, self.row_len), dtype=float)
        self.fuzziness_matrix = np.zeros(shape=(self.num_rows, self.row_len), dtype=float)
        self.left_flat = left_map.flatten()
        self.right_flat = right_map.flatten()

        self.j_left_all = np.zeros(shape=(self.num_rows, self.row_len), dtype=int)
        self.j_right_all = np.zeros(shape=(self.num_rows, self.row_len), dtype=int)
        self.j_left_hot = np.zeros(shape=(self.num_rows, self.row_len), dtype=int)
        self.j_right_hot = np.zeros(shape=(self.num_rows, self.row_len), dtype=int)
        self.j_left_cold = np.zeros(shape=(self.num_rows, self.row_len), dtype=int)
        self.j_right_cold = np.zeros(shape=(self.num_rows, self.row_len), dtype=int)

        self.jaccard = {}
        self.total_percentage = 0




    def get_increase(self, old, new):
        """
        Return calculated increased percent
        """
        # increase = new - old
        return ((new - old) / old) * 100



    def get_decrease(self, old, new):
        """
        Return calculated decreased percent
        """
        # decrease = old - new
        return (((old - new) / old) * 100) * -1



    def calculate_percentage(self):
        """
        Calculates the percentage of overlap
        """
        self.total_percentage = round(len(set(self.left_flat)&set(self.right_flat)) / float(len(set(self.left_flat) | set(self.right_flat))) * 100, 1)



    def get_percentage(self):
        """
        Returns the calculated total percentage
        """
        return self.total_percentage



    def calculate_overlap(self):
        """
        Manually traverse the hotspots and find overlap
        Works on both increased and decreased values
        """

        for y_index, y_val in enumerate(self.left_map):
            for x_index, x_val in enumerate(y_val):
                old_nr = round(self.left_map[y_index][x_index], 1)
                new_nr = round(self.right_map[y_index][x_index], 1)

                if old_nr != 0.0 and new_nr != 0.0:
                    if old_nr > 0.0 and new_nr > 0.0:
                        if old_nr > new_nr:
                            self.overlap_matrix[y_index][x_index] = self.get_decrease(old_nr, new_nr)
                        elif old_nr < new_nr:
                            self.overlap_matrix[y_index][x_index] = self.get_increase(old_nr, new_nr)
                        elif old_nr == new_nr:
                            self.overlap_matrix[y_index][x_index] = 0.0
                    elif old_nr < 0.0 and new_nr < 0.0:
                        if old_nr > new_nr:
                            self.overlap_matrix[y_index][x_index] = self.get_increase(old_nr, new_nr)
                        elif old_nr < new_nr:
                            self.overlap_matrix[y_index][x_index] = self.get_decrease(old_nr, new_nr)
                        elif old_nr == new_nr:
                            self.overlap_matrix[y_index][x_index] = 0.0
                    else:
                        self.overlap_matrix[y_index][x_index] = None
                elif old_nr == 0.0 and new_nr == 0.0:
                    self.overlap_matrix[y_index][x_index] = None
                elif old_nr == 0.0 and new_nr != 0:
                    self.overlap_matrix[y_index][x_index] = None
                elif new_nr == 0.0 and old_nr != 0:
                    self.overlap_matrix[y_index][x_index] = None



    def get_overlap(self):
        """
        Returns the calculated overlap matrix
        """
        return self.overlap_matrix



    def calculate_jaccard(self):
        """
        Sets up two matrices to be used for jaccard calculation
        calculates the jaccard index
        """
        # left = self.left_map
        # right = self.right_map

        left_all = np.copy(self.left_map)
        right_all = np.copy(self.right_map)

        left_hot = np.copy(self.left_map)
        right_hot = np.copy(self.right_map)

        left_cold = np.copy(self.left_map)
        right_cold = np.copy(self.right_map)

        left_all[left_all != 0] = 1
        right_all[right_all != 0] = 1

        left_hot[left_hot > 0] = 1
        left_hot[left_hot < 0] = 0 #  clear coldspots

        right_hot[right_hot > 0] = 1
        right_hot[right_hot < 0] = 0 #  clear coldspots

        left_cold[left_cold > 0] = 0 #  clear hotspots
        left_cold[left_cold < 0] = 1
        # print("here", left_cold)

        right_cold[right_cold > 0] = 0 #  clear hotspots
        right_cold[right_cold < 0] = 1

        # for y_index, y_val in enumerate(self.left_map):
        #     for x_index, x_val in enumerate(y_val):
        #         # LEFT SET
        #         if self.left_map[y_index][x_index] != 0.0: # all
        #             self.j_left_all[y_index][x_index] = 1
        #             if self.left_map[y_index][x_index] > 0.0: # hotspot
        #                 self.j_left_hot[y_index][x_index] = 1
        #
        #             if self.left_map[y_index][x_index] < 0.0: # coldspot
        #                 self.j_left_cold[y_index][x_index] = 1
        #
        #         # RIGHT SET
        #         if self.right_map[y_index][x_index] != 0.0: # all
        #             self.j_right_all[y_index][x_index] = 1
        #             if self.right_map[y_index][x_index] > 0.0: # hotspot
        #                 self.j_right_hot[y_index][x_index] = 1
        #
        #             if self.right_map[y_index][x_index] < 0.0: # coldspot
        #                 self.j_right_cold[y_index][x_index] = 1
        #
        # j_all = jaccard(self.j_left_all.flatten(), self.j_right_all.flatten())
        # j_hot = jaccard(self.j_left_hot.flatten(), self.j_right_hot.flatten())
        # j_cold = jaccard(self.j_left_cold.flatten(), self.j_right_cold.flatten())

        j_all = sc.jaccard(left_all.flatten(), right_all.flatten())
        j_hot = sc.jaccard(left_hot.flatten(), right_hot.flatten())
        j_cold = sc.jaccard(left_cold.flatten(), right_cold.flatten())


        self.jaccard = {
            "similarity": {
                "all": round((j_all)*100, 1),
                "hot": round((j_hot)*100, 1),
                "cold": round((j_cold)*100, 1)
            },
            "unique": {
                "all": round((1-j_all)*100, 1),
                "hot": round((1-j_hot)*100, 1),
                "cold": round((1-j_cold)*100, 1)
            }
        }


    def get_jaccard(self):
        """
        Returns the calculated jaccard dict
        """
        return self.jaccard
