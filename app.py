#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Main file
Generates the heatmap and render the image in template
"""

import functions
import config
from flask import Flask, render_template, request, make_response
import time
import os, glob
import collections
from aoristic import parse
from hotspot import Hotspot
from timeline.timeline import Timeline
from visual import Visual
import calendar
import shutil



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
                datafile_as_dict = parse.csv_to_dict(hotspot.filter_value, hotspot.filter_column, hotspot.datafile)
                hotspot.getis, hotspot.conf_levels = functions.calculate_hotspot(hotspot, datafile_as_dict, "getis")
                hotspot.data = functions.calculate_hotspot(hotspot, datafile_as_dict)

            elif hotspot.datafile.endswith(".log"):
                hotspot.data, hotspot.getis, hotspot.conf_levels = functions.calculate_hotspot(hotspot)

            if hotspot.save_me:
                print("Saving aoristic csv...")
                functions.save_csv(hotspot.data, "static/maps/", hotspot.title, "_aoristic.csv")

                print("Saving getis csv...")
                functions.save_csv(hotspot.getis, "static/maps/", hotspot.title, "_gi.csv")


            # Creates the getis hotspot
            getis_hotspot = functions.create_hotspot(hotspot, "getis", hotspot.pvalue)
            # Save getis hotspot as png
            functions.save_figure(getis_hotspot, "static/maps/", hotspot.title, "_gi.png")
            # Creates the aoristic hotspot
            aoristic_hotspot = functions.create_hotspot(hotspot, "data")
            # Save aoristic hotspot as png
            functions.save_figure(aoristic_hotspot, "static/maps/", hotspot.title, "_aoristic.png")
            # Save the html table of confidence levels
            functions.save_table(hotspot.title, hotspot.conf_levels)
            # Get the saved pngs
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
# @nocache
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
        "jaccard": {},
        # "z_min": 0,
        # "z_max": 0,
        # "j_unique_all": 0,
        # "j_unique_hot": 0,
        # "j_unique_cold": 0,
        "data": []
    }
    try:
        os.remove("static/compare/compare.png")
        print("Removed compare.png!")
    except Exception as e:
        print("No such file: ", e)

    if request.method == "POST":
        if request.form["chooseCompareOne"] != request.form["chooseCompareTwo"]:
            if "Choose a hotspot..." not in (request.form["chooseCompareOne"], request.form["chooseCompareTwo"]):
                comparing = True

                compared_hotspot = functions.init_compare(request.form["chooseCompareOne"], request.form["chooseCompareTwo"])
                # compared_hotspot["j_unique_all"] = round(float(1 - compared_hotspot["jaccard"]["all"])*100, 3)
                # compared_hotspot["j_unique_hot"] = round(float(1 - compared_hotspot["jaccard"]["hot"])*100, 3)
                # compared_hotspot["j_unique_cold"] = round(float(1 - compared_hotspot["jaccard"]["cold"])*100, 3)
                functions.create_compared_heatmap(compared_hotspot["data"])
                compared_pngs.append(request.form["chooseCompareOne"])
                compared_pngs.append(request.form["chooseCompareTwo"])
            else:
                error = "You have to choose two files."
        else:
            error = "Can not compare the same files."



    return render_template("compare.html", created=sorted(all_folders), error=error, comparing=comparing, compared_pngs=compared_pngs, percent=compared_hotspot["all_percentage"], jaccard=compared_hotspot["jaccard"], time="?"+str(time.time()))



@app.route('/visualize/', methods=["POST", "GET"])
def visualize():
    """
    Visualize route
    """

    if request.method == "GET":
        choose_data = config.get_datafiles()
        return render_template("visualize.html", choose_data=choose_data)
    elif request.method == "POST":
        try:
            shutil.rmtree("static/visualize")
            print(">>> Removed folder: visualized")
        except Exception as e:
            print("No such folder: ", e)

        data_for_timeline = collections.OrderedDict()
        month_names = []
        hotspots = []
        hotspot = {}
        conflevel = request.form["setupConfidenceLevel"]

        months = calendar.month_name
        dates = ["", "2014-01", "2014-02", "2014-03", "2014-04", "2014-05", "2014-06", "2014-07", "2014-08", "2014-09", "2014-10", "2014-11", "2014-12"]
        empty_hotspots = []
        splitted_months = functions.split_csv(request.form["setupData"])
        for mon in range(1, 13):
            hotspot = Visual(request.form["setupData"], months[mon], conflevel, units)
            hotspot.getis, hotspot.conf_levels = functions.calculate_hotspot(hotspot, splitted_months[mon-1]["data"], "getis")

            data_for_timeline[months[mon]] = hotspot.getis

            functions.save_csv(hotspot.getis, "static/visualize/", hotspot.title, ".csv")
            # Creates the getis hotspot
            getis_hotspot = functions.create_hotspot(hotspot, "getis_visual", hotspot.pvalue)
            # Save getis hotspot as png
            functions.save_figure(getis_hotspot, "static/visualize/", hotspot.title, ".png")

            month_names.append(months[mon])
            # hotspots.append(hotspot)

        # Timeline takes a list of dataFrames
        timeline = Timeline(data_for_timeline)
        timeline.calculate_total()
        timeline.calculate_percentage()
        timeline_result = timeline.create_timeline()

        functions.save_figure(timeline_result, "static/visualize/", "timeline", ".png")

        return render_template("visualize.html", months=month_names, csvfile=request.form["setupData"], conf=conflevel, time="?"+str(time.time()))



if __name__ == '__main__':
    app.run(debug=True)
