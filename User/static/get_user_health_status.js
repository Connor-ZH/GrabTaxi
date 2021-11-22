var Health_status = {
    Normal : 1,
    Abnormal : 0,
};


function get_user_health_status() {
    window.refreshIntervalId = window.setInterval(startTimer, 1000);
};

function startTimer(){
    var xhr = new XMLHttpRequest();
    var url = 'http://'+window.location.host+'/get_user_health_status';
    xhr.open('post', url, true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.setRequestHeader('token', localStorage.getItem("token"));
    xhr.send("token="+localStorage.getItem("token"));
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            var data = JSON.parse(xhr.response);
            var pulse = data["pulse"];
            var temperature = data["temperature"];
            var updated_at = data["updated_at"];
            var status  = data["status"]; 
            var pulse_p = document.getElementById("pulse")
            var temperature_p = document.getElementById("temperature")
            var updated_at_p = document.getElementById("updated_at")
            temperature_p.innerText = "Body temperature: " + temperature;
            pulse_p.innerText = "Pulse rate : " + pulse;
            updated_at_p.innerText = "Updated at : " + updated_at;
            if (parseInt(status) == Health_status.Abnormal){
                clearInterval(window.refreshIntervalId);
                window.alert("Your health status is Abnormal!")
                location.replace('http://'+window.location.host+'/')
            }
        }
    };
};
