#!/usr/bin/env python
"""
Test aoristic method
"""
import json
from aoristic import date_functions as dt_func
from aoristic import read_csv as rc



def aoristic_method(events, t_map, x, y):
    """
    Start aoristic analysis on events
    """
    # Denn funktion borde nog bli två så man kan skicka in färdig processerad data från annat håll.

    measure_unit, create_dict_func = get_measure_unit(x, y)

    for event_data in events:
    # event_data = events[3]
        event = create_dict_func(event_data)
        fill_map(t_map, event, x, y, measure_unit)



def get_measure_unit(x, y):
    """
    Check which unit and create functions should be used for aoristic method
    """
    measure_unit = x["unit"] if x["order"] < y["order"] else y["unit"] # Find out which unit is used to measure, days or hours
    if measure_unit == "Days":
        create_func = dt_func.create_days_event
    elif measure_unit == "Hours":
        create_func = dt_func.create_hours_event

    return measure_unit, create_func



def get_nr_of_timeslots(event, unit):
    """
    Return how many units duration span.
    """
    res = 0
    if unit == "Hours":
        res = dt_func.get_nr_hours(event["duration"])
    elif unit == "Months":
        res = dt_func.get_nr_months(event["start"], event["end"])
    elif unit =="Days":
        res = dt_func.get_nr_days(event["start"], event["end"], event["duration"])

    return float(res)



def calc_aoristic_value(event, unit):
    """
    Calculate the incremental value for each time slot
    """
    time_span = get_nr_of_timeslots(event, unit)
    return  round(1 / time_span, 3)



def fill_map(t_map, event, xu, yu, unit):
    """
    Add incr to t_map for each slot event spans
    """
    incr = calc_aoristic_value(event, unit)
    start = event["start"]
    end = event["end"]

    while start < end:
        x, y = get_xy(start, xu, yu)
        value = round(t_map[y][x] + incr, 3)
        t_map[y][x] = value
        start += dt_func.create_timedelta(unit)



def get_xy(date, x, y):
    """
    return x and y indexes
    """
    xy = get_unit_value(date, x["unit"]), get_unit_value(date, y["unit"])
    return xy



def get_unit_value(date, unit):
    """
    Return unit
    """
    if unit == "Hours":
        return date.hour
    elif unit == "Months":
        return date.month - 1
    elif unit == "Days":
        return date.weekday()



def main():
    """
    Starts program
    """
    # events = json.load(open("events.json", "r"))
    events = rc.csv_to_dict("datafiles/temp.data.2014.csv")
    units = json.load(open("aoristic/units.json", "r"))

    # weekday X time of day [7*24]
    unit_x = units["hours"]
    unit_y = units["days"]

    # weekday X month [7*12]
    # unit_x = units["days"]
    # unit_y = units["months"]

    t_map = [[0 for y in range(unit_y["size"])] for x in range(unit_x["size"])]

    aoristic_method(events, t_map, unit_x, unit_y)

    # for i, row in enumerate(t_map):
        # print(i, row)

    return t_map



if __name__ == "__main__":
    main()
