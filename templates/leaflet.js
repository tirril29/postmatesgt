var map = L.map('map').setView([33.99279, -118.24379], 11);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpandmbXliNDBjZWd2M2x6bDk3c2ZtOTkifQ._QA7i5Mpkd_m30IGElHziw', {
  maxZoom: 18,
  attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
    '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
    'Imagery © <a href="http://mapbox.com">Mapbox</a>',
  id: 'mapbox.streets'
}).addTo(map);

//var latlngs = {L.latLng}
//var polyline = L.polyline(latlngs, {color: 'red'}).addTo(map);

// zoom the map to the polyline
//map.fitBounds(polyline.getBounds());

loadDoc("http://ec2-50-112-190-90.us-west-2.compute.amazonaws.com:5000/newest");

function loadDoc(url) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (xhttp.readyState == 4 && xhttp.status == 200) {
     var arr = xhttp.response;
     var json = JSON.parse(arr.toString());
        for(var i in json.brd){
		var pts = json.brd[i].best_effort.points;
		var latlngs = new Array();
		for(var j = 0; j < pts.length; j++) {
			latlngs.push(L.latLng(pts[j].point.lat, pts[j].point.lng));
		}
		var polyline = L.polyline(latlngs, {color: 'red'}).addTo(map);
		map.fitBounds(polyline.getBounds());
         }
    }
  };
  xhttp.open("GET", url, true);
  xhttp.send();
}


