#!/usr/bin/env python3
import json
import sys
import numpy
import itertools
import csv
sys.path.append('..')
from aoristic import aoristic
from aoristic import parse as parser
class ProcessEvents:

    def __init__(self, units):
        self.y = units["hours"]
        self.x = units["days"]
        self.combined_list = list()

    def process_data(self):
        for y in range(1, 5):
            for m in range(1, 13):
                search = "201{}-{}".format(y,self.zero_pad(m))
                # number = "201{}{}".format(y,self.zero_pad(m))
                filtered_aoristic = self.filter_to_list(search)
                one_month_list = self.aoristic_to_tuples(search, filtered_aoristic)
                # one_month_list = self.aoristic_to_tuples(number, filtered_aoristic)

                self.combined_list = list(itertools.chain(self.combined_list, one_month_list))
        self.save_to_csv()

    def save_to_csv(self):
        with open('data.csv','w',  newline='') as out:
            csv_out=csv.writer(out)
            csv_out.writerow(['day','crimes'])
            for row in self.combined_list:
                csv_out.writerow(row)

    def aoristic_to_tuples(self, date, aoristic):
        nr_events_with_date = [(self.create_date(date, i), data) for i, data  in enumerate(aoristic)]
        return nr_events_with_date

    def create_date(self, date, index):
        INRC_DAY = 1
        hour = index // self.x["size"]
        day = index % self.x["size"]  + INRC_DAY
        date += "-{day} {hour}:00".format(day=self.zero_pad(day), hour=self.zero_pad(hour))
        # date += "{day}.{hour}".format(day=self.zero_pad(day), hour=self.zero_pad(hour))
        return date

    def filter_to_list(self, search):
        raw_data = parser.csv_to_dict(search, "datestart", "total_v2.csv")
        aoristic_data = [[0 for x in range(self.x["size"])] for y in range(self.y["size"])] # x y, init matrix
        aoristic.aoristic_method(raw_data, aoristic_data, self.x, self.y)
        arr = numpy.matrix(aoristic_data).flat
        return arr

    @staticmethod
    def zero_pad(number):
        return  number if number > 9 else "0" + str(number)

if __name__ == "__main__":
    units = json.load(open("../units.json", "r"))
    p = ProcessEvents(units)
    p.process_data()
