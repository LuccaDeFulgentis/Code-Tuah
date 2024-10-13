from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import random

app = Flask(__name__)
app.secret_key = 'random_secret_key'  # Required for session management

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

# Generate a list of exercises based on user's preferences
def generate_exercises(equipment, difficulty, muscles):
    visited = {}
    for _ in range(1000):
        equipmentRandom = random.choice(equipment)
        experienceRandom = random.randint(1, difficulty)
        # Randomly select one of the muscle groups
        selected_muscle = random.choice(muscles)
        prediction = model.predict([[equipmentRandom, selected_muscle, experienceRandom]])
        if prediction[0] not in visited:
            visited[prediction[0]] = 1
        else:
            visited[prediction[0]] += 1

    # Sort exercises by frequency (most frequent first)
    sorted_exercises = sorted(visited.items(), key=lambda item: item[1], reverse=True)
    # Instead of returning only the exercise name, return full rows of data
    full_exercise_data = [df[df['Exercise Name'] == exercise[0]].to_dict(orient='records')[0] for exercise in sorted_exercises]
    return full_exercise_data



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    equipment = list(map(int, request.form.getlist('equipment')))
    difficulty = int(request.form['difficulty'])
    # Collect selected muscle groups as a list of integers
    muscles = list(map(int, request.form.getlist('muscle')))
    days_per_week = int(request.form['days_per_week'])  # Get the days per week from the form

    session['equipment'] = equipment
    session['difficulty'] = difficulty
    session['muscle'] = muscles  # Store list of muscles in session
    session['days_per_week'] = days_per_week  # Store in session
    session['selected_exercises'] = []  # Reset selected exercises
    session['rejected_exercises'] = []  # Track rejected exercises
    session['exercise_list'] = generate_exercises(equipment, difficulty, muscles)  # Pass muscles as a list

    return redirect(url_for('exercise_page'))

@app.route('/exercise_page', methods=['GET', 'POST'])
@app.route('/exercise_page', methods=['GET', 'POST'])
def exercise_page():
    selected_exercises = session.get('selected_exercises', [])
    rejected_exercises = session.get('rejected_exercises', [])
    exercise_list = session.get('exercise_list', [])

    # If user has already selected 3 exercises, redirect to the summary
    if len(selected_exercises) >= 3:
        return redirect(url_for('summary'))

    if request.method == 'POST':
        action = request.form['action']
        current_exercise = exercise_list[0]  # Get the current top exercise

        if action == 'accept':
            selected_exercises.append(current_exercise)  # Add accepted exercise
        elif action == 'reject':
            rejected_exercises.append(current_exercise)  # Add rejected exercise
        
        # Remove the current exercise from the exercise list
        exercise_list = [e for e in exercise_list if e['Exercise Name'] != current_exercise['Exercise Name']]

        session['selected_exercises'] = selected_exercises
        session['rejected_exercises'] = rejected_exercises
        session['exercise_list'] = exercise_list

        if len(selected_exercises) >= 3:
            return redirect(url_for('summary'))

    # Get the first exercise that hasn't been rejected and isn't already selected
    if exercise_list:
        current_exercise = exercise_list[0]
    else:
        current_exercise = None  # No more exercises left

    return render_template('exercise_page.html', exercise=current_exercise)

@app.route('/summary')
def summary():
    selected_exercises = session.get('selected_exercises', [])
    return render_template('summary.html', exercises=selected_exercises)

if __name__ == '__main__':
    app.run(debug=True)
