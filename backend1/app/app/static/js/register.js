// AJAX code to check input field values when onblur event triggerd.
function validate(field, query) {

	var xmlhttp;
	if (window.XMLHttpRequest) { // for IE7+, Firefox, Chrome, Opera, Safari
		xmlhttp = new XMLHttpRequest();
	} else { // for IE6, IE5
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	xmlhttp.onreadystatechange = function() {

		if (xmlhttp.readyState != 4 && xmlhttp.status == 200) {
			document.getElementById(field).innerHTML = "Validating..";
		} else if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			var data = JSON.parse(xmlhttp.responseText); 
			document.getElementById(field).innerHTML = data['status'];
				
		} else {
			document.getElementById(field).innerHTML = "Error - Please <a href='"+window.location.href+"'>Refresh the Page</a>";
		}
	}
	xmlhttp.open("POST", window.location.href, true);
	xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xmlhttp.setRequestHeader("request-type", "ev");
	xmlhttp.send('email='+query);
	};

function checkForm(){
	var form = document.getElementById("myForm");
	for ( var i = 0; i < form.elements.length; i++ ) {
   		var e = form.elements[i];
   		console.log(e);
   		if (e.value == ''){
   			document.getElementById("err-"+e.name).innerHTML = 'Please fill me in!';
   			return;
   			}
   			}
   	console.log("submitted!");
   	form.submit();
}

function clear(){
	var form = document.getElementById("myForm");
	for ( var i = 0; i < form.elements.length; i++ ) {
   		form.elements[i].innerHTML = '';
}
 }




