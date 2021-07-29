function login(host,port) {
    var xhr = new XMLHttpRequest();
    var url = 'http://'+host+':'+port+'/login';
    xhr.open('post', url);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    var user_name = document.getElementById("user_name").value;
    var password = document.getElementById("password").value;
    xhr.send("user_name="+user_name+'&'+"password="+password);
    xhr.onreadystatechange = function () {
        if (this.readyState == 4) {
            if(xhr.response != "Wrong password"){
                token = xhr.response;
                localStorage.setItem("token",token);
                localStorage.setItem("host",host);
                localStorage.setItem("port",port);
                window.location.replace('http://'+host+':'+port+'/booking');
            }
            else{
                window.alert("Wrong user_name or password")
                console.log("No token is gained");
            }
        }
    }
}
