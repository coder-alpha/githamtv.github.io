var tag = document.createElement('script');
tag.src = "//www.youtube.com/player_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
function onYouTubePlayerAPIReady() {
    var players = document.querySelectorAll('#gifs-container div')
    for (var i = 0; i < players.length; i++) {
        new YT.Player(players[i], {
            playerVars: {
                'autoplay': 0,
                'modestbranding': 1,
                 'controls': 0,'showinfo': 0, 'rel': 0, 'loop':1,'autohide':1,'wmode':'opaque',
            },
            videoId: players[i].dataset.id
        });
    }
}
