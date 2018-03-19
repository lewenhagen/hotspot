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


from measures import jaccard as ji

# from pai import pai


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

        j_all = ji.jaccard(left_all.flatten(), right_all.flatten())
        j_hot = ji.jaccard(left_hot.flatten(), right_hot.flatten())
        j_cold = ji.jaccard(left_cold.flatten(), right_cold.flatten())


        self.jaccard = {
            "similarity": {
                "all": round((1-j_all)*100, 1),
                "hot": round((1-j_hot)*100, 1),
                "cold": round((1-j_cold)*100, 1)
            },
            "unique": {
                "all": round((j_all)*100, 1),
                "hot": round((j_hot)*100, 1),
                "cold": round(j_cold*100, 1)
            }
        }


    def get_jaccard(self):
        """
        Returns the calculated jaccard dict
        """
        return self.jaccard



    # def get_prev_hour_hot(self, y, x):
    #     """
    #     Based on hours
    #     Returns a tuple with the previous coordinates if there ae a hotspot -
    #     - in left or right heatmap
    #     """
    #     fuzzy = False
    #     y_pos = y
    #     x_pos = x
    #     new_x = x
    #     new_y = (y-1) % self.num_rows
    #     if new_y == 24:
    #         new_x = (x-1) % self.row_len
    #
    #     if self.left_map[new_y][new_x] > 0.0 or self.right_map[new_y][new_x] > 0.0:
    #         fuzzy = True
    #         y_pos = new_y
    #         x_pos = new_x
    #
    #     return (fuzzy, y_pos, x_pos)



    # def get_next_hour_hot(self, y, x):
    #     """
    #     Based on hours
    #     Returns a tuple with the next coordinates if there ae a hotspot -
    #     - in left or right heatmap
    #     """
    #     fuzzy = False
    #     y_pos = y
    #     x_pos = x
    #     new_x = x
    #
    #     new_y = (y+1) % self.num_rows
    #     if new_y == 0:
    #         new_x = (x+1) % self.row_len
    #
    #     if self.left_map[new_y][new_x] > 0.0 or self.right_map[new_y][new_x] > 0.0:
    #         fuzzy = True
    #         y_pos = new_y
    #         x_pos = new_x
    #
    #     return (fuzzy, y_pos, x_pos)



    # def calculate_fuzziness(self):
    #     """
    #     Calculates the fuzziness in the overlap
    #     Takes nearby hours into account
    #     """
    #     for y_index, y_val in enumerate(self.left_map):
    #         for x_index, x_val in enumerate(y_val):
    #             if self.left_map[y_index][x_index] > 0.0 and self.right_map[y_index][x_index] > 0.0: # hotspot overlap
    #                 self.fuzziness_matrix[y_index][x_index] = 1
    #                 fuzzy, y, x = self.get_next_hour_hot(y_index, x_index)
    #                 if fuzzy:
    #                     self.fuzziness_matrix[y][x] = 1
    #
    #                 fuzzy, y, x = self.get_prev_hour_hot(y_index, x_index)
    #                 if fuzzy:
    #                     self.fuzziness_matrix[y][x] = 1
    #
    #             if self.left_map[y_index][x_index] < 0.0 and self.right_map[y_index][x_index] < 0.0: # coldspot overlap
    #                 self.fuzziness_matrix[y_index][x_index] = -1
    #                 # fuzzy, y, x = self.get_next_hour_cold(y_index, x_index)
    #                 # if fuzzy:
    #                 #     self.fuzziness_matrix[y][x] = -1
    #     print("here:", self.fuzziness_matrix)


# No similarity
# input_a = np.array([[ 0, 0, 0, 0, 0, 0, 0 ],
#                     [ 0, -1, -1, 0, 0, 0, 0 ],
#                     [ -1, -1, 0, 0, 0, 0, 0 ],
#                     [ 0, 0, 0, 0, 0, 0, 0 ],
#                     [ 0, 0, 1, 0, 0, 0, 0 ],
#                     [ 0, 1, 1, 0, 0, 0, 0 ],
#                     [ 0, 0, 0, 0, 0, 0, 0 ]])
#
# input_b = np.array([[ 0, 0, 0, 0, 0, 0, 0 ],
#                     [ 0, 0, 0, 0, 0, 0, 0 ],
#                     [ 0, 0, 0, 0, 0, 0, 0 ],
#                     [ 0, 0, 0, 1, 0, 0, 0 ],
#                     [ 0, 0, 0, 1, 1, 0, 0 ],
#                     [ 0, 0, 0, 1, 1, 0, 0 ],
#                     [ 0, 0, 0, 0, 0, 0, 0 ]])
#
# #
# # print(a.flatten())
# # print(b.flatten())
# print("> No similarity")
# print("Jaccard-Needham Similarity:", ((1 - ( jaccard(input_a.flatten(), input_b.flatten())) ) * 100) )
# print("Jaccard-Needham Dissimilarity:", ( jaccard(input_a.flatten(), input_b.flatten()) ) * 100 )
#
# print("Jaccard Index Similarity:", ( ji.jaccard(input_a.flatten(), input_b.flatten()) ) * 100 )
# print("Jaccard Index Dissimilarity:", ((1 - ( ji.jaccard(input_a.flatten(), input_b.flatten())) ) * 100) )
#
# # Identical
# input_a = np.array([[ 0, 0, 0, 0, 0, 0, 0 ],
#               [ 0, -1, -1, 0, 0, 0, 0 ],
#               [ -1, -1, 0, 0, 0, 0, 0 ],
#               [ 0, 0, 0, 0, 0, 0, 0 ],
#               [ 0, 0, 1, 0, 0, 0, 0 ],
#               [ 0, 1, 1, 0, 0, 0, 0 ],
#               [ 0, 0, 0, 0, 0, 0, 0 ]])
#
# input_b = np.array([[ 0, 0, 0, 0, 0, 0, 0 ],
#               [ 0, -1, -1, 0, 0, 0, 0 ],
#               [ -1, -1, 0, 0, 0, 0, 0 ],
#               [ 0, 0, 0, 0, 0, 0, 0 ],
#               [ 0, 0, 1, 0, 0, 0, 0 ],
#               [ 0, 1, 1, 0, 0, 0, 0 ],
#               [ 0, 0, 0, 0, 0, 0, 0 ]])
#
# print("> Identical")
# print("Jaccard-Needham Similarity:", ((1 - ( jaccard(input_a.flatten(), input_b.flatten())) ) * 100) )
# print("Jaccard-Needham Dissimilarity:", ( jaccard(input_a.flatten(), input_b.flatten()) ) * 100 )
#
# print("Jaccard Index Similarity:", ( ji.jaccard(input_a.flatten(), input_b.flatten()) ) * 100 )
# print("Jaccard Index Dissimilarity:", ((1 - ( ji.jaccard(input_a.flatten(), input_b.flatten())) ) * 100) )
#
# # Partial
# input_a = np.array([[ 0, 0, 0, 0, 0, 0, 0 ],
#                     [ 1, 0, 0, 0, 0, 0, 0 ],
#                     [ 0, 0, 0, 0, 0, 0, 0 ],
#                     [ 0, 0, 0, 0, 0, 0, 0 ],
#                     [ 0, 0, 0, 0, 0, 0, 0 ],
#                     [ 0, 0, 0, 0, 0, 0, 0 ],
#                     [ 0, 0, 0, 0, 0, 0, 0 ]])
#
# input_b = np.array([[ 0, 0, 0, 0, 0, 0, 0 ],
#                     [ 1, 0, 1, 0, 0, 0, 0 ],
#                     [ 0, 0, 0, 0, 0, 0, 0 ],
#                     [ 0, 0, 0, 0, 0, 0, 0 ],
#                     [ 0, 0, 0, 0, 0, 0, 0 ],
#                     [ 0, 0, 0, 0, 0, 0, 0 ],
#                     [ 0, 0, 0, 0, 0, 0, 0 ]])
#
# print("> Partial")
# print("Jaccard-Needham Similarity:", ((1 - ( jaccard(input_a.flatten(), input_b.flatten())) ) * 100) )
# print("Jaccard-Needham Dissimilarity:", ( jaccard(input_a.flatten(), input_b.flatten()) ) * 100 )
#
# print("Jaccard Index Similarity:", ( jaccard_similarity_score(input_a.flatten(), input_b.flatten()) ) * 100 )
# print("Jaccard Index Dissimilarity:", ((1 - ( jaccard_similarity_score(input_a.flatten(), input_b.flatten())) ) * 100) )
#
# print("Hamming Index Similarity:", ((1 - ( hamming(input_a.flatten(), input_b.flatten())) ) * 100) )
# print("Hamming Index Dissimilarity:", ( hamming(input_a.flatten(), input_b.flatten()) ) * 100 )
#
# print("Kulsinski Index Similarity:", ((1 - ( kulsinski(input_a.flatten(), input_b.flatten())) ) * 100) )
# print("Kulsinski Index Dissimilarity:", ( kulsinski(input_a.flatten(), input_b.flatten()) ) * 100 )

# a = np.array([ 1, -1, 1, 0, 1 ])
# b = np.array([ 0, -1, 0, 1, 1 ])
#
# print(ji.jaccard(a, b))

# def square_rooted(x):
#    return round(sqrt(sum([a*a for a in x])),3)
#
#
#
# def cosine_similarity(x,y):
#
#  numerator = sum(a*b for a,b in zip(x,y))
#  denominator = square_rooted(x)*square_rooted(y)
#
#  return round(numerator/float(denominator),3)
#
#
#
# def similar(a, b):
#     return SequenceMatcher(None, a, b).ratio()



# def calculate_percentage(file_a, file_b):
#     """
#     Returns the percentage of overlap
#     """
#     file_a = file_a.flatten()
#     file_b = file_b.flatten()
#
#     self.total_percentage = round(len(set(file_a)&set(file_b)) / float(len(set(file_a) | set(file_b))) * 100, 1)
#
#
#
# def get_total_percentage(self):
#     return self.total_percentage
#
#
#
# def get_increase(old, new):
#     """
#     Return calculated increased percent
#     """
#     increase = new - old
#     return (increase / old) * 100
#
#
#
# def get_decrease(old, new):
#     """
#     Return calculated decreased percent
#     """
#     decrease = old - new
#     return ((decrease / old) * 100) * -1
#
#
#
# def calculate_overlap(a, b):
#     """
#     Manually traverse the hotspots and find overlap
#     Works on both increased and decreased values
#     """
#     num_rows, row_len = a.shape
#     result = np.zeros(shape=(num_rows, row_len), dtype=float)
#
#
#     for y_index, y_val in enumerate(a):
#         for x_index, x_val in enumerate(y_val):
#             old_nr = round(a[y_index][x_index], 1)
#             new_nr = round(b[y_index][x_index], 1)
#
#             if old_nr != 0.0 and new_nr != 0.0:
#                 if old_nr > 0.0 and new_nr > 0.0:
#                     if old_nr > new_nr:
#                         result[y_index][x_index] = get_decrease(old_nr, new_nr)
#                     elif old_nr < new_nr:
#                         result[y_index][x_index] = get_increase(old_nr, new_nr)
#                     elif old_nr == new_nr:
#                         result[y_index][x_index] = 0.0
#                 elif old_nr < 0.0 and new_nr < 0.0:
#                     if old_nr > new_nr:
#                         result[y_index][x_index] = get_increase(old_nr, new_nr)
#                     elif old_nr < new_nr:
#                         result[y_index][x_index] = get_decrease(old_nr, new_nr)
#                     elif old_nr == new_nr:
#                         result[y_index][x_index] = 0.0
#                 else:
#                     result[y_index][x_index] = None
#             elif old_nr == 0.0 and new_nr == 0.0:
#                 result[y_index][x_index] = None
#             elif old_nr == 0.0 and new_nr != 0:
#                 result[y_index][x_index] = None
#             elif new_nr == 0.0 and old_nr != 0:
#                 result[y_index][x_index] = None
#     return result
#
#
#
# def calculate_jaccard(file_a, file_b):
#     """
#     Sets up two matrices to be used for jaccard calculation
#     calculates the jaccard index
#     """
#
#     num_rows, row_len = file_a.shape
#
#     j_matrix_left_all = np.zeros(shape=(num_rows, row_len), dtype=int)
#     j_matrix_right_all = np.zeros(shape=(num_rows, row_len), dtype=int)
#     j_matrix_left_hot = np.zeros(shape=(num_rows, row_len), dtype=int)
#     j_matrix_right_hot = np.zeros(shape=(num_rows, row_len), dtype=int)
#     j_matrix_left_cold = np.zeros(shape=(num_rows, row_len), dtype=int)
#     j_matrix_right_cold = np.zeros(shape=(num_rows, row_len), dtype=int)
#
#     for y_index, y_val in enumerate(file_a):
#         for x_index, x_val in enumerate(y_val):
#             # LEFT SET
#
#             if file_a[y_index][x_index] != 0.0: # all
#                 j_matrix_left_all[y_index][x_index] = 1
#                 if file_a[y_index][x_index] > 0.0: # hotspot
#                     j_matrix_left_hot[y_index][x_index] = 1
#
#                 if file_a[y_index][x_index] < 0.0: # coldspot
#                     j_matrix_left_cold[y_index][x_index] = 1
#
#             # RIGHT SET
#             if file_b[y_index][x_index] != 0.0: # all
#                 j_matrix_right_all[y_index][x_index] = 1
#                 if file_b[y_index][x_index] > 0.0: # hotspot
#                     j_matrix_right_hot[y_index][x_index] = 1
#
#                 if file_b[y_index][x_index] < 0.0: # coldspot
#                     j_matrix_right_cold[y_index][x_index] = 1
#
#     # left2 =  [1, 0, 0, 0, 0, 1, 0, 0, 0, 0]
#     # right2 = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
#     # print("Jaccard1:", (1 - jaccard(left2, right2)))
#     # print("Cosine:", cosine_similarity(left2, right2))
#     # print("Jaccard:", jaccard_similarity(left2, right2 ))
#     # print("Pearson:", pearsonr(j_matrix_left_cold.flatten(), j_matrix_right_cold.flatten()))
#     # print("jaccard2:", jaccard(j_matrix_left_cold.flatten(), j_matrix_right_cold.flatten()))
#     # print(set(j_matrix_left_cold.flatten()).union(set(j_matrix_right_cold.flatten())))
#
#     j_all = jaccard(j_matrix_left_all.flatten(), j_matrix_right_all.flatten())
#     j_hot = jaccard(j_matrix_left_hot.flatten(), j_matrix_right_hot.flatten())
#     j_cold = jaccard(j_matrix_left_cold.flatten(), j_matrix_right_cold.flatten())
#
#
#     return {
#         "similarity": {
#             "all": round((1-j_all)*100, 1),
#             "hot": round((1-j_hot)*100, 1),
#             "cold": round((1-j_cold)*100, 1)
#         },
#         "unique": {
#             "all": round((j_all)*100, 1),
#             "hot": round((j_hot)*100, 1),
#             "cold": round(j_cold*100, 1)
#         }
#     }
#
#
#
# def calculate_fuzziness(left_map, right_map):
#     """
#     Calculates a
#     """
#     num_rows, row_len = left_map.shape
#
#     fuzz_matrix = np.zeros(shape=(num_rows, row_len), dtype=float)
#
#
# def compare(left_map, right_map):
#     """
#     Compare two hotspots
#     """
#     # max_value_a = round(left_map.max(), 1)
#     # max_value_b = round(right_map.max(), 1)
#     # use_max = max_value_a if max_value_a > max_value_b else max_value_b
#     #
#     # min_value_a = round(left_map.min(), 1)
#     # min_value_b = round(right_map.min(), 1)
#     # use_min = min_value_a if min_value_a > min_value_b else min_value_b
#     #
#     # print("MAX: ", use_max)
#     # print("MIN: ", use_min)
#
#     result = {
#         "data": calculate_overlap(left_map, right_map),
#         "all_percentage": calculate_percentage(left_map, right_map),
#         "jaccard": calculate_jaccard(left_map, right_map),
#         "fuzziness": 0
#         # "z_max": use_max,
#         # "z_min": use_min
#     }
#
#     return result
