from firebase import firebase
from data_util import Experiment_Condition, Stat_Definitions
firebase = firebase.FirebaseApplication('https://twister-analysis.firebaseio.com/', None)

cObj = Stat_Definitions()
cObj.addDuration(10.00)
cObj.addLeftDiameter(0.7)
cObj.addRightDiameter(0.8)
cObj.addTaskType("N")
result = firebase.post('/participant_example', cObj)
print result