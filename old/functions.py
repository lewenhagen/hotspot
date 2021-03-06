#!usr/bin/env python3

"""
Functions for hotspot
"""

import pandas
import random
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def get_ticks(data_type):
    """
    Returns a dataset for x axis
    """
    data = {
        "weekdays": ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        "hours": [
            '00:00', '01:00', '02:00', '03:00', '04:00', '05:00',
            '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
            '12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
            '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'
        ],
        "months": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    }

    try:
        return data[data_type]
    except KeyError:
        raise SystemExit("No such tick data: {}. Change input and save file to reload.".format(data_type))


def get_data(hotspot):
    """
    Returns DataFrame (2D-list) with data
    """

    data = []

    for i, v in enumerate(hotspot["yticks"]):
        data.append([])
        for _ in hotspot["xticks"]:
            data[i].append(random.randint(0, 100))

    return pandas.DataFrame(data=data,
                            index=hotspot["yticks"],
                            columns=hotspot["xticks"])



def create_hotspot(hotspot, cbar=True):
    """
    Creates a hotspot
    """
    # Returns a tuple containing a figure and axes object(s)
    fig, ax = plt.subplots(figsize=(7,7))

    # Creates a heatmap. ax = axes object, cmap = colorscheme, annot = display data in map, fmt = format on annot
    sns.heatmap(hotspot["data"], ax=ax, cmap="gist_gray_r", annot=True, fmt="d", cbar=cbar)

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
    plt.savefig("static/" + hotspot["filename"])
