function chat(host,port,trip_id) {
    window.location.replace('http://'+window.location.host+'/chat');
};

function back(host,port,trip_id) {
 window.location.replace('http://'+window.location.host+'/show_trip'+'/'+localStorage.getItem("trip_id"));
};

function sendMessage(host, port) {
    var btn = document.getElementById("btn");
    var txt = document.getElementById("txt");
    var driver = document.getElementById("driver")
    var p = document.getElementsByTagName("p");
    if(txt.value=="") {
        alert("Please don't send blank message!");
    }
    else {
        var user = document.createElement("p");
        user.style.backgroundColor="yellowgreen";
        user.style.clear="both";
        user.style.float="right";
        user.style.marginRight="15px";
        user.innerText=txt.value;
        driver.appendChild(user);

        // XMLHttpRequest Stuff
        localStorage.setItem("trip_ongoing", "true");
        // console.log("checkpoint 1");
        var xhr = new XMLHttpRequest();
        var url = "http://" + window.location.host + "/chat";
        xhr.open("post", url, true);
        // console.log("checkpoint 2");
        xhr.setRequestHeader("token", localStorage.getItem("token"))
        xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhr.send("txt="+txt.value);
        xhr.onreadystatechange = function() {
            // console.log("checkpoint 3");
            if (xhr.readyState == 4) {
                // console.log(xhr.responseText);
                if (xhr.responseText == "expired") {
                    window.alert("you need to login again")
                    window.location.replace("http://"+window.location.host+"/login");
                }
            }
        }
        txt.value="";
        user.scrollIntoView();
    }
}
