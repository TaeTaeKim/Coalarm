google.charts.load("current", {packages:["corechart"]});
google.charts.setOnLoadCallback(drawChart);
function drawChart() {
var data = google.visualization.arrayToDataTable([
    ['ID', 'X', 'Y', 'Temperature'],
    ['',   80,  167,      120],
    ['',   79,  136,      130],
    ['',   78,  184,      50],
    ['',   72,  278,      230],
    ['',   81,  200,      210],
    ['',   72,  170,      100],
    ['',   68,  477,      80]
]);

var options = {
    hAxis: {title:'코로나 감염자수'},
    vAxis: {title: '백신 접종률'},
    colorAxis: {colors: ['yellow', 'red']}
};

var chart = new google.visualization.BubbleChart(document.getElementById('chart_div'));
chart.draw(data, options);
}