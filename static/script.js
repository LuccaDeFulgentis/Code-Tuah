document.getElementById('exerciseForm').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent form from submitting the traditional way

    const formData = new FormData(event.target);
    fetch('/get_exercise', {
        method: 'POST',
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('result').innerHTML = `<p>Recommended Exercise: ${data.exercise}</p>`;
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('result').innerHTML = `<p>Error fetching exercise</p>`;
        });
});
