document.getElementById('scraper-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const url = document.getElementById('url').value;

    fetch('/api/scrape', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: url })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            displayScrapedContent(data.content);
        }
    })
    .catch(error => {
        console.error('Error scraping content:', error);
        alert('Failed to scrape content.');
    });
});

function displayScrapedContent(content) {
    const scraperResultsDiv = document.getElementById('scraper-results');
    scraperResultsDiv.innerHTML = ''; // Clear previous results

    const contentElement = document.createElement('div');
    contentElement.className = 'scraped-content';
    contentElement.innerHTML = content; // Display the scraped content
    scraperResultsDiv.appendChild(contentElement);
} 