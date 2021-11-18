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
  $('.info-help div:first').html('코로나 관련 <b>여행자 요약 정보</b>별로 확인해보세요.<br>❗꼭 전체 정보를 확인하세요')
})
$('.allcontent').on('click',function(){
  
  $('.category-group').addClass('hidden')
  $('.all').removeClass('hidden')

  $('.info-help div:first').html('코로나 관련 <b>여행자 전체 정보</b>를 확인해보세요.<br>요약정보를 보러면 요약을 클릭하세요')
})


// 국기 추가하는 부분
let iso = window.location.pathname.slice(9,11).toLowerCase();
let tag = `<img src="https://flagcdn.com/40x30/${iso}.png" alt="">`
$(".flag").html(tag)



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
      yAxis: {
        title: '',
      },
      tooltip: {
        formatter: function() {
          return this.series.name+ " : " + this.y + '%'
        },
        hideDelay: 100
      },
      plotOptions: {
        series: {
          dataLabels: {
              enabled: true,
              format: '{y} %'
          }
      }
      },
      series: [{
          name: `1차 접종률`,
          data: [parseInt(document.querySelector('#chart2Data1').textContent)],
      }, {
          name: `2차 접종률`,
          data: [parseInt(document.querySelector('#chart2Data2').textContent)]
      }]
  });
});



// 숫자 애니메이션
function numberWithCommas(x) {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

var Endnum_list = document.querySelectorAll('.coronadata')
for(let i=0;i<Endnum_list.length;i++){
  endnum = parseInt(Endnum_list[i].innerText);
  if(endnum == -1){
    Endnum_list[i].innerText = '정보가 없습니다!'
  }
  else{
    $({ val : 0 }).animate({ val : endnum }, {
      duration: 1000,
     step: function() {
       var num = numberWithCommas(Math.floor(this.val));
       Endnum_list[i].innerText = num;
     },
     complete: function() {
       var num = numberWithCommas(Math.floor(this.val));
       Endnum_list[i].innerText = num;
     }
     });
  }
}
// 환율 계산기
let rate = $('.rate').text();
rate = Number(rate.replace(/[^0-9.-]+/g,""));

$('.exchangefrom').keyup(function(){
  let value = $('.exchangefrom').val();
  value = Number(value)
  let cal = value *(1/rate)
  cal = cal.toFixed(3)
  $('.exchangeto').text(cal)

})
$('.reverse-cal').on('click',function(){
  const fromname = $('.calculator div:first p').text()
  const toname = $('.calculator div:last p:first').text()
  $('.calculator div:first p').text(toname)
  $('.calculator div:last p:first').text(fromname)
  rate = 1/rate
  
})

//댓글 입력창 자동크기 조절
function resize(obj) {
  obj.style.height = '1px';
  obj.style.height = (3 + obj.scrollHeight)+ 'px';
}

//댓글 버튼 활성화
function btnActive() {
  const inputNickname = document.querySelector('.input-nickname');
  const inputComment = document.querySelector('.input-comment');
  const btnSubmit = document.querySelector('.btn-submit');
  if ((inputNickname.value !=='')&&(inputComment.value !=='')) {
    btnSubmit.removeAttribute('disabled');
  } else {
    btnSubmit.setAttribute('disabled','true');
  }
}