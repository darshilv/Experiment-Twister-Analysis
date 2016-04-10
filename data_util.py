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
    def __init__(self, duration=0.0, dleft=0.0, dright=0.0, taskType=""):
        self.duration = duration
        self.dleft = dleft
        self.dright = dright
        self.taskType = taskType
        pass

    def to_json(self):
        return "{u'taskType' : %r}" % self.taskType

    def addDuration(self,dvalue):
        self.duration = self.duration + dvalue

    def addLeftDiameter(self,dvalue):
        self.dleft = self.dleft + dvalue

    def addRightDiameter(self,dvalue):
        self.dright = self.dright + dvalue

    def calc_mean_duration(self,total_observations):
        mean_duration = self.duration/total_observations
        print("Mean of gaze duration : " , mean_duration)
        return mean_duration

    def calc_mean_left_diameter(self, total_observations):
        mean_left_diameter = self.dleft/total_observations
        print("Mean of Left Diameter : " , mean_left_diameter)
        return mean_left_diameter

    def calc_mean_right_diameter(self, total_observations):
        mean_right_diameter = self.dright/total_observations
        print("Mean of Right Diameter : " , mean_right_diameter)
        return mean_right_diameter

class Participant_Stat(object):
    def __init__(self, task_means=[], participant=""):
        self.participant = participant
        self.task_means = task_means

    def addTaskMeans(self, taskMean):
        self.task_means.append(taskMean)


class Stat_Means(object):
    def __init__(self, mDuration=0.0, mLeft=0.0, mRight=0.0, tType=""):
        self.mDuration = mDuration
        self.mLeft = mLeft
        self.mRight = mRight
        self.tType = tType
        pass
