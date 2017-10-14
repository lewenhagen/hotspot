from flask import Flask, render_template

import functions

# import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import math
import csv
import pandas


app = Flask(__name__)


@app.route('/')
def main():
    # The filename for hotspot image
    filename = "static/map.png"
    # columns = ["Time", "Weekday", "Events"]

    # Get the data for the x axis
    x_axis_data = functions.get_axis_data("weekdays")

    # Get the data for the y axis
    y_axis_data = functions.get_axis_data("hours")

    # Sets up data for csv-file, using pandas
    # data = functions.setup_matrix(columns, x_axis_data, y_axis_data)
    # print(data)
    data = pandas.DataFrame(data=[
        [5, 5, 5, 1, 2, 3, 4],
        [5, 5, 5, 1, 2, 3, 4],
        [5, 5, 5, 1, 2, 3, 4],
        [5, 5, 5, 1, 2, 3, 4],
        [5, 5, 5, 1, 2, 3, 4],
        [5, 5, 5, 1, 2, 3, 4],
        [5, 5, 5, 1, 2, 3, 4],
        [5, 5, 5, 1, 2, 3, 4],
        [5, 5, 5, 1, 2, 3, 4],
        [5, 5, 5, 1, 2, 3, 4],
        [5, 5, 5, 1, 2, 3, 4],
        [5, 5, 5, 1, 2, 3, 4],
        [5, 5, 5, 1, 2, 3, 4],
        [5, 5, 5, 1, 2, 3, 4],
        [5, 5, 5, 1, 2, 3, 4],
        [5, 5, 5, 1, 2, 3, 4],
        [5, 5, 5, 1, 2, 3, 4],
        [5, 5, 5, 1, 2, 3, 4],
        [5, 5, 5, 1, 2, 3, 4],
        [5, 5, 5, 1, 2, 3, 4],
        [5, 5, 5, 1, 2, 3, 4],
        [5, 5, 5, 1, 2, 3, 4],
        [5, 5, 5, 1, 2, 3, 4],
        [5, 5, 5, 1, 2, 3, 4],


    ],
    index=y_axis_data,
    columns=x_axis_data)
    # Saves data to .csv
    # functions.save_csv("hotspot.csv", data, columns)

    # Creates a DataFrame to use, x_axis_data = correct order of x-axis-column
    # df = functions.create_dataframe("hotspot.csv", x_axis_data, columns)
    # print(type(df))
    fig, ax = plt.subplots(figsize=(7,7))
    sns.heatmap(data, ax=ax, cmap="YlOrRd", annot=True, fmt="d")

    ax.set_xlabel('Weekdays', fontsize=14)
    ax.set_ylabel('Hours', fontsize=14)

    plt.yticks(rotation=0,fontsize=8);
    plt.xticks(rotation=0, fontsize=8);
    plt.tight_layout()
    plt.savefig(filename)

    return render_template("index.html", hotspot=filename)


if __name__ == '__main__':
    app.run(debug=True)
