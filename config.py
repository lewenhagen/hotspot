#!/usr/bin/env python3

import pandas as pd

"""
Configuration file for hotspot
"""

setup = {
    "y_ticks": ["hours", "months"],
    "x_ticks": ["weekdays", "months"],
    "available_data": ["testdata", "realdata"],
    "cities": sorted(list(set(pd.read_csv("aoristic/temp.data.2014.csv", sep=";", usecols=["city"]).city.tolist())))
}
# y_ticks = ["hours", "months"]
# x_ticks = ["weekdays", "months"]
# available_data = ["testdata", "realdata"]
#
# # theData = pd.read_csv("aoristic/temp.data.2014.csv", sep=";", usecols=["city"])
# city_list = sorted(list(set(pd.read_csv("aoristic/temp.data.2014.csv", sep=";", usecols=["city"]).city.tolist())))
