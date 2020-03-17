$(document).ready(function(){
	$('.header').height($(window).height());
                        /*
                        ** Top Trends data from Philly:
                        ** http://18.214.197.203:5000/toptrends?woeid=2471217
                        ** Locations data:
                        ** http://18.214.197.203:5000/locations
                        ** CORS proxy:
                        ** https://cors-anywhere.herokuapp.com/
                        */
                            let markers;
                            let trend_data;
                            $.getJSON("https://cors-anywhere.herokuapp.com/http://18.214.197.203:5000/locations", function(data){
                                markers = data;
                            });

                            const width = 1000, height = 600;

                            const Tooltip = d3.select(".row")
                                .append("div")
                                .attr("class", "tooltip");

                            const mouseover = function(d){
                                Tooltip.style("opacity", 1)
                            };

                            const mousemove = function(d) {
                                Tooltip
                                    .html(d.city_id + "<br>" + "long: " + d.longitude + "<br>" + "lat: " + d.latitude)
                                    .style("left", (d3.mouse(this)[0] + 50) + "px")
                                    .style("top", (d3.mouse(this)[1]) + "px")
                            };

                            const mouseout = function(d){
                                Tooltip.style("opacity", 0)
                            };

                            const handleClick = function(d) {  // Add interactivity
                                document.querySelector('#bg-modal').style.display = 'flex';
                                document.querySelector('.top-trends-title').innerHTML = "Top Trends for " + d.city_id;
                                var trendUrl = "https://cors-anywhere.herokuapp.com/http://18.214.197.203:5000/toptrends?woeid=" + d.woeid;
                                trend_data = retrieveTrends(trendUrl);
                            };

                            let svg = d3.select("svg");

                            const usDataUrl = 'https://gist.githubusercontent.com/d3byex/65a128a9a499f7f0b37d/raw/176771c2f08dbd3431009ae27bef9b2f2fb56e36/us-states.json',
                                citiesDataUrl = 'https://gist.githubusercontent.com/d3byex/65a128a9a499f7f0b37d/raw/176771c2f08dbd3431009ae27bef9b2f2fb56e36/us-cities.csv';

                            /* Test Location Data
                            var markers = [
                                {name: 'Philadelphia', longitude: -75.165222, latitude: 39.952583}, <!-- Philadelphia -->
                                {name: 'Chicago', longitude: -87.632401, latitude: 41.883228}, <!-- Chicago -->
                                {name: 'Detroit', longitude: -83.045753, latitude: 42.331429}, <!-- Detroit -->
                                {name: 'Orlando', longitude: -81.378883, latitude: 28.538330}, <!-- Orlando -->
                                {name: 'Charlotte', longitude: -80.843124, latitude: 35.227085}, <!-- Charlotte -->
                                {name: 'Los Angeles', longitude: -118.4108, latitude: 34.0194}, <!-- Los Angeles -->
                                {name: 'San Diego', longitude: -117.135, latitude: 32.8153}, <!-- San Diego -->
                                {name: 'Seattle', longitude: -122.3509, latitude: 47.6205},  <!-- Seattle -->
                                {name: 'Houston', longitude: -95.3863, latitude: 29.7805}, <!-- Houston -->
                                {name: 'Vegas', longitude: -115.264, latitude: 36.2277}, <!-- Vegas -->
                                {name: 'Oklahoma City', longitude: -97.5137, latitude: 35.4671}  <!-- Oklahoma City -->
                            ];*/

                            queue()
                                .defer(d3.json, usDataUrl)
                                .defer(d3.csv, citiesDataUrl)
                                .await(function (error, states, cities) {
                                    let path = d3.geo.path();
                                    let projection = d3.geo.albersUsa()
                                        .translate([width / 2, height / 2])
                                        .scale([1200]);
                                    path.projection(projection);

                                    svg.append("g")
                                        .attr("class", "states")
                                        .selectAll('path')
                                        .data(states.features)
                                        .enter()
                                        .append('path')
                                        .attr('d', path);

                                    svg.append("g")
                                        .attr("class", "marker")
                                        .selectAll('myCircles')
                                        .data(markers)
                                        .enter()
                                        .append('circle')
                                        .each(function (d) {
                                            let location = projection([d.longitude, d.latitude]);
                                            d3.select(this).attr({
                                                cx: location[0], cy: location[1],
                                                r: 4
                                            });
                                        })
                                        .on('mouseover', mouseover)
                                        .on('mousemove', mousemove)
                                        .on('mouseout', mouseout)
                                        .on('click', handleClick)
                                });

                            document.querySelector('#close').addEventListener('click', function() {
                                document.querySelector('#bg-modal').style.display = "none";
                            });

                            //document.querySelector('.trend-1').addEventListener('click', getMoreInfo());
                            //document.querySelector('.trend-2').addEventListener('click', getMoreInfo());
                            //document.querySelector('.trend-3').addEventListener('click', getMoreInfo());
                            //document.querySelector('.trend-4').addEventListener('click', getMoreInfo());
                            //document.querySelector('.trend-5').addEventListener('click', getMoreInfo());

});

function retrieveTrends(trendUrl) {
	let trends = null;
	$.getJSON(trendUrl, function(data){
		trends = data;
	}).then(function() {
	    document.querySelector('.trend-1').innerHTML = "1. " + trends[0].trend_content;
	    document.querySelector('.trend-2').innerHTML = "2. " + trends[1].trend_content;
	    document.querySelector('.trend-3').innerHTML = "3. " + trends[2].trend_content;
	    document.querySelector('.trend-4').innerHTML = "4. " + trends[3].trend_content;
	    document.querySelector('.trend-5').innerHTML = "5. " + trends[4].trend_content;
	});
}

function getMoreInfo() {

}