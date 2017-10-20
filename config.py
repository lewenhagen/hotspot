#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
        if datafile.endswith(".csv") or datafile.endswith(".log"):
            datafiles.append(datafile)

    return datafiles



def get_column_as_list(file_name, column):
    """
    Returns a unique values from column in a file
    """
    return sorted(list(set(pd.read_csv("datafiles/" + file_name, sep=";", usecols=[column])[column].tolist())))



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

    unit_x = x
    unit_y = y

    t_map = [[0 for x in range(unit_x["size"])] for y in range(unit_y["size"])]

    return t_map



def get_csv_header(file_name):
    """
    Get headers from csv file
    """
    return sorted(pd.read_csv("datafiles/" + file_name, sep=";", encoding = 'utf8', nrows=0).columns.tolist())



setup = {
    "datafile": "",
    "y_ticks": get_units()["keys"],
    "x_ticks": get_units()["keys"],
    "filter": {
        "column": "",
        "values": []
    }
}
