const time_svg_id= "time-svg";

$(document).ready(function(){
    const default_csv = "https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/data_connectedscatter.csv";
    makeLineGraph(default_csv);

    document.getElementById('update-graph-btn').addEventListener('click', function () {
        let temporalURL = 'http://18.214.197.203:5000/temporal?trends=';
        let length = temporalURL.length;
        let time = document.getElementById('temporal-slider').value;
        let trend1 = document.getElementById('search1').value;
        let trend2 = document.getElementById('search2').value;
        let trend3 = document.getElementById('search3').value;
        let trend4 = document.getElementById('search4').value;
        let trend5 = document.getElementById('search5').value;

        if(trend1 === '' && trend2 === '' && trend3 === '' && trend4 === '' && trend5 === ''){
            alert('No trends supplied')
        } else {

            if (trend1 !== '') {
                temporalURL += encodeURIComponent(trend1);
                if (trend2 !== '' || trend3 !== '' || trend4 !== '' || trend5 !== '') {
                    temporalURL += ',';
                }
            }
            if (trend2 !== '') {
                temporalURL += encodeURIComponent(trend2);
                if (trend3 !== '' || trend4 !== '' || trend5 !== '') {
                    temporalURL += ',';
                }
            }
            if (trend3 !== '') {
                temporalURL += encodeURIComponent(trend3);
                if (trend4 !== '' || trend5 !== '') {
                    temporalURL += ',';
                }
            }
            if (trend4 !== '') {
                temporalURL += encodeURIComponent(trend4);
                if (trend5 !== '') {
                    temporalURL += ',' + encodeURIComponent(trend5);
                }
            }
        }
        temporalURL += '&days=0&hours=3';
        //todo temporalURL += '&from=' + time; //YYYY-mm-dd HH:MM:SS
        //alert(temporalURL);

        const svgPresent = !! document.getElementById(time_svg_id)
        if (svgPresent) { d3.select("#" + time_svg_id).remove(); }


        makeLineGraph(temporalURL);
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
            $(this).next(value).html(this.value + " Weeks");
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

function makeLineGraph(csv_url) {
    let margin = {top: 10, right: 10, bottom: 10, left: 100},
        width = 800 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    let svg = d3.select("#linegraph")
        .append("svg")
        .attr("id", time_svg_id)
        .attr("viewBox", "0 0 900 500")
        .classed("svg-content-responsive", true)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    d3.csv(csv_url, function(data) {
        if (data.length === 0) {
            console.log("no data received for graphing. terminating graphing routine")
            return;
        }

        let allGroup = []; //group names in the csv

        let trend1 = document.getElementById('search1').value;
        if(trend1) { allGroup.push(trend1);}
        let trend2 = document.getElementById('search2').value;
        if(trend2) { allGroup.push(trend2);}
        let trend3 = document.getElementById('search3').value;
        if(trend3) { allGroup.push(trend3);}
        let trend4 = document.getElementById('search4').value;
        if(trend4) { allGroup.push(trend4);}
        let trend5 = document.getElementById('search5').value;
        if(trend5) { allGroup.push(trend5);}

        console.log(allGroup.toString());

        //convert datetime strings to Date objects accurate to the hour
        for (var snapshot of data) {
            jsDate = new Date(snapshot.datetime+"Z");
            jsDate.setMinutes(0);
            jsDate.setSeconds(0);
            jsDate.setMilliseconds(0);
            snapshot.datetime = jsDate;
        }

        const earliestDate = data.reduce(
            (min, snap) => snap.datetime <= min ? snap.datetime : min , data[0].datetime);

        var maxPopularity= 0;

        //format the data to get tuples
        let dataReady = allGroup.map( function(grpName) {
            return {
                name: grpName,
                values: data.map(function(d) {
                    const millisDiff = Math.abs(d.datetime.getTime() - earliestDate.getTime());
                    const hoursDiff = millisDiff/(60*60*1000);

                    const popVal = +d[grpName];

                    if (popVal > maxPopularity) {
                        maxPopularity = popVal;
                    }


                    return {time : hoursDiff, value: popVal};
                })
            };
        });

        let myColor = d3.scaleOrdinal()
            .domain(allGroup)
            .range(d3.schemePaired); //changes color schemes, schemeSet2 is nice too

        //x axis
        let x = d3.scaleLinear()
            .domain([0,10])
            .range([ 0, width ]);
        svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x));

        //y axis
        let y = d3.scaleLinear()
            .domain( [0, maxPopularity])
            .range([ height, 0 ]);
        svg.append("g")
            .call(d3.axisLeft(y));

        //lines
        let line = d3.line()
            .x(function(d) { return x(+d.time) })
            .y(function(d) { return y(+d.value) })
        svg.selectAll("myLines")
            .data(dataReady)
            .enter()
            .append("path")
            .attr("class", function(d){ return d.name })
            .attr("d", function(d){ return line(d.values) } )
            .attr("stroke", function(d){ return myColor(d.name) })
            .style("stroke-width", 4)
            .style("fill", "none");

        //tooltip stuff
        let Tooltip = d3.select("#linegraph")
            .append("div")
            .style("opacity", 0)
            .attr("class", "tooltip");

        let mouseover = function(d) {
            Tooltip
                .style("opacity", 1)
        };
        let mousemove = function(d) {
            Tooltip
                .html("Value: " + d.value)
                .style("left", (d3.mouse(this)[0]+100) + "px")
                .style("top", (d3.mouse(this)[1]) + "px")
        };
        let mouseleave = function(d) {
            Tooltip
                .style("opacity", 0)
        };

        //points
        svg
            .selectAll("myDots")
            .data(dataReady)
            .enter()
            .append('g')
            .style("fill", function(d){ return myColor(d.name) })
            .attr("class", function(d){ return d.name })
            .selectAll("myPoints")
            .data(function(d){ return d.values })
            .enter()
            .append("circle")
            .attr("cx", function(d) { return x(d.time) } )
            .attr("cy", function(d) { return y(d.value) } )
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
            .attr("class", function(d){ return d.name })
            .datum(function(d) { return {name: d.name, value: d.values[d.values.length - 1]}; }) // keep only the last value of each time series
            .attr("transform", function(d) { return "translate(" + x(d.value.time) + "," + y(d.value.value) + ")"; }) // Put the text at the position of the last point
            .attr("x", 12) // shift the text a bit more right
            .text(function(d) { return d.name; })
            .style("fill", function(d){ return myColor(d.name) })
            .style("font-size", 15);

        //interactivity, line disappears on click of name in upper left
        //the failsafe, just in case adding new trends doesn't work, can just get top however many trends up front and change opacity to fulfill that feature requirement
        svg
            .selectAll("myLegend")
            .data(dataReady)
            .enter()
            .append('g')
            .append("text")
            .attr('x', function(d,i){ return 30 + i*60})
            .attr('y', 30)
            .text(function(d) { return d.name; })
            .style("fill", function(d){ return myColor(d.name) })
            .style("font-size", 17)
            .on("click", function(d){
                currentOpacity = d3.selectAll("." + d.name).style("opacity");
                d3.selectAll("." + d.name).transition().style("opacity", currentOpacity === 1 ? 0:1) //switch opacity
            })
    });
}