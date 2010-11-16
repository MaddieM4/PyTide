tooltip_timer = null;
tooltip_object = $('<div class="tooltip ubuntu invisible"> \
			<div class="left"></div> \
			<div class="content"></div> \
			<div class="right"></div> \
		</div>').appendTo($('body'));

function subscribeTooltip(selector, text) {
	$(selector).live('mouseover mousemove', function(){
		$(this).data('timer',openTooltip(this, text)[1]);
	}).live('mouseout', function(){
		var timer = $(this).data('timer');
		if (timer) {
			console.log("clearing timeout:" + timer);
			clearTimeout(timer);
		}
	});
}

function openTooltip(obj, text) {
	var tt = makeTooltip(text);
	setTTpos(tt, obj);
	return [tt, tooltip_reset_timer()];
}

function makeTooltip(text) {
	// "text" can also be a jQuery object
	tooltip_object.children('.content').empty().append(text);
	return tooltip_object;
}

function setTTpos(tt, obj) {
	var winwidth = $(window).width(), winheight = $(window).height();
	var dim = getDimensions(obj);
	if (winheight-dim.bottom > dim.top){
		// more room on the bottom
		tt.css('top', dim.bottom);
	} else {
		// more room on the top
		tt.css('bottom', winheight-dim.top);
	}
	var percent = ((dim.left + dim.right)/2)/winwidth;
	tt.children('.left').attr('style','-webkit-box-flex:'+percent+'; ');
	tt.children('.right').attr('style','-webkit-box-flex:'+(1-percent)+'; ');
}

function getDimensions(obj) {
	var target = $(obj);
	var result = target.offset();
	result['width'] = target.width();
	result['height'] = target.height();
	result['bottom'] = result['top'] + result['height'];
	result['right'] = result['left'] + result['width'];
	return result;
}

$(window).mousemove(function() {
	tooltip_object.addClass('invisible');
});

function tooltip_reset_timer() {
	if (tooltip_timer != null) clearTimeout(tooltip_timer);
	tooltip_timer = setTimeout('tooltip_object.removeClass("invisible")',400);
	return tooltip_timer;
}
