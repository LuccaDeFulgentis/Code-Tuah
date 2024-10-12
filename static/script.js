document.addEventListener('DOMContentLoaded', function() {
    const swipeLeftBtn = document.getElementById('swipe-left');
    const swipeRightBtn = document.getElementById('swipe-right');
    
    const muscleGroups = JSON.parse(document.getElementById('muscle-groups').textContent);

    // Handle swipe actions
    swipeLeftBtn.addEventListener('click', function() {
        getNewExercise();
    });
    
    swipeRightBtn.addEventListener('click', function() {
        // TODO: Save the exercise to the user's routine
        getNewExercise();
    });
    
    function getNewExercise() {
        fetch('/get_exercise', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ muscle_groups: muscleGroups })
        })
        .then(response => response.json())
        .then(exercise => {
            updateExerciseCard(exercise);
        });
    }
    
    function updateExerciseCard(exercise) {
        document.getElementById('exercise-name').textContent = exercise['Exercise Name'];
        document.getElementById('exercise-main-muscle').textContent = exercise['Main_muscle'];
        document.getElementById('exercise-difficulty').textContent = 'Difficulty: ' + exercise['Difficulty (1-5)'];
    }
});
