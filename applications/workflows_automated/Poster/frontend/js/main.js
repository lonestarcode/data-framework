document.getElementById('video-upload').addEventListener('change', () => {
    const fileInput = document.getElementById('video-upload');
    const file = fileInput.files[0];

    if (file) {
        const formData = new FormData();
        formData.append('video', file);

        fetch('/api/categorize-video', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                alert(`Predicted Category: ${data.category}`);
            }
        })
        .catch(error => {
            console.error('Error categorizing video:', error);
            alert('Failed to categorize video.');
        });
    } else {
        alert('Please select a video file to upload.');
    }
});

document.getElementById('album-selection').addEventListener('change', (e) => {
    const newAlbumSection = document.getElementById('new-album-section');
    if (e.target.value === 'create-new') {
        newAlbumSection.style.display = 'block';
    } else {
        newAlbumSection.style.display = 'none';
    }
});

function updateAlbumList(albums) {
    const albumSelection = document.getElementById('album-selection');
    albumSelection.innerHTML = '<option value="" disabled selected>Select Album</option><option value="create-new">Create New Album</option>';
    albums.forEach(album => {
        const option = document.createElement('option');
        option.value = album;
        option.textContent = album;
        albumSelection.appendChild(option);
    });
}

document.getElementById('create-album-button').addEventListener('click', () => {
    const newAlbumNameInput = document.getElementById('new-album-name');
    const albumName = newAlbumNameInput.value.trim();

    if (!albumName) {
        alert('Please enter a name for the new album.');
        return;
    }

    fetch('/api/create-album', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ album_name: albumName })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert('Album created successfully!');
            updateAlbumList(data.albums);
            newAlbumNameInput.value = ''; // Clear the input
            document.getElementById('new-album-section').style.display = 'none'; // Hide the new album section
        }
    })
    .catch(error => {
        console.error('Error creating album:', error);
        alert('Failed to create album.');
    });
});

document.getElementById('schedule-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const postTime = document.getElementById('post-time').value;

    const scheduleData = {
        post_time: postTime
    };

    fetch('/api/schedule', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(scheduleData)
    })
    .then(response => response.json())
    .then(data => {
        alert('Schedule updated successfully!');
    })
    .catch(error => {
        console.error('Error updating schedule:', error);
        alert('Failed to update schedule.');
    });
});

document.getElementById('post-selected-button').addEventListener('click', () => {
    const selectedPlatforms = Array.from(document.querySelectorAll('input[name="platform"]:checked'))
                                   .map(checkbox => checkbox.value);

    if (selectedPlatforms.length === 0) {
        alert('Please select at least one platform to post.');
        return;
    }

    const captions = {};
    selectedPlatforms.forEach(platform => {
        const captionInput = document.querySelector(`input[name="${platform}-caption"]`);
        if (captionInput) {
            captions[platform] = captionInput.value;
        }
    });

    fetch('/api/post-selected', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ platforms: selectedPlatforms, captions: captions })
    })
    .then(response => response.json())
    .then(data => {
        alert('Posted to selected platforms successfully!');
    })
    .catch(error => {
        console.error('Error posting to selected platforms:', error);
        alert('Failed to post to selected platforms.');
    });
});

document.getElementById('train-ai-button').addEventListener('click', () => {
    const category = document.getElementById('category').value;
    if (!category) {
        alert('Please select a category for AI training.');
        return;
    }

    fetch('/api/get-recommendations', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ category: category })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            displayRecommendedVideos(data.recommendations);
        }
    })
    .catch(error => {
        console.error('Error getting recommendations:', error);
        alert('Failed to get recommendations.');
    });
});

function displayRecommendedVideos(recommendations) {
    const recommendedVideosDiv = document.getElementById('recommended-videos');
    recommendedVideosDiv.innerHTML = ''; // Clear previous recommendations

    recommendations.forEach(video => {
        const videoElement = document.createElement('div');
        videoElement.className = 'recommended-video';
        videoElement.textContent = `${video.title} (${video.category})`; // Display title and category
        recommendedVideosDiv.appendChild(videoElement);
    });
}
