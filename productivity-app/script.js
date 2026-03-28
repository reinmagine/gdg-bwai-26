const DURATIONS = {
    pomodoro: 25 * 60,
    shortBreak: 5 * 60,
    longBreak: 15 * 60
};

let currentMode = 'pomodoro';
let timeLeft = DURATIONS[currentMode];
let timerInterval = null;
let isRunning = false;

const timeDisplay = document.getElementById('time-display');
const modeButtons = document.querySelectorAll('.mode-btn');
const startBtn = document.getElementById('start-btn');
const resetBtn = document.getElementById('reset-btn');
const startText = document.getElementById('start-text');
const startIcon = startBtn.querySelector('.icon');

const circle = document.getElementById('progress-circle');
const radius = circle.r.baseVal.value;
const circumference = radius * 2 * Math.PI;

circle.style.strokeDasharray = `${circumference} ${circumference}`;
circle.style.strokeDashoffset = 0;

function setProgress(percent) {
    const offset = circumference - percent / 100 * circumference;
    circle.style.strokeDashoffset = offset;
}

function updateDisplay() {
    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;
    timeDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    document.title = `${timeDisplay.textContent} - Pomodoro`;

    // Update Progress Ring
    const totalTime = DURATIONS[currentMode];
    const percentage = (timeLeft / totalTime) * 100;
    setProgress(percentage);
}

function switchMode(mode) {
    currentMode = mode;
    timeLeft = DURATIONS[currentMode];
    
    // Update active button
    modeButtons.forEach(btn => btn.classList.remove('active'));
    document.querySelector(`[data-mode="${mode}"]`).classList.add('active');

    // Update Theme
    document.body.setAttribute('data-theme', mode);

    resetTimer();
    updateDisplay();
}

function startTimer() {
    if (isRunning) return;
    
    isRunning = true;
    startText.textContent = 'Pause';
    startIcon.innerHTML = `
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M10 5H7V19H10V5Z" fill="currentColor"/>
            <path d="M17 5H14V19H17V5Z" fill="currentColor"/>
        </svg>
    `;

    timerInterval = setInterval(() => {
        if (timeLeft > 0) {
            timeLeft--;
            updateDisplay();
        } else {
            clearInterval(timerInterval);
            isRunning = false;
            // Play notification sound
            playAlarm();
        }
    }, 1000);
}

function pauseTimer() {
    isRunning = false;
    clearInterval(timerInterval);
    startText.textContent = 'Start';
    startIcon.innerHTML = `
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M8 5V19L19 12L8 5Z" fill="currentColor"/>
        </svg>
    `;
}

function resetTimer() {
    pauseTimer();
    timeLeft = DURATIONS[currentMode];
    updateDisplay();
}

function playAlarm() {
    // A soft, pleasant notification sound (using Web Audio API for a calm tone)
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    
    // Elegant double chime
    function playChime(freq, timeOffset) {
        const osc = audioCtx.createOscillator();
        const gainNode = audioCtx.createGain();
        
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime + timeOffset);
        
        gainNode.gain.setValueAtTime(0, audioCtx.currentTime + timeOffset);
        gainNode.gain.linearRampToValueAtTime(0.5, audioCtx.currentTime + timeOffset + 0.1);
        gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + timeOffset + 2);
        
        osc.connect(gainNode);
        gainNode.connect(audioCtx.destination);
        
        osc.start(audioCtx.currentTime + timeOffset);
        osc.stop(audioCtx.currentTime + timeOffset + 2.5);
    }

    playChime(523.25, 0); // C5
    playChime(659.25, 0.4); // E5
    playChime(783.99, 0.8); // G5
}

// Event Listeners
startBtn.addEventListener('click', () => {
    if (isRunning) {
        pauseTimer();
    } else {
        startTimer();
    }
});

resetBtn.addEventListener('click', resetTimer);

modeButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
        const mode = e.target.dataset.mode;
        switchMode(mode);
    });
});

// Initialize
updateDisplay();
