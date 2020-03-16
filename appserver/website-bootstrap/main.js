$(document).ready(function(){
	$('.header').height($(window).height());
})

function retrieveTrends(trendUrl) {
	var trends = null;
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