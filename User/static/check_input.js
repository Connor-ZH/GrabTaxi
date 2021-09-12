const submitHandler = document.querySelector(".submit");

// check point
console.log("checkpoint");
console.log(submitHandler);

if (submitHandler === null) {
    console.log("submitHandler is null");
} else {
    submitHandler.addEventListener("click", checkinput);
    function checkinput() {
        const long_of_pickup = Number(document.querySelector(".long_of_pickup").value);
        const lati_of_pickup = Number(document.querySelector(".lati_of_pickup").value);
        const long_of_dropoff = Number(document.querySelector(".long_of_dropoff").value);
        const lati_of_dropoff = Number(document.querySelector(".lati_of_dropoff").value);

        var checkpoint = 1;

        if (isNaN(long_of_pickup) || isNaN(lati_of_pickup) || isNaN(long_of_dropoff) || isNaN(lati_of_dropoff)) {
            checkpoint = 0;
        }

        if (long_of_pickup < 0 || long_of_pickup > 90 ) {
            checkpoint = 0;
        }

        if (lati_of_pickup < 0 || lati_of_pickup > 90 ) {
            checkpoint = 0;
        }

        if (long_of_dropoff < 0 || long_of_dropoff > 90 ) {
            checkpoint = 0;
        }

        if (lati_of_dropoff < 0 || lati_of_dropoff > 90 ) {
            checkpoint = 0;
        }

        if (checkpoint === 0) {
            alert("The Pickup & Dropoff Location Shall be a Valid Number within [0, 90]!")
        }
    }
}