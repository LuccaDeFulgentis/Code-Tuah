import pandas as pd

# Load the dataset
df = pd.read_csv('gym_exercise_dataset.csv')

# Strip leading/trailing whitespace from all string columns
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# Columns to remove
columns_to_remove = ['Variation', 'Utility', 'Target_Muscles', 
                     'Synergist_Muscles', 'Stabilizer_Muscles', 
                     'Antagonist_Muscles', 'Dynamic_Stabilizer_Muscles', 
                     'parent_id']

# Drop the specified columns
df = df.drop(columns=columns_to_remove)

# Remove rows where Main_muscle is "Neck"
df = df[df['Main_muscle'] != 'Neck']

# Rename 'Main_muscle' based on 'Force' for Upper Arm exercises
for index, row in df.iterrows():
    if row['Main_muscle'] == 'Upper Arms':
        if row['Force'] == 'Pull':
            df.loc[index, 'Main_muscle'] = 'Biceps'
        elif row['Force'] == 'Push':
            df.loc[index, 'Main_muscle'] = 'Triceps'

# Remove the 'Force' column
df = df.drop(columns=['Force'])

# Save the cleaned dataset
df.to_csv('gym_exercise_dataset_cleaned.csv', index=False)