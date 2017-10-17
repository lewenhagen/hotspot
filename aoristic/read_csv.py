#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Read data from csv files.
"""
import csv


def csv_to_dict(file_name="temp.csv", deli=";"):
    """
    Read csv with header, create list with dicts. key is header value
    """
    reader = csv.reader(open(file_name, "r"), delimiter=deli)
    headers = reader.__next__()
    result = []
    for row in reader:
        dic = {}
        for index, value in enumerate(row):
            dic[headers[index]] = value
        result.append(dic)

    return result

def main():
    """
    Test reading from file.
    """
    for row in csv_to_dict():
        print(row)


if __name__ == "__main__":
    main()
