#!/usr/bin/env python3
"""
Timeline file
"""

import pandas
import numpy as np
import matplotlib.pyplot as plt
# from scipy.interpolate import spline
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
        Creates the timeline and saves it
        """
        # rcParams.update({'figure.autolayout': True})

        # df_data1 = pandas.DataFrame(data=self.hotspot_percent,
        #                         index=[1, 0.8, 0.6, 0.4, 0.2, 0, -0.2, -0.4, -0.6, -0.8, -1],
        #                         columns=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])

        plt.close("all")
        fig, ax = plt.subplots(figsize=(7,4))

        hot = self.hotspot_percent
        cold = self.coldspot_percent
        # print(len(hot))
        # print(len(cold))
        # print("")

        # xnew_hot = np.linspace(min(hot),max(hot),300)
        # xnew_cold = np.linspace(min(cold),max(cold),300)


        # power_smooth_hot = spline(hot,cold,xnew_hot)
        # power_smooth_cold = spline(hot,cold,xnew)


        ax.set_xticks(np.arange(len(hot)))
        x_ticks_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        ax.set_xticklabels(x_ticks_labels, fontsize=9)
        # fig.gca().set_prop_cycle(['red', 'blue'])

        ax.plot(hot, marker='o', linestyle='-', color='r', label='Hotspot')
        ax.plot(cold, marker='o', linestyle='-', color='b', label='Coldspot')

        # ax.plot(x, y)
        # ax.plot(y, y)
        # plt.plot(x, 3 * x)
        # plt.plot(x, 4 * x)

        ax.legend(['Hotspot', 'Coldspot'], loc='upper left')
        plt.tight_layout()

        plt.show()


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
