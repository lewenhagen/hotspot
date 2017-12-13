#!/usr/bin/env python
"""
Test aoristic method
"""
import json
from functools import partial, reduce
# from aoristic.units import Unit
# from aoristic.units import Hour

from units import Unit
from units import Hour
import parse
import time
import operator

from multiprocessing.pool import Pool
from multiprocessing.sharedctypes import RawArray
import multiprocessing
import ctypes
# import numpy as np



# https://stackoverflow.com/questions/1675766/how-to-combine-pool-map-with-array-shared-memory-in-python-multiprocessing
shared_array_base = multiprocessing.Array(ctypes.c_double, 7*24, lock=False)
# shared_array2 = np.ctypeslib.as_array(shared_array_base)
# shared_array = shared_array2.reshape(24, 7)

def aoristic_method(events, x, y):
    """
    Start aoristic analysis on events
    """
    Unit_class = setup_class(x, y)


    multi_method = partial(multi_proc, Unit_class=Unit_class)

    with Pool(multiprocessing.cpu_count()-1) as p:
        p.map(multi_method, events)



def test1(tmp_map, res):
    [list(map(operator.add,res[i], tmp_map[i])) for i in range(len(res))]
    # hej = [print(res[i], tmp_map[i]) for i in range(len(res))]
    # print(hej)
    # exit()
    # return hej

def self_sum(tmp, res):
    for x in range(len(tmp)):
        for y in range(len(tmp[x])):
            res[x][y] = res[x][y] + tmp[x][y]

def multi_proc(event, Unit_class, t_map=shared_array_base):
    eventO = Unit_class(event)

    fill_map(t_map, eventO)



def calc_xy(x, y):
    return (y*7)+x


def setup_class(x, y):
    """
    Create partial for class creation
    """
    unit_class = get_measure_unit(x, y)
    get_x = get_get_unit(x["unit"])
    get_y = get_get_unit(y["unit"])

    unit_class = partial(unit_class, get_x=get_x, get_y=get_y)

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

    x, y = event.get_x(event.start), event.get_y(event.start)
    i = get_i(x, y)

    for _ in range(event.get_duration()):
        add_incr(t_map, i, a_value)
        i = incr_i(i)



def get_i(x,y):
    """
    return list index based on x,y cord. Based on days X hours, where hours in on Y.
    """
    return (y * 7) + x



def incr_i(i):
    """
    Get next list index. Based on days X hours, where hours in on Y.
    """
    tmp = i + 7
    if tmp >= 174: # 7*24+6:
        return 0
    else:
        return tmp % 168 + divmod(tmp, 168)[0] # 7*24



def add_incr(t_map, i, incr=1):
    """
    Add incr to t_map for current units(x,y)
    """
    value = t_map[i] + incr
    t_map[i] = value


# @profile
def main():
    """
    Starts program
    """
    # events = json.load(open("events.json", "r"))
    events = parse.csv_to_dict_no_filter("../datafiles/crime-2014.csv")
    # events = parse.csv_to_dict_no_filter("../datafiles/crime-extended.csv")
    units = json.load(open("../units.json", "r"))


    # weekday X time of day [7*24]
    unit_y = units["hours"]
    unit_x = units["days"]

    # weekday X month [7*12]
    # unit_x = units["days"]
    # unit_y = units["months"]

    # weekday X weeks [7*52]
    # unit_x = units["days"]
    # unit_y = units["weeks"]

    # t_map = [[0 for x in range(unit_x["size"])] for y in range(unit_y["size"])]
    # t_map = [0 for x in range(7*24)]
    # print(json.dumps(t_map, indent=4))
    start_time = time.time()
    aoristic_method(events, unit_x, unit_y)
    print("--- %s seconds ---" % (time.time() - start_time))

    t_map2 = [shared_array_base[i:i+7] for i in range(0, len(shared_array_base), 7)]
    for i, row in enumerate(t_map2):
        print(i, row)



if __name__ == "__main__":
    main()
