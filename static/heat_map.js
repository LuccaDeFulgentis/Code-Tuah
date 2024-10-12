const daysContainer = document.getElementById('days-container');
const addDayButton = document.getElementById('add-day');
const generateButton = document.getElementById('generate-heatmap');
const heatmapImage = document.getElementById('heatmap-image');
let dayCount = 1;

const muscleGroups = ["chest", "shoulders", "triceps", "biceps", "forearm", "thighs", "hips", "calves", "back"];

addDayButton.addEventListener('click', () => {
    const newDayDiv = document.createElement('div');
    newDayDiv.id = `day-${dayCount}`;
    newDayDiv.innerHTML = `<h3>Day ${dayCount}</h3>`;

    const exerciseInput = document.createElement('input');
    exerciseInput.type = 'text';
    exerciseInput.placeholder = 'Exercise Name';

    const muscleSelect = document.createElement('select');
    muscleGroups.forEach(muscle => {
        const option = document.createElement('option');
        option.value = muscle;
        option.text = muscle;
        muscleSelect.appendChild(option);
    });

    const addExerciseButton = document.createElement('button');
    addExerciseButton.textContent = 'Add Exercise';

    const exercisesList = document.createElement('ul');

    addExerciseButton.addEventListener('click', () => {
        const exerciseName = exerciseInput.value;
        const mainMuscle = muscleSelect.value;

        if (exerciseName) {
            const listItem = document.createElement('li');

            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.checked = true;

            checkbox.addEventListener('change', () => {
                updateHeatmap();
            });

            listItem.appendChild(checkbox);
            const exerciseText = document.createTextNode(`${exerciseName} (${mainMuscle})`);
            listItem.appendChild(exerciseText);
            listItem.dataset.mainMuscle = mainMuscle;
            exercisesList.appendChild(listItem);

            exerciseInput.value = '';
        }
    });

    newDayDiv.appendChild(exerciseInput);
    newDayDiv.appendChild(muscleSelect);
    newDayDiv.appendChild(addExerciseButton);
    newDayDiv.appendChild(exercisesList);

    daysContainer.appendChild(newDayDiv);
    dayCount++;
});

function updateHeatmap() {
    let workout_schedule = {};
    for (let i = 1; i < dayCount; i++) {
        const dayDiv = document.getElementById(`day-${i}`);
        const exercisesList = dayDiv.querySelector('ul');
        const exercises = Array.from(exercisesList.children).map(listItem => ({
            name: listItem.textContent.split(' (')[0],
            main_muscle: listItem.dataset.mainMuscle,
            checked: listItem.querySelector('input[type="checkbox"]').checked
        }));
        workout_schedule[`day-${i}`] = exercises;
    }

    fetch('/generate_heatmap', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(workout_schedule)
    })
    .then(response => response.blob())
    .then(blob => {
        const objectURL = URL.createObjectURL(blob);
        heatmapImage.src = objectURL;
    })
    .catch(error => console.error('Error:', error));
}

generateButton.addEventListener('click', updateHeatmap); 
