from flask import Flask, render_template, request, jsonify
import pandas as pd
import random

app = Flask(__name__)

# Load dataset
df = pd.read_csv('gym_exercise_dataset_cleaned.csv')

# Preprocess the dataset (you can add more advanced processing later)
muscle_groups = df['Main_muscle'].unique().tolist()

# Route for the home page (diagnostic questions)
@app.route('/')
def index():
    return render_template('index.html', muscle_groups=muscle_groups)

# Route to process diagnostic form data
@app.route('/diagnostic', methods=['POST'])
def diagnostic():
    # Get diagnostic data from the form
    data = request.form
    preferences = {
        'muscle_groups': data.getlist('muscle_groups'),
        'avoid_muscle_groups': data.getlist('avoid_muscle_groups'),
        'workout_days': data.get('workout_days'),
        'gym_access': data.get('gym_access'),
        'skill_level': data.get('skill_level')
    }
    
    # Filter dataset based on preferences
    filtered_df = df[df['Main_muscle'].isin(preferences['muscle_groups'])]
    filtered_df = filtered_df[~filtered_df['Main_muscle'].isin(preferences['avoid_muscle_groups'])]
    
    # Send the first exercise and muscle groups to swipe page
    first_exercise = filtered_df.sample().to_dict(orient='records')[0]
    
    return render_template('swipe.html', exercise=first_exercise, muscle_groups=preferences['muscle_groups'])

# Route to fetch new exercise after swipe
@app.route('/get_exercise', methods=['POST'])
def get_exercise():
    preferences = request.get_json()
    muscle_groups = preferences['muscle_groups']
    
    # Filter dataset based on preferences again (same as before)
    filtered_df = df[df['Main_muscle'].isin(muscle_groups)]
    
    # Randomly pick an exercise that hasn't been shown yet
    exercise = filtered_df.sample().to_dict(orient='records')[0]
    
    return jsonify(exercise)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
