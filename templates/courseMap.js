loadDoc("http://ec2-50-112-190-90.us-west-2.compute.amazonaws.com:5000/newest");

function click(name) {
    document.getElementById("name").innerHTML = name;
	console.log("tesst");
}

function loadDoc(url) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (xhttp.readyState == 4 && xhttp.status == 200) {
     var arr = xhttp.response;
     var json = JSON.parse(arr.toString());

        for(var i = 0; i < json.users.length; i++){
	    //var row = "<a onclick=\"click("+"&quot;test&quot;"+"); return false;\">" + json.users[i] +"</a>";
           // var row = "<a class=\"list\" href='#'>" + json.users[i] + "</a>";
	    //document.getElementById("myDropdown").innerHTML += row;

	    
	 }
    }
  };
  xhttp.open("GET", url, true);
  xhttp.send();
}

function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {

    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}
