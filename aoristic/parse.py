#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Parse data from csv and log files.
"""
import csv
import re
from aoristic import aoristic
from aoristic.units import Unit
# import aoristic
# import time


def log_to_dict(hotspot, t_map):
    """
    Reads log file and creates a dict
    """
    # counter = 0
    pattern = re.compile(r"\[([0-9]{2})/([A-z]{3})/(\d{4}):([\d]{2})")
    get_x = aoristic.get_get_unit(hotspot.xticks["unit"])
    get_y = aoristic.get_get_unit(hotspot.yticks["unit"])

    with open("datafiles/" + hotspot.datafile, "r") as filehandler:
        lines = filehandler.readlines()

    for line in lines:
        match = pattern.search(line)
        try:
            new_date = Unit.create_datetime_tupl(match.groups())
        except:
            print("Error regex parsing log line: ", line)
            continue
        aoristic.add_incr(t_map, get_x(new_date), get_y(new_date))
        # counter += 1



def csv_to_dict(filter_v, filter_c, file_name="temp.csv", deli=";"):
    """
    Read csv with header, create list with dicts. key is header value
    """
    reader = csv.reader(open("datafiles/" + file_name, "r"), delimiter=deli)
    headers = reader.__next__()
    try:
        filter_index = headers.index(filter_c)
    except:
        filter_index = -1

    result = []

    if filter_index == -1:
        read_csv_rows(result, reader, headers)
    else:
        if "date" in filter_c or "time" in filter_c:
            read_csv_rows_filter_datetime(result, reader, headers, filter_index, filter_v)
        else:
            read_csv_rows_filter(result, reader, headers, filter_index, filter_v)

    return result



def read_csv_rows(res, reader, headers):
    """
    Read a csv row
    """
    for row in reader:
        res.append(create_row(row, headers))
    return res



def read_csv_rows_filter(res, reader, headers, fi, fv):
    """
    Read a csv row and filter
    """
    for row in reader:
        if row[fi] == fv:
            res.append(create_row(row, headers))
    return res

def read_csv_rows_filter_datetime(res, reader, headers, fi, fv):
    """
    Read a csv row and filter
    """
    for row in reader:
        if fv in row[fi]:
            res.append(create_row(row, headers))
    return res



def create_row(row, headers):
    """
    Iterate over row and create dict
    """
    dic = {}
    for index, value in enumerate(row):
        dic[headers[index]] = value
    return dic



def csv_to_dict_no_filter(file_name="temp.csv", deli=";"):
    """
    Read csv with header, create list with dicts. key is header value
    """
    reader = csv.reader(open(file_name, "r"), delimiter=deli)
    headers = reader.__next__()
    result = []

    read_csv_rows(result, reader, headers)

    return result



def main():
    """
    Test reading from file.
    """
    # for row in csv_to_dict_no_filter():
        # print(row)
    t_map = [[0 for y in range(53)] for x in range(7)]
    hotspot = {}
    hotspot.datafile = "access.log"
    hotspot.yticks = "Days"
    hotspot.xticks = "Weeks"
    start_time = time.time()
    log_to_dict(hotspot, t_map)
    print("--- %s seconds ---" % (time.time() - start_time))
    print(t_map)


if __name__ == "__main__":
    main()
