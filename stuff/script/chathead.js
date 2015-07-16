
var MAIN = {}; // Global object

// CHATHEADMODAL
MAIN.chatheadmodal = function(obj) {
  // REQUIRED PROPERTIES:
  // content: [cloned jQuery element and contents, independently styled]
  
  // OPTIONAL PROPERTIES:
  // fade: [int] fade duration in milliseconds
  // callback: [function]

  // Position the chatheadmodal right where the user is in the scroll
  $('.js-chatheadmodal').css('top', $(window).scrollTop() + 15);
  // Load contents
  $('.js-chatheadmodal__content').html(obj.content.clone().show()); // show() because they were hidden on the page already
  // Set fade
  MAIN.chatheadmodal.fade = parseInt(obj.fade) || 1; // "1" instead of "0" because jQuery will ignore the zero, and one millisecond is close enough to having no fade as a default! :)
  // FadeIn chatheadmodal
  $('.js-chatheadmodal, .js-chatheadmodal-overlay').fadeIn(MAIN.chatheadmodal.fade);
  // Run callback
  try { obj.callback(); } catch(e) {}
}; // end MAIN.chatheadmodal
MAIN.chatheadmodal.fade = 1;
MAIN.chatheadmodal.close = function() {
  $('.js-chatheadmodal, .js-chatheadmodal-overlay').fadeOut(MAIN.chatheadmodal.fade);
  setTimeout(function() { $('.js-chatheadmodal__content').html(''); }, MAIN.chatheadmodal.fade);
};
MAIN.chatheadmodal.init = function() {
  // Assign close listeners
  $('.js-chatheadmodal__close, .js-chatheadmodal-overlay').on('click', function() {
    MAIN.chatheadmodal.close();
  });
  $(document).keyup(function(e) {
    var kc = e.keyCode;
    if (kc == 13 || kc == 27) {
      MAIN.chatheadmodal.close();
    }
  });
};
MAIN.chatheadmodal.init();


$('.js-learn-more').on('click', function() {
  MAIN.chatheadmodal({
    content: $('.js-content'),
    fade: 250,
    callback: function() {
      console.log("One use for this callback is in case you need to assign listeners to elements within the chatheadmodal after they get injected since it wouldn't work assigning them on page load.\n\nMake sure to append a chatheadmodal class name before your selectors otherwise, you'll target both the hidden elements AND the ones in the chatheadmodal!\n\nExample: $('.js-form-elem') would be $('.js-chatheadmodal .js-form-elem') in the callback.");
    }
  });
});
