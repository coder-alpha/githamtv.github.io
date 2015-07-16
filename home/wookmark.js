(function ($){
var $tiles = $('#tiles'),
$handler = $('li', $tiles),
$main = $('#main'),
$window = $(window),
$document = $(document),
options = {
autoResize: true, // This will auto-update the layout when the browser window is resized.
container: $main, // Optional, used for some extra CSS styling
offset: 20, // Optional, the distance between grid items
itemWidth:280 // Optional, the width of a grid item
};
/**
* Reinitializes the wookmark handler after all images have loaded
*/
function applyLayout() {
$tiles.imagesLoaded(function() {
// Destroy the old handler
if ($handler.wookmarkInstance) {
$handler.wookmarkInstance.clear();
}
// Create a new layout handler.
$handler = $('li', $tiles);
$handler.wookmark(options);
});
}
/**
* When scrolled all the way to the bottom, add more tiles
*/
function onScroll() {
// Check if we're within 100 pixels of the bottom edge of the broser window.
var winHeight = window.innerHeight ? window.innerHeight : $window.height(), // iphone fix
closeToBottom = ($window.scrollTop() + winHeight > $document.height() - 100);
if (closeToBottom) {
// Get the first then items from the grid, clone them, and add them to the bottom of the grid
var $items = $('li', $tiles),
$firstTen = $items.slice(0, 0);
$tiles.append($firstTen.clone());
applyLayout();
}
};
// Call the layout function for the first time
applyLayout();
// Capture scroll event.
$window.bind('scroll.wookmark', onScroll);
})(jQuery);
