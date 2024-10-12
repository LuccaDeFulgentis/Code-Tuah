from flask import Flask, render_template, request, jsonify, send_file
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import io

app = Flask(__name__)

# Muscle group mapping 
muscle_group_mapping = {
    "chest": 0, "shoulders": 1, "triceps": 2, "biceps": 3, "forearm": 4,
    "thighs": 5, "hips": 6, "calves": 7, "back": 8 
}

@app.route('/')
def index():
    return render_template('heat_map.html')

@app.route('/generate_heatmap', methods=['POST'])
def generate_heatmap():
    workout_schedule = request.get_json() 

    activation_data = np.zeros((1, len(muscle_group_mapping)))  
    
    for day, exercises in workout_schedule.items():
        for exercise in exercises:
            if exercise["checked"]: 
                muscle_index = muscle_group_mapping[exercise["main_muscle"].lower()]
                activation_data[0, muscle_index] += 1 

    plt.figure(figsize=(8, 6))
    sns.heatmap(activation_data, annot=True, cmap="YlGnBu", 
                xticklabels=muscle_group_mapping.keys(), yticklabels=["Week"])
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    return send_file(buffer, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
