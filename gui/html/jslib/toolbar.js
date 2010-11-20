searchbox = $('.search input');

// Search bar - highlight and non-highlight
searchbox.focusin(function(){
	$('.search').addClass("highlighted")
});
searchbox.focusout(function(){
	$('.search').removeClass("highlighted")
});

hiddenTools = new Array();

function hideTool(jqobj) {
	hiddenTools[hiddenTools.length] = {"class":jqobj.attr("class"),"label":jqobj.text()};
	jqobj.addClass("invisible");
}

function clearTools() {hiddenTools = new Array()}

function pullTools() {
	retstring = ""
	for (i in hiddenTools) {
		retstring+="<li class='"+hiddenTools[i]['class']+"'><div>"+hiddenTools[i]['label']+"</div>";
	}
	return retstring;
}

adjusting=false;
// adjust toolbar in resize events
function adj_toolbar(){
	if (adjusting) return false;
	adjusting=true;
	clearTools();
	toolbar = $('.toolbar ul:not(.invisible)');
	totalwidth = $(window).width();
	runningwidth = 0;
	showMore = false;
	if (options['tbshorten']=='autoshorten') {
		// test to see if normal style is too long
		$('.toolbar').removeClass('noicons').removeClass('nolabels');
		tc = toolbar.children(':not(.more)');
		last = toolbar.children(':not(.more):last');
		tc.removeClass('invisible').removeClass('icononly').each(function(index){
			t = $(tc[tc.length-index-1]);
			var wid = last.position().left+last.outerWidth();
			if (wid > totalwidth || last.position().top > 1) {
				t.addClass('icononly');
			}
		});
		runningwidth=0;
	}
	toolbar.children(':not(.more)').removeClass('invisible').each(function(){
		t = $(this);
		runningwidth+=t.outerWidth();
		if (runningwidth-4 > totalwidth || t.position().top > 1) {
			hideTool(t);
			showMore = true;
		}
	});
	if (showMore) {
		$('.toolbar .more').removeClass('invisible')
	} else {
		if (!$('.toolbar .more').hasClass('active')) {
			$('.toolbar .more').addClass('invisible');
		}
	}
	adjusting=false;
}

$(window).resize(adj_toolbar);
adj_toolbar()

$('.toolbar .more').live('click',function() {
	if ($(this).hasClass("active")) {
		closeMenu();
		$(this).removeClass("active");
		adj_toolbar();
	} else {
		openMenu("<ul class='tools'>"+pullTools()+"</ul>",3, function (){
			$('.toolbar .more').removeClass('active');
			closeMenu();
		});
		activateToolbars(true);
		$(this).addClass("active");
		$('.toolbar .gotoOptions').removeClass("active");
	}
});

// toolbar hover
livehover('.toolbar li');
