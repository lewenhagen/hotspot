#!/usr/bin/env python3
"""
Main file for predicting hotspots
"""
import json
import numpy
import sys
import itertools
import pandas as pd
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 15, 6 # donno
sys.path.append('..')
from gi.getis import Gi
from aoristic import aoristic
from aoristic import parse as parser


class Sapphire:
    def __init__(self, pre_lists, goal):
        self.pre_lists = pre_lists
        self.goal = goal
        self.res_sum_mat = numpy.zeros(shape=(24*7))

    def add(self):
        # add all pre_lists make hotspots
        # compare with goal hotspot
        for mat in self.pre_lists.items():
            self.res_sum_mat = self.res_sum_mat + mat[1]
        # print(res)

    def calc_gi(self):
        gi = Gi(self.res_sum_mat)
        # start_time = time.time()
        gi.calculate()
        result = {}
        result["conf_levels"] = {
        "0.90": gi.confidence_interval(0.90),
        "0.95": gi.confidence_interval(0.95),
        "0.99": gi.confidence_interval(0.99)
        }

        gi.clear_zscore(0.05) # ?
        # gi.clear_zscore(0.95) ?

        result["getis"] = gi.get_result().reshape(24, 7)
        # print(result["getis"])
        self.pprint(result["getis"])

    @staticmethod
    def pprint(matrix):
        for i, row in enumerate(matrix):
            print(i, row)

    def setup(self):
        units = json.load(open("../units.json", "r"))
        unit_y = units["hours"]
        unit_x = units["days"]
        all_data = list()
        for y in range(1, 5):
            for m in range(1, 13):
                search = "201{}-{}".format(y, m if m > 9 else "0" + str(m))
                raw_data = parser.csv_to_dict(search, "datestart", "total_v2.csv")
                aoristic_data = [[0 for x in range(unit_x["size"])] for y in range(unit_y["size"])] # x y
                aoristic.aoristic_method(raw_data, aoristic_data, unit_x, unit_y)
                arr = numpy.matrix(aoristic_data).flat
                all_data = list(itertools.chain(all_data, arr))

        plt.plot(all_data) # plot timeseries
        plt.show()

if __name__ == "__main__":
    all = json.load(open("test/all.json"))
    dic = {}
    for i, l in enumerate(all.items()):
        dic[i] = numpy.matrix(l[1])
    res = dic[len(dic)-1]
    del dic[len(dic)-1]
    #
    s = Sapphire(dic, res)
    #s.setup()
    s.add()
    s.calc_gi()

# 1 skapa en hotspot av alla tidigare hur skiljer den hotspot från framtid?
# 2 kan man kolla skillnad mellan matriser och försöka bygga den nya från den innan med hjälpa av average skillnader?
# 3 man man invertera från 1 -> 2 -> 3 -> 4 -> 5 på bågot sätt, kolla länkar.
