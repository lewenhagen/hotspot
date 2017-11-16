#!/usr/bin/env python3
"""
Module for calculating the confidence interval
"""

import numpy as np
from math import sqrt
import scipy.stats as st

def conf_interval(data, confidence=0.95):
    """
    Calculates the confidence interval for given data.
    Defaults at 95% confidence level.
    """
    mean = data.mean()
    var = np.var(data)
    std = sqrt(var)

    return st.norm.interval(confidence, loc=mean, scale=std)
