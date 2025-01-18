document.getElementById('load-video-button').addEventListener('click', () => {
    const fileInput = document.getElementById('video-file');
    const file = fileInput.files[0];

    if (file) {
        const videoEditor = document.getElementById('video-editor');
        videoEditor.innerHTML = ''; // Clear previous content

        const videoElement = document.createElement('video');
        videoElement.controls = true;
        videoElement.src = URL.createObjectURL(file);
        videoElement.className = 'w-100';

        videoEditor.appendChild(videoElement);

        // Additional video editing tools can be added here
    } else {
        alert('Please select a video file to load.');
    }
}); 