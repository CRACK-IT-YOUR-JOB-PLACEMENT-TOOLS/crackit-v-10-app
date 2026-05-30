document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('hero-video');
    const playPauseBtn = document.getElementById('play-pause-btn');
    const progressBar = document.getElementById('progress-bar');
    const progressContainer = document.getElementById('progress-container');
    const timeDisplay = document.getElementById('time-display');
    const muteBtn = document.getElementById('mute-btn');
    const customControls = document.querySelector('.custom-controls');

    // Make controls active temporarily on mobile/touch when video is clicked
    video.addEventListener('click', () => {
        customControls.classList.add('active');
        setTimeout(() => {
            if(!video.paused) {
                customControls.classList.remove('active');
            }
        }, 3000);
    });

    // Play/Pause
    function togglePlay() {
        if (video.paused) {
            video.play();
            playPauseBtn.innerHTML = '<i class="fa-solid fa-pause"></i>';
        } else {
            video.pause();
            playPauseBtn.innerHTML = '<i class="fa-solid fa-play"></i>';
        }
    }

    playPauseBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        togglePlay();
    });
    
    video.addEventListener('click', togglePlay);

    // Update Progress and Time
    function formatTime(seconds) {
        const min = Math.floor(seconds / 60);
        const sec = Math.floor(seconds % 60);
        return `${min}:${sec < 10 ? '0' : ''}${sec}`;
    }

    video.addEventListener('timeupdate', () => {
        const percent = (video.currentTime / video.duration) * 100;
        progressBar.style.width = `${percent}%`;

        if (!isNaN(video.duration)) {
            timeDisplay.textContent = `${formatTime(video.currentTime)} / ${formatTime(video.duration)}`;
        }
    });

    video.addEventListener('loadedmetadata', () => {
        timeDisplay.textContent = `0:00 / ${formatTime(video.duration)}`;
    });

    // Seek
    progressContainer.addEventListener('click', (e) => {
        const rect = progressContainer.getBoundingClientRect();
        const pos = (e.clientX - rect.left) / rect.width;
        video.currentTime = pos * video.duration;
    });

    // Mute/Unmute
    function toggleMute(e) {
        if(e) e.stopPropagation();
        video.muted = !video.muted;
        if (video.muted) {
            muteBtn.innerHTML = '<i class="fa-solid fa-volume-xmark"></i>';
            muteBtn.style.color = '#a0a0a0';
        } else {
            muteBtn.innerHTML = '<i class="fa-solid fa-volume-high"></i>';
            muteBtn.style.color = 'white';
        }
    }

    muteBtn.addEventListener('click', toggleMute);

    // End of video handling
    video.addEventListener('ended', () => {
        playPauseBtn.innerHTML = '<i class="fa-solid fa-rotate-right"></i>';
        customControls.classList.add('active');
    });
});
