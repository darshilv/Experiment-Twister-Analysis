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

class Experiment_Condition(object):
    def __init__(self, x_position=0.0, y_position=0.0, gaze_duration=0.0, pupil_diameter_left=0.0, pupil_diameter_right=0.0):
        self.x_position = x_position
        self.y_position = y_position
        self.gaze_duration = gaze_duration
        self.pupil_diameter_left = pupil_diameter_left
        self.pupil_diameter_right = pupil_diameter_right


class Stat_Definitions(object):
    #total count is initialized to 1 simply as the initializing counts as one observation
    def __init__(self, esum=0.0,csum=0.0, etotal_count=0, ctotal_count=0, isExperiment=False):
        self.sum_value_experiment = esum
        self.sum_value_control = csum
        self.total_count_experiment = etotal_count
        self.total_count_control = ctotal_count
        self.experiment_mean = 0
        self.control_mean = 0

    def update_sum_experiment(self,newValue):
        self.sum_value_experiment = self.sum_value_experiment + newValue

    def update_sum_control(self,newValue):
        self.sum_value_control = self.sum_value_control + newValue

    def increment_experiment_counter(self):
        self.total_count_experiment = self.total_count_experiment + 1

    def increment_control_counter(self):
        self.total_count_control = self.total_count_control + 1
    
    def calc_mean(self):
        if self.total_count_experiment > 0:
            self.experiment_mean = self.sum_value_experiment/self.total_count_experiment
        
        if self.total_count_control > 0:
            self.control_mean = self.sum_value_control / self.total_count_control

    
class Participant_Stat(object):
    def __init__(self, search_types=[], participant=""):
        self.participant = participant
        self.search_types = search_types
        

class Search_Type(object):
    def __init__(self, name="", stats=[]):
        self.name = name
        self.stats = stats

    def addStats(self, taskMean):
        self.stats.append(taskMean)

class Stat_Means(object):
    def __init__(self, fixation, pupil_left, pupil_right, tType="", participantId="", total_observations=0):
        self.mDuration_x = fixation.sum_value_experiment
        self.mLeft_x = pupil_left.experiment_mean
        self.mRight_x = pupil_right.experiment_mean
        self.mDurationCount_x = fixation.total_count_experiment
        self.mLeftCount_x = pupil_left.total_count_experiment
        self.mRightCount_x = pupil_right.total_count_experiment
        self.mDuration_c = fixation.sum_value_control
        self.mLeft_c = pupil_left.control_mean
        self.mRight_c = pupil_right.control_mean
        self.mDurationCount_c = fixation.total_count_control
        self.mLeftCount_c = pupil_left.total_count_control
        self.mRightCount_c = pupil_right.total_count_control
        self.tType = tType
        self.participantId = participantId
        self.total_observations = total_observations
        pass
