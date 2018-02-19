#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Functions for hotspot
"""

import os, glob
import pandas
import random
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# import lisa # call lisa.get_neigbours(datalist, y, x, distance)
import config
from aoristic import aoristic
from aoristic import parse
from gi.getis import Gi
from compare import compare

import csv
# import time
# from hotspot import Hotspot
# from shutil import copyfile

def calculate_hotspot(hotspot, data=None):
    """
    call methods to calculate hotspot
    """
    t_map = config.create_empty_matrix(hotspot.xticks, hotspot.yticks)

    get_matrix(hotspot, t_map, data)
    res = get_data_frame(hotspot, t_map)

    return res



def get_matrix(hotspot, t_map, data):
    """
    Returns matrix with data
    """

    if hotspot.datafile.endswith(".csv"):
        aoristic.aoristic_method(data, t_map, hotspot.xticks, hotspot.yticks)
    elif hotspot.datafile.endswith(".log"):
        parse.log_to_dict(hotspot, t_map)



def get_data_frame(hotspot, t_map):
    """
    Returns DataFrame (2D-list) with data
    """
    # Use hotspot["city"] to select data.
    # CITYNAME or all


    print(t_map)
    print(hotspot)

    gi = Gi(t_map)
    # start_time = time.time()
    gi.calculate()
    result = {}
    result["conf_levels"] = {
    "0.90": gi.confidence_interval(0.90),
    "0.95": gi.confidence_interval(0.95),
    "0.99": gi.confidence_interval(0.99)
    }

    if hotspot.pvalue != "all":
        gi.clear_zscore(float(hotspot.pvalue))

    result["getis"] = gi.get_result()
    # print("--- %s seconds ---" % (time.time() - start_time))
    # result = lisa.calculate_from_matrix(t_map)

    df_getis = pandas.DataFrame(data=result["getis"],
                            index=hotspot.yticks["ticks"],
                            columns=hotspot.xticks["ticks"])

    df_data = pandas.DataFrame(data=t_map,
                            index=hotspot.yticks["ticks"],
                            columns=hotspot.xticks["ticks"])

    # g_map = lisa.calculate_from_matrix(t_map)
    # hotspot["getis"] = lisa.calculate_from_matrix(t_map)

    if hotspot.save_me:
        print("Saving file!")
        if not os.path.exists("static/maps/" + hotspot.title):
            print("Creating folder")
            os.makedirs("static/maps/" + hotspot.title)

        df_getis.to_csv("static/maps/" + hotspot.title + "/" + hotspot.title + "_gi.csv", sep=",", encoding="utf-8")
        df_data.to_csv("static/maps/" + hotspot.title + "/" + hotspot.title + "_aoristic.csv", sep=",", encoding="utf-8")
        print("Saved csv files.")
    # lisa.get_neigbours(data, 5, 5, 2)
    return (df_data, df_getis, result["conf_levels"])



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
    # setup_filter = req_form["setupFilter"]
    setup_x_ticks = req_form["setupXticks"]
    setup_y_ticks = req_form["setupYticks"]
    setup_title = req_form["setupTitle"]
    filename = req_form["setupTitle"]

    if any(field is "" for field in (setup_x_ticks, setup_y_ticks, setup_title, filename)):
        result["valid"] = False
        result["error"] = "You forgot something in the form."

    if os.path.exists("static/maps/" + filename):
        result["valid"] = False
        result["error"] = "Filename already exists."

    return result



# def setup_hotspot(req_form, units):
#     """
#     Creates the hotspot base dict and returns it
#     """
#     hotspot = Hotspot(req_form, units)
#
#     # hotspot.datafile = req_form["datachosen"]
#     # hotspot.title = req_form["setupTitle"]
#     # hotspot.filter_value = req_form.get("setupFilter")
#     # hotspot.filter_column = req_form.get("filtercolumn")
#     # hotspot.xticks = units[req_form["setupXticks"]]
#     # hotspot.yticks = units[req_form["setupYticks"]]
#     # hotspot.labels = {
#     #     "xlabel": units[req_form["setupXticks"]]["unit"],
#     #     "ylabel": units[req_form["setupYticks"]]["unit"]
#     # }
#     # hotspot.save_me = True if req_form.getlist("savecsv") else False
#     # hotspot.pvalue = req_form["setupConfidenceLevel"]
#     # hotspot.units = units
#
#     return hotspot
    # hotspot = {
    #     # "filename": req_form["setupFilename"],
    #     "datafilename": req_form["datachosen"],
    #     "title": req_form["setupTitle"],
    #     "filtervalue": req_form.get("setupFilter"),
    #     "filtercolumn": req_form.get("filtercolumn"),
    #     "xticks": units[req_form["setupXticks"]],
    #     "yticks": units[req_form["setupYticks"]],
    #     "labels": {
    #         "xlabel": units[req_form["setupXticks"]]["unit"],
    #         "ylabel": units[req_form["setupYticks"]]["unit"]
    #     },
    #     "save_me": True if req_form.getlist("savecsv") else False,
    #     "pvalue": req_form["setupConfidenceLevel"],
    #     "units": units
    # }

    # if req_form["datachosen"].endswith(".csv"):
    #     hotspot.data, hotspot.getis, hotspot.conf_levels = get_data_frame(hotspot, parse.csv_to_dict(hotspot["filtervalue"], hotspot["filtercolumn"], req_form["datachosen"]))
    #
    # elif req_form["datachosen"].endswith(".log"):
    #     hotspot.data, hotspot.getis, hotspot.conf_levels = get_data_frame(hotspot)

    # return hotspot



def create_hotspot(hotspot, use_hotspot, levels=None, cbar=True):
    """
    Creates a hotspot
    """
    # if use_hotspot == "getis":
    #     hotspot["title"] += "-getis"
    # Returns a tuple containing a figure and axes object(s)
    fig, ax = plt.subplots(figsize=(7,7))

    # Creates a heatmap. ax = axes object, cmap = colorscheme, annot = display data in map, fmt = format on annot
    if use_hotspot == "getis":
        sns.heatmap(hotspot.getis, ax=ax, cmap="bwr", annot=True, fmt=".1f", cbar=cbar)
        ax.set_title(hotspot.title + "-Gi* p-value: " + levels)

    elif use_hotspot == "data":
        sns.heatmap(hotspot.data, ax=ax, cmap="bwr", annot=True, fmt=".1f", cbar=cbar)
        ax.set_title(hotspot.title + "-Aoristic")

    # Sets labels and title
    ax.set_xlabel(hotspot.labels["xlabel"], fontsize=14)
    ax.set_ylabel(hotspot.labels["ylabel"], fontsize=14)
    # if use_hotspot == "getis":
    #     ax.set_title(hotspot.title + "-Gi* p-value: " + levels)
    # else:
    #     ax.set_title(hotspot.title + "-Aoristic")

    # Moves tick marker outside both axis
    ax.tick_params(axis='both', direction="out")

    # Config for the axis ticks
    plt.yticks(rotation=0,fontsize=8);
    plt.xticks(rotation=0, fontsize=8);

    # Makes sure the image (labels) is not cut off
    plt.tight_layout()

    # Saves the figure as an image
    if not os.path.exists("static/maps/" + hotspot.title):
        os.makedirs("static/maps/" + hotspot.title)

    if use_hotspot == "getis":
        plt.savefig("static/maps/" + hotspot.title + "/" + hotspot.title + "_gi.png")
    else:
        plt.savefig("static/maps/" + hotspot.title + "/" + hotspot.title + "_aoristic.png")


def create_compared_heatmap(data):
    """
    Create heatmap with overlap from comparison
    """
    heatmap = sns.heatmap(data, cmap="bwr", annot=True, fmt=".1f")
    heatmap.figure.savefig("static/compare/compare.png")
    print("Saved compared png!")



def get_folders():
    """
    Returns saved folders
    """
    return [ name for name in os.listdir("static/maps") if os.path.isdir(os.path.join("static/maps", name)) ]
    # return os.listdir('static')



def get_saved_png(folder):
    """
    Returns a list of all saved .png images
    """
    created_hotspots = []

    for image in os.listdir("static/maps/" + folder):
        if image.endswith(".png"):
            created_hotspots.append(image)

    return created_hotspots



def get_saved_csv(folder):
    """
    Returns a list of the saved csv's
    """
    created_csvs = []
    # ändra här för att jämföra fler alternativ! (pil nedåt)
    for csv_file in os.listdir("static/maps/" + folder):
        if csv_file.endswith("_gi.csv"):
            created_csvs.append(csv_file)

    return created_csvs



def save_table(folder, lisa):
    """
    Saves a copy of the html table
    """
    if not os.path.exists("templates/created/" + folder):
        os.makedirs("templates/created/" + folder)

    table = """<table class="table table-striped">
    <thead>
        <tr>
            <th>Confidence level</th>
            <th>p-value</th>
            <th>z-score range</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>0.90%</td><td>0.10</td><td>{} < Z < {}</td></tr>
        <tr><td>0.95%</td><td>0.05</td><td>{} < Z < {}</td></tr>
        <tr><td>0.99%</td><td>0.01</td><td>{} < Z < {}</td></tr>
    </tbody>
</table>
    """.format(lisa["0.90"][0], lisa["0.90"][1], lisa["0.95"][0], lisa["0.95"][1], lisa["0.99"][0], lisa["0.99"][1])

    with open("templates/created/" + folder + "/getis_table.html", "w+") as f:
        f.write(table)

def init_compare(hotspot_one, hotspot_two):
    """
    Initialize comparison of hotspots
    """
    path_for_one = "static/maps/" + hotspot_one + "/" + get_saved_csv(hotspot_one)[0]
    path_for_two = "static/maps/" + hotspot_two + "/" + get_saved_csv(hotspot_two)[0]

    csv_one = pandas.read_csv(path_for_one, usecols=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], encoding="utf-8").values
    csv_two = pandas.read_csv(path_for_two, usecols=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], encoding="utf-8").values

    return compare(csv_one, csv_two)
