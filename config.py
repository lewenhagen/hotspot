#!/usr/bin/env python3

import pandas as pd

"""
Configuration file for hotspot
"""
y_ticks = ["hours", "months"]
x_ticks = ["weekdays", "months"]
available_data = ["testdata", "realdata"]

theData = pd.read_csv("aoristic/temp.data.2014.csv", sep=";", usecols=["city"])
city_list = sorted(list(set(theData.city.tolist())))
