function chat(host,port,trip_id) {
    window.location.replace('http://'+window.location.host+'/chat');
};

function back(host,port,trip_id) {
 window.location.replace('http://'+window.location.host+'/show_trip'+'/'+localStorage.getItem("trip_id"));
};



