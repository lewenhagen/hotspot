#!/usr/bin/env python3

"""
Main file
Generates the heatmap and render the image in template
"""

import functions
import config
# from config import setup
from flask import Flask, render_template, request
import os, glob
import sys
sys.path.insert(0, 'aoristic/')
import aoristic
# print(sys.path)
# from aoristic import aoristic
# from aoristic import date_functions
# from aoristic import read_csv


# setup = config.setup

app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def main():
    """
    Main route
    """
    if request.method == "GET":
        choose_data = config.get_datafiles()

        return render_template("index.html", choose_data=choose_data)

    elif request.method == "POST":
        data_chosen = request.form["setupData"]

        setup = config.setup
        setup["cities"] = config.get_cities_as_list(data_chosen)

        return render_template("index.html", data_chosen=data_chosen, setup=setup)


@app.route("/hotspot", methods=["POST"])
def hotspot():
    """ Hotspot route """

    if request.method == "POST":
        setup_data = request.form["datachosen"]
        setup_city = request.form["setupCity"]
        setup_x_ticks = request.form["setupXticks"]
        setup_y_ticks = request.form["setupYticks"]
        setup_title = request.form["setupTitle"]
        filename = request.form["setupFilename"]
        save_as_csv = False

        # Display error if any field is empty
        if any(field is "" for field in (setup_data, setup_city, setup_x_ticks, setup_y_ticks, setup_title, filename)):
            return render_template("index.html", error=True, setup=setup)

        # Save csv if checked
        if request.form.getlist("savecsv"):
            save_as_csv = True

        # if file exists, choose another filename
        if filename in os.listdir("static"):
            return render_template("index.html", duplicate=True, setup=setup)
        else:
            hotspot_one = {
                "filename": filename,
                "title": setup_title,
                "xticks": functions.get_ticks(setup_x_ticks),
                "yticks": functions.get_ticks(setup_y_ticks),
                "labels": {
                    "xlabel": setup_x_ticks,
                    "ylabel": setup_y_ticks
                }
            }

            # Get a 2d list, dataframe
            hotspot_one["data"] = functions.get_data(hotspot_one, setup_data, save_as_csv, setup_city)

            # Creates the hotspot
            functions.create_hotspot(hotspot_one)

            # The filename for hotspot image
            filename = hotspot_one["filename"] + ".png"

    return render_template("hotspot.html", hotspot=filename)

@app.route('/created', methods=["POST", "GET"])
def created():
    """
    Created route
    """

    created_hotspots = functions.get_saved_png()
    view_hotspots = []

    if request.method == "POST":
        view_hotspots = request.form.getlist("image")

    return render_template("created.html", created=sorted(created_hotspots), view_hotspots=view_hotspots)




if __name__ == '__main__':
    app.run(debug=True)
