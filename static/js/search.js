var map;

function autocompleteCallback() {
	var card = document.getElementById('pac-card');
	var input = document.getElementById('pac-input');
	var rides = document.getElementById('ride-selector');
	var strictBounds = document.getElementById('strict-bounds-selector');
	
	map.controls[google.maps.ControlPosition.TOP_RIGHT].push(card);
	
	var autocomplete = new google.maps.places.Autocomplete(input);
	
	// Bind the map's bounds (viewport) property to the autocomplete object,
	// so that the autocomplete requests use the current map bounds for the
	// bounds option in the request.
	autocomplete.bindTo('bounds', map);
	
	var infowindow = new google.maps.InfoWindow();
	var infowindowContent = document.getElementById('infowindow-content');
	infowindow.setContent(infowindowContent);
	var marker = new google.maps.Marker({
	  map: map,
	  anchorPoint: new google.maps.Point(0, -29)
	});
	
	autocomplete.addListener('place_changed', function() {
	  infowindow.close();
	  marker.setVisible(false);
	  var place = autocomplete.getPlace();
	  if (!place.geometry) {
	    // User entered the name of a Place that was not suggested and
	    // pressed the Enter key, or the Place Details request failed.
	    window.alert("No details available for input: '" + place.name + "'");
	    return;
	  }
	
	  // If the place has a geometry, then present it on a map.
	  if (place.geometry.viewport) {
	    map.fitBounds(place.geometry.viewport);
	  } else {
	    map.setCenter(place.geometry.location);
	    map.setZoom(15);  // Why 17? Because it looks good.
	  }
	  marker.setPosition(place.geometry.location);
	  marker.setVisible(true);
	
	  submitLocation(myLatLng, place.geometry.location);
	  
	  var address = '';
	  if (place.address_components) {
	    address = [
	      (place.address_components[0] && place.address_components[0].short_name || ''),
	      (place.address_components[1] && place.address_components[1].short_name || ''),
	      (place.address_components[2] && place.address_components[2].short_name || '')
	    ].join(' ');
	  }
	
	  infowindowContent.children['place-icon'].src = place.icon;
	  infowindowContent.children['place-name'].textContent = place.name;
	  infowindowContent.children['place-address'].textContent = address;
	  infowindow.open(map, marker);
	});
	
	// Sets a listener on a radio button to change the type of ride requested. 
	
	function setupRideListener(id, rideType) {
		  var radioButton = document.getElementById(id);
		  radioButton.addEventListener('click', function() {
		    updateRideType(rideType);
		  });
		}
		
		setupRideListener('changeride-shared', 'shared');
		setupRideListener('changeride-regular', 'reg');
		setupRideListener('changeride-big', 'big');
		setupRideListener('changeride-fancy', 'fancy');
		
		document.getElementById('use-strict-bounds')
		    .addEventListener('click', function() {
		      console.log('Checkbox clicked! New state=' + this.checked);
		          autocomplete.setOptions({strictBounds: this.checked});
		        });

}

/*
 * Send the ride type. 
 * {
 * 	rideType:"something"
 *  }
 */
function updateRideType(ride){
	var xhr = new XMLHttpRequest();
	xhr.open("POST", "http://127.0.0.1:5000/api/ride/", true);
	
	var payload = JSON.stringify({
		"rideType": ride});
	xhr.setRequestHeader('Content-Type', 'application/json');
	xhr.send(payload);
	
	PICK = ride;
};

/*
 * Submit the location and ride type.
 * {
 * 	start_coord:(lat, lng),
 * 	end_coord:(lat,lng)
 *  }
 */
function submitLocation(start_coord, end_coord) {
	var xhr = new XMLHttpRequest();
	xhr.open("POST", "http://127.0.0.1:5000/api/seed/", true);
	
	var payload = JSON.stringify({
		"startCoord": (start_coord.lat(), start_coord.lng()),
		"endCoord": (end_coord.lat(), end_coord.lng())});
	xhr.setRequestHeader('Content-Type', 'application/json');
	xhr.send(payload);
};