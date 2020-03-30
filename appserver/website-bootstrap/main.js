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
	let trend_data, centered;
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
		let trendUrl = "http://18.214.197.203:5000/toptrends?woeid=" + d.woeid;
		trend_data = retrieveTrends(trendUrl);
	};

	const mapsvg = d3.select("#mapsvg")
		.attr("width", width)
		.attr("height", height);


	const usDataUrl = 'https://gist.githubusercontent.com/d3byex/65a128a9a499f7f0b37d/raw/176771c2f08dbd3431009ae27bef9b2f2fb56e36/us-states.json',
		citiesDataUrl = 'https://gist.githubusercontent.com/d3byex/65a128a9a499f7f0b37d/raw/176771c2f08dbd3431009ae27bef9b2f2fb56e36/us-cities.csv',
		locationsUrl = 'http://18.214.197.203:5000/locations';

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
		.defer(d3.json, locationsUrl)
		.await(function (error, states, cities, locations) {
			let path = d3.geo.path();
			let projection = d3.geo.albersUsa()
				.translate([width / 2, height / 2])
				.scale([1200]);
			path.projection(projection);

			mapsvg.append("g")
				.attr("class", "states")
				.selectAll('path')
				.data(states.features)
				.enter()
				.append('path')
				.attr('stateName', function(d){return d.properties.name;})
				.attr('d', path)
				.attr('cursor', 'pointer')
				.on('click', function clicked(d)
				{
					let x, y, zoomLevel;

					if (d && centered !== d) {
						let centroid = path.centroid(d);
						x = centroid[0];
						y = centroid[1];
						zoomLevel = 4;
						centered = d;
					} else {
						x = width / 2;
						y = height / 2;
						zoomLevel = 1;
						centered = null;
					}

					mapsvg.selectAll("path")
						.classed("active", centered && function(d) { return d === centered; });

					mapsvg.transition()
						.duration(1000)
						.style("stroke-width", 1.5 / zoomLevel + "px")
						.attr("transform",
							"translate(" + width / 2  + "," + height / 2 + ")scale(" + zoomLevel + ")translate(" + -x + "," + -y + ")");
				});

			mapsvg.append("g")
				.attr("class", "marker")
				.selectAll('myCircles')
				.data(locations)
				.enter()
				.append('circle')
				.attr('cityName', function(d){return d.city_id;})
				.attr('woeid', function(d){return d.woeid;})
				.each(function (d) {
					let location = projection([d.longitude, d.latitude]);
					d3.select(this).attr({
						cx: location[0], cy: location[1],
						r: 5
					});
				})
				.on('mouseover', mouseover)
				.on('mousemove', mousemove)
				.on('mouseout', mouseout)
				.on('click', handleClick)
		});

	document.querySelector('#close').addEventListener('click', function() {
		document.querySelector('#bg-modal').style.display = "none";
		document.getElementById('trend-1').innerText = '';
		document.getElementById('trend-2').innerText = '';
		document.getElementById('trend-3').innerText = '';
		document.getElementById('trend-4').innerText = '';
		document.getElementById('trend-5').innerText = '';
	});
	getStartingNews();
});

function retrieveTrends(trendUrl) {
	let trends = null;
	$.getJSON(trendUrl, function(data){
		trends = data;
	}).then(function() {
	    document.querySelector('#trend-1').innerHTML = trends[0].trend_content;
        document.getElementById('trend-1').addEventListener('click', getMoreInfo);
	    document.querySelector('#trend-2').innerHTML = trends[1].trend_content;
	    document.getElementById('trend-2').addEventListener('click', getMoreInfo);
	    document.querySelector('#trend-3').innerHTML = trends[2].trend_content;
	    document.getElementById('trend-3').addEventListener('click', getMoreInfo);
	    document.querySelector('#trend-4').innerHTML = trends[3].trend_content;
	    document.getElementById('trend-4').addEventListener('click', getMoreInfo);
	    document.querySelector('#trend-5').innerHTML = trends[4].trend_content;
	    document.getElementById('trend-5').addEventListener('click', getMoreInfo);

	});
}

function getMoreInfo() {
    let trend = this.innerHTML;
    let trend_news = null;
    orig_trend= trend
    if (trend.startsWith('#')){
        trend = trend.substring(1);
    }
    let newsURL = "http://18.214.197.203:5000/trend_news?trend=" + trend;
    $.getJSON(newsURL, function (news) {
        trend_news = news;

        document.getElementById('article-title-1').innerHTML = trend_news[0].title;
        let blurb = trend_news[0].description;
        blurb = blurb.slice(0, 150) + '...';
        document.getElementById('article-blurb-1').innerHTML = blurb;
        document.getElementById('article-url-1').setAttribute("href", trend_news[0].link_url);
        document.getElementById('article-url-1').innerText = 'Read More!';

        document.getElementById('article-title-2').innerHTML = trend_news[1].title;
        blurb = trend_news[1].description;
        blurb = blurb.slice(0, 150) + '...';
        document.getElementById('article-blurb-2').innerHTML = blurb;
        document.getElementById('article-url-2').setAttribute("href", trend_news[1].link_url);
        document.getElementById('article-url-2').innerText = 'Read More!';

        document.getElementById('article-title-3').innerHTML = trend_news[2].title;
        blurb = trend_news[2].description;
        blurb = blurb.slice(0, 150) + '...';
        document.getElementById('article-blurb-3').innerHTML = blurb;
        document.getElementById('article-url-3').setAttribute("href", trend_news[2].link_url);
        document.getElementById('article-url-3').innerText = 'Read More!';
    });

    let tweetsURL = "http://18.214.197.203:5000/toptweets?query=" + orig_trend;
    $.getJSON(tweetsURL, function (tweets) {
    	var most_retweeted_tweet = null;
    	var max_retweets=0;
		var most_liked_tweet = null;
		var second_most_liked_tweet = null;
    	var max_likes=0;
		for (const tweet of tweets) {
			if (tweet.retweets >= max_retweets) {
				most_retweeted_tweet = tweet;
				max_retweets = tweet.retweets;
			}
			if (tweet.likes >= max_likes) {
				second_most_liked_tweet = most_liked_tweet;
				most_liked_tweet = tweet;
				max_likes = tweet.likes;
			}
		}

		if (most_retweeted_tweet === most_liked_tweet) {
			most_liked_tweet = second_most_liked_tweet;
		}

		document.getElementById('tweet-author-1').innerHTML = "Author id" + most_retweeted_tweet.user_id;
		document.getElementById('tweet-content-1').innerHTML = most_retweeted_tweet.content;
		document.getElementById("tweet-date-1").innerHTML = most_retweeted_tweet.tweet_date;
		//todo? document.getElementById('tweet-url-1').setAttribute("href", most_retweeted_tweet.?);

		document.getElementById('tweet-author-2').innerHTML = "Author id" + most_liked_tweet.user_id;
		document.getElementById('tweet-content-2').innerHTML = most_liked_tweet.content;
		document.getElementById("tweet-date-2").innerHTML = most_liked_tweet.tweet_date;
		//todo? document.getElementById('tweet-url-1').setAttribute("href", most_retweeted_tweet.?);
	});

}

function getStartingNews() {
	let world_trend_url = "http://18.214.197.203:5000/toptrends?woeid=1";
	let world_news_url = "http://18.214.197.203:5000/trend_news?trend=";
	let world_trends = null;
	let top_world_trend = null;
	let world_news = null;

	$.getJSON(world_trend_url, function(data){
		world_trends = data;
	}).then(function() {
		top_world_trend = world_trends[0].trend_content;
		if (top_world_trend.startsWith('#')){
        	top_world_trend = top_world_trend.substring(1);
		}
		world_news_url = world_news_url + top_world_trend;
		$.getJSON(world_news_url, function (news) {
			world_news = news;

			document.getElementById('article-title-1').innerHTML = world_news[0].title;
			let blurb = world_news[0].description;
			blurb = blurb.slice(0, 150) + '...';
			document.getElementById('article-blurb-1').innerHTML = blurb;
			document.getElementById('article-url-1').setAttribute("href", world_news[0].link_url);
			document.getElementById('article-url-1').innerText = 'Read More!';

			document.getElementById('article-title-2').innerHTML = world_news[1].title;
			blurb = world_news[1].description;
			blurb = blurb.slice(0, 150) + '...';
			document.getElementById('article-blurb-2').innerHTML = blurb;
			document.getElementById('article-url-2').setAttribute("href", world_news[1].link_url);
			document.getElementById('article-url-2').innerText = 'Read More!';

			document.getElementById('article-title-3').innerHTML = world_news[2].title;
			blurb = world_news[2].description;
			blurb = blurb.slice(0, 150) + '...';
			document.getElementById('article-blurb-3').innerHTML = blurb;
			document.getElementById('article-url-3').setAttribute("href", world_news[2].link_url);
			document.getElementById('article-url-3').innerText = 'Read More!';
		});
	});
}