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
from multiprocessing.pool import Pool
import operator
# import cProfile
# import pstats

def aoristic_method(events, t_map, x, y, ts):
    """
    Start aoristic analysis on events
    """
    Unit_class = setup_class(x, y)
    multi_method = partial(multi_proc, Unit_class=Unit_class)

    matrix = [0 for y in range(7*24)]
    # test = partial(test1, res=matrix)

    with Pool() as p:
        new_m = p.map(multi_method, events)
        # matrix = [list(map(operator.add,tmp_map[i], matrix[i])) for i in p.map(multi_method, events))]
        # print("----------------------------------------------")
        # print(len(new_m))
        # print(tmp_map[0])
    # for arr in tmp_map:
        # map(sum, a)
        # print(reduce(test1, matrix))
        print("--- %s seconds ---" % (time.time() - ts))
        # print(len(list(map(test, new_m))))
        # [test(i) for i in new_m]
        # for i in new_m:
            # self_sum(i, matrix)
        # print(matrix)
        # matrix = [list(map(operator.add,tmp_map[i], matrix[i])) for i in range(len(tmp_map))]

    # print(matrix)
    return matrix

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

def multi_proc(event, Unit_class):
    eventO = Unit_class(event)
    t_map = [0 for y in range(7*24)]
    fill_map(t_map, eventO)
    return t_map


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
    # https://www.toptal.com/python/beginners-guide-to-concurrency-and-parallelism-in-python
    # https://stackoverflow.com/questions/11340299/appending-merging-2d-arrays
    # events = json.load(open("events.json", "r"))
    # events = parse.csv_to_dict_no_filter("../datafiles/crime-2014.csv")
    events = parse.csv_to_dict_no_filter("../datafiles/crime-extended.csv")
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
    t_map = [0 for x in range(7*24)]
    # print(json.dumps(t_map, indent=4))
    start_time = time.time()
    #
    # cProfile.runctx('aoristic_method(events, t_map, unit_x, unit_y)', globals(), locals(), 'myFunction.profile')
    aoristic_method(events, t_map, unit_x, unit_y, start_time)
    print("--- %s seconds ---" % (time.time() - start_time))
    # stats = pstats.Stats('myFunction.profile')
    # stats.strip_dirs().sort_stats('time').print_stats()
    # t_map2 = [t_map[i:i+7] for i in range(0, len(t_map), 7)]
    # for i, row in enumerate(t_map2):
        # print(i, row)
    # print(t_map)



if __name__ == "__main__":
    main()
