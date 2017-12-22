// AJAX code to check input field values when onblur event triggerd.
function validate(field, query) {
	console.log("yesss");
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
			document.getElementById(field).innerHTML = xmlhttp.responseText;
		} else {
			document.getElementById(field).innerHTML = "Error - Please <a href='"+window.location.href+"'>Refresh the Page</a>";
		}
	}
	xmlhttp.open("POST", window.location.href, true);
	xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xmlhttp.send('email='+query);
	}




function checkForm() {
	var email = document.getElementById("email").value;
	var email1 = document.getElementById("err-1");
	var password = document.getElementById("psw").value;
	var password1 = document.getElementById("err-2");

	if (password == ''){
		password1.innerHTML = 'Password cannot be empty!'
	} else if (email == ''){
		email1.innerHTML = 'Please fill me in!'
	} else{
	//Submit Form When All values are valid.
		document.getElementById("myForm").submit();
		}
	}

