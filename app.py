#!/usr/bin/env python3

"""
Main file
Generates the heatmap and render the image in template
"""

import functions
import config
from flask import Flask, render_template, request
import os, glob
# import sys
# sys.path.insert(0, 'aoristic/')
import aoristic



app = Flask(__name__)



units_json = config.get_units()

units = units_json["units"]
units_keys = units_json["keys"]
setup = config.setup


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

        setup["cities"] = config.get_cities_as_list(data_chosen)

        return render_template("index.html", data_chosen=data_chosen, setup=setup)


@app.route("/hotspot", methods=["POST"])
def hotspot():
    """ Hotspot route """

    if request.method == "POST":
        valid_form = functions.validate_form(request.form)

        # Display error if any field is empty
        if not valid_form["valid"]:
            return render_template("index.html", error=valid_form["error"], data_chosen=valid_form["datachosen"], setup=setup)

        else:
            # Setup the hotspot dict
            hotspot = functions.setup_hotspot(request.form, units)

            # Creates the hotspot
            functions.create_hotspot(hotspot)




    return render_template("hotspot.html", hotspot=hotspot["filename"] + ".png")

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
