import sys
import csv
from os import system
from csv_data_parser import read_calib_file, get_stat_means_per_task

#Check if the calibration and experiment files need to be generated for consumption
# 1 means we need to generate c&e files
# 0 means we don't need to generate c&e files
generate_data = sys.argv[1]

#this will only be fired once to create the necessary files and firebase structure
#to record output
if generate_data == 1:
    for x in range(1,2):
        myDir = "p" + str(x)
        # creating the calib data file
        os.system("python csv_data_parser.py " + myDir)
        os.system("python experiment_data_creator.py " + myDir)
        # print("python csv_data_parser.py " + myDir)
        # print("python experiment_data_creator.py " + myDir)
        pass

# if we are here the c&e files have been created
# we now read through the task_key and provide parameters to the parser to generate means
try:
    with open("task_key.csv") as task_key:
        task_key_reader = csv.DictReader(task_key)
        for row in task_key_reader:
            # os.system("python csv_data_parser.py " + row["Participant"].lower() +" "+ row["Start_Time"]+" "+ row["End_Time"]+" "+row["E_Pos"])
            if "L" not in row["E_Pos"]:
                output_means = get_stat_means_per_task(row["Participant"].lower(), row["Start_Time"], row["End_Time"], 0, read_calib_file(row["Participant"].lower()), row["Task"])
            else:
                output_means = get_stat_means_per_task(row["Participant"].lower(), row["Start_Time"], row["End_Time"], 1, read_calib_file(row["Participant"].lower()), row["Task"])
            print(output_means)
        pass
except IOError as e:
    raise e