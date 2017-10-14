#!/usr/bin/env python3

"""
Main file
Generates the heatmap and render the image in template
"""

import seaborn as sns
import matplotlib.pyplot as plt
import functions
from flask import Flask, render_template



app = Flask(__name__)



@app.route('/')
def main():
    """
    Main route
    """
    # The filename for hotspot image
    filename = "static/map.png"

    # Get a 2d list, dataframe
    data = functions.get_data()

    # Returns a tuple containing a figure and axes object(s)
    fig, ax = plt.subplots(figsize=(7,7))

    # Creates a heatmap. ax = axes object, cmap = colorscheme, annot = display data in map, fmt = format on annot
    sns.heatmap(data, ax=ax, cmap="YlOrRd", annot=True, fmt="d")

    # Sets labels and title
    ax.set_xlabel('Weekdays', fontsize=14)
    ax.set_ylabel('Hours', fontsize=14)
    ax.set_title("Temporal Hotspot")

    # Moves tick marker outside both axis
    ax.tick_params(axis='both', direction="out")

    # Config for the axis ticks
    plt.yticks(rotation=0,fontsize=8);
    plt.xticks(rotation=0, fontsize=8);

    # Makes sure the image (labels) is not cut off
    plt.tight_layout()

    # Saves the figure as an image
    plt.savefig(filename)

    return render_template("index.html", hotspot=filename)



if __name__ == '__main__':
    app.run(debug=True)
