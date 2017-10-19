#!/usr/bin/env python3

import pandas as pd
import os, glob

"""
Configuration file for hotspot
"""

def get_datafiles():
    """
    Returns a list of all datafiles (.csv)
    """
    datafiles = []

    for datafile in os.listdir("datafiles"):
        if datafile.endswith(".csv"):
            datafiles.append(datafile)
    datafiles.append("testdata")

    return datafiles


setup = {
    "datafiles": get_datafiles(),
    "y_ticks": ["hours", "months"],
    "x_ticks": ["weekdays", "months"],
    "available_data": ["testdata", "realdata"],
    "cities": sorted(list(set(pd.read_csv("datafiles/temp.data.2014.csv", sep=";", usecols=["city"]).city.tolist())))
}
# y_ticks = ["hours", "months"]
# x_ticks = ["weekdays", "months"]
# available_data = ["testdata", "realdata"]
#
# # theData = pd.read_csv("aoristic/temp.data.2014.csv", sep=";", usecols=["city"])
# city_list = sorted(list(set(pd.read_csv("aoristic/temp.data.2014.csv", sep=";", usecols=["city"]).city.tolist())))
