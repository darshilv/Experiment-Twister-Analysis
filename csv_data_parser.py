#!/usr/bin/python

import sys
from os import listdir,getcwd
# import re
import csv
from data_util import change_current_directory, Experiment_Condition, Stat_Definitions, Stat_Means

# we need to first read calibration data and return values for our screen width variable
def read_calib_file(participantId):
    # if participantId not in getcwd():
    #     change_current_directory(participantId)

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
    
    #creating stat calculation object
    #initialize experiment + control variables
    fixation = Stat_Definitions()
    pupil_diameter_left = Stat_Definitions()
    pupil_diameter_right = Stat_Definitions()

    # reading the data file
    # print("Current working directory is: " + getcwd())
    
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
                        if int(row['BPOGV']) == 1:
                            calc_position_x = float(row['BPOGX']) * int(screen_width)
                            # we dont need the Y position as the regions of interest are divided horizontally
                            # calc_position_y = float(row['BPOGY']) * float(SCREEN_HEIGHT)
                            
                            if float(row["TIME"]) >= float(start_time) and float(row["TIME"]) <= float(end_time):

                                #identify if the observation is in experiment or control region
                                #if x coordinate value is greater than 700 it is in the experiment region
                                if calc_position_x >= 700:
                                    # if the fixation is valid store the fixation duration
                                    if int(row['FPOGV']) == 1:
                                        fixation.update_sum_experiment(float(row['FPOGD']))
                                        fixation.increment_experiment_counter()
                                    
                                    #if the Left Pupil Diameter is valid we store that
                                    if int(row[LPUPILV]) > 0:
                                        pupil_diameter_left.update_sum_experiment(float(row['LPUPILD']))
                                        pupil_diameter_left.increment_experiment_counter()

                                    #if the right pupil diameter is valid we store that
                                    if int(row[RPUPILV]) > 0:
                                        pupil_diameter_right.update_sum_experiment(float(row['RPUPILD']))
                                        pupil_diameter_right.increment_experiment_counter()
                                else:
                                    # if the fixation is valid store the fixation duration
                                    if int(row['FPOGV']) == 1:
                                        fixation.update_sum_control(float(row['FPOGD']))
                                        fixation.increment_control_counter()
                                    
                                    #if the Left Pupil Diameter is valid we store that
                                    if int(row[LPUPILV]) > 0:
                                        pupil_diameter_left.update_sum_control(float(row['LPUPILD']))
                                        pupil_diameter_left.increment_control_counter()

                                    #if the right pupil diameter is valid we store that
                                    if int(row[RPUPILV]) > 0:
                                        pupil_diameter_right.update_sum_control(float(row['RPUPILD']))
                                        pupil_diameter_right.increment_control_counter()

                            #calculate means for all
                            fixation.calc_mean()
                            pupil_diameter_right.calc_mean()
                            pupil_diameter_left.calc_mean()
                            valid_idx = valid_idx + 1
                        else:
                            pass
            except IOError as e:
                print("Error reading data file")
                raise e
    # print("Total Valid data points : " + str(valid_idx))
    # print("Total experiment condition : " + str(len(eCondition)))
    # print("Total control condition : " + str(len(controlCondition)))
    # print("===================Means================")
    # depending on the position of the results the experimental and control condition need to be swapped
    return Stat_Means(fixation.experiment_mean, fixation.total_count_experiment, pupil_diameter_left.experiment_mean, pupil_diameter_right.experiment_mean, fixation.control_mean, pupil_diameter_left.control_mean, pupil_diameter_right.control_mean, task_type, participantId, valid_idx)
# print (read_calib_file("p1"))
# read_calib_file("p1")
# print("=====================================SCREEN PARAMETERS SET=====================================")
# output_means = get_stat_means_per_task("p1", 32, 51, 0, read_calib_file("p1"), "N")
# print(output_means.__dict__)