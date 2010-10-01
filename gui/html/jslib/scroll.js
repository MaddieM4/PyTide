function bindScrollbar(scrollbar, scrollable) {
	$(scrollbar).data('target',scrollable);
	$(scrollable).mousemove(function(e){scroll(e)});
}

function scroll(e) {
	// this is where the magic happens
	if (scrollDriver != null) {
		// find the percentage at the mouse position
		percent = Math.max(Math.min((e.pageY-124)/scrollDriver.parent().height()*100,100),0)
		scrollDriver.css('top',""+percent+"%");
		if (scrollTarget != null) {
			scrollTarget = $(scrollTarget)
			lastkid = $(scrollTarget).children().last()
			maxscroll = lastkid.position().top+lastkid.outerHeight()+scrollTarget.scrollTop()-scrollTarget.height();
			scrollTarget.scrollTop(maxscroll*percent/100)
		}
	}
}

scrollTarget = null;
scrollDriver = null;

$('.scrollregion').mousedown(function (e){
	// start a drag
	scrollDriver = $($(this).children('.scrollbar')[0]);
	scrollTarget = scrollDriver.data('target');
	scroll(e)
}).mouseup(function() {
	// end it
	scrollDriver = null;
	scrollTarget = null;
}).mousemove(function(e){
	scroll(e)
});

$('body').mouseup(function() {
	scrollDriver = null;
	scrollTarget = null;
})
