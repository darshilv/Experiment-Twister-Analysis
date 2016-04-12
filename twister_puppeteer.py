import sys
import csv
from os import system, getcwd, chdir
from csv_data_parser import read_calib_file, get_stat_means_per_task
from data_util import change_current_directory, Experiment_Condition, Stat_Definitions, Stat_Means

#storing the home directory
home_directory = getcwd()

#Check if the calibration and experiment files need to be generated for consumption
# 1 means we need to generate c&e files
# 0 means we don't need to generate c&e files
generate_data = sys.argv[1]
print(generate_data)

#initializing the output list
output_list = []

print("Creating the calibration files")
#this will need to be fired once to create the necessary files and firebase structure
#to record output
if int(generate_data) == 1:
    for x in range(1,40):
        print("Creating calibration files : " + str(x))
        myDir = "p" + str(x)
        # creating the calib data file
        system("python callib_data_creator.py " + myDir)
        system("python experiment_data_creator.py " + myDir)
        # print("python csv_data_parser.py " + myDir)
        # print("python experiment_data_creator.py " + myDir)
else:
    print("Calibration files dont need to be created \n")
    pass
# if we are here the c&e files have been created
# we now read through the task_key and provide parameters to the parser to generate means
print("Crunching numbers...\n\n")
try:
    #changing directory to home to be able to read the task key once read the other function calls can change the directory
    chdir(home_directory)
    with open("task_key.csv") as task_key:
        task_key_reader = csv.DictReader(task_key)
        for row in task_key_reader:
            # os.system("python csv_data_parser.py " + row["Participant"].lower() +" "+ row["Start_Time"]+" "+ row["End_Time"]+" "+row["E_Pos"])
            participantId = row["Participant"].lower()
            
            #we are going to change the working directories outside the function calls of the parsers
            if participantId not in str(getcwd()):
                chdir(home_directory)
                change_current_directory(participantId)

            if "L" not in row["E_Pos"]:
                output_list.append(get_stat_means_per_task(participantId, row["Start_Time"], row["End_Time"], 0, read_calib_file(participantId), row["Task"]))
            else:
                output_list.append(get_stat_means_per_task(participantId, row["Start_Time"], row["End_Time"], 1, read_calib_file(participantId), row["Task"]))
            # print(output_means.__dict__)
        pass
except IOError as e:
    raise e

try:
    chdir(home_directory)
    with open("twister_output.csv", "a") as output_file:
        key_fieldnames = ["mDuration_x","mLeft_x","mRight_x","mDurationCount_x","mLeftCount_x","mRightCount_x","mDuration_c","mLeft_c","mRight_c","mDurationCount_c","mLeftCount_c","mRightCount_c","tType","participantId", "total_observations"]
        writer = csv.DictWriter(output_file, fieldnames=key_fieldnames)
        writer.writeheader()
        for row in output_list:
            # print(row.__dict__)
            writer.writerow(row.__dict__)
except IOError as e:
    raise e
print("Output file created!")