import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import math
import random

df = pd.read_csv("gym_exercise_dataset_cleaned.csv", skipinitialspace=True)
pd.set_option('display.max_rows', 700)

#Cleaning & Reassigning Values for Fitting
df['Equipment'] = df['Equipment'].map({'Barbell': 1, 'Cable': 2, 'Dumbbell': 3, 'Lever (plate loaded)': 4, 'Lever (selectorized)\u200b\u200b\u200b\u200b\u200b\u200b\u200b': 4, 'Sled': 5, 'Smith\u200b\u200b\u200b\u200b\u200b\u200b\u200b': 6, 'Body Weight': 7, 'Suspended': 8, 'Lever (selectorized)': 4, 'Smith': 6, 'Assisted': 9, 'Weighted': 10, 'Band-assisted': 11, 'Self-assisted': 9, 'Sled (selectorized)': 5, 'Sled (plate loaded)': 5, 'Assisted (machine)': 9, 'Assisted (partner)': 9, 'Suspension': 8, 'Plyometric': 12, 'Assisted  Chest Dip': 13, 'Cable  Standing Fly': 14, 'Lever (selectorized)  Chest Dip': 13, 'Weighted  Chest Dip': 13, 'Self-assisted\u200b\u200b\u200b\u200b\u200b\u200b\u200b': 9, 'Cable (pull side)': 2, 'Lever': 4})
df['Main_muscle'] = df['Main_muscle'].map({'Shoulder': 1, 'Triceps': 2, 'Biceps': 3, 'Forearm': 4, 'Back': 5, 'Chest': 6, 'Hips': 7, 'Thighs': 8, 'Calves': 9})
df.at[408, 'Secondary Muscles'] = 'Gluteus Maximus'

#Changing Column Datatypes
df['Equipment'] = df['Equipment'].astype(int)
df['Main_muscle'] = df['Main_muscle'].astype(int)
df['Difficulty (1-5)'] = df['Difficulty (1-5)'].astype(int)

#Model Fitting
x = df.drop(columns = ['Exercise Name', 'Mechanics', 'Preparation', 'Execution', 'Secondary Muscles'])
y = df.drop(columns = ['Equipment', 'Difficulty (1-5)', 'Main_muscle'])
model = DecisionTreeClassifier()
model.fit(x,y)

"""
#Sample Prediction
predictions = model.predict([[2, 3, 1]])
tempdict = {}
tempdict[predictions[0][0]] = 1
print(tempdict)
"""



#Equipment User Input & Processing
equipmentHave = []
print("What equipment do you have access to? List of equipment & corresponding numbers: Barbell - 1, Cable - 2, Dumbbell - 3, Levers - 4, Sleds - 5, Smith Machine - 6, Body Weight 7, Suspension - 8, Assisted Machines - 9, Weighted Workouts - 10, Bands - 11, Plyometrics - 12, Chest-Dip Machine 13, Cable Flies - 14")
equipmentInput = str(input("Please input in this format: #, #, # \n"))
temp = ""
for i in range(len(equipmentInput)):
    if equipmentInput[i] != "," and equipmentInput[i] != " ":
        temp += equipmentInput[i]
    else:
        if temp != "":
            equipmentHave.append(int(temp))
            temp = ""
equipmentHave += [int(temp)]

#Difficulty User Input & Processing
experience = int(input("How experienced are you from 1 - 5?: \n"))

#Muscle Group User Input & Processing
muscleGroups = []
print("What muscle group groups would you like to hit? List of muscle groups & corresponding numbers: Shoulder - 1, Triceps - 2, Biceps - 3, Forearm - 4, Back - 5, Chest - 6, Hips - 7, Thighs - 8, Calves - 9")
muscleInput = str(input("Please input in this format: #, #, # \n"))
temp = ""
for i in range(len(muscleInput)):
    if muscleInput[i] != "," and muscleInput[i] != " ":
        temp += muscleInput[i]
    else:
        if temp != "":
            muscleGroups.append(int(temp))
            temp = ""
muscleGroups += [int(temp)]

#Recommendation Loop
choices = []
for i in muscleGroups:
    visited = {}
    for j in range(1000):
        equipmentRandom = random.choice(equipmentHave)
        experienceRandom = random.randint(1, experience)
        predictions = model.predict([[equipmentRandom, i, experienceRandom]]) 
        if predictions[0][0] not in visited:
            visited[predictions[0][0]] = 1
        else:
            visited[predictions[0][0]] += 1
    choices += [visited]

