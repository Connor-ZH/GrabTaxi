function myMap() {
    var mapProp= {
      center:new google.maps.LatLng(1.3+parseFloat(localStorage.getItem('lati_pickup'))/1000,103.6+parseFloat(localStorage.getItem('long_pickup'))/300),
      zoom:12,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    window.map = new google.maps.Map(document.getElementById("googleMap"),mapProp);
    lat = parseFloat(localStorage.getItem('lati_pickup'))/1000+1.3001
    lng = parseFloat(localStorage.getItem('long_pickup'))/300+103.6001
    var myLatLng = new google.maps.LatLng(lat, lng);
    var marker = new google.maps.Marker({
      position: myLatLng,
      title: "Hello World!",
      color: "white",
      label: "User",
    });
    marker.setMap(map);  
}
