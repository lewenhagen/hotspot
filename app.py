#!/usr/bin/env python3

"""
Main file
Generates the heatmap and render the image in template
"""

import functions
import config
from flask import Flask, render_template, request
import os, glob
import sys
sys.path.insert(0, 'aoristic/')
import aoristic
# print(sys.path)
# from aoristic import aoristic
# from aoristic import date_functions
# from aoristic import read_csv




app = Flask(__name__)


@app.route('/')
def main():
    """
    Main route
    """


    return render_template("index.html", xticks=config.x_ticks, yticks=config.y_ticks)


@app.route("/hotspot", methods=["POST"])
def hotspot():
    """ Hotspot route """
    save_as_csv = False

    if request.method == "POST":
        filename = request.form["setupFilename"]

        if request.form["savecsv"]:
            save_as_csv = True

        # if file exists, choose another filename
        if filename in os.listdir("static"):
            return render_template("index.html", xticks=config.x_ticks, yticks=config.y_ticks, duplicate=filename)
        else:
            hotspot_one = {
                "filename": filename,
                "title": request.form["setupTitle"],
                "xticks": functions.get_ticks(request.form["setupXticks"]),
                "yticks": functions.get_ticks(request.form["setupYticks"]),
                "labels": {
                    "xlabel": request.form["setupXticks"],
                    "ylabel": request.form["setupYticks"]
                }
            }

            # Get a 2d list, dataframe

            hotspot_one["data"] = functions.get_data(hotspot_one, request.form["setupData"], save_as_csv)

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

    created_hotspots = []
    view_hotspots = []

    for image in os.listdir("static"):
        if image.endswith(".png"):
            created_hotspots.append(image)


    if request.method == "POST":
        view_hotspots = request.form.getlist("image")

    return render_template("created.html", created=sorted(created_hotspots), view_hotspots=view_hotspots)




if __name__ == '__main__':
    app.run(debug=True)
