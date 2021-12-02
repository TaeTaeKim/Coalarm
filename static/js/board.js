google.charts.load("current", {packages:["corechart"]});
google.charts.setOnLoadCallback(drawChart);
function drawChart() {
    const data = new google.visualization.DataTable();
    data.addColumn('string', '대륙이름');
    data.addColumn('number', '코로나 발생률');
    data.addColumn('number', '백신 접종률');
    data.addColumn('string', '대륙');
    $.ajax({
        url:'/boarddata',
        type:'GET',
        datatype:'json',
        async:false,
        success:function(res){
            let chartdata = res.chart_data;
            chartdata.forEach((el)=>{
                data.addRow([
                    el.continent,
                    el.data[0],
                    el.data[1],
                    el.continent
                ])
            })
        },
        error:function(){
            alert('통계 데이터 로드 실패')
            window.location.reload();
        }
    })

    var options = {
        colorAxis: {colors: ['yellow', 'red']},
        chartArea:{width:'90%',height:'80%'},
        vAxis:{title: '백신 접종률',maxValue:100,minValue:0},
        hAxis:{title:'코로나 발생률',minValue:0,maxValue:150000},
        legend:'none'
};

var chart = new google.visualization.BubbleChart(document.getElementById('chart_div'));
chart.draw(data, options);
}

// 초기 실행시  개수 20개를 띄움 전체국가를 띄움
let num =30
let board_continent = 'all'
let board_length = 0
//테이블을 불러오는 함수
function load_board(num,conti){
    $('#board-data').html("")
    $.ajax({
        url:'/boarddata',
        type:'GET',
        datatype:'json',
        async:false,
        success:function(res){
            let data = res.merged
            board_length = data.length
            for(i=0;i<num;i++){
                // 결측치 처리
                if(data[i]['new_cases']==-1){
                    data[i]['new_cases'] = "-"
                };
                if(data[i]['new_deaths']==-1){
                    data[i]['new_deaths'] = "-"
                };
                if(data[i]['new_recovered']==-1){
                    data[i]['new_recovered'] = "-"
                };
                if(data[i]['country_kr']==-1){
                    data[i]['country_kr'] = data[i]['country_x']
                };
                if(data[i]['critical_ratio']==-1){
                    data[i]['critical_ratio'] = "-"
                };
                if(data[i]['recovered_ratio']==-1){
                    data[i]['recovered_ratio'] = "-"
                };
                if(data[i]['total_caeses_per_1million_population']==-1){
                    data[i]['total_caeses_per_1million_population'] = "-"
                };
                if(data[i]['vaccinated']==-1){
                    data[i]['vaccinated'] = "-"
                };
                if(data[i]['fully_vaccinated']==-1){
                    data[i]['fully_vaccinated'] = "-"
                };
                if(data[i]['total_recovered']==-1){
                    data[i]['total_recovered'] = "-"
                };
                if(data[i]['total_deaths']==-1){
                    data[i]['total_deaths'] = "-"
                };
                // 대륙분류 기능
                if(conti=='all'){
                    $('#board-data').append(`
                        <tr>
                            <td><a style="color:black;" target="_blank" rel="noopener noreferrer" href ="/country/${data[i]['iso_code']}">${data[i]["country_kr"]} </a></td>
                            <td>${data[i]["total_cases"]}<span class="new-statistic">(${data[i]["new_cases"]})</span></td>
                            <td>${data[i]["total_deaths"]}<span class="new-statistic">(${data[i]["new_deaths"]})</span></td>
                            <td>${data[i]["total_recovered"]}<span class="new-statistic">(${data[i]["new_recovered"]})</span></td>
                            <td>${data[i]["critical_ratio"]}%</td>
                            <td>${data[i]["recovered_ratio"]}%</td>
                            <td>${data[i]["total_caeses_per_1million_population"]}명</td>
                            <td>${data[i]["vaccinated"]}%</td>
                            <td>${data[i]["fully_vaccinated"]}%</td>
                        </tr>
                    `)  
                }
                else if(conti =='Europe'){
                    if(data[i]['continent']=='Europe'){
                        $('#board-data').append(`
                            <tr>
                                <td><a style="color:black;" target="_blank" rel="noopener noreferrer" href ="/country/${data[i]['iso_code']}">${data[i]["country_kr"]}</a></td>
                                <td>${data[i]["total_cases"]}<span class="new-statistic">(${data[i]["new_cases"]})</span></td>
                                <td>${data[i]["total_deaths"]}<span class="new-statistic">(${data[i]["new_deaths"]})</span></td>
                                <td>${data[i]["total_recovered"]}<span class="new-statistic">(${data[i]["new_recovered"]})</span></td>
                                <td>${data[i]["critical_ratio"]}%</td>
                                <td>${data[i]["recovered_ratio"]}%</td>
                                <td>${data[i]["total_caeses_per_1million_population"]}명</td>
                                <td>${data[i]["vaccinated"]}%</td>
                                <td>${data[i]["fully_vaccinated"]}%</td>
                            </tr>
                        `)
                    }
                }
                else if(conti =='Asia'){
                    if(data[i]['continent']=='Asia'){
                        $('#board-data').append(`
                            <tr>
                                <td><a style="color:black;" target="_blank" rel="noopener noreferrer" href ="/country/${data[i]['iso_code']}">${data[i]["country_kr"]}</a></td>
                                <td>${data[i]["total_cases"]}<span class="new-statistic">(${data[i]["new_cases"]})</span></td>
                                <td>${data[i]["total_deaths"]}<span class="new-statistic">(${data[i]["new_deaths"]})</span></td>
                                <td>${data[i]["total_recovered"]}<span class="new-statistic">(${data[i]["new_recovered"]})</span></td>
                                <td>${data[i]["critical_ratio"]}%</td>
                                <td>${data[i]["recovered_ratio"]}%</td>
                                <td>${data[i]["total_caeses_per_1million_population"]}명</td>
                                <td>${data[i]["vaccinated"]}%</td>
                                <td>${data[i]["fully_vaccinated"]}%</td>
                            </tr>
                        `)
                    }
                }
                else if(conti =='North America'){
                    if(data[i]['continent']=='NorthernAmerica'){
                        $('#board-data').append(`
                            <tr>
                                <td><a style="color:black;" target="_blank" rel="noopener noreferrer" href ="/country/${data[i]['iso_code']}">${data[i]["country_kr"]}</a></td>
                                <td>${data[i]["total_cases"]}<span class="new-statistic">(${data[i]["new_cases"]})</span></td>
                                <td>${data[i]["total_deaths"]}<span class="new-statistic">(${data[i]["new_deaths"]})</span></td>
                                <td>${data[i]["total_recovered"]}<span class="new-statistic">(${data[i]["new_recovered"]})</span></td>
                                <td>${data[i]["critical_ratio"]}%</td>
                                <td>${data[i]["recovered_ratio"]}%</td>
                                <td>${data[i]["total_caeses_per_1million_population"]}명</td>
                                <td>${data[i]["vaccinated"]}%</td>
                                <td>${data[i]["fully_vaccinated"]}%</td>
                            </tr>
                        `)
                    }
                }
                else if(conti =='South America'){
                    if(data[i]['continent']=='America'){
                        $('#board-data').append(`
                            <tr>
                                <td><a style="color:black;" target="_blank" rel="noopener noreferrer" href ="/country/${data[i]['iso_code']}">${data[i]["country_kr"]}</a></td>
                                <td>${data[i]["total_cases"]}<span class="new-statistic">(${data[i]["new_cases"]})</span></td>
                                <td>${data[i]["total_deaths"]}<span class="new-statistic">(${data[i]["new_deaths"]})</span></td>
                                <td>${data[i]["total_recovered"]}<span class="new-statistic">(${data[i]["new_recovered"]})</span></td>
                                <td>${data[i]["critical_ratio"]}%</td>
                                <td>${data[i]["recovered_ratio"]}%</td>
                                <td>${data[i]["total_caeses_per_1million_population"]}명</td>
                                <td>${data[i]["vaccinated"]}%</td>
                                <td>${data[i]["fully_vaccinated"]}%</td>
                            </tr>
                        `)
                    }
                }
                else if(conti =='Oceania'){
                    if(data[i]['continent']=='Oceania'){
                        $('#board-data').append(`
                            <tr>
                                <td><a style="color:black;" target="_blank" rel="noopener noreferrer" href ="/country/${data[i]['iso_code']}">${data[i]["country_kr"]}</a></td>
                                <td>${data[i]["total_cases"]}<span class="new-statistic">(${data[i]["new_cases"]})</span></td>
                                <td>${data[i]["total_deaths"]}<span class="new-statistic">(${data[i]["new_deaths"]})</span></td>
                                <td>${data[i]["total_recovered"]}<span class="new-statistic">(${data[i]["new_recovered"]})</span></td>
                                <td>${data[i]["critical_ratio"]}%</td>
                                <td>${data[i]["recovered_ratio"]}%</td>
                                <td>${data[i]["total_caeses_per_1million_population"]}명</td>
                                <td>${data[i]["vaccinated"]}%</td>
                                <td>${data[i]["fully_vaccinated"]}%</td>
                            </tr>
                        `)
                    }
                }
                else if(conti =='Africa'){
                    if(data[i]['continent']=='Africa'){
                        $('#board-data').append(`
                            <tr>
                                <td><a style="color:black;" target="_blank" rel="noopener noreferrer" href ="/country/${data[i]['iso_code']}">${data[i]["country_kr"]}</a></td>
                                <td>${data[i]["total_cases"]}<span class="new-statistic">(${data[i]["new_cases"]})</span></td>
                                <td>${data[i]["total_deaths"]}<span class="new-statistic">(${data[i]["new_deaths"]})</span></td>
                                <td>${data[i]["total_recovered"]}<span class="new-statistic">(${data[i]["new_recovered"]})</span></td>
                                <td>${data[i]["critical_ratio"]}%</td>
                                <td>${data[i]["recovered_ratio"]}%</td>
                                <td>${data[i]["total_caeses_per_1million_population"]}명</td>
                                <td>${data[i]["vaccinated"]}%</td>
                                <td>${data[i]["fully_vaccinated"]}%</td>
                            </tr>
                        `)
                    }
                }
                
            }
        }
    })
}
// 접어보기 펼쳐보기 기능
$('.loadall').on('click',()=>{
    $('#board-data').html("");
    if(document.querySelector('.loadall').innerText=='전체보기'){
        load_board(board_length,board_continent);
        $('.loadall').html('접어보기');
    }else{
        load_board(num,board_continent);
        $('.loadall').html('전체보기');
    };
    
})
// 대륙선택 기능
$('#board-select').change(function(){
    board_continent = $('#board-select option:selected').val()
    load_board(board_length,board_continent)
    $('.loadall').html('접어보기');
})

//발생률 툴팁
// $('.caseper1millon').on('mouseover', function () {
//     $('.tooltip').removeClass('fadeout');
//   });
// $('.caseper1millon').on('mouseleave', function () {
//     $('.tooltip').addClass('fadeout');
// });
// 사이트 실행시 보드 렌더링
load_board(num,board_continent)
