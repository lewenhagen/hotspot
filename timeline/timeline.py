#!/usr/bin/env python3
"""
Timeline file
"""

import numpy as np
import matplotlib.pyplot as plt

class Timeline():
    """
    Class for creating a Timeline
    """
    def __init__(self, data):
        """
        Init method
        """
        self.data = data
        self.total_hotspots = 0
        self.total_coldspots = 0
        self.montly_count = []

    def setup_data(self):
        """
        Loops through dataframes and counts hotspots and coldspots
        """
        print(self.data["January"])
        for key, val in self.data.items():
            if key == "January":
                for index, row in val:
                    if float(row) > 0.0:
                        print(index[row])
                # print("key:", key)
                # print("val:", val)




# fig, ax = plt.subplots(figsize=(7,4))

# month = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
# hot = [0.6, 0.75, 0.2, 0, 0.9, 0.7, 0.5, 0.3, 0.6, 0.5, 0.4, 1]
# cold = [-0.6, -0.75, -0.2, -0.4, -0.9, -0.7, 0, -0.3, -0.6, -0.5, -0.4, -1]
# # plt.plot(radius, area, label='Circle')
# x_ticks_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
# ax.set_xticks(hot)
# # Set ticks labels for x-axis
# ax.set_xticklabels(x_ticks_labels, fontsize=9)
# # ax.tick_params(axis='both', direction="out")
# ax.plot(hot, marker='o', linestyle='-', color='r', label='Hotspot')
# ax.plot(cold, marker='o', linestyle='-', color='b', label='Coldspot')
# plt.xlabel('Month')
# plt.ylabel('# of hotspots')
# plt.title('TEsting')
#
# ax.legend(['Hotspot', 'Coldspot'], loc='upper left')
# plt.show()
