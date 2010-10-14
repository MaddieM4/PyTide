searchbox = $('.search input'); // legacy

// Search bar - highlight and non-highlight
$('search input').live('focusin',function(){
	$('.search').addClass("highlighted")
}).live('focusout',function(){
	$('.search').removeClass("highlighted")
});

function FindBox(deftext, callback) {
	box = $('<input class="find inactive" value="'+deftext+'"/>');
	if (callback) {newlinecallback(box, callback)}
	return box;
}

$('input.find').live('focusin', function() {
	if ($(this).hasClass('inactive')) {
		$(this).removeClass('inactive').val('');
	}
}).live('focusout', function () {
	if ($(this).val() == "") {
		$(this).addClass('inactive').val($(this).data('deftext'));
	}
});
