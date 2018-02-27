#!/usr/bin/env python3
"""
Containts Visual class
"""

class Visual():
    """
    Visual class
    """

    def __init__(self, month, conflevel, units):
        """
        init method
        """
        # self.datafile = req_form["datachosen"]
        self.title = month
        # self.filter_value = req_form.get("setupFilter")
        # self.filter_column = req_form.get("filtercolumn")
        self.xticks = "days" #units[req_form["setupXticks"]]
        self.yticks = "hours" #units[req_form["setupYticks"]]
        self.labels = {
            "xlabel": units["days"]["unit"],
            "ylabel": units["hours"]["unit"]
        }
        self.pvalue = conflevel
        self.units = units
