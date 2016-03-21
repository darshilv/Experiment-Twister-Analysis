#!/usr/bin/python

import sys
from os import getcwd, listdir
import data_util
# import re
# import csv

#initialize the file suffix
calib_file_suffix = "_calib.csv"

#change it to the one provided as the file argument
arg_one = str(sys.argv[1])
data_util.change_current_directory(arg_one)

#creating a function to create and write calibration data for each directory
def create_calib_data(cfile, file_data):
    try:
        with open(cfile, 'w') as calib_file:
            calib_file.write(file_data)
    except IOError as e:
        print("There was some problem writing to the file")
        raise e
    finally:
        print("Calibration file(s) have been created")    


#we need to find all the files that have calibration data
file_list = listdir(getcwd())
for file_item in file_list:
    if file_item.endswith(".csv") and "recording" in file_item:
        print(file_item)
        try:
            with open(file_item) as data_file:
                writeable_info = data_file.readline() + data_file.readline()
                file_to_create = arg_one + calib_file_suffix
                create_calib_data(file_to_create, writeable_info)
        except IOError as e:
            raise e
    else:
        print("discarding file: ", file_item)
