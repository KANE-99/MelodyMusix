
let current_playing_number = 0;
function calculateTotalValue(length) {
    var minutes = Math.floor(length / 60),
        seconds_int = length - minutes * 60;
    if (seconds_int >= 10) {
        seconds_str = seconds_int.toString();
    } else {
        seconds_str = '0' + seconds_int.toString();
    }
    seconds = seconds_str.substr(0, 2);
    time = minutes + ':' + seconds;

    return time;
}

function calculateCurrentValue(currentTime) {
    var current_hour = parseInt(currentTime / 3600) % 24,
        current_minute = parseInt(currentTime / 60) % 60,
        current_seconds_long = currentTime % 60,
        current_seconds = current_seconds_long.toFixed(),
        current_time = (current_minute < 10 ? "0" + current_minute : current_minute) + ":" + (current_seconds < 10 ? "0" + current_seconds : current_seconds);

    return current_time;
}

function initPlayers() {
    last = songs.length - 1;
    // Variables
    // ----------------------------------------------------------
    // audio embed object
    playBtn = document.getElementById('play-or-pause');
    forwardBtn = document.getElementById('forward');
    backwardBtn = document.getElementById('backward');

}
function initProgressBar() {
    var player = document.getElementById('player');
    let length = player.duration;
    let current_time = player.currentTime;

    var totalLength = calculateTotalValue(length)
    jQuery(".end-time").html(totalLength);

    // calculate current value time
    var currentTime = calculateCurrentValue(current_time);
    jQuery(".start-time").html(currentTime);

    newprogress = (player.currentTime / player.duration) * 100;
    $('#seekObj').attr('aria-valuenow', newprogress).css('width', newprogress + '%');


    if (player.currentTime == player.duration) {
        forwardPlay();
    }
};
$('.progress').click(
    function (evt) {
        var $this = $(this);
        player = document.getElementById('player');
        var widthclicked = evt.pageX - $this.offset().left;
        var totalWidth = $this.width();
        dura = player.duration;
        player.pause();
        player.currentTime = (widthclicked / totalWidth) * dura;
        // player.currentTime = (widthclicked / totalWidth) * dura;
        console.log("kkk:" + player.currentTime);
        player.play();
        $('#play-or-pause-icon').removeClass().addClass("fas fa-pause-circle fa-3x");
        newprogress = (player.currentTime / dura) * 100;
        console.log(newprogress);
        $('#seekObj').attr('aria-valuenow', newprogress).css('width', newprogress + '%');

    });
function togglePlay() {
    player = document.getElementById("player");
    if (player.paused === false) {
        player.pause();
        isPlaying = false;
        $('#play-or-pause-icon').removeClass().addClass("fas fa-play-circle fa-3x");



    } else {
        if (player.readyState === 0) {
            player.src = songs[current_playing_number].upload;
            player.load();
        }

        player.play();
        $('#play-or-pause-icon').removeClass().addClass("fas fa-pause-circle fa-3x");
        isPlaying = true;
        console.log("ready:" + player.readyState);

    }
}
var playfunc = function playing() {
    current_playing_number = this.id;
    player.src = songs[current_playing_number].upload;
    player.load();
    player.play();
    $('#play-or-pause-icon').removeClass().addClass("fas fa-pause-circle fa-3x");
    song_title = document.getElementById('song-title');
    song_title.textContent = this.closest('span').childNodes[3].textContent;
    if (location.pathname.includes('songs')) {
        var image = document.getElementById('song-img');
        image.src = songs[current_playing_number].album_logo;
    }

}
$("span button").click(playfunc);
function backwardPlay() {

    if (current_playing_number > 0) {
        current_playing_number -= 1;
        if (songs[current_playing_number + 1]) {
            forwardBtn.disabled = false;
        }
        if (current_playing_number == 0) {
            backwardBtn.disabled = true;

        }
        player = document.getElementById('player');
        if (location.pathname.includes('songs')) {
            player.src = songs[current_playing_number].upload;
            player.load();
            player.play();
            $('#play-or-pause-icon').removeClass().addClass("fas fa-pause-circle fa-3x");
            song_title = document.getElementById('song-title');
            song_title.textContent = songs[current_playing_number].title;
            var image = document.getElementById('song-img');
            image.src = songs[current_playing_number].album_logo;

        } else {
            var parent = document.getElementById("audio-player");
            var child = document.getElementById('player');
            child.pause();
            child.currentTime = 0;
            var player = document.createElement('audio');
            player.id = 'player';
            player.src = songs[current_playing_number].upload;
            player.type = 'audio/mpeg';
            player.preload = 'auto';
            player.ontimeupdate = function () { initProgressBar(); };
            parent.removeChild(child);
            parent.appendChild(player);
            player.load();
            player.onloadeddata = function () {
                player.play();
                $('#play-or-pause-icon').removeClass().addClass("fas fa-pause-circle fa-3x");
            };
            song_title = document.getElementById('song-title');
            song_title.textContent = songs[current_playing_number].title;
        }
    } else {
        player.currentTime = 0;
        $('#seekObj').attr('aria-valuenow', 0).css('width', 0 + '%');
    }


}
function forwardPlay() {

    if (current_playing_number < last) {
        current_playing_number += 1;
        if (songs[current_playing_number - 1]) {
            backwardBtn.disabled = false;
        }
        if (current_playing_number == last) {
            forwardBtn.disabled = true;
        }
        player = document.getElementById('player');
        if (location.pathname.includes('songs')) {
            player.src = songs[current_playing_number].upload;
            player.load();
            player.play();
            $('#play-or-pause-icon').removeClass().addClass("fas fa-pause-circle fa-3x");
            song_title = document.getElementById('song-title');
            song_title.textContent = songs[current_playing_number].title;
            var image = document.getElementById('song-img');
            image.src = songs[current_playing_number].album_logo;

        } else {
            var parent = document.getElementById("audio-player");
            var child = document.getElementById('player');
            child.pause();
            child.currentTime = 0;
            var player = document.createElement('audio');
            player.id = 'player';
            player.src = songs[current_playing_number].upload;
            song_title = document.getElementById('song-title');
            song_title.textContent = songs[current_playing_number].title;
            player.type = 'audio/mpeg';
            player.preload = 'auto';
            player.ontimeupdate = function () { initProgressBar(); };
            parent.removeChild(child);
            parent.appendChild(player);
            // player.pause();
            // player.setAttribute('src', songs[current_playing_number].upload);
            player.load();
            player.onloadeddata = function () {
                player.play();
                $('#play-or-pause-icon').removeClass().addClass("fas fa-pause-circle fa-3x");
            }
        }
    } else {
        player.currentTime = 0;
        $('#seekObj').attr('aria-valuenow', 0).css('width', 0 + '%');
    }
}


initPlayers();