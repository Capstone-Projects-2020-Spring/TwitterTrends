$(document).ready(function(){
    let margin = {top: 10, right: 10, bottom: 10, left: 100},
        width = 800 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    let svg = d3.select("#linegraph")
        .append("svg")
        .attr("viewBox", "0 0 900 500")
        .classed("svg-content-responsive", true)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    d3.csv("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/data_connectedscatter.csv", function(data) {
        //this stand-in csv is formatted time,valueA,valueB,valueC
        let allGroup = ["valueA", "valueB", "valueC"] //group names in the csv

        //format the data to get tuples
        let dataReady = allGroup.map( function(grpName) {
            return {
                name: grpName,
                values: data.map(function(d) {
                    //WHEN CSV TIME IS Y-M-D, do this to parse the time
                    //return {time : d3.timeParse("%Y-%m-%d")(d.time), value: +d[grpName]};
                    return {time: d.time, value: +d[grpName]};
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
            .domain( [0,20])
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
                d3.selectAll("." + d.name).transition().style("opacity", currentOpacity == 1 ? 0:1) //switch opacity
            })
    });




    document.getElementById('update-graph-btn').addEventListener('click', function () {
        let time = document.getElementById('temporal-slider').value;
        let trend1 = document.getElementById('search1').value;
        let trend2 = document.getElementById('search2').value;
        let trend3 = document.getElementById('search3').value;
        let trend4 = document.getElementById('search4').value;
        let trend5 = document.getElementById('search5').value;
        let temporalURL = 'http://18.214.197.203:5000/snapshot?trends=' + trend1 + ',' + trend2 + ',' + trend3 + ',' + trend4 + ',' + trend5 + '&from=' + time; //YYYY-mm-dd HH:MM:SS
        temporalCSV(temporalURL);
    });

    rangeSlider();
});


//slider function
var rangeSlider = function(){
    var slider = $('.rangeslider'),
        range = $('.slider'),
        value = $('.range-slider-value');

    slider.each(function(){

        value.each(function(){
            var value = $(this).prev().attr('value');
            $(this).html(value);
        });

        range.on('input', function(){
            $(this).next(value).html(this.value + " Weeks");
        });
    });
};

//add another trend function
function addSearch() {

    var search2 = document.getElementById('search2');
	var search3 = document.getElementById('search3');
	var search4 = document.getElementById('search4');
	var search5 = document.getElementById('search5');
	var add = 2;
	var remove = 2;
	var test1 = document.getElementById('remove-trend-btn');
	var test2 = document.getElementById('add-trend-btn');



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

    var search2 = document.getElementById('search2');
	var search3 = document.getElementById('search3');
	var search4 = document.getElementById('search4');
	var search5 = document.getElementById('search5');
	var add = 2;
	var remove = 2;
	var test1 = document.getElementById('remove-trend-btn');
	var test2 = document.getElementById('add-trend-btn');

	if (search3.style.display == "none"){
	    search2.style.display = "none";
	    add = 1;
	    remove = 0;
    }
	else if(search4.style.display == "none"){
	    search3.style.display = "none";
	    add = 1;
	}
	else if(search5.style.display == "none"){
	    search4.style.display = "none";
	    add = 1;
	}
	else{
	    search5.style.display = "none";
	    add = 1;
	}

	if (remove == 0){
	    test1.style.visibility = "hidden";
	}
	if (add == 1){
	    test2.style.visibility = "visible";
	}
}

function temporalCSV(temporalURL) {
    alert(temporalURL);
}