 /* 
	 HackMIT 2017
	 Author: Andrew Tu
	 Github: github.com/drewtu2
 */

  // Global Variables (I know its shitty but its a hackathon)
  
  //var API_KEY = "AIzaSyAXrIT_Y0Diusx9r9osN1QgBdEY4m5yjcE";
  // printerList is an array of Printer Objects
  var map;
  var myLatLng
  var RADIUS = .125;

  $(document).ready(function(){
	
  });
  
/*
 * initGeolocation()
 * Starts the geolocation funcitons. 
 *  
 */  
  function initGeolocation() {
	  console.log("Hello world");	
	
    if (navigator && navigator.geolocation) {
    /*var watchId = navigator.geolocation.watchPosition(successCallback, 
                                                      errorCallback,
                                                      {enableHighAccuracy:true,timeout:60000,maximumAge:0});*/
    var watchId = navigator.geolocation.getCurrentPosition(successCallback,
			errorCallback);
    
    } else {
      console.log('Geolocation is not supported');
    }
  }
 
  function errorCallback() {
	  console.log("Error with locaiton tracking...")
  }
  
  /*
   * Callback function for the navigator.geolocation.watchPosition() function. 
   */
  function successCallback(position) {
	
    //myLatLng = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
	myLatLng = new google.maps.LatLng(42.340108, -71.088185);
    // To be run the first time the callback is called. (Creates the map object)
    if(map == undefined) {
      var myOptions = {
        zoom: 15,
        center: myLatLng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
      }
      map = new google.maps.Map(document.getElementById("map"), myOptions); 
    }
    //else map.panTo(myLatlng);
    plotHexagon(map, myLatLng, '#FF0000');
    generateNeighbors(map, myLatLng, RADIUS);
}
 
	/*
	 * Generates a hexagon and its neighbors on a map 
	 * 			1
	 *   	 *******    
	 *   6  *       *   2
	 *     *    *C   *  
	 *   5  *       *  3
	 *       *******
	 *          4
	 */
	function generateNeighbors(input_map, point, radius) {
		
		var conv = latLngDecConv(point.lat(), 30);
		console.log(conv);
		var neighbors = {
			p1 : new google.maps.LatLng({
				lat: point.lat() + (2 * radius * conv.mile2lat),
				lng: point.lng()}),
			p2 : new google.maps.LatLng({
				lat: point.lat() + (2 * radius * conv.diag_y), 	
				lng: point.lng() + (2 * radius * conv.diag_x)}),
			p3 : new google.maps.LatLng({
				lat: point.lat() - (2 * radius * conv.diag_y), 	
				lng: point.lng() + (2 * radius * conv.diag_x)}),
			p4 : new google.maps.LatLng({
				lat: point.lat() - (2 * radius * conv.mile2lat), 
				lng: point.lng()}),
			p5 : new google.maps.LatLng({
				lat: point.lat() - (2 * radius * conv.diag_y), 	
				lng: point.lng() - (2 * radius * conv.diag_x)}),
			p6 : new google.maps.LatLng({
				lat: point.lat() + (2 * radius * conv.diag_y), 	
				lng: point.lng() - (2 * radius * conv.diag_x)})
		}
		
		for (var neighbor in neighbors) {
			console.log(neighbor);
			plotHexagon(input_map, neighbors[neighbor], 'DarkGreen');
		}
		
	}
  
	/*
	 * Creates a hexagon of a given color from a set of points. Places on a given map. 
	 *     
	 */
  function plotHexagon(input_map, point, color) {
	  var hexagonVerticies = generateHexagon(point, RADIUS);
	  //console.log(hexagonVerticies);
	  var hexagon = new google.maps.Polygon({
          paths: hexagonVerticies,
          strokeColor: color,
          strokeOpacity: 0.8,
          strokeWeight: 2,
          fillColor: color,
          fillOpacity: 0.35
        });
	  
	  	hexagon.addListener('mouseover', darkenOpacity);
		hexagon.addListener('mouseout', lightenOpacity);
		
        hexagon.setMap(input_map);
  }
  
  
 /*
  * Given a point, return a list of points representing the vertexes of hexagon where the center to vertex is of a given length in miles.
  * 
  *  2	 *******   3
  *  	*       * 
  *  1 *    *C   * 4
  *  	*       *
  *  6   *******   5
  */
  function generateHexagon(point, radius) {
	  
	  // Create conversion constants
	  var conv = latLngDecConv(point.lat(), 60);
  	  console.log(conv);
	  var p1 = {lat: point.lat(), 							lng: point.lng() - (radius * conv.mile2long)};
	  var p2 = {lat: point.lat() + (radius * conv.diag_y), 	lng: point.lng() - (radius * conv.diag_x)};
	  var p3 = {lat: point.lat() + (radius * conv.diag_y), 	lng: point.lng() + (radius * conv.diag_x)};
	  var p4 = {lat: point.lat(), 							lng: point.lng() + (radius * conv.mile2long)};
	  var p5 = {lat: point.lat() - (radius * conv.diag_y), 	lng: point.lng() + (radius * conv.diag_x)};
	  var p6 = {lat: point.lat() - (radius * conv.diag_y), 	lng: point.lng() - (radius * conv.diag_x)};
	  
	  return [p1, p2, p3, p4, p5, p6]
  }
  
 /*
  * Given a latitude, return the number of miles in one degree of longitude
  */
  function longitude(latitude){
	return Math.cos(latitude * Math.PI/180)*69.172;
  }
 
  /*
   * Creates a constant object base on a given latitude that can be used to convert between lat/long and miles
   */
  function latLngDecConv(latitude, angle_to_zero) {
	  var l_mile2lat = 1/69;
	  var l_mile2long = 1/(longitude(latitude));
	  var l_diag_x = l_mile2long * Math.cos(angle_to_zero*Math.PI/180);
	  var l_diag_y = l_mile2lat * Math.sin(angle_to_zero*Math.PI/180);
	  
	  var convObj = {
		mile2lat: l_mile2lat,		
		mile2long: l_mile2long,
		diag_x: l_diag_x,
		diag_y: l_diag_y
	};
	
	  return convObj;
  };
  
  /*
   * Darkens the plot area moused over
   */
  function darkenOpacity(event) {
	  var polygonOptions = {fillOpacity: 0.8}
	  this.setOptions(polygonOptions);
  }
  
  /*
   * Lightens the plot area moused out
   */
  function lightenOpacity(event) {
	  var polygonOptions = {fillOpacity: 0.35};
	  this.setOptions(polygonOptions);
  }
  