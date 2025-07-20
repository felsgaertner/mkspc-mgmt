window.onload = function () {
    const timer = document.getElementById('checkin-timer');
    if (timer) {
        updateTimer(timer);
        setInterval(function () { updateTimer(timer); }, 1000);
    }
}

function updateTimer(timer) {
    let diff = (new Date() - new Date(timer.dataset.since)) / 1000;
    const hh = Math.floor(diff / 60 / 60);
    diff -= hh * 60 * 60;
    const mm = Math.floor(diff / 60);
    const ss = Math.floor(diff - mm * 60);
    timer.textContent = `${hh}h ${mm}min ${ss}s`;
}

function showNoteModal(show) {
    const div = document.getElementById('note-modal');
    if (show) {
        div.style.display = 'block';
        setTimeout(() => div.classList.add('show'), 10);
    } else {
        div.classList.remove('show');
        setTimeout(() => div.style.display = null, 200); // wait for fade
    }
}
