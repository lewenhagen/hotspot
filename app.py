#!/usr/bin/env python3

"""
Main file
Generates the heatmap and render the image in template
"""

import functions
import config
from flask import Flask, render_template, request
import os, glob



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

    if request.method == "POST":
        filename = request.form["setupFilename"] + ".png"

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


            # hotspot_two = {
            #     "filename": "map2.png",
            #     "title": "Temporal hotspot 2",
            #     "xticks": functions.get_ticks("weekdays"),
            #     "yticks": functions.get_ticks("hours"),
            #     "labels": {
            #         "xlabel": "Weekdays",
            #         "ylabel": "Hours"
            #     }
            # }

            # Get a 2d list, dataframe
            hotspot_one["data"] = functions.get_data(hotspot_one)
            # hotspot_two["data"] = functions.get_data(hotspot_two)

            # Creates the hotspot
            functions.create_hotspot(hotspot_one)
            # functions.create_hotspot(hotspot_two)

            # The filenames for hotspot images
            filenames = []

            filenames.append(hotspot_one["filename"])
            # filenames.append(hotspot_two["filename"])

    return render_template("hotspot.html", hotspots=filenames)

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

    return render_template("created.html", created=created_hotspots, view_hotspots=view_hotspots)




if __name__ == '__main__':
    app.run(debug=True)
