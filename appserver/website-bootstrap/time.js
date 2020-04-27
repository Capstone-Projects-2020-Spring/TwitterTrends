const time_svg_id= "time-svg";
const location_field_id = "location-search-box";

var citiesMap = new Map();

locationsUrl = 'http://18.214.197.203:5000/locations';

$.getJSON(locationsUrl, function (cityObjects) {

    for (let cityObj of cityObjects) {
        citiesMap.set(cityObj.city_id, cityObj.woeid);
    }

    citiesMap.set("United States", 23424977);
    citiesMap.set("World", 23424775);

    cityNamesArr = Array.from(citiesMap.keys())

    autocomplete(document.getElementById(location_field_id), cityNamesArr);
});




$(document).ready(function(){
    const default_csv = "https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/data_connectedscatter.csv";
    makeLineGraph(default_csv);

    document.getElementById('update-graph-btn').addEventListener('click', function () {
        let temporalURL = 'http://18.214.197.203:5000/temporal?trends=';
        let trendGroup = [];
        let time = document.getElementById('temporal-slider').value;
        let trend1 = document.getElementById('search1').value;
        let trend2 = document.getElementById('search2').value;
        let trend3 = document.getElementById('search3').value;
        let trend4 = document.getElementById('search4').value;
        let trend5 = document.getElementById('search5').value;

        if(!trend1 && !trend2 && !trend3  && !trend4  && !trend5 ){
            alert('No trends supplied')
        } else {

            if (trend1 !== '') {
                temporalURL += encodeURIComponent(trend1);
                trendGroup.push(trend1);
                if (trend2 !== '' || trend3 !== '' || trend4 !== '' || trend5 !== '') {
                    temporalURL += ',';
                }
            }
            if (trend2 !== '') {
                temporalURL += encodeURIComponent(trend2);
                trendGroup.push(trend2);
                if (trend3 !== '' || trend4 !== '' || trend5 !== '') {
                    temporalURL += ',';
                }
            }
            if (trend3 !== '') {
                temporalURL += encodeURIComponent(trend3);
                trendGroup.push(trend3);
                if (trend4 !== '' || trend5 !== '') {
                    temporalURL += ',';
                }
            }
            if (trend4 !== '') {
                temporalURL += encodeURIComponent(trend4);
                trendGroup.push(trend4);
                if (trend5 !== '') {
                    temporalURL += ',' + encodeURIComponent(trend5);
                    trendGroup.push(trend5);
                }
            }
        }


        const daysInMillis = time*24*60*60*1000;
        const displayIntervalDateObj = new Date(daysInMillis); //wrapping the # of milliseconds in a Date object might not be necessary

        const currDate = Date.now();

        const startDate = new Date(currDate - displayIntervalDateObj);

        var startDateStr = startDate.toISOString();
        //todo why isn't the backend just following the ISO standard for datetime values?
        startDateStr = startDateStr.replace("T", " ");
        //cuts off the milliseconds and the 'Z' at the end of the string
        const millisPeriodIndex = startDateStr.lastIndexOf(".");
        startDateStr = startDateStr.substring(0, millisPeriodIndex);

        startDateStr = encodeURIComponent(startDateStr);
        temporalURL += '&from=' + startDateStr; //YYYY-mm-dd HH:MM:SS
        //alert(temporalURL);

        const svgPresent = !! document.getElementById(time_svg_id);
        if (svgPresent) { d3.select("#" + time_svg_id).remove(); }

        let locationFieldElem = document.getElementById(location_field_id);
        let locationVal = locationFieldElem.value;
        if(locationVal && citiesMap.has(locationVal)) {
            locationWoeid = citiesMap.get(locationVal);
            temporalURL += "&woeid=" + locationWoeid;
        }


        makeLineGraph(temporalURL, trendGroup);
    });

    rangeSlider();
});


//slider function
let rangeSlider = function(){
    let slider = $('#rangeslider'),
        range = $('.slider'),
        value = $('.range-slider-value');

    slider.each(function(){

        value.each(function(){
            let value = $(this).prev().attr('value');
            $(this).html(value);
        });

        range.on('input', function(){
            if (this.value > 1){
                $(this).next(value).html(this.value + " Days");
            } else {
                $(this).next(value).html(this.value + " Day");
            }

        });
    });
};

//add another trend function
function addSearch() {

    let search2 = document.getElementById('search2');
	let search3 = document.getElementById('search3');
	let search4 = document.getElementById('search4');
	let search5 = document.getElementById('search5');
	let add = 2;
	let remove = 2;
	let test1 = document.getElementById('remove-trend-btn');
	let test2 = document.getElementById('add-trend-btn');

	if (search4.style.display == "block"){
	    search5.style.display = "block";
	    remove = 1;
	    add = 0;
    }
	else if(search3.style.display == "block"){
	    search4.style.display = "block";
	    remove = 1;
	}
	else if(search2.style.display == "block"){
	    search3.style.display = "block";
	    remove = 1;
	}
	else{
	    search2.style.display = "block";
	    remove = 1;
	}
	if (remove == 1){
	    test1.style.visibility = "visible";
	}
	if (add == 0){
	    test2.style.visibility = "hidden";
	}
}

function removeSearch() {

    let search2 = document.getElementById('search2');
    let search3 = document.getElementById('search3');
    let search4 = document.getElementById('search4');
    let search5 = document.getElementById('search5');
    let add = 2;
    let remove = 2;
    let test1 = document.getElementById('remove-trend-btn');
    let test2 = document.getElementById('add-trend-btn');

	if (search3.style.display === "none"){
	    search2.style.display = "none";
	    search2.value = "";
	    add = 1;
	    remove = 0;
    }
	else if(search4.style.display === "none"){
	    search3.style.display = "none";
	    search3.value = "";
	    add = 1;
	}
	else if(search5.style.display === "none"){
	    search4.style.display = "none";
	    search4.value = "";
	    add = 1;
	}
	else{
	    search5.style.display = "none";
	    search5.value = "";
	    add = 1;
	}

	if (remove === 0){
	    test1.style.visibility = "hidden";
	}
	if (add === 1){
	    test2.style.visibility = "visible";
	}
}

function makeLineGraph(csv_url, trendGroup) {
    let margin = {top: 20, right: 10, bottom: 10, left: 150},
        width = 800 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    let svg = d3.select("#linegraph")
        .append("svg")
        .attr("id", time_svg_id)
        .attr("viewBox", "0 0 900 500")
        .classed("svg-content-responsive", true)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    d3.csv(csv_url, function (data) {
        if (data.length === 0) {
            console.log("no data received for graphing. terminating graphing routine")
            return;
        }

        console.log(trendGroup.toString());

        //convert datetime strings to Date objects accurate to the hour
        for (let snapshot of data) {
            let jsDate = new Date(snapshot.datetime + "Z");
            jsDate.setMinutes(0);
            jsDate.setSeconds(0);
            jsDate.setMilliseconds(0);
            snapshot.datetime = jsDate;
        }

        const earliestDate = data.reduce(
            (min, snap) => snap.datetime <= min ? snap.datetime : min, data[0].datetime);

        let maxPopularity = 0;
        let latestHourOffset = 0;

        //format the data to get tuples
        let dataReady = trendGroup.map(function (grpName) {
            return {
                name: grpName,
                values: data.map(function (d) {
                    //todo try removing this Math.abs() wrapper, it shouldn't be doing anything
                    const millisDiff = Math.abs(d.datetime.getTime() - earliestDate.getTime());
                    const hoursDiff = millisDiff / (60 * 60 * 1000);

                    const popVal = +d[grpName];

                    if (popVal > maxPopularity) {
                        maxPopularity = popVal;
                    }
                    if (hoursDiff > latestHourOffset) {
                        latestHourOffset = hoursDiff;
                    }

                    return {time: hoursDiff, value: popVal};
                })
            };
        });

        let myColor = d3.scaleOrdinal()
            .domain(trendGroup)
            .range(d3.schemeSet2); //changes color schemes, schemePaired is nice too

        //x axis
        let x = d3.scaleLinear()
            .domain([-latestHourOffset, 0])//0,latestHourOffset])
            .range([0, width]);
        svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x));

        //y axis
        let y = d3.scaleLinear()
            .domain([0, maxPopularity])
            .range([height, 0]);
        svg.append("g")
            .call(d3.axisLeft(y));

        // text label for the x axis
        svg.append("text")
            .attr("transform",
                "translate(" + (width / 2) + " ," +
                (height + margin.top + 20) + ")")
            .style("text-anchor", "middle")
            .text("Time (Hours Prior to Present)");

        // text label for the y axis
        svg.append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 0 - 100)
            .attr("x", 0 - (height / 2))
            .attr("dy", "1em")
            .style("text-anchor", "middle")
            .text("Interactions");


        //lines
        let line = d3.line()
            .x(function (d) {
                return x(-latestHourOffset + d.time)
            })
            .y(function (d) {
                return y(+d.value)
            })
        svg.selectAll("myLines")
            .data(dataReady)
            .enter()
            .append("path")
            .attr("class", function (d) {
                return d.name
            })
            .attr("d", function (d) {
                return line(d.values)
            })
            .attr("stroke", function (d) {
                return myColor(d.name)
            })
            .style("stroke-width", 4)
            .style("fill", "none");

        //tooltip stuff
        let Tooltip = d3.select("#linegraph")
            .append("div")
            .style("opacity", 0)
            .attr("class", "tooltip");

        let mouseover = function (d) {
            Tooltip
                .style("opacity", 1)
                .style("z-index", 1);
        };
        let mousemove = function (d) {
            Tooltip
                .html("Value: " + d.value)
                .style("left", (d3.mouse(this)[0] + 30) + "px")
                .style("top", (d3.mouse(this)[1] + 40) + "px")
        };
        let mouseleave = function (d) {
            Tooltip
                .style("opacity", 0)
                .style("z-index", -1);
        };

        //points
        svg
            .selectAll("myDots")
            .data(dataReady)
            .enter()
            .append('g')
            .style("fill", function (d) {
                return myColor(d.name)
            })
            .attr("class", function (d) {
                return d.name
            })
            .selectAll("myPoints")
            .data(function (d) {
                return d.values
            })
            .enter()
            .append("circle")
            .attr("cx", function (d) {
                return x(-latestHourOffset + d.time)
            })
            .attr("cy", function (d) {
                return y(d.value)
            })
            .attr("r", 8)
            .on("mouseover", mouseover)
            .on("mousemove", mousemove)
            .on("mouseleave", mouseleave);

        //line labels to the right of the last data point
        svg
            .selectAll("myLabels")
            .data(dataReady)
            .enter()
            .append('g')
            .append("text")
            .attr("class", function (d) {
                return d.name
            })
            .datum(function (d) {
                return {name: d.name, value: d.values[d.values.length - 1]};
            }) // keep only the last value of each time series
            .attr("transform", function (d) {
                return "translate(" + x(-latestHourOffset + d.value.time) + "," + y(d.value.value) + ")";
            }) // Put the text at the position of the last point
            .attr("x", 12) // shift the text a bit more right
            .text(function (d) {
                return d.name;
            })
            .style("fill", function (d) {
                return myColor(d.name)
            })
            .style("font-size", 15);


        //this is for the legend labels, don't really need it because each individual line is labeled.
        //svg
        //.selectAll("myLegend")
        //.data(dataReady)
        //.enter()
        //.append('g')
        //.append("text")
        //.attr('x', function(d,i){return 30 + i*60})
        //.attr('y', 30)
        //.text(function(d) { return d.name; })
        //.style("fill", function(d){ return myColor(d.name) })
        //.style("font-size", 17)
        //.on("click", function(d){
        //   currentOpacity = d3.selectAll("." + d.name).style("opacity");
        //    d3.selectAll("." + d.name).transition().style("opacity", currentOpacity === 1 ? 0:1) //switch opacity
        //})
    });
}

//autocomplete
function autocomplete(inp, arr) {

  var currentFocus;

  inp.addEventListener("input", function(e) {
      var a, b, i, val = this.value;

      closeAllLists();
      if (!val) { return false;}
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

          b.addEventListener("click", function(e) {

              inp.value = this.getElementsByTagName("input")[0].value;

              closeAllLists();
          });
          a.appendChild(b);
        }
      }
  });

  inp.addEventListener("keydown", function(e) {
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


