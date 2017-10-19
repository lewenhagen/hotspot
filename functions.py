#!usr/bin/env python3

"""
Functions for hotspot
"""

import os, glob
import pandas
import random
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import lisa # call lisa.get_neigbours(datalist, y, x, distance)
import config
import csv
import sys
sys.path.insert(0, 'aoristic/')
import aoristic



def csv_to_dict(file_name="temp.csv", deli=";"):
    """
    Read csv with header, create list with dicts. key is header value
    """
    reader = csv.reader(open("datafiles/" + file_name, "r"), delimiter=deli)
    headers = reader.__next__()
    result = []
    for row in reader:
        dic = {}
        for index, value in enumerate(row):
            dic[headers[index]] = value
        result.append(dic)

    return result



def get_data(hotspot, datafile_to_use, save_as_csv, city, filename):
    """
    Returns DataFrame (2D-list) with data
    """
    # Use city to select data.
    # CITYNAME or all
    t_map = config.create_empty_matrix(hotspot["xticks"], hotspot["yticks"])

    # data = []
    if filename.endswith(".csv"):
        aoristic.aoristic_method(datafile_to_use, t_map, hotspot["xticks"], hotspot["yticks"])

    df = pandas.DataFrame(data=t_map,
                            index=hotspot["yticks"]["ticks"],
                            columns=hotspot["xticks"]["ticks"])

    if save_as_csv:
        df.to_csv("saved_csv_hotspots/" + hotspot["filename"] + ".csv", sep="\t", encoding="utf-8")
    # lisa.get_neigbours(data, 5, 5, 2)
    return df



def create_hotspot(hotspot, cbar=True):
    """
    Creates a hotspot
    """
    # Returns a tuple containing a figure and axes object(s)
    fig, ax = plt.subplots(figsize=(7,7))

    # Creates a heatmap. ax = axes object, cmap = colorscheme, annot = display data in map, fmt = format on annot
    sns.heatmap(hotspot["data"], ax=ax, cmap="YlOrRd", annot=True, fmt=".1f", cbar=cbar)

    # Sets labels and title
    ax.set_xlabel(hotspot["labels"]["xlabel"], fontsize=14)
    ax.set_ylabel(hotspot["labels"]["ylabel"], fontsize=14)
    ax.set_title(hotspot["title"])

    # Moves tick marker outside both axis
    ax.tick_params(axis='both', direction="out")

    # Config for the axis ticks
    plt.yticks(rotation=0,fontsize=8);
    plt.xticks(rotation=0, fontsize=8);

    # Makes sure the image (labels) is not cut off
    plt.tight_layout()

    # Saves the figure as an image
    plt.savefig("static/" + hotspot["filename"] + ".png")



def get_saved_png():
    """
    Returns a list of all saved .png images
    """
    created_hotspots = []

    for image in os.listdir("static"):
        if image.endswith(".png"):
            created_hotspots.append(image)

    return created_hotspots
