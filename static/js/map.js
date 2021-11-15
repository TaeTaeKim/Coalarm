let Zoom = 'world';
const countryCode = [
  //전세카이
  {name: '.world', code: 'world'},
  //아프리카
  {name: '.Africa', code: '002'},
  {name: '.northernAfrica', code: '015'},
  {name: '.westernAfrica', code: '011'},
  {name: '.middleAfrica', code: '017'},
  {name: '.easternAfrica', code: '014'},
  {name: '.southernAfrica', code: '018'},
  //유럽
  {name: '.Europe', code: '150'},
  {name: '.northernEurope', code: '154'},
  {name: '.westernEurope', code: '155'},
  {name: '.easternEurope', code: '151'},
  {name: '.southernEurope', code: '039'},
  //미대륙
  {name: '.Americas', code: '019'},
  {name: '.northernAmericas', code: '021'},
  {name: '.caribbean', code: '029'},
  {name: '.centralAmericas', code: '013'},
  {name: '.southAmericas', code: '005'},
  //아시아
  {name: '.Asia', code: '142'},
  {name: '.centralAsia', code: '143'},
  {name: '.easternAsia', code: '030'},
  {name: '.southernAsia', code: '034'},
  {name: '.southEasternAsia', code: '035'},
  {name: '.westernAsia', code: '145'},
  //오세아니아
  {name: '.Oceania', code: '009'},
  {name: '.australiaAndNewZealand', code: '053'},
  {name: '.melanesia', code: '054'},
  {name: '.micronesia', code: '057'},
  {name: '.polynesia', code: '061'}
];

// 지도 소분류 클릭 이동하기
countryCode.forEach((el) => {
  $(el.name).on('click', function () {
    Zoom = el.code;
    rendermap();
  })
});

// 페이지 resize시에 지도 갱신
$(window).resize(function(){location.reload();});

//dropmenu관련 설정
$(document).ready(()=>{
  $('.dropmenu').addClass('hidden')
  $('.btn').on('mouseover',function(){
    $(this).children('.dropmenu').removeClass('hidden')
  })
  $('.btn').on('mouseleave',()=>{
    $('.dropmenu').addClass('hidden')
  })

})





//map rendering하는 함수
function rendermap() {
  google.charts.load('current', {'packages': ['geochart']});
  google.charts.setOnLoadCallback(drawRegionsMap);

  function drawRegionsMap() {
    const data = new google.visualization.DataTable();
    data.addColumn('string', 'Country');
    data.addColumn('number', '확진자');
    $.ajax({
        url:'/data',
        type:'GET',
        dataType:'json',
        async:false,
        success: function(res){
          let mapdata = res.caution;
          mapdata.forEach((el)=>{
            data.addRows([
              [{
                v:el.country_iso_alp2,
                f:el.country_name
              }, parseInt(el.confirmed)]
            ])
          })
        },
        error: function(){
          alert('지도 데이터 로드 실패')
        }
    })    
    //   for(let i=0;i<data.length;i++){
    //       data.addRows([
    //           [{v:`${}`,f:`${}`},`${}`]
    //       ])
    //   }
    const options = {
      colorAxis: {colors: ['#00853f', 'black', '#e31b23']},
      backgroundColor: '#FFFFFF',
      region: Zoom,
      defaultColor: '#222222'
    };

    const chart = new google.visualization.GeoChart(document.getElementById('regions_div'));
    google.visualization.events.addListener(chart, 'select', function () {
      let selection = chart.getSelection();
      if (selection.length == 1) {
        var selectedRow = selection[0].row;
        var selectedRegion = data.getValue(selectedRow, 0);
        // 여기다가 클릭시 넘어가는 페이지 만들면 될듯.
        // $.ajax({
        //   url:
        // })
        $.ajax({
          url:`/country/${selectedRegion}`,
          type:'GET',
          async:false,
          success:function(){
            window.location.href = `/country/${selectedRegion}`
          },
          error:function(){
            alert('페이지 이동 실패 다시 시도해주세요')
          }
        })
      }
    });
    chart.draw(data, options);
  }
}



rendermap();