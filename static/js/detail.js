let categoryEl = document.querySelector('.information-content');

function categoryHandler(event) {
  if (event.target.getAttribute('class') === 'category-title') {
    event.target.nextElementSibling.classList.toggle('look');
  } else if (event.target.getAttribute('class') === 'click-guide') {
    event.target.parentElement.nextElementSibling.classList.toggle('look');
  }
}

categoryEl.addEventListener('click', categoryHandler);

$('.summary').on('click', function () {
  $('.category-group').removeClass('hidden');
  $('.all').addClass('hidden');
  $('.summary').addClass('active');
  $('.allcontent').removeClass('active');
  $('.info-help div:first').html(
    '코로나 관련 <b>여행자 요약 정보</b>별로 확인해보세요.<br>❗꼭 <b>전체</b> 정보를 확인하세요'
  );
});
$('.allcontent').on('click', function () {
  $('.category-group').addClass('hidden');
  $('.all').removeClass('hidden');
  $('.allcontent').addClass('active');
  $('.summary').removeClass('active');

  $('.info-help div:first').html(
    '코로나 관련 <b>여행자 전체 정보</b>를 확인해보세요.<br>요약정보를 보러면 <b>요약</b>을 클릭하세요'
  );
});

// 국기 추가하는 부분
let iso = window.location.pathname.slice(9, 11).toLowerCase();
let tag = `<img src="https://flagcdn.com/40x30/${iso}.png" alt="">`;
$('.flag').html(tag);

// 그래프
document.addEventListener('DOMContentLoaded', function () {
  if (document.querySelector('#chart2Data1').textContent === '-1.0') {
    const containerEl = document.querySelector('#container');
    let containerDiv = document.createElement('div');
    containerDiv.setAttribute('class', 'notData');
    containerDiv.textContent = '백신 접종률에 대한 데이터가 없습니다.';
    containerEl.append(containerDiv);
  } else {
    Highcharts.setOptions({
      colors: ['#058DC7', '#64E572'],
    });
    const chart = Highcharts.chart('container', {
      chart: {
        type: 'column',
      },
      credits: { enabled: false },
      title: {
        text: '백신접종률',
      },
      xAxis: {
        categories: [''],
      },
      yAxis: {
        title: '',
      },
      tooltip: {
        formatter: function () {
          return this.series.name + ' : ' + this.y + '%';
        },
        hideDelay: 100,
      },
      plotOptions: {
        series: {
          dataLabels: {
            enabled: true,
            format: '{y} %',
          },
        },
      },

      series: [
        {
          name: `1차 접종률`,
          data: [parseInt(document.querySelector('#chart2Data1').textContent)],
        },
        {
          name: `2차 접종률`,
          data: [parseInt(document.querySelector('#chart2Data2').textContent)],
        },
      ],
    });
  }
});

// 숫자 애니메이션
function numberWithCommas(x) {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}
function numberAnimation(className) {
  let Endnum_list = document.querySelectorAll(className);
  for (let i = 0; i < Endnum_list.length; i++) {
    endnum = parseInt(Endnum_list[i].innerText);
    if (endnum == -1) {
      Endnum_list[i].innerText = '정보가 없습니다!';
    } else {
      $({ val: 0 }).animate(
        { val: endnum },
        {
          duration: 1000,
          step: function () {
            let num = numberWithCommas(Math.floor(this.val));
            Endnum_list[i].innerText = num;
          },
          complete: function () {
            let num = numberWithCommas(Math.floor(this.val));
            Endnum_list[i].innerText = num;
          },
        }
      );
    }
  }
}
numberAnimation('.coronadata');
numberAnimation('.safe-point');

// 환율 계산기
let rate = $('.rate').text();
rate = Number(rate.replace(/[^0-9.-]+/g, ''));

$('.exchangefrom').keyup(function () {
  let value = $('.exchangefrom').val();
  value = Number(value);
  let cal = value * (1 / rate);
  cal = cal.toFixed(3);
  $('.exchangeto').text(cal);
});
$('.reverse-cal').on('click', function () {
  const fromname = $('.calculator div:first p').text();
  const toname = $('.calculator div:last p:first').text();
  $('.calculator div:first p').text(toname);
  $('.calculator div:last p:first').text(fromname);
  rate = 1 / rate;
});

$('.safe-point-group').on('mouseover', function () {
  $('.tooltip').removeClass('fadeout');
});
$('.safe-point-group').on('mouseleave', function () {
  $('.tooltip').addClass('fadeout');
});
// 안전점수 색입히기
function safeColor() {
  const safePointEl = document.querySelector('.safe-point');
  const sagePoint = parseInt(safePointEl.textContent);
  if (sagePoint >= 85) {
    safePointEl.classList.remove('middle', 'low');
    safePointEl.classList.add('high');
  } else if (sagePoint >= 70) {
    safePointEl.classList.remove('high', 'low');
    safePointEl.classList.add('middle');
  } else {
    safePointEl.classList.remove('high', 'middle');
    safePointEl.classList.add('low');
  }
}

const colorTimer = setInterval(() => {
  safeColor();
}, 100);

const clearcolorTimer = setTimeout(() => {
  clearInterval(colorTimer);
}, 1100);
