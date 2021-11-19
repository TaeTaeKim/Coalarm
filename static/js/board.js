google.charts.load("current", {packages:["corechart"]});
google.charts.setOnLoadCallback(drawChart);
function drawChart() {
    const data = new google.visualization.DataTable();
    data.addColumn('string', '대륙');
    data.addColumn('number', '총 확진자');
    data.addColumn('number', '백신 접종률');
    $.ajax({
        url:'/boarddata',
        type:'GET',
        datatype:'json',
        async:false,
        success:function(res){
            let chartdata = res.boarddata.chart_data;
            chartdata.forEach((el)=>{
                data.addRow([
                    el.continent,
                    el.data[0],
                    el.data[1]
                ])
            })
        },
        error:function(){
            alert('통계 데이터 로드 실패')
        }
    })

    var options = {
        hAxis: {title:'코로나 감염자수'},
        vAxis: {title: '백신 접종률'},
        colorAxis: {colors: ['yellow', 'red']}
};

var chart = new google.visualization.BubbleChart(document.getElementById('chart_div'));
chart.draw(data, options);
}




$.ajax({
    url:'/boarddata',
    type:'GET',
    datatype:'json',
    async:false,
    success:function(res){
        let data = res.boarddata.merged
        
        for(i=0;i<=data.length;i++){
            $('#board-data').append(`
            <tr>
                <td>${data[i]["country_x"]}</td>
                <td>${data[i]["total_cases"]}<span class="new-statistic">(${data[i]["new_cases"]})</span></td>
                <td>${data[i]["total_deaths"]}<span class="new-statistic">(${data[i]["new_deaths"]})</span></td>
                <td>${data[i]["total_recovered"]}<span class="new-statistic">(${data[i]["new_recovered"]})</span></td>
                <td>${data[i]["critical_ratio"]}</td>
                <td>${data[i]["recovered_ratio"]}</td>
                <td>${data[i]["total_caeses_per_1million_population"]}</td>
                <td>${data[i]["vaccinated"]}</td>
                <td>${data[i]["fully_vaccinated"]}</td>
            </tr>
        `)
        }
    }
})