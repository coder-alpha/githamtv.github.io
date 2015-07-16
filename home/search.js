var search = $("#search");
var listItems = $("li");
search.on("keyup", function() {
var terms = search.val();
if (terms == '') {
listItems.show();
} else {
listItems.hide();
$("li:contains('" + terms + "')").show();
}
});
jQuery.expr[':'].contains = function(a, i, m) {
return jQuery(a).text().toUpperCase()
.indexOf(m[3].toUpperCase()) >= 0;
};
