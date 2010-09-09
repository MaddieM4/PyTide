searchbox = $('.search input');

// Search bar - highlight and non-highlight
searchbox.focusin(function(){
	$('.search').addClass("highlighted")
});
searchbox.focusout(function(){
	$('.search').removeClass("highlighted")
});

