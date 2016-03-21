#!/usr/bin/python

from os import getcwd,chdir,path
import sys

def change_current_directory(newpath):

    #get the current working directory
    os_cwd = getcwd()
    print("Participant Experiment data to process : ", newpath)
    change_dir = path.join(os_cwd, newpath)
    chdir(change_dir)
    #testing if the directory change worked
    print("Changing the current directory to Participant directory: ", getcwd())