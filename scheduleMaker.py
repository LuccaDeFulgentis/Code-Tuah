import pandas as pd

def create_workout_schedule(days, muscle_groups, exercises):
    """
    
    Args:
        days (int): Number of workout days (3, 4, 5, or 6).
        muscle_groups (list): List of muscle groups to be trained.
        exercises (list): List of exercise names to be included.
        
        REQUIRES NUMBER OF EXERCISES TO BE AT LEAST NUMBER OF DAYS

    Returns:
        dict: A dictionary representing the workout schedule.
    """

    df = pd.read_csv("gym_exercise_dataset_cleaned.csv")

    # Define muscle group clusters
    clusters = [
        ["Hips", "Calves", "Thighs"], 
        ["Back", "Biceps"], 
        ["Shoulder", "Chest", "Triceps"]
    ]

    # Filter dataframe
    df_filtered = df[df["Exercise Name"].isin(exercises) & df["Main_muscle"].isin(muscle_groups)]

    # Remove duplicate exercises
    df_filtered = df_filtered.drop_duplicates(subset="Exercise Name", keep="first")

    # Create the workout schedule (initial distribution)
    schedule = {day: [] for day in range(1, days + 1)}
    for cluster_index, cluster in enumerate(clusters):
        cluster_exercises = df_filtered[df_filtered["Main_muscle"].isin(cluster)]["Exercise Name"].tolist()
        if not cluster_exercises:
            continue
        for i, exercise in enumerate(cluster_exercises):
            schedule_day = (cluster_index * days // len(clusters) + i % (days // len(clusters)) + 1) % days + 1 
            schedule[schedule_day].append(exercise) 

    # Redistribute exercises to empty days
    while any(not schedule[day] for day in schedule): 
        # Find the day with the most exercises
        most_loaded_day = max(schedule, key=lambda day: len(schedule[day]))
        num_exercises_to_move = len(schedule[most_loaded_day]) // 2

        # Find an empty day
        empty_day = next(day for day in schedule if not schedule[day])

        # Move exercises from most loaded day to empty day
        schedule[empty_day].extend(schedule[most_loaded_day][-num_exercises_to_move:])
        del schedule[most_loaded_day][-num_exercises_to_move:]

    return schedule

days = 7
muscle_groups = ["Hips", "Chest", "Shoulder"]
exercises = ["Glute Kickback", "Split Squat", "Step-up", "Rear Lunge", "Single Leg Split Squat", "Hip Thrust", "Bench Press", "Military Press"]
workout_schedule = create_workout_schedule(days, muscle_groups, exercises)
print(workout_schedule)
