loadDoc("http://ec2-50-112-190-90.us-west-2.compute.amazonaws.com:5000/leaders");

function loadDoc(url) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (xhttp.readyState == 4 && xhttp.status == 200) {
     var arr = xhttp.response;
     var json = JSON.parse(arr.toString());     

     var count = 1;
	for(i in json.leaderboard){
	    var row = "<tr>";
	    row += "<td>" + count + "</td>";
	    var img = json.leaderboard[i][count].best_effort.courier.img_href;
	    row += "<td><img src=" + img + "></img></td>";
	    row += "<td>" + json.leaderboard[i][count].best_effort.courier.vehicle_type + "</td>";
	    row += "<td>" + json.leaderboard[i][count].name + "</td>";
	    row += "<td>" + json.leaderboard[i][count].best_effort.time + "</td>";
	    row += "<td>" + json.leaderboard[i][count].best_effort.start_time + "</td>";
            row += "<td>" + json.leaderboard[i][count].best_effort.end_time + "</td>";
	    document.getElementById("board").innerHTML += row;
	    count++;
	}	
    }
  };
  xhttp.open("GET", url, true);
  xhttp.send();
} 
