#!/usr/bin/env python3

"""
Main file
Generates the heatmap and render the image in template
"""

import functions
from flask import Flask, render_template



app = Flask(__name__)



@app.route('/')
def main():
    """
    Main route
    """
    hotspot_one = {
        "filename": "map.png",
        "title": "Temporal hotspot 1",
        "xticks": functions.get_ticks("weekdays"),
        "yticks": functions.get_ticks("hours"),
        "labels": {
            "xlabel": "Weekdays",
            "ylabel": "Hours"
        }
    }

    hotspot_two = {
        "filename": "map2.png",
        "title": "Temporal hotspot 2",
        "xticks": functions.get_ticks("weekdays"),
        "yticks": functions.get_ticks("hours"),
        "labels": {
            "xlabel": "Weekdays",
            "ylabel": "Hours"
        }
    }

    # Get a 2d list, dataframe
    hotspot_one["data"] = functions.get_data(hotspot_one)
    hotspot_two["data"] = functions.get_data(hotspot_two)

    # Creates the hotspot
    functions.create_hotspot(hotspot_one)
    functions.create_hotspot(hotspot_two)

    # The filenames for hotspot images
    filenames = []

    filenames.append(hotspot_one["filename"])
    filenames.append(hotspot_two["filename"])

    return render_template("index.html", hotspots=filenames)



if __name__ == '__main__':
    app.run(debug=True)
