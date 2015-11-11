// Url for extracting the time series data
var url = "http://informatics.environment.scotland.gov.uk/SpotfireWeb/ViewAnalysis.aspx?file=%2fProjects%2fSE+Web+(LIFE)%2fClimate+trends%2fStandalone%2fClimate+Trends+Application&waid=b1c065a9ea8a78159ef9a-22190685cfa82c";

// paste lines 4-16 on a google-chrome developer console for the url above
// in order to scrape data points from climate timeseries in to the variable master
// then just copy(Master) and paste in to a text file
var Master = [];

// function that uses the tooltip in order to extract the dat from the graph
function ggt(){
	console.log('run');
	a = document.getElementsByClassName('Tooltip');
	if(a.length > 0){
		Master.push(a[0].innerHTML);;}
	}

// timer every
window.setInterval(function(){
  ggt();
}, 50);
