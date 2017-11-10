#!/usr/bin/env python
"""
Contains all unit classes
"""
class Unit:
    """
    Base class for units
    """
    def __init__(self, event):
        self.start = self.create_dt(event, "start")
        self.end = self.create_dt(event, "end")
        self.duration = ""
        
    def create_dt(self, event, when):
        """
        create datetime object
        """
        hour = int(hour)

        day = int(event["date" + when][8:])
        month = int(event["date" + when][5:7])
        year = int(event["date" + when][:4])

        return datetime.date(hour=hour, day=day, month=month, year=year)
