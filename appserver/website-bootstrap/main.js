$(document).ready(function(){
	$('.header').height($(window).height());
})

function retrieveTrends(trendUrl) {
	var trends = null;
	$.getJSON(trendUrl, function(data){
		trends = data;
	}).then(function() {
	    document.querySelector('.trend-1').innerHTML = trends[0].trend_content;
	    document.querySelector('.trend-2').innerHTML = trends[1].trend_content;
	    document.querySelector('.trend-3').innerHTML = trends[2].trend_content;
	    document.querySelector('.trend-4').innerHTML = trends[3].trend_content;
	    document.querySelector('.trend-5').innerHTML = trends[4].trend_content;
	});
}