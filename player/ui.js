 $(".closeButton").click(function() {
  $(this).parent().slideToggle();
});
$("#search").focus(function() {
  $(".header").animate({height:"80px"}, 500);
  $(".cloud").animate({opacity:"0"}, 500);
  $(".cards").animate({opacity:"0"}, 500);
  $(".loading").animate({opacity:"1"}, 500);
});
$("#search").blur(function() {
  $(".header").animate({height:"80px"}, 500);
  $(".cloud").animate({opacity:"1"}, 500);
  $(".cards").animate({opacity:"1"}, 500);
  $(".loading").animate({opacity:"0"}, 500);
});
$(window).scroll(function() {
  if($(document).scrollTop()>10) {
    $(".header").animate({height:"80px"}, 100);
    $(".cloud").animate({opacity:"0"}, 100);
  }
  else {
    $(".header").animate({height:"80px"}, 100);
    $(".cloud").animate({opacity:"1"}, 100);
  }
});
 
