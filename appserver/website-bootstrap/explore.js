function autocomplete(inp, cities) {
    let arr = Array.from(cities.keys());
    var currentFocus;

    inp.addEventListener("input", function (e) {
        var a, b, i, val = this.value;

        closeAllLists();
        if (!val) {
            return false;
        }
        currentFocus = -1;

        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");

        this.parentNode.appendChild(a);

        for (i = 0; i < arr.length; i++) {

            if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {

                b = document.createElement("DIV");

                b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
                b.innerHTML += arr[i].substr(val.length);

                b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";

                b.addEventListener("click", function (e) {

                    inp.value = this.getElementsByTagName("input")[0].value;

                    closeAllLists();
                });
                a.appendChild(b);
            }
        }
    });

    inp.addEventListener("keydown", function (e) {
        var x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {

            currentFocus++;

            addActive(x);
        } else if (e.keyCode == 38) { //up

            currentFocus--;

            addActive(x);
        } else if (e.keyCode == 13) {

            e.preventDefault();
            if (currentFocus > -1) {

                if (x) x[currentFocus].click();
            }
        }
    });

    function addActive(x) {

        if (!x) return false;

        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length - 1);

        x[currentFocus].classList.add("autocomplete-active");
    }

    function removeActive(x) {

        for (var i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }

    function closeAllLists(elmnt) {

        var x = document.getElementsByClassName("autocomplete-items");
        for (var i = 0; i < x.length; i++) {
            if (elmnt != x[i] && elmnt != inp) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }

    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });
}

/*An array containing all the country names in the world:*/
var cities = ["New York","Los Angeles","Chicago","Houston","Phoenix","Philadelphia","San Antonio","Dallas","San Diego","San Jose","Detroit", "San Francisco","Jacksonville","Indianapolis","Austin","Columbus","Charlotte","Memphis","Baltimore","Boston","El Paso","Milwaukee","Denver","Seattle","Nashville","Washington","Las Vegas","Portland","Louisville","Oklahoma City","Tucson","Atlanta","Albuquerque","Kansas City","Fresno","Sacramento","Long Beach","Mesa","Omaha","Cleveland","Virginia Beach","Miami","Raleigh","Minneapolis","Colorado Springs","Honolulu","St. Louis","Tampa","New Orleans","Cincinnati","Pittsburgh","Greensboro","Norfolk","Orlando","Birmingham","Baton Rouge","Richmond","Salt Lake City","Jackson","Tallahassee","Providence","New Haven","Harrisburg"];


var citiesMap = new Map();

locationsUrl = 'http://18.214.197.203:5000/locations';

$.getJSON(locationsUrl, function (cityObjects) {

    for (let cityObj of cityObjects) {
        citiesMap.set(cityObj.city_id, cityObj.woeid);
    }

    citiesMap.set("United States", 23424977);
    citiesMap.set("World", 23424775);

    autocomplete(document.getElementById("myInput"), citiesMap);
    autocomplete(document.getElementById("myInput2"), citiesMap);
});

$(document).ready(function(){
    document.querySelector("#trends-display-city").addEventListener('click', function() {
        let cityTrendUrl = 'http://18.214.197.203:5000/toptrends?woeid=';
        let city = document.getElementById('myInput').value;
        let woeid = citiesMap.get(city);
        if(woeid){
            cityTrendUrl += woeid;
            alert(cityTrendUrl);
        } else {
            alert("Please provide a valid city name!");
        }

    });

    document.querySelector("#trends-display-tweets").addEventListener('click', function() {
        let tweetTrendUrl = 'http://18.214.197.203:5000/toptweets?query=';
        let trend = document.getElementById("tweet-trend").value;
        if(trend){
            tweetTrendUrl += trend;
            alert(tweetTrendUrl);
        } else {
            alert("Please provide a trend!");
        }
    });

    document.querySelector("#trends-display-city-time").addEventListener('click', function() {
        let cityTrendUrl = 'http://18.214.197.203:5000/temporal?woeid=';
        let city = document.getElementById('myInput2').value;
        let woeid = citiesMap.get(city);
        cityTrendUrl += woeid;

        if(woeid){
            cityTrendUrl += woeid;
            let fromDate = document.getElementById('start').value;
            let toDate = document.getElementById('end').value;
            if(!fromDate || !toDate){
                alert("Please provide start and ends dates!");
            } else {
                let startDate = new Date(fromDate);
                let startBoundary = new Date("02/29/2020");
                let endDate = new Date(toDate);
                let endBoundary = Date.now();

                if(startDate < startBoundary || endDate > endBoundary) {
                    alert("Please enter valid  dates between March 1, 2020 and today!");
                } else if(startDate > endDate){
                    alert("Please make sure end date is after start date!");
                } else {
                    let startDateStr = startDate.toISOString();
                    startDateStr = startDateStr.replace("T", " ");
                    //cuts off the milliseconds and the 'Z' at the end of the string
                    let millisPeriodIndex = startDateStr.lastIndexOf(".");
                    startDateStr = startDateStr.substring(0, millisPeriodIndex);

                    startDateStr = encodeURIComponent(startDateStr);
                    cityTrendUrl += '&from=' + startDateStr; //YYYY-mm-dd HH:MM:SS

                    let endDateStr = endDate.toISOString();
                    endDateStr = endDateStr.replace("T", " ");
                    //cuts off the milliseconds and the 'Z' at the end of the string
                    millisPeriodIndex = endDateStr.lastIndexOf(".");
                    endDateStr = endDateStr.substring(0, millisPeriodIndex);

                    endDateStr = encodeURIComponent(endDateStr);
                    cityTrendUrl += '&to=' + endDateStr; //YYYY-mm-dd HH:MM:SS

                    alert(cityTrendUrl);
                }
            }
        } else {
            alert("Please provide a valid city name!");
        }
    });
});


