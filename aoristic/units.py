#!/usr/bin/env python
"""
Contains all unit classes
"""
import datetime
import math

class Unit():
    """
    Base class for units.
    Used for Days, Hours inherits.
    """

    @staticmethod
    def get_hour(time):
        """
        Return the hour of the time
        """
        return time.hour

    @staticmethod
    def get_day(time):
        """
        Return the weekday of the time
        """
        return time.weekday()

    @staticmethod
    def get_month(time):
        """
        Return the month of the time
        """
        return time.month - 1

    @staticmethod
    def get_week(time):
        """
        Return the week number of the time
        """
        return time.isocalendar()[1]



    def __init__(self, event, get_x, get_y):
        self.start = self.create_dt(event, "start")
        self.end = self.create_dt_end(event)
        self.duration = self.end - self.start

        self.get_x = get_x
        self.get_y = get_y



    def create_dt(self, event, when):
        """
        create datetime object
        """
        hour = self.create_hour(event, when)
        day = int(event["date" + when][8:])
        month = int(event["date" + when][5:7])
        year = int(event["date" + when][:4])

        return datetime.datetime(hour=hour, day=day, month=month, year=year)



    def create_dt_end(self, event):
        """
        Creates datetime for evend end
        """
        end = self.create_dt(event, "end")
        round_up = self.create_timedelta()
        return end + round_up



    def create_hour(self, event, when):
        """
        Create hour for datetime

        Overriden in Hour class
        """
        return 0



    def calc_aoristic_value(self):
        """
        Calculate and return the aoristic value
        """
        time_span = self.get_duration()
        return 1.0 / time_span



    def create_timedelta(self, days=1):
        """
        Creates a timedelta for round up of end datetime

        Overriden in Hour class
        """
        return datetime.timedelta(days=days)



    def get_duration(self):
        """
        Return events durations as days, rounded up.
        """
        #remove float?
        return float(self.duration.days)



    @staticmethod
    def create_datetime_tupl(date_tupl):
        """
        Create datetime object from tuple
        """
        return datetime.datetime(day=int(date_tupl[0]),
            month=Unit.abbr_to_nr_month(date_tupl[1]),
            year=int(date_tupl[2]), hour=int(date_tupl[3]))



    @staticmethod
    def abbr_to_nr_month(month):
        """
        convert abbr month to number
        """
        return{
                'Jan' : 1,
                'Feb' : 2,
                'Mar' : 3,
                'Apr' : 4,
                'May' : 5,
                'Jun' : 6,
                'Jul' : 7,
                'Aug' : 8,
                'Sep' : 9,
                'Oct' : 10,
                'Nov' : 11,
                'Dec' : 12
        }[month]



    def __repr__(self):
        """
        Used in prints
        """
        return "Start: {start}\nEnd: {end}\nDuration: {dur}".format(start=self.start, end=self.end, dur=self.duration)



    # Generator method
    def __iter__(self):
        """
        Iterate over dates
        """
        dt = self.create_timedelta()
        while self.start < self.end:
            yield self.start
            self.start += dt



class Hour(Unit):
    """
    Sub class of Unit for hours
    """

    def create_hour(self, event, when):
        """
        Create hour for datetime
        """
        return int(event["time" + when][:2])



    def create_timedelta(self, hours=1):
        """
        Creates a timedelta for round up of end datetime

        Overriden in Hour class
        """
        return datetime.timedelta(hours=hours)



    def get_duration(self):
        """
        Return events durations as hours, rounded up.
        """
        #remove float?
        return math.ceil((self.duration.total_seconds()/3600))
