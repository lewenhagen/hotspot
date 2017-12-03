#!/usr/bin/env python3
import csv
import random
random.seed("crime-2014")

with open('crime-2014.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)

header = data[0:1][0][0]
data = data[1:]
number = len(data) * 10

ext = [random.choice(data) for _ in range(number)]

with open("crime-extended.csv", 'w') as f:
    f.write(header + "\n")
    f.write("\n".join([y for x in ext for y in x]))
