import random
from io import BytesIO

from flask import Flask, render_template, make_response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import plotly.plotly as py
import plotly.tools as tls
import datetime
from matplotlib.dates import DateFormatter
import plotly.graph_objs as go

tls.set_credentials_file(username='lewenhagen', api_key='AVixNJUGOkXkaWaZHGZC')

app = Flask(__name__)


@app.route('/')
def plot():

    filename = "static/map.png"

    # ys={
    #     '00:00': '00:00',
    #     '01:00': '01:00',
    #     '02:00': '02:00',
    #     '03:00': '03:00',
    #     '04:00': '04:00',
    #     '05:00': '05:00',
    #     '06:00': '06:00',
    #     '07:00': '07:00',
    #     '08:00': '08:00',
    #     '09:00': '09:00',
    #     '10:00': '10:00',
    #     '11:00': '11:00',
    #     '12:00': '12:00',
    #     '13:00': '13:00',
    #     '14:00': '14:00',
    #     '15:00': '15:00',
    #     '16:00': '16:00',
    #     '17:00': '17:00',
    #     '18:00': '18:00',
    #     '19:00': '19:00',
    #     '20:00': '20:00',
    #     '21:00': '21:00',
    #     '22:00': '22:00',
    #     '23:00': '23:00'
    # }
    #
    # yss=[
    # '00:00',
    # '01:00',
    # '02:00',
    # '03:00',
    # '04:00',
    # '05:00',
    # '06:00',
    # '07:00',
    # '08:00',
    # '09:00',
    # '10:00',
    # '11:00',
    # '12:00',
    # '13:00',
    # '14:00',
    # '15:00',
    # '16:00',
    # '17:00',
    # '18:00',
    # '19:00',
    # '20:00',
    # '21:00',
    # '22:00',
    # '23:00']
    #
    # xss = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # stamps = [{"start": "13:00", "weekday": "Friday"}]
    # z = []
    # for stamp in stamps:
    #     for i, v in enumerate(yss):
    #         if (v == stamp["start"]):
    #             if z[i] == None or z[i]:
    #                 z.append([1])
    #             else:
    #                 z.append()
    #         else:
    #             z.append(None)



    trace = go.Heatmap(
        z=[
            [None],                     # y[0]
            [None, 10, 20, 34]        # y[1]
        ],
        x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        y=[
            '00:00',
            '01:00',
            '02:00',
            '03:00',
            '04:00',
            '05:00',
            '06:00',
            '07:00',
            '08:00',
            '09:00',
            '10:00',
            '11:00',
            '12:00',
            '13:00',
            '14:00',
            '15:00',
            '16:00',
            '17:00',
            '18:00',
            '19:00',
            '20:00',
            '21:00',
            '22:00',
            '23:00'
        ]
        )

    data = [trace]
    layout = go.Layout(title="tjoho", width=800, height=800)
    fig = go.Figure(data=data, layout=layout)

    py.image.save_as(fig, filename=filename)

    return render_template("index.html", hotspot=filename)


if __name__ == '__main__':
    app.run(debug=True)
