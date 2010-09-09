// dependencies
//   * contact.css
//   * Jquery

function renderContact(contact) {
	result = "<div class='contact'>";
	result += "<img src='"+contact['avatar']+"'/>";
	result += "<div class='name'>"+contact['name']+" <span class='address'>("+contact['address']+")</span></div>";
	result += "<div class='buttonseries'></div>"
	result += "</div>";
	jqobj = $(result);
	buttonseries = jqobj.children('.buttonseries')
	renderButton('Hit this person with a stick',function (){
		alert("Ow! What the %#*$?!! WHY DID YOU DO THAT???!");
	}).appendTo(buttonseries);
	return jqobj;
}
