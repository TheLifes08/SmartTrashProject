var menu_state = false;
var latlng = new google.maps.LatLng(61.786035, 34.351448);
var options = {
	zoom: 15,
	center: latlng,
	mapTypeId: 'roadmap',
	mapTypeControlOptions: {
      mapTypeIds: ['roadmap', 'terrain', 'hybrid', 'satellite'],
      style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
    }
}
var map, geocoder;
var markers = [];
var widthDevice = $(window).width()

$(document).ready(function(){
	$("#menu-button").bind('click', function(){

    if ($(window).width() < 769){
        if(menu_state)
			$("#header-section").animate({'left': -widthDevice + 50 + "px"}, 300);
		else
			$("#header-section").animate({'left':'0'}, 300);
		menu_state = !menu_state;
    }
    else {
		if(menu_state)
			$("#header-section").animate({'left':'-250px'}, 300);
		else
			$("#header-section").animate({'left':'0px'}, 300);
		menu_state = !menu_state;
    }
	});
	
	$("#control_panel_map_button").bind('click', function(){
		alert("update");
		update_points();
	});
	
	$("#search-input").bind('focusin', function(){
		$("#search-input").css({"background-color":"white"}) 
    });
	$("#search-input").bind('focusout', function(){
		$("#search-input").css({"background-color":"lightgray"});
    });
	
	map = new google.maps.Map(document.getElementById("map-div"), options);
	geocoder = new google.maps.Geocoder();
	display_map_points(61.786035, 34.351448, 0.1);
});

function hide_panel(){
	if(menu_state){
    if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
            $("#header-section").animate({'left':'0'}, 300);
            menu_state = !menu_state;
        }
        else {
            $("#header-section").animate({'left': -widthDevice + 50 + "px"}, 300);
            menu_state = !menu_state;
        }
	}
    
}

function update_points(){
	var k = Number($('#radius-input').val());
	display_map_points(map.getCenter().lat(), map.getCenter().lng(), k);
}

function delete_map_points(){
	for(var i = 0; i < markers.length; i++)
		markers[i].setMap(null);
	markers = [];
}

function jump_to_point(a) {
    alert(markers[a].position);
    map.setCenter(markers[a].position);
}

function display_point(latlng, occupancy, j){
	geocoder.geocode({'latLng': latlng}, function(results, status){
		if (status == google.maps.GeocoderStatus.OK){
			var address = results[0].formatted_address;
			var infowindow = new google.maps.InfoWindow({
				content: '<div id="marker_contest"><div style="margin-bottom: 5px;"><strong>' + address + '</strong></div>Заполненость: ' + Number(occupancy) + '%</div>'
			});
			var marker = new google.maps.Marker({
				position: latlng,
				map: map,
				title: address,
				icon: {
					url: "images/markers/bin-marker.png",
					scaledSize: new google.maps.Size(50, 50)
				}
			});
			markers.push(marker);
			google.maps.event.addListener(marker, 'click', function() {
				infowindow.open(map, marker);
			});
			var block =`<li class="trashlist-object" onclick="jump_to_point(` + j + `)">
							<div class="trash-status">
								<p class="trash-status-percents" style="font-size: 12px;">` + Number(occupancy) + `%</p>
								<i class="fas fa-trash" style="color: #d33900"></i>
							</div>
                        
							<div class="trash-object-info">
								<div class="trash-object-address">
									<p>` + address + `</p>
								</div>
							</div>
						</li>`;
			$("#trashlist").append(block);
            j++;
		}
	});
}

function display_map_points(lat, lon, k){
	$("#trashlist").html("");
	
	$.ajax({
		method: 'POST',
		url: 'php/get_points_from_db.php',
		data: {'lat': lat, 'lon': lon, 'k': 0.1}
	}).done(function (data){
		delete_map_points();
		for(var i = 0; i < data.length; i++){ 
			var latlng = new google.maps.LatLng(data[i].lat, data[i].lon);
			var occupancy = data[i].occupancy;
			display_point(latlng, occupancy, i);
		}
	});
}

function change_city(city){
	alert(city);
	geocoder.geocode({'address': 'Россия, г. ' + city}, function(results, status){
		if (status == google.maps.GeocoderStatus.OK){
			map.setCenter(results[0].geometry.location);
			display_map_points(results[0].geometry.location.lat(), results[0].geometry.location.lng(), 0.1);
		}
	});
}