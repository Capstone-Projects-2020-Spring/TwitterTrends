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
        let trends = null;
        if(woeid){
            cityTrendUrl += woeid;
            $.getJSON(cityTrendUrl, function(data){
		        trends = data;
	        }).then(function() {
	            document.getElementById("city-title").innerHTML ="Top Trends for " + city;
                let table_body = document.createElement('tbody');
                document.getElementById("display-trends-table").replaceChild(table_body, document.getElementById("display-trends-table-body"));
                table_body.id = "display-trends-table-body";
                for(let i = 0; i < trends.length; i++){
                    let row = table_body.insertRow(i);
                    let cell1 = row.insertCell(0);
                    cell1.innerHTML = trends[i].trend_content;
                    let cell2 = row.insertCell(1);
                    cell2.innerHTML = trends[i].tweet_volume.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); // adds commas every third digit for numbers greater than 999
                }
            });
        } else {
            alert("Please provide a valid city name!");
        }

    });

    document.querySelector("#trends-display-tweets").addEventListener('click', function() {
        let tweetTrendUrl = 'http://18.214.197.203:5000/toptweets?query=';
        let trend = document.getElementById("tweet-trend").value;
        let tweets = null;
        if(trend){
            let tweetTrendUrlArg = encodeURIComponent(trend); // so we can search for trends with hashtags
            tweetTrendUrl += tweetTrendUrlArg;
            $.getJSON(tweetTrendUrl, function(data){
		        tweets = data;
	        }).then(function() {
	            document.getElementById("tweets-title").innerHTML = "Recent Tweets for " + trend;
                let table_body = document.createElement('tbody');
                document.getElementById("display-tweets-table").replaceChild(table_body, document.getElementById("display-tweets-table-body"));
                table_body.id = "display-tweets-table-body";
                for(let i = 0; i < tweets.length; i++){
                    let row = table_body.insertRow(i);
                    let cell1 = row.insertCell(0);
                    cell1.innerHTML = tweets[i].content;
                    let cell2 = row.insertCell(1);
                    cell2.innerHTML = tweets[i].username;
                    let cell3 = row.insertCell(2);
                    let t_date = (tweets[i].tweet_date).substring(0, 20);
                    cell3.innerHTML = t_date;
                    let cell4 = row.insertCell(3);
                    cell4.innerHTML = tweets[i].retweets.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); // adds commas every third digit for numbers greater than 999
                    let cell5 = row.insertCell(4);
                    cell5.innerHTML = tweets[i].likes.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); // adds commas every third digit for numbers greater than 999
                }
            });

        } else {
            alert("Please provide a trend!");
        }
    });

    document.querySelector("#trends-display-city-time").addEventListener('click', function() {
        let cityTrendUrl = 'http://18.214.197.203:5000/temporal_options?';
        let city = document.getElementById('myInput2').value;
        let woeid = citiesMap.get(city);
        if(city){ // check if a city was provided
            if(woeid){ // check if the provided city was valid (spelled correctly and in our map)
                document.getElementById("city-time-title").innerHTML = "Top Trends for " + city + " Over the Specified Dates"; // change the header of the table to match the city provided by the user
                cityTrendUrl += ('woeid=' + woeid); // append the woeid to the url before handling the date inputs
                handleDates(cityTrendUrl);
            } else { // if the city provided by the user doesn't return a woeid from our map(spelled wrong or not a city we have data for), let the user know it is not a valid option
                alert(city + " is not a valid option!")
            }
        } else { // if no city provided handle to date inputs without appending a woeid to the url
            handleDates(cityTrendUrl);
        }
    });
});

function fillTemporalTable(temporalCityUrl){
    let trends = null;
    alert(temporalCityUrl);
    $.getJSON(temporalCityUrl, function(data){
        trends = data;
    }).then(function() {
        let table_body = document.createElement('tbody');
        document.getElementById("display-timetrends-table").replaceChild(table_body, document.getElementById("display-timetrends-table-body"));
        table_body.id = "display-timetrends-table-body";
        if(trends.length > 50){
            trends = trends.slice(0, 50);
            populateCells(table_body, trends);
        } else {
            populateCells(table_body, trends);
        }
    });
}

function populateCells(table, trends) {
    for(let i = 0; i < trends.length; i++){
        let row = table.insertRow(i);
        let cell1 = row.insertCell(0);
        cell1.innerHTML = trends[i].trend_content;
        let cell2 = row.insertCell(1);
        cell2.innerHTML = cleanUpDateFormat(trends[i].first_date);
        let cell3 = row.insertCell(2);
        cell3.innerHTML = cleanUpDateFormat(trends[i].last_date); //(trends[i].last_date).substring(4, 19).replace(/-/g, " ").replace("T", " ");
        let cell4 = row.insertCell(3);
        cell4.innerHTML = trends[i].max_tweet_volume.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        let cell5 = row.insertCell(4);
        if(Number.isInteger(trends[i].avg_tweet_volume)){
            cell5.innerHTML = trends[i].avg_tweet_volume.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        } else {
            let avg = trends[i].avg_tweet_volume;
            avg = avg.toFixed(0);
            cell5.innerHTML = avg.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        }
        let cell6 = row.insertCell(5);
        let numLocIds = trends[i].locations.length;
        if(numLocIds > 5){
            cell6.innerHTML = numLocIds + " Locations";
        } else {
            cell6.innerHTML = trends[i].locations[0];
            for(let j = 1; j < numLocIds; j++){
                cell6.innerHTML += ", " + trends[i].locations[j];
            }
        }
    }
}

function handleDates(url) {
    let fromDate = document.getElementById('start').value;
    let toDate = document.getElementById('end').value;
    if(!fromDate && !toDate){ // if no dates are provided, don't need to add from or to parameters to the url
        fillTemporalTable(url);
    } else if(fromDate && !toDate){ // if a start date is provided but not an end date
        startButNoEndDate(fromDate, url);
    } else if(!fromDate && toDate){ // if an end date is provided but not a start date
        alert("If you enter a To Date, please also enter a From Date!");
    } else { // if both a start date and an end date is provided
        startAndEndDate(fromDate, toDate, url);
    }
}

function startAndEndDate(start, end, url) {
    let startDate = new Date(start);
    let startBoundary = new Date("02/29/2020");
    let endDate = new Date(end);
    let endBoundary = Date.now();

    if(startDate < startBoundary || endDate > endBoundary) {
        alert("Please enter valid  dates between March 1, 2020 and today!");
    } else if(startDate > endDate){
        alert("Please make sure that the end date is after the start date!");
    } else {
        let startDateStr = formatStart(startDate);
        url += '&from=' + startDateStr; //YYYY-mm-dd HH:MM:SS
        let endDateStr = formatEnd(endDate);
        url += '&to=' + endDateStr; //YYYY-mm-dd HH:MM:SS
        fillTemporalTable(url);
    }
}

function startButNoEndDate(start, url) {
    let startDate = new Date(start);
    let startBoundary = new Date("02/29/2020");

    if(startDate < startBoundary) {
        alert("Please enter a valid start date between March 1, 2020 and today!");
    } else {
        let startDateStr = formatStart(startDate);
        url += '&from=' + startDateStr; //YYYY-mm-dd HH:MM:SS
        fillTemporalTable(url);
    }
}

// function endButNoStartDate(end, url) {
//     let endDate = new Date(end);
//     let endBoundary = Date.now();
//
//     if(endDate > endBoundary) {
//         alert("Please enter a valid end date between March 1, 2020 and today!");
//     } else {
//         let endDateStr = formatEnd(endDate);
//         url += '&to=' + endDateStr; //YYYY-mm-dd HH:MM:SS
//         fillTemporalTable(url);
//     }
// }

function formatStart(start){
    let startDateStr = start.toISOString();
    startDateStr = startDateStr.replace("T", " ");
    //cuts off the milliseconds and the 'Z' at the end of the string
    let millisPeriodIndex = startDateStr.lastIndexOf(".");
    startDateStr = startDateStr.substring(0, millisPeriodIndex);

    startDateStr = encodeURIComponent(startDateStr);
    return startDateStr;
}

function formatEnd(end){
    let endDateStr = end.toISOString();
        endDateStr = endDateStr.replace("T", " ");
        //cuts off the milliseconds and the 'Z' at the end of the string
        let millisPeriodIndex = endDateStr.lastIndexOf(".");
        endDateStr = endDateStr.substring(0, millisPeriodIndex);

        endDateStr = encodeURIComponent(endDateStr);
        return endDateStr;
}

function cleanUpDateFormat(date) {
    let d = new Date(date);
    d = d.toString();
    d = d.substring(0, 24);
    d = d.replace("2020", "");
    return d;
}

