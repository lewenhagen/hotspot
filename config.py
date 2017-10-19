#!/usr/bin/env python3

import pandas as pd
import os, glob
import json

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

    return datafiles



def get_cities_as_list(from_file):
    """
    Returns cities from file
    """
    return sorted(list(set(pd.read_csv("datafiles/" + from_file, sep=";", usecols=["city"]).city.tolist())))

def get_units():
    """
    Get units from json file
    """
    units = json.load(open("units.json", "r"))

    return {
        "units": units,
        "keys": sorted(units.keys())
        }



def create_empty_matrix(x, y):
    """
    Creates an empty matrix of the correct size
    """
    print("X: ", x)
    print("Y: ", y)

    # units = get_units()["units"]
    unit_x = x
    unit_y = y

    t_map = [[0 for x in range(unit_x["size"])] for y in range(unit_y["size"])]

    return t_map


setup = {
    "datafiles": get_datafiles(),
    "y_ticks": get_units()["keys"],
    "x_ticks": get_units()["keys"],
    # "available_data": ["testdata", "realdata"],
    "cities": []
}
# y_ticks = ["hours", "months"]
# x_ticks = ["weekdays", "months"]
# available_data = ["testdata", "realdata"]
#
# # theData = pd.read_csv("aoristic/temp.data.2014.csv", sep=";", usecols=["city"])
# city_list = sorted(list(set(pd.read_csv("aoristic/temp.data.2014.csv", sep=";", usecols=["city"]).city.tolist())))
