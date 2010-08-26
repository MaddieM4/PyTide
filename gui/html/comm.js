function sendObject(obj) {
	obj['timestamp'] = new Date()
	str = JSON.stringify(obj);
	document.title = str;
}
