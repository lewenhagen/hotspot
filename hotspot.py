#!/usr/bin/env python3
"""
Containts Hotspot class
"""

class Hotspot():
    """
    Hotspot class
    """

    def __init__(self, req_form, units):
        """
        inti method
        """
        self.datafile = req_form["datachosen"]
        self.title = req_form["setupTitle"]
        self.filter_value = req_form.get("setupFilter")
        self.filter_column = req_form.get("filtercolumn")
        self.xticks = units[req_form["setupXticks"]]
        self.yticks = units[req_form["setupYticks"]]
        self.labels = {
            "xlabel": units[req_form["setupXticks"]]["unit"],
            "ylabel": units[req_form["setupYticks"]]["unit"]
        }
        self.save_me = True if req_form.getlist("savecsv") else False
        self.pvalue = req_form["setupConfidenceLevel"]
        self.units = units
