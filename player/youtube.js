var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var ytplayer;
function onYouTubeIframeAPIReady()
{
  ytplayer = new YT.Player('myytplayer', {
    height: vheight,
    width: vwidth,
    videoId: 'DEMMydPFbGU',
    events: {
      'onReady': onYouTubePlayerReady,
      'onStateChange': onytplayerStateChange,
      'onError': onytplayerError
    }
  });
}
