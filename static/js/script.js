function getWeekNumber(date) {
    const startOfYear = new Date(date.getFullYear(), 0, 1);
    const pastDaysOfYear = (date - startOfYear) / 86400000;
    return Math.ceil((pastDaysOfYear + startOfYear.getDay() + 1) / 7);
}

function displayDateAndWeek() {
    const now = new Date();
    const dateString = now.toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
    const weekNumber = getWeekNumber(now);
    const container = document.getElementById('date-week-container');
    container.textContent = `Today is ${dateString}, Week ${weekNumber} of the year.`;
}

// Call the function on page load
displayDateAndWeek();

document.getElementById('search-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const query = document.getElementById('query').value;
    const encodedQuery = encodeURIComponent(query);
    const resultsContainer = document.getElementById('results');

    resultsContainer.innerHTML = '';

    fetch(`/api/search?query=${encodedQuery}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                resultsContainer.innerHTML = `<p>${data.error}</p>`;
            } else if (data.length > 0) {
                data.forEach(item => {
                    const div = document.createElement('div');
                    div.className = 'result-item';
                    div.innerHTML = `
                        <hr>
                        <h2>${item.Grade}</h2>
                        <h3>Week ${item['Week Number']}</h3>
                        <p><strong>Topic:</strong> ${item.Topic} (${item.Code})</p>
                        <p><strong>Lesson Title:</strong> ${item['Lesson Title']}</p>
                        <p><strong>Objective:</strong> ${item.Objective}</p>
                        <p><strong>Content:</strong> ${item.Content}</p>
                        <p><strong>${item['Type of Activity']}:</strong> ${item.Activities}</p>
                    `;
                    resultsContainer.appendChild(div);
                });
            } else {
                resultsContainer.innerHTML = '<p>No matching records found.</p>';
            }
        })
        .catch(error => {
            resultsContainer.innerHTML = `<p>An error occurred: ${error.message}</p>`;
        });
});
