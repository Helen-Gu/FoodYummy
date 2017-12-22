// AJAX code to check input field values when onblur event triggerd.
function getUserInfo(selectObject) {
	var value = selectObject.value;
	var xmlhttp;
	if (window.XMLHttpRequest) { // for IE7+, Firefox, Chrome, Opera, Safari
		xmlhttp = new XMLHttpRequest();
	} else { // for IE6, IE5
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	xmlhttp.onreadystatechange = function() {

		if (xmlhttp.readyState != 4 && xmlhttp.status == 200) {
			document.getElementById("results").innerHTML = "Searching..";
		} else if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			// var data = JSON.parse(xmlhttp.responseText); 
			document.getElementById("results").innerHTML = xmlhttp.responseText;
				
		} else {
			document.getElementById("results").innerHTML = "Error - Please <a href='"+window.location.href+"'>Refresh the Page</a>";
		}
	}
	xmlhttp.open("GET", window.location.href+"?id="+value, true);
	// xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xmlhttp.send();
	};


function submit(){
	var xmlhttp;
	if (window.XMLHttpRequest) { // for IE7+, Firefox, Chrome, Opera, Safari
		xmlhttp = new XMLHttpRequest();
	} else { // for IE6, IE5
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	xmlhttp.onreadystatechange = function() {

		if (xmlhttp.readyState != 4 && xmlhttp.status == 200) {
			document.getElementById("results").innerHTML = "submiting..";
		} else if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			var data = JSON.parse(xmlhttp.responseText);
			console.log("failed");
			if (data['status'] == 'failed'){
				for (var i in data){
					if (i != 'status'){
						console.log("error "+i+" = "+data[i])
						document.getElementById("err-"+i).innerHTML = data[i];
					}
				}
			}
			else if (data['status'] == 'success'){
				document.getElementById("status").innerHTML = "Successfully update the user!";
			}
		} else {
			document.getElementById("results").innerHTML = "Error - Please <a href='"+window.location.href+"'>Refresh the Page</a>";
		}
	}
	xmlhttp.open("POST", window.location.href,true);
	xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xmlhttp.send(document.getElementById("user-form"));
};




