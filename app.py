from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import random

app = Flask(__name__)

# Load dataset
df = pd.read_csv('gym_exercise_dataset_cleaned.csv', skipinitialspace=True)

# Clean and prepare the dataset
df['Equipment'] = df['Equipment'].map({'Barbell': 1, 'Cable': 2, 'Dumbbell': 3, 'Lever (plate loaded)': 4, 'Sled': 5, 'Smith': 6, 'Body Weight': 7, 'Suspension': 8, 'Assisted': 9, 'Weighted': 10, 'Bands': 11, 'Plyometrics': 12, 'Chest-Dip Machine': 13, 'Cable Flies': 14})
df['Main_muscle'] = df['Main_muscle'].map({'Shoulder': 1, 'Triceps': 2, 'Biceps': 3, 'Forearm': 4, 'Back': 5, 'Chest': 6, 'Hips': 7, 'Thighs': 8, 'Calves': 9})
df['Difficulty (1-5)'] = df['Difficulty (1-5)'].astype(int)

# Separate feature and target columns
x = df.drop(columns=['Exercise Name', 'Mechanics', 'Preparation', 'Execution', 'Secondary Muscles'])
y = df['Exercise Name']

# Fit the model
model = DecisionTreeClassifier()
model.fit(x, y)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_exercise', methods=['POST'])
def get_exercise():
    equipment = list(map(int, request.form.getlist('equipment')))
    difficulty = int(request.form['difficulty'])
    muscle = int(request.form['muscle'])

    visited = {}
    for _ in range(1000):
        equipmentRandom = random.choice(equipment)
        experienceRandom = random.randint(1, difficulty)
        prediction = model.predict([[equipmentRandom, muscle, experienceRandom]])
        if prediction[0] not in visited:
            visited[prediction[0]] = 1
        else:
            visited[prediction[0]] += 1

    recommended_exercise = max(visited, key=visited.get)
    return jsonify({'exercise': recommended_exercise})

if __name__ == '__main__':
    app.run(debug=True)
