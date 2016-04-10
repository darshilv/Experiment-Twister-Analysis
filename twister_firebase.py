from firebase import firebase
from data_util import Experiment_Condition, Stat_Definitions, Stat_Means, Participant_Stat
firebase = firebase.FirebaseApplication('https://twister-analysis.firebaseio.com/', None)


def create_participant_node(participantName):
    result = firebase.post("/"+participantName,{"exploratory" : ["x"], "lobster" : ["y"]})
    pass

create_participant_node("p1")
# participantObj = Participant_Stat([],"p1")
# participantObj.addTaskMeans(Stat_Means(10.00, 0.7, 0.8, "N").__dict__)
# participantObj.addTaskMeans(Stat_Means(10.00, 0.7, 0.8, "TS").__dict__)
# participantObj.addTaskMeans(Stat_Means(10.00, 0.7, 0.8, "HE").__dict__)
# participantObj.addTaskMeans(Stat_Means(10.00, 0.7, 0.8, "S").__dict__)
# participantObj.addTaskMeans(Stat_Means(10.00, 0.7, 0.8, "L").__dict__)


# result = firebase.post('/participant_example', participantObj.__dict__)
# print(result)