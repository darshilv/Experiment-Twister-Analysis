#!/usr/bin/python

import sys
from os import getcwd, listdir
import data_util
# import re
# import csv

# to list directories
# list_participants = os.listdir(os_cwd)
idx = 0
file_ext = ".csv"
subject_file_suffix = "_subject_data_"


#change it to the one provided as the file argument
arg_one = str(sys.argv[1])
data_util.change_current_directory(arg_one)

#creating a function to create and write data to a file
def create_data_file(dfile, file_data):
    try:
        with open(dfile, 'w') as data_file:
            data_file.write(file_data)
    except IOError as e:
        print("There was some problem writing to the file")
        raise e
    finally:
        print("Data file(s) have been created")    

file_list = listdir(getcwd())
for file_item in file_list:
    if file_item.endswith(".csv") and "recording" in file_item:
        print(file_item)
        idx = idx + 1
        file_to_create = arg_one + subject_file_suffix + str(idx) + file_ext
        print("File to be created as output :", file_to_create)
        try:
            with open(file_item) as data_file:
                #skipping the first two lines
                data_file.readline()
                data_file.readline()
                writeable_info = data_file.read()
                create_data_file(file_to_create, writeable_info)
        except IOError as e:
            raise e
    else:
        print("discarding file: ", file_item)

# for file in list_participants:
#     if os.path.isdir(file):
#         # print os.listdir(file)
#         parse_csv_data(os.path.join(os_cwd,file), file)
#     else:
#         print "not a directory", file

# print("Hello, Python!")