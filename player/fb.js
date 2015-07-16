(function(d, s, id) {
var js, fjs = d.getElementsByTagName(s)[0];
if (d.getElementById(id)) return;
js = d.createElement(s); js.id = id;
js.src = "//connect.facebook.net/en_US/sdk.js#xfbml=1&appId=1469814199962644&version=v2.0";
fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));
// ON PAGE LOAD
setTimeout(function(){
resizeFacebookComments();
}, 1000);
// ON PAGE RESIZE
$(window).on('resize', function(){
resizeFacebookComments();
});
function resizeFacebookComments(){
var src = $('.fb-comments iframe').attr('src').split('width='),
width = $('#container').width();
$('.fb-comments iframe').attr('src', src[0] + 'width=' + width);
}
