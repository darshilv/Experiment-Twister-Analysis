#!/usr/bin/python

import sys
from os import listdir,getcwd
# import re
import csv
from data_util import change_current_directory, Experiment_Condition, Stat_Definitions


#initializing variables
valid_idx = 0
data_header = ""
SCREEN_WIDTH = 0
SCREEN_HEIGHT = 0

#change it to the one provided as the file argument
arg_one = str(sys.argv[1])
#START_TIME = float(sys.argv[2])
#STOP_TIME = float(sys.argv[3])
change_current_directory(arg_one)

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

#creating arrays to store relevant data as objects
eCondition = []
controlCondition = []

#creating stat calculation object
eStatDefinition = Stat_Definitions()
cStatDefinition = Stat_Definitions()
# reading the data file
file_list = listdir(getcwd())
for filename in file_list:
    if filename.endswith(".csv") and "_subject_data" in filename:
        try:
            with open(filename) as data_file:
                csv_reader = csv.DictReader(data_file)
                data_header = csv_reader.fieldnames
                # print(data_header)
                for row in csv_reader:
                    # print(row['BPOGV'])
                    if int(row['BPOGV']) == 1 and int(row['FPOGV']) == 1:
                        calc_position_x = float(row['BPOGX']) * float(SCREEN_WIDTH)
                        calc_position_y = float(row['BPOGY']) * float(SCREEN_HEIGHT)
                        # if the fixation is valid store the fixation duration
                        fixation_duration = float(row['FPOGD'])
                        pupil_diam_left = float(row['LPUPILD'])
                        pupil_diam_right = float(row['RPUPILD'])
                        # print(str(calc_position_x) + "::" + str(calc_position_y) + "::" + str(calc_duration))
                        # print(row['BPOGX'] + "::" + row['BPOGY'] + "::" + row["FPOGD"] + "::" + row["FPOGV"])

                        # print("============" + row['TIME'] + "==========")
                        # print(str(calc_position_x) + "::" + str(calc_position_y))
                        if calc_position_x >= 700:
                            eCondition.append(Experiment_Condition(calc_position_x,calc_position_y, fixation_duration, pupil_diam_left, pupil_diam_right))
                            eStatDefinition.addDuration(fixation_duration)
                            eStatDefinition.addLeftDiameter(pupil_diam_left)
                            eStatDefinition.addRightDiameter(pupil_diam_right)
                        else:
                            controlCondition.append(Experiment_Condition(calc_position_x,calc_position_y, fixation_duration, pupil_diam_left, pupil_diam_right))
                            cStatDefinition.addDuration(fixation_duration)
                            cStatDefinition.addLeftDiameter(pupil_diam_left)
                            cStatDefinition.addRightDiameter(pupil_diam_right)
                        # print(row['LPUPILD'] + "::" + row['LPUPILV'] + "||" + row['RPUPILD'] + "::" + row['RPUPILV'] + "--" + row['FPOGD'])
                        valid_idx = valid_idx + 1
                    else:
                        pass
        except IOError as e:
            print("Error reading data file")
            raise e
        print("Total Valid data points : " + str(valid_idx))
        print("Total experiment condition : " + str(len(eCondition)))
        print("Total control condition : " + str(len(controlCondition)))
        print("===================Means================")
        eStatDefinition.calc_mean(len(eCondition))
        cStatDefinition.calc_mean(len(controlCondition))
