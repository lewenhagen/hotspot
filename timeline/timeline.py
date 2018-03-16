#!/usr/bin/env python3
"""
Timeline file
"""

import pandas
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import spline
# from matplotlib import rcParams

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

        self.hotspot_values = []
        self.coldspot_values = []

        self.hotspot_percent = []
        self.coldspot_percent = []



    def calculate_total(self):
        """
        Loops through dataframes and counts hotspots and coldspots
        """
        for month in self.data:
            # if month == "January":
            month_hot_sum = (np.array(self.data[month].values.tolist()) > 0.0).sum()
            month_cold_sum = (np.array(self.data[month].values.tolist()) < 0.0).sum()
            self.total_hotspots += month_hot_sum
            self.total_coldspots += month_cold_sum
            self.hotspot_values.append(month_hot_sum)
            self.coldspot_values.append(month_cold_sum)



    def calculate_percentage(self):
        """
        Adds the percentage score to the lists *_values
        """
        for hot in self.hotspot_values:
            self.hotspot_percent.append(float("{0:.3f}".format(hot / self.total_hotspots)))

        for cold in self.coldspot_values:
            self.coldspot_percent.append(float("{0:.3f}".format((cold / self.total_coldspots) * -1)))



    def get_hot_percent(self):
        """
        Returns the list with hotspot percents
        """
        return self.hotspot_percent



    def get_cold_percent(self):
        """
        Returns the list with coldspot percents
        """
        return self.coldspot_percent



    def create_timeline(self):
        """
        Creates the timeline and returns the plot
        """

        plt.close("all")

        fig, ax = plt.subplots(figsize=(6,2))

        hot = self.hotspot_percent
        cold = self.coldspot_percent
        mid = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        ax.set_xticks(np.arange(12))

        x_ticks_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        ax.set_xticklabels(x_ticks_labels, fontsize=9)

        # ax.set_title("Overview")

        ax.plot(hot, marker='o', linestyle='-', color='r', label='Hotspot')
        ax.plot(cold, marker='o', linestyle='-', color='b', label='Coldspot')
        ax.plot(mid, color="black")
        ax.tick_params(labelsize=9, direction="out")
        # ax.set_ylim([-1, 1])

        xticks, xticklabels = plt.xticks()

        xmin = (3*xticks[0] - xticks[1])/3
        xmax = (3*xticks[-1] - xticks[-2])/2
        plt.xlim(xmin, xmax)
        plt.xticks(xticks)

        yticks, yticklabels = plt.yticks()

        ymin = (3*yticks[0] - yticks[1])/2
        ymax = (3*yticks[-1] - yticks[-2])/2
        plt.ylim(ymin, ymax)
        plt.yticks(yticks)

        plt.tight_layout()

        return plt
        # plt.show()
        # plt.close("all")
