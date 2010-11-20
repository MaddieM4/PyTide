menuLevel = 0;

function menuSlide(dir, fade) {
	leftalter = ((dir=="left") ? "-=":"+=")+$(window).width();
	rightalter = ((dir=="left") ? "+=":"-=")+$(window).width();
	map = {};
	map['left'] = leftalter;
	map['right']= rightalter;
	if (fade == "in") {
		map['opacity'] = 1;
	} else if (fade == "out") {
		map['opacity'] = 0;
	}
	$('.menu').animate(map, function() {
		// animation complete
		// tidy up
		left = parseInt($(this).css("left"));
		if (left!=0) $(this).remove()
	});
}

function newMenu() {
	return $('<div class="menu"></div>').appendTo($('#mainwindow'));
}

function newMenuLeft(nofade) {
	menu = newMenu();
	menu.css({"left":-$(window).width(),"right":$(window).width()});
	if (nofade!=true) menu.css("opacity",0);
	return menu;
}
function newMenuRight(nofade) {
	menu = newMenu();
	menu.css({"left":$(window).width(),"right":-$(window).width()});
	if (nofade!=true) menu.css("opacity",0);
	return menu;
}

function openMenu(html, level, exitcallback) {
	fade = !($('.menu').length>0)
	//console.log("fade = "+fade);
	// if new menu is greater level, come from right, slide left
	slideLeft = (level>menuLevel);
	menu = slideLeft ? newMenuRight(!fade):newMenuLeft(!fade);
	if (exitcallback==null){
		exitcallback = function () {closeMenu()}
	}
	menu.append($(html)).prepend($("<div class='menuexit'></div>"));;
	$('.menuexit').mouseenter(function (){$(this).addClass("over")})
	$('.menuexit').mousedown(function (){$(this).addClass("down")})
	$('.menuexit').mouseup(function (){$(this).removeClass("down")})
	$('.menuexit').mouseleave(function (){$(this).removeClass("over").removeClass("down")})
	$('.menuexit').click(exitcallback)
	menuSlide((slideLeft ? "left":"right"),(fade)?"in":"none");
	menuLevel = level;
}

function closeMenu() {
	menuSlide(((menuLevel>0) ? "right":"left"),"out");
	menuLevel = 0;
}

