function bindScrollbar(scrollbar, scrollable) {
	$(scrollbar).data('target',scrollable);
	$(scrollable).data('controller',scrollbar).mousemove(function(e){scroll(e)}).bind('mousewheel',
	    function(e, delta, deltaX,deltaY){
		targ = $(this);
		//alert(e.wheelDelta)
		newscroll = targ.scrollTop()+(e.wheelDelta/-5);
		maxscroll = getMaxScroll(targ);
		newscroll = Math.max(Math.min(maxscroll, newscroll),0)
		targ.scrollTop(newscroll)
		setScrollbarFromScrollable(targ)
	});
	setScrollbarFromScrollable($(scrollable));
}

function unbindScrollbar(scrollbar) {
	scrollable = $(scrollbar.data('target'))
	scrollable.unbind('mousemove').removeData('controller')
	scrollbar.removeData('target')
}

function getMaxScroll(scrollTarget) {
	lastkid = $($(scrollTarget).children().last())
	if (lastkid.length==0) {return 0}
	return lastkid.position().top+lastkid.outerHeight()+scrollTarget.scrollTop()-scrollTarget.height();
}

function setScrollbarFromScrollable(scrollable) {
	maxscroll = getMaxScroll(scrollable);
	percent = scrollable.scrollTop()/maxscroll*100;
	$(scrollable.data('controller')).css('top',""+percent+"%");
}

function setAllScrollbars() {
	$('.scrollbar').each(function(){
		setScrollbarFromScrollable($($(this).data('target')))
	});
}

function resolveScrollbar(scrollbar) {
	if (scrollbar==null) {
		return $('.scrollbar');
	} else {
		return $(scrollbar);
	}
}

function getScroll(scrollbar) {
	// returns percentage scrolled
	return parseFloat(resolveScrollbar(scrollbar).css("top"))
}

function setScroll(scrollbar, percent) {
	// sets percentage scrolled
	scrollbar = resolveScrollbar(scrollbar);
	starget = $(scrollbar.data('target'))

	scrollbar.css('top',""+percent+"%");
	if (starget != null) {
		maxscroll = getMaxScroll(starget)
		starget.scrollTop(maxscroll*percent/100)
	}
}

$(window).resize(setAllScrollbars);

function reset_scroll(scrollable){
	scrollable.scrollTop(0);
	$(scrollable.data('controller')).css('top',"0%");	
}

function scroll(e) {
	// this is where the magic happens
	if (scrollDriver != null) {
		// find the percentage at the mouse position
		percent = Math.max(Math.min((e.pageY-147)/scrollDriver.parent().height()*100,100),0)
		setScroll(scrollDriver, percent);
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
