#!usr/bin/env python3
import sys
import pandas
import random

"""
Functions for hotspot
"""

def get_axis_data(data_type):
    """
    Returns a dataset for x axis
    """
    data = {
        "weekdays": ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        "hours": ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00',
            '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
            '12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
            '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'
        ]
    }

    try:
        return data[data_type]
    except KeyError:
        print("Data not in dict.")
        return []



def save_csv(filename, data, columns):
    """
    Saves DataFrame as CSV
    """
    df_save = pandas.DataFrame(data, columns=columns)
    df_save.to_csv(filename)



def setup_matrix(columns, x_data, y_data):
    """
    Returns the data
    """
    data = {}
    data[columns[0]] = []
    data[columns[1]] = []
    data[columns[2]] = []
    for y in y_data:
        for x in x_data:
            data[columns[0]].append(y)
            data[columns[1]].append(x)
            data[columns[2]].append(random.randint(0, 100))

    return data



def create_dataframe(filename, sort_on, columns):
    """
    Creates a DataFrame file from csv
    """
    csv_file = pandas.read_csv(filename)
    df = csv_file.pivot_table(index=columns[0], columns=columns[1], values=columns[2], fill_value=0)
    df = df.reindex_axis(sort_on, axis=1) # Sort columns and their data

    return df
