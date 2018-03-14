#!/usr/bin/env python3
"""
Main file for calculating PAI index (Prediction Accuracy Index)
"""

import numpy as np



def pai_index(study_area, prediction_area):
    """
    Calculates pai index on a prediction of hotspots
    Returns pai index score as a float
    """

    N = np.sum(study_area)
    n = np.sum(prediction_area)
    A = study_area.size
    a = prediction_area.size

    return ((n / N) * 100) / ((a / A) * 100)

if __name__ == "__main__":

    a = np.array([[ 0, 0, 0, 0, 0, 0, 0 ],
                [ 0, 34, 23, 0, 0, 0, 0 ],
                [ -1, 0, 0, 0, 0, 0, 0 ],
                [ 0, 0, 0, 0, 0, 0, 0 ],
                [ 0, 0, 1, 0, 1, 0, 0 ],
                [ 0, 1, 1, 0, 0, 0, 0 ],
                [ 0, 0, 0, 0, 0, 0, 0 ]])
    b = np.array([[ 0, 0, 0, 0, 0, 0, 0 ],
                [ 0, 33, 23, 0, 0, 0, 0 ],
                [ -1, 0, 0, 0, 0, 0, 0 ],
                [ 0, 0, 0, 0, 0, 0, 0 ],
                [ 0, 0, 1, 0, 1, 0, 0 ],
                [ 0, 1, 1, 0, 0, 0, 0 ],
                [ 0, 0, 0, 0, 0, 0, 0 ]])



    pai_index(a, b)
