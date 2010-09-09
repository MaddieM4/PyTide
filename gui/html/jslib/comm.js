function sendObject(obj) {
	obj['timestamp'] = new Date()
	str = JSON.stringify(obj);
	document.title = str;
}

// start monitoring the document title with the search input
function doctitle() {
	$('.search input').val(document.title);
	t=setTimeout("doctitle()",300);
}

function printHTML() {
	sendObject({
		'type':'sendHTML',
		'html':$('body').html()
	});
}

