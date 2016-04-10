#!/usr/bin/python

import sys
from os import listdir,getcwd
# import re
import csv
from data_util import change_current_directory, Experiment_Condition, Stat_Definitions, Stat_Means

# we need to first read calibration data and return values for our screen width variable
def read_calib_file(participantId):
    change_current_directory(participantId)
    calib_filename = participantId + "_calib.csv"
    screen_width = 0
    try:
        with open(calib_filename) as calib_file:
            calib_csv_reader = csv.DictReader(calib_file)
            # calib_header = calib_csv_reader.fieldnames
            # print(calib_header)
            for row in calib_csv_reader:
                # SCREEN_HEIGHT = row['SCREEN_HEIGHT']
                screen_width = row['SCREEN_WIDTH']
                # print(SCREEN_WIDTH + "::" + SCREEN_HEIGHT)
    except IOError as e:
        print("Error reading calibration data")
        raise e
    return screen_width
'''
we need to parse the experiment data based on  
    participant Id,
    start time, 
    end time,
    location of the search results v/s experiment results
    screen_width,
    task_type
the return value from this function will be an object 
'''
def get_stat_means_per_task(participantId, start_time, end_time, search_pos, screen_width, task_type):
    #initializing variables
    valid_idx = 0
    
    #creating arrays to store relevant data as objects
    eCondition = []
    controlCondition = []

    #creating stat calculation object
    eStatDefinition = Stat_Definitions()
    cStatDefinition = Stat_Definitions()
    # reading the data file
    if participantId not in str(getcwd()):
        change_current_directory(participantId)
    
    file_list = listdir(getcwd())
    for filename in file_list:
        if filename.endswith(".csv") and "_subject_data" in filename:
            try:
                with open(filename) as data_file:
                    csv_reader = csv.DictReader(data_file)
                    data_header = csv_reader.fieldnames
                    # print(data_header)
                    for row in csv_reader:
                        '''
                        considering only valid data points based on
                        Best Point Of Gaze Valid Flag (BPOGV)
                        Fixation Point Of Gaze Valid Flag (FPOGV)
                        '''
                        # print(row['BPOGV'])
                        if int(row['BPOGV']) == 1 and int(row['FPOGV']) == 1 and float(row["TIME"]) >= start_time and float(row["TIME"]) <= end_time:
                            calc_position_x = float(row['BPOGX']) * int(screen_width)
                            # calc_position_y = float(row['BPOGY']) * float(SCREEN_HEIGHT)
                            # if the fixation is valid store the fixation duration
                            fixation_duration = float(row['FPOGD'])
                            pupil_diam_left = float(row['LPUPILD'])
                            pupil_diam_right = float(row['RPUPILD'])
                            # print(str(calc_position_x) + "::" + str(calc_position_y) + "::" + str(calc_duration))
                            # print(row['BPOGX'] + "::" + row['BPOGY'] + "::" + row["FPOGD"] + "::" + row["FPOGV"])

                            # print("============" + row['TIME'] + "==========")
                            # print(str(calc_position_x) + "::" + str(calc_position_y))
                            if calc_position_x >= int(screen_width) / 2:
                                eCondition.append(Experiment_Condition(calc_position_x,0,fixation_duration, pupil_diam_left, pupil_diam_right))
                                eStatDefinition.addDuration(fixation_duration)
                                eStatDefinition.addLeftDiameter(pupil_diam_left)
                                eStatDefinition.addRightDiameter(pupil_diam_right)
                            else:
                                controlCondition.append(Experiment_Condition(calc_position_x,0, fixation_duration, pupil_diam_left, pupil_diam_right))
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
    # depending on the position of the results the experimental and control condition need to be swapped
    return Stat_Means(eStatDefinition.calc_mean_duration(len(eCondition)), eStatDefinition.calc_mean_left_diameter(len(eCondition)), eStatDefinition.calc_mean_right_diameter(len(eCondition)), cStatDefinition.calc_mean_duration(len(controlCondition)), cStatDefinition.calc_mean_left_diameter(len(controlCondition)), cStatDefinition.calc_mean_right_diameter(len(controlCondition)), task_type)
# print (read_calib_file("p1"))
# read_calib_file("p1")
print("=====================================SCREEN PARAMETERS SET=====================================")
output_means = get_stat_means_per_task("p1", 32, 51, 0, read_calib_file("p1"), "N")
print(output_means.__dict__)