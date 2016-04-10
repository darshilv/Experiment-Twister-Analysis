import sys
import csv
from os import system


#first we check if that the data files have been created appropriately
for x in range(1,40):
    myDir = "p" + str(x)
    # creating the calib data file
    # os.system("python csv_data_parser.py " + myDir)        
    print("python csv_data_parser.py " + myDir)
    print("python experiment_data_creator.py " + myDir)
    pass
