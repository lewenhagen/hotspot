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
import calendar
import csv


def save_csv(file_to_save, file_path, file_name, file_ending):
    """
    Saves file as csv
    """
    print("Saving file!")
    if not os.path.exists(file_path + file_name):
        print("Creating folder:", file_path + file_name)
        os.makedirs(file_path + file_name)

    file_to_save.to_csv(file_path + file_name + "/" + file_name + file_ending, sep=",", encoding="utf-8")
    print("Saved csv files.")


def save_figure(file_to_save, file_path, file_name, file_ending):
    """
    Saves file as png
    """
    if not os.path.exists(file_path + file_name):
        os.makedirs(file_path + file_name)

    file_to_save.savefig(file_path + file_name + "/" + file_name + file_ending)



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

    # print(t_map)
    # print(hotspot)

    gi = Gi(t_map)
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

    df_getis = pandas.DataFrame(data=result["getis"],
                            index=hotspot.yticks["ticks"],
                            columns=hotspot.xticks["ticks"])

    df_data = pandas.DataFrame(data=t_map,
                            index=hotspot.yticks["ticks"],
                            columns=hotspot.xticks["ticks"])

    if hotspot.save_me:
        print("Saving getis csv...")
        save_csv(df_getis, "static/maps/", hotspot.title, "_gi.csv")
        print("Saving aoristic csv...")
        save_csv(df_data, "static/maps/", hotspot.title, "_aoristic.csv")

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



def create_hotspot(hotspot, use_hotspot, levels=None, cbar=True):
    """
    Creates a hotspot
    """

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

    # Moves tick marker outside both axis
    ax.tick_params(axis='both', direction="out")

    # Config for the axis ticks
    plt.yticks(rotation=0,fontsize=8)
    plt.xticks(rotation=0, fontsize=8)

    # Makes sure the image (labels) is not cut off
    plt.tight_layout()

    return plt
    # if use_hotspot == "getis":
    #     save_figure(plt, "static/maps/", hotspot.title, "_gi.png")
    # else:
    #     save_figure(plt, "static/maps/", hotspot.title, "_aoristic.png")



def create_compared_heatmap(data):
    """
    Create heatmap with overlap from comparison
    """
    ticks = {
        "yticks": [
            "00:00", "01:00", "02:00", "03:00", "04:00", "05:00",
            "06:00", "07:00", "08:00", "09:00", "10:00", "11:00",
            "12:00", "13:00", "14:00", "15:00", "16:00", "17:00",
            "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"
        ],
        "xticks": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    }
    fig, ax = plt.subplots(figsize=(7,7))
    ax.set_title("Percentual increase/decrease")
    ax.tick_params(axis='both', direction="out")

    # Config for the axis ticks
    plt.yticks(rotation=0,fontsize=8);
    plt.xticks(rotation=0, fontsize=8);

    # Makes sure the image (labels) is not cut off
    plt.tight_layout()
    heatmap = sns.heatmap(data, ax=ax, annot=True, fmt=".1f", cbar=True)

    if not os.path.exists("static/compare/"):
        os.makedirs("static/compare")
        print(">>> Created folder: static/compare")

    heatmap.figure.savefig("static/compare/compare.png")
    print(">>> Saved compared png!")



def get_folders():
    """
    Returns saved folders
    """
    return [ name for name in os.listdir("static/maps") if os.path.isdir(os.path.join("static/maps", name)) ]



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

def init_compare(hotspot_one, hotspot_two, overlap=False):
    """
    Initialize comparison of hotspots
    """
    compared = {}
    path_for_one = "static/maps/" + hotspot_one + "/" + get_saved_csv(hotspot_one)[0]
    path_for_two = "static/maps/" + hotspot_two + "/" + get_saved_csv(hotspot_two)[0]

    csv_one = pandas.read_csv(path_for_one, usecols=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], encoding="utf-8").values
    csv_two = pandas.read_csv(path_for_two, usecols=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], encoding="utf-8").values

    return compare(csv_one, csv_two, overlap)



def split_csv(big_file):
    """
    Splits csv into months dict
    """
    # csv_to_dict(filter_v, filter_c, file_name="temp.csv", deli=";"):
    # filter_v = 2014-01
    # filter_c = datestart
    splitted_months = {}
    months = calendar.month_name

    for mon in range(1, 13):
        splitted_months[months[mon]] = []

    all_months = pandas.read_csv("datafiles/" + big_file, encoding="utf-8").values

    for row in all_months:
        part = np.core.defchararray.split(row.astype(str), ";").tolist()

        if "2014-01" in part[0][1]:
            splitted_months["January"].append(row.tolist())
        elif "2014-02" in part[0][1]:
            splitted_months["February"].append(row.tolist())
        elif "2014-03" in part[0][1]:
            splitted_months["March"].append(row.tolist())
        elif "2014-04" in part[0][1]:
            splitted_months["April"].append(row.tolist())
        elif "2014-05" in part[0][1]:
            splitted_months["May"].append(row.tolist())
        elif "2014-06" in part[0][1]:
            splitted_months["June"].append(row.tolist())
        elif "2014-07" in part[0][1]:
            splitted_months["July"].append(row.tolist())
        elif "2014-08" in part[0][1]:
            splitted_months["August"].append(row.tolist())
        elif "2014-09" in part[0][1]:
            splitted_months["September"].append(row.tolist())
        elif "2014-10" in part[0][1]:
            splitted_months["October"].append(row.tolist())
        elif "2014-11" in part[0][1]:
            splitted_months["November"].append(row.tolist())
        elif "2014-12" in part[0][1]:
            splitted_months["December"].append(row.tolist())


    return all_months.tolist()





def init_visualization():
    """
    Initialize the visualization
    """
    # months = split_csv()
