#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Main file
Generates the heatmap and render the image in template
"""

import functions
import config
from flask import Flask, render_template, request
import os, glob
from aoristic import parse
from hotspot import Hotspot



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
        if "setupData" in request.form: # Data has been chosen, next choose filter if csv
            setup["datafile"] = request.form["setupData"]

            if setup["datafile"].endswith(".csv"):
                csv_header = config.get_csv_header(setup["datafile"])

                return render_template("index.html", choose_filter=csv_header, setup=setup)

            elif setup["datafile"].endswith(".log"):

                return render_template("index.html", setup=setup)

        elif "setupFilter" in request.form: # filter has been chosen, next prepate setup hotspot
            if "filter" not in request.form:
                setup["filter"]["column"] = request.form["setupFilter"]
                setup["filter"]["values"] = config.get_column_as_list(setup["datafile"], setup["filter"]["column"])

                return render_template("index.html", setup=setup, chose_filter=True)
            else:
                return render_template("index.html", setup=setup)



@app.route("/hotspot", methods=["POST"])
def hotspot():
    """
    Hotspot route
    """
    if request.method == "POST":
        valid_form = functions.validate_form(request.form)
        # Display error if any field is empty
        if not valid_form["valid"]:
            return render_template("index.html", error=valid_form["error"], data_chosen=valid_form["datachosen"], setup=setup)

        else:
            # Setup the hotspot
            # hotspot = functions.setup_hotspot(request.form, units)
            hotspot = Hotspot(request.form, units)

            if hotspot.datafile.endswith(".csv"):
                hotspot.data, hotspot.getis, hotspot.conf_levels = functions.calculate_hotspot(hotspot, parse.csv_to_dict(hotspot.filter_value, hotspot.filter_column, hotspot.datafile))

            elif hotspot.datafile.endswith(".log"):
                hotspot.data, hotspot.getis, hotspot.conf_levels = functions.calculate_hotspot(hotspot)


            # Creates the hotspots
            functions.create_hotspot(hotspot, "data")
            functions.create_hotspot(hotspot, "getis", hotspot.pvalue)

            functions.save_table(hotspot.title, hotspot.conf_levels)

            filelist = functions.get_saved_png(hotspot.title)
            #os.listdir('static/maps/' + hotspot["title"])


    return render_template("hotspot.html", folder=hotspot.title, hotspots=filelist, lisa=hotspot.conf_levels)



@app.route('/show/', methods=["POST", "GET"])
@app.route('/show/<folder>', methods=["POST", "GET"])
def show(folder=None):
    """
    Show route
    """
    all_folders = functions.get_folders()

    if folder is None:
        view_hotspots = []
    elif folder in functions.get_folders():
        view_hotspots = functions.get_saved_png(folder)

    return render_template("show.html", created=sorted(all_folders), view_hotspots=view_hotspots, folder=folder)



@app.route('/compare/', methods=["POST", "GET"])
def compare():
    """
    Compare route
    """
    comparing = False
    error = False
    compared_pngs = []
    all_folders = functions.get_folders()
    compared_hotspot = {
        "all_percentage": 0,
        "data": []
    }
    try:
        os.remove("static/compare/compare.png")
        print("Removed compare.png!")
    except Exception as e:
        print("No such file: ", e)

    if request.method == "POST":
        if request.form["chooseCompareOne"] != request.form["chooseCompareTwo"]:
            comparing = True
            if "overlap" in request.form:
                compared_hotspot = functions.init_compare(request.form["chooseCompareOne"], request.form["chooseCompareTwo"], True)
            else:
                compared_hotspot = functions.init_compare(request.form["chooseCompareOne"], request.form["chooseCompareTwo"])
            functions.create_compared_heatmap(compared_hotspot["data"])
            compared_pngs.append(request.form["chooseCompareOne"])
            compared_pngs.append(request.form["chooseCompareTwo"])
        else:
            error = "Can not compare the same hotspots."



    return render_template("compare.html", created=sorted(all_folders), error=error, comparing=comparing, compared_pngs=compared_pngs, percent=compared_hotspot["all_percentage"])



if __name__ == '__main__':
    app.run(debug=True)
