function bindScrollbar(scrollbar, scrollable) {
	$(scrollbar).data('target',scrollable);
}

scrollTarget = null;
scrollDriver = null;

$('.scrollregion').mousedown(function (){
	// start a drag
	scrollDriver = $($(this).children('.scrollbar')[0]);
	scrollTarget = scrollDriver.data('target');
	//console.log(scrollDriver)
	//console.log(scrollTarget)
}).mouseup(function() {
	// end it
	scrollDriver = null;
	scrollTarget = null;
}).mousemove(function(e){
	// this is where the magic happens
	if (scrollDriver != null) {
		// find the percentage at the mouse position
		percent = Math.max(Math.min((e.pageY-124)/$(this).height()*100,100),0)
		scrollDriver.css('top',""+percent+"%");
		if (scrollTarget != null) {
			scrollTarget = $(scrollTarget)
			lastkid = $(scrollTarget).children().last()
			maxscroll = lastkid.position().top+lastkid.outerHeight()+scrollTarget.scrollTop()-scrollTarget.height();
			//console.log(maxscroll)
			scrollTarget.scrollTop(maxscroll*percent/100)
		}
	}
});
