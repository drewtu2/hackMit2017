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
  var NUMBER_PRINTERS_REC = 3;
  var MAX_NUM_DESTINATIONS = 25;
  var printerStatus = 0;
  var global_dmResponse = {
	  "destinationAddresses": [],
	  "originAddresses": [],
	  "rows": [{"elements": []}]
	  }
  var countDmResponse = 0;
  
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
	
    myLatLng = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
	//myLatLng = new google.maps.LatLng(42.340108, -71.088185);
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
}