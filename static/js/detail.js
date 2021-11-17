let categoryEl = document.querySelector('.information-content');

function categoryHandler(event){
  if (event.target.getAttribute('class') === 'category-title'){
    event.target.nextElementSibling.classList.toggle('look')
  }
}

categoryEl.addEventListener('click',categoryHandler)

$('.summary').on('click',function(){
  $('.category-group').removeClass('hidden')
  $('.all').addClass('hidden')
  $('.info-help div:first').html('코로나 관련 <b>요약 정보</b>별로 확인해보세요.<br>❗꼭 전체 정보를 확인하세요')
})
$('.allcontent').on('click',function(){
  
  $('.category-group').addClass('hidden')
  $('.all').removeClass('hidden')
  $('.info-help div:first').html('코로나 관련 <b>전체 정보</b>를 확인해보세요.<br>요약정보를 보러면 요약을 클릭하세요')
})
// 그래프
document.addEventListener('DOMContentLoaded', function () {
  const chart = Highcharts.chart('container', {
      chart: {
          type: 'column'
      },
      credits:{enabled:false},
      title: {
          text: '백신접종률'
      },
      xAxis: {
          categories: ['']
      },
      tooltip: {
        formatter: function() {
          return this.series.name+ " : " + this.y + '%'
      }
      },
      series: [{
          name: '1차 접종률',
          data: [parseInt(document.querySelector('#chart2Data1').textContent)]
      }, {
          name: '2차 접종률',
          data: [parseInt(document.querySelector('#chart2Data2').textContent)]
      }]
  });
});
// 숫자 애니메이션
var 누적확진자= parseInt(document.querySelector('#confirmedNum').textContent);
  
$({ val : 0 }).animate({ val : 누적확진자 }, {
 duration: 1000,
step: function() {
  var num = numberWithCommas(Math.floor(this.val));
  $("#confirmedNum").text(num);
},
complete: function() {
  var num = numberWithCommas(Math.floor(this.val));
  $("#confirmedNum").text(num);
}
});
function numberWithCommas(x) {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}