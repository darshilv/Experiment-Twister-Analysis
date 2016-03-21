#!/usr/bin/python

import sys
from os import listdir,getcwd
# import re
import csv
import data_util

#initializing variables
valid_idx = 0
data_header = ""
SCREEN_WIDTH = 0
SCREEN_HEIGHT = 0

#change it to the one provided as the file argument
arg_one = str(sys.argv[1])
START_TIME = float(sys.argv[2])
STOP_TIME = float(sys.argv[3])
data_util.change_current_directory(arg_one)

# we need to first read calibration data to initialize screen variables
calib_filename = arg_one + "_calib.csv"
try:
    with open(calib_filename) as calib_file:
        calib_csv_reader = csv.DictReader(calib_file)
        # calib_header = calib_csv_reader.fieldnames
        # print(calib_header)
        for row in calib_csv_reader:
            SCREEN_HEIGHT = row['SCREEN_HEIGHT']
            SCREEN_WIDTH = row['SCREEN_WIDTH']
            print(SCREEN_WIDTH + "::" + SCREEN_HEIGHT)
    pass
except IOError as e:
    print("Error reading calibration data")
    raise e

print("=====================================SCREEN PARAMETERS SET=====================================")

# reading the data file
file_list = listdir(getcwd())
for filename in file_list:
    if filename.endswith(".csv") and "_subject_data" in filename:
        try:
            with open(filename) as data_file:
                csv_reader = csv.DictReader(data_file)
                data_header = csv_reader.fieldnames
                print(data_header)
                for row in csv_reader:
                    # print(row['BPOGV'])
                    if int(row['BPOGV']) == 1:
                        calc_position_x = float(row['BPOGX']) * float(SCREEN_WIDTH)
                        calc_position_y = float(row['BPOGY']) * float(SCREEN_HEIGHT)
                        # print(str(calc_position_x) + "::" + str(calc_position_y))
                        # print(row['BPOGX'] + "::" + row['BPOGY'])
                        valid_idx = valid_idx + 1
                    else:
                        pass
        except IOError as e:
            print("Error reading data file")
            raise e
        print("Total Valid data points : " + str(valid_idx))
        
