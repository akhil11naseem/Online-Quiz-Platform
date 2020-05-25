//timer function
function getTimeRemaining(endtime) {
    var t = Date.parse(endtime) - Date.parse(new Date());
    var seconds = Math.floor((t / 1000) % 60);
    var minutes = Math.floor((t / 1000 / 60) % 60);
    var hours = Math.floor((t / (1000 * 60 * 60)) % 24);
    var days = Math.floor(t / (1000 * 60 * 60 * 24));
    return {
        'total': t,
        'days': days,
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds
    };
}
//pairs the timer with an end time and draws to player
function initializeClock(endtime) {

    function updateClock() {
        var t = getTimeRemaining(endtime);

        document.getElementById("timer-box").innerHTML = ('0' + t.minutes).slice(-2) + ":" + ('0' + t.seconds).slice(-2);

        if (t.total <= 0) {
            clearInterval(timeinterval);
            timeUP = true;
            processResults();
        }
    }

    updateClock();
    var timeinterval = setInterval(updateClock, 1000);
}

var timeInMinutes = 20;
var currentTime = Date.parse(new Date());
var deadline = new Date(currentTime + timeInMinutes * 60 * 1000);
var timeUP = false;

initializeClock(deadline);