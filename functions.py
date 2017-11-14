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
import lisa # call lisa.get_neigbours(datalist, y, x, distance)
import config
from aoristic import aoristic
from aoristic import parser



def get_data_frame(hotspot, datafile_to_use=None):
    """
    Returns DataFrame (2D-list) with data
    """
    # Use hotspot["city"] to select data.
    # CITYNAME or all
    t_map = config.create_empty_matrix(hotspot["xticks"], hotspot["yticks"])
    if hotspot["datafilename"].endswith(".csv"):
        aoristic.aoristic_method(datafile_to_use, t_map, hotspot["xticks"], hotspot["yticks"])
    elif hotspot["datafilename"].endswith(".log"):
        parser.log_to_dict(hotspot, t_map)
        # print(t_map)

    result = lisa.calculate_from_matrix(t_map)

    df_getis = pandas.DataFrame(data=result["getis"],
                            index=hotspot["yticks"]["ticks"],
                            columns=hotspot["xticks"]["ticks"])

    df_data = pandas.DataFrame(data=t_map,
                            index=hotspot["yticks"]["ticks"],
                            columns=hotspot["xticks"]["ticks"])

    # g_map = lisa.calculate_from_matrix(t_map)
    # hotspot["getis"] = lisa.calculate_from_matrix(t_map)

    if hotspot["save_me"]:
        if not os.path.exists("static/" + hotspot["title"]):
            os.makedirs("static/" + hotspot["title"])
        # ändra sep till ","/";"?
        df_getis.to_csv("static/" + hotspot["title"] + "_getis.csv", sep=",", encoding="utf-8")
        df_data.to_csv("static/" + hotspot["title"] + "_aoristic.csv", sep=",", encoding="utf-8")

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
    filename = req_form["setupFilename"]

    if any(field is "" for field in (setup_x_ticks, setup_y_ticks, setup_title, filename)):
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
        "filtervalue": req_form.get("setupFilter"),
        "filtercolumn": req_form.get("filtercolumn"),
        "xticks": units[req_form["setupXticks"]],
        "yticks": units[req_form["setupYticks"]],
        "labels": {
            "xlabel": units[req_form["setupXticks"]]["unit"],
            "ylabel": units[req_form["setupYticks"]]["unit"]
        },
        "save_me": True if req_form.getlist("savecsv") else False,
        "units": units
    }
    if req_form["datachosen"].endswith(".csv"):
        hotspot["data"], hotspot["getis"], hotspot["conf_levels"] = get_data_frame(hotspot, parser.csv_to_dict(hotspot["filtervalue"], hotspot["filtercolumn"], req_form["datachosen"]))

    elif req_form["datachosen"].endswith(".log"):
        hotspot["data"] = get_data_frame(hotspot)
    return hotspot



def create_hotspot(hotspot, use_hotspot, cbar=True):
    """
    Creates a hotspot
    """
    if use_hotspot == "getis":
        hotspot["filename"] += "-getis"
    # Returns a tuple containing a figure and axes object(s)
    fig, ax = plt.subplots(figsize=(7,7))

    # Creates a heatmap. ax = axes object, cmap = colorscheme, annot = display data in map, fmt = format on annot
    sns.heatmap(hotspot[use_hotspot], ax=ax, cmap="bwr", annot=True, fmt=".1f", cbar=cbar)

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
    if not os.path.exists("static/" + hotspot["title"]):
        os.makedirs("static/" + hotspot["title"])
    plt.savefig("static/" + hotspot["title"] + "/" + hotspot["filename"] + ".png")



def get_saved_png():
    """
    Returns a list of all saved .png images
    """
    created_hotspots = []

    for image in os.listdir("static"):
        if image.endswith(".png"):
            created_hotspots.append(image)

    return created_hotspots
