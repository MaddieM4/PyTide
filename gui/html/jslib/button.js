// dependencies:
//   * textbutton.css
//   * Jquery

function renderButton(label, callback) {
	html = "<table class='textbutton noselect'><tr>";
	html+= "<td class='left'></td>";
	html+= "<td class='center'>"+label+"</td>";
	html+= "<td class='right'></td>";
	html+= "</tr></table>";
	button = $(html).click(callback);
	button.mousedown(function () {$(this).addClass("depressed")});
	button.mouseup(function () {$(this).removeClass("depressed")});
	button.mouseleave(function () {$(this).removeClass("depressed")});
	return button;
}
