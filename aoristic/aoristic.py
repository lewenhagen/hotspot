#!/usr/bin/env python
"""
Test aoristic method
"""
import json
from functools import partial
from aoristic.units import Unit
from aoristic.units import Hour

# from units import Unit
# from units import Hour
# import parse
# import time


def aoristic_method(events, t_map, x, y):
    """
    Start aoristic analysis on events
    """
    Unit_class = setup_class(x, y)

    for event_data in events:
        event = Unit_class(event_data)

        fill_map(t_map, event)



def setup_class(x, y):
    """
    Create partial for class creation
    """
    unit_class = get_measure_unit(x, y)
    get_x = get_get_unit(x["unit"])
    get_y = get_get_unit(y["unit"])

    unit_class = partial(Hour, get_x=get_x, get_y=get_y)

    return unit_class



def get_get_unit(unit):
    """
    Return the static class method for get_(unit)
    """
    if unit == "Hours":
        return Unit.get_hour
    elif unit == "Days":
        return Unit.get_day
    elif unit == "Months":
        return Unit.get_month
    elif unit == "Weeks":
        return Unit.get_week

    raise ValueError



def get_measure_unit(x, y):
    """
    Check which unit is smallest and what Class should be used for the events
    """
    smallest = x["unit"] if x["order"] < y["order"] else y["unit"] # Find out which unit is used to measure, days or hours
    if smallest == "Days":
        unit_class = Unit
    elif smallest == "Hours":
        unit_class = Hour

    return unit_class



def fill_map(t_map, event):
    """
    Fills map and use add_incr to t_map for each slot event spans
    """
    a_value = event.calc_aoristic_value()

    for e in event:
        x, y = event.get_x(e), event.get_y(e)
        add_incr(t_map, x, y, a_value)



def add_incr(t_map, x, y, incr=1):
    """
    Add incr to t_map for current units(x,y)
    """
    value = round(t_map[y][x] + incr, 3)
    t_map[y][x] = value



def main():
    """
    Starts program
    """
    # events = json.load(open("events.json", "r"))
    events = parse.csv_to_dict_no_filter("../datafiles/crime-2014.csv")
    units = json.load(open("../units.json", "r"))

    start_time = time.time()

    # weekday X time of day [7*24]
    # unit_x = units["hours"]
    # unit_y = units["days"]

    # weekday X month [7*12]
    # unit_x = units["days"]
    # unit_y = units["months"]

    # weekday X weeks [7*52]
    unit_x = units["days"]
    unit_y = units["weeks"]

    t_map = [[0 for x in range(unit_x["size"])] for y in range(unit_y["size"])]
    # print(json.dumps(t_map, indent=4))
    aoristic_method(events, t_map, unit_x, unit_y)
    print("--- %s seconds ---" % (time.time() - start_time))
    for i, row in enumerate(t_map):
        print(i, row)

    # print(t_map)



if __name__ == "__main__":
    main()
