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
# import sys
import re
# sys.path.insert(0, 'aoristic/')
from aoristic import aoristic



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



def log_to_dict(filename):
    result = []
    pattern = r"\[([\w]{1,2}).*([A-z]{3}).*([\w]{4}):([\w]{2}:[\w]{2}:[\w]{2})\s"
    with open("datafiles/" + filename, "r") as filehandler:
        lines = filehandler.readlines()

    for line in lines:
        match = re.findall( pattern, line )

        part = {
            "day": match[0][0],
            "month": match[0][1],
            "year": match[0][2],
            "timestart": match[0][3],
            "timeend": match[0][3]
        }
        result.append(part)

    return result


def get_data(hotspot, datafile_to_use):
    """
    Returns DataFrame (2D-list) with data
    """
    # Use hotspot["city"] to select data.
    # CITYNAME or all
    t_map = config.create_empty_matrix(hotspot["xticks"], hotspot["yticks"])

    if hotspot["datafilename"].endswith(".csv"):
        aoristic.aoristic_method(datafile_to_use, t_map, hotspot["xticks"], hotspot["yticks"])

    df = pandas.DataFrame(data=t_map,
                            index=hotspot["yticks"]["ticks"],
                            columns=hotspot["xticks"]["ticks"])

    if hotspot["save_me"]:
        # ändra sep till ","/";"?
        df.to_csv("saved_csv_hotspots/" + hotspot["filename"] + ".csv", sep="\t", encoding="utf-8")
    # lisa.get_neigbours(data, 5, 5, 2)
    return df



def validate_form(req_form):
    """
    Makes sure the form is proper filled
    """
    result = {
        "valid": True,
        "error": None,
        "datachosen": req_form["datachosen"]
    }

    # setup_data = req_form["datachosen"]
    setup_city = req_form["setupCity"]
    setup_x_ticks = req_form["setupXticks"]
    setup_y_ticks = req_form["setupYticks"]
    setup_title = req_form["setupTitle"]
    filename = req_form["setupFilename"]

    if any(field is "" for field in (setup_city, setup_x_ticks, setup_y_ticks, setup_title, filename)):
        result["valid"] = False
        result["error"] = "You forgot something in the form."

    if filename + ".png" in os.listdir("static"):
        result["valid"] = False
        result["error"] = "Filename already exists."

    return result



def setup_hotspot(req_form, units):
    """
    Creates the hotspot base dict and returns it
    """
    hotspot = {
        "filename": req_form["setupFilename"],
        "datafilename": req_form["datachosen"],
        "title": req_form["setupTitle"],
        "city": req_form["setupCity"],
        "xticks": units[req_form["setupXticks"]],
        "yticks": units[req_form["setupYticks"]],
        "labels": {
            "xlabel": units[req_form["setupXticks"]]["unit"],
            "ylabel": units[req_form["setupYticks"]]["unit"]
        },
        "save_me": True if req_form.getlist("savecsv") else False,
        "units": units
    }

    hotspot["data"] = get_data(hotspot, csv_to_dict(req_form["datachosen"]))

    return hotspot



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
