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
	return button;
}

$('.textbutton').live('mousedown',function(){
	$(this).addClass("depressed")
}).live('mouseup',function(){
	$(this).removeClass("depressed")
}).live('mouseleave',function(){
	$(this).removeClass("depressed")
});
