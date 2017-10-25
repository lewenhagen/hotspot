#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Parse data from csv and log files.
"""
import csv
import re
from aoristic import date_functions as dt_func
from aoristic import aoristic


def log_to_dict(hotspot, t_map):
    """
    Reads log file and creates a dict
    """
    counter = 0
    pattern = re.compile(r"\[([\w]{1,2}).*([A-z]{3}).*([\w]{4}):([\w]{2}:[\w]{2}:[\w]{2})\s")

    with open("datafiles/" + hotspot["datafilename"], "r") as filehandler:
        lines = filehandler.readlines()
    for line in lines:
        match = pattern.search(line)
        new_date = dt_func.create_datetime_tupl(match.groups())
        
        aoristic.add_incr(t_map, new_date, hotspot["xticks"], hotspot["yticks"])

        # print("Working on line:", counter, "/", len(lines))
        counter += 1



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
    for row in csv_to_dict_no_filter():
        print(row)


if __name__ == "__main__":
    main()
