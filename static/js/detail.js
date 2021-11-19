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
  if (document.querySelector('#chart2Data1').textContent ==='-1.0') {
    const containerEl = document.querySelector('#container');
    let containerDiv = document.createElement('div');
    containerDiv.setAttribute('class', 'notData');
    containerDiv.textContent = "백신 접종률에 대한 데이터가 없습니다.";
    containerEl.append(containerDiv);
  } else {
    Highcharts.setOptions({
      colors: ['#058DC7', '#64E572']
      // #64E572
      // #6AF9C4
      // #50B432
  });
    const chart = Highcharts.chart('container', {
      chart: {
          type: 'column',
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
      
      series: [
        {
          name: `1차 접종률`,
          data: [parseInt(document.querySelector('#chart2Data1').textContent)],
      }, {
          name: `2차 접종률`,
          data: [parseInt(document.querySelector('#chart2Data2').textContent)]
      }]
    });
  }
  
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
  const inputNicknameEl = document.querySelector('.input-nickname');
  const inputCommentEl = document.querySelector('.input-comment');
  const inputPwEl = document.querySelector('.input-pw');
  const btnSubmitEl = document.querySelector('.btn-submit');
  if ((inputNicknameEl.value !=='')&&(inputCommentEl.value !=='') && (inputPwEl.value !=='')) {
    btnSubmitEl.removeAttribute('disabled');
  } else {
    btnReset()
  }
}
function btnReset() {
  const btnSubmitEl = document.querySelector('.btn-submit');
  btnSubmitEl.setAttribute('disabled','false');
}


//댓글 임시 데이터
data =[
  {
    name: "첫번째",
    content : "블라블라블라블라블라블라블라블라블라블라블라블라블라블라블라블라블라블라블라블라블라블라블라블라블라블라블라블라블라블라블라블라블라블라블라블라",
    pw: "1234",
    time: "2021-01-03",
    like: 96,
    hate: 33,
    otherComment:[
      {
        name: "첫번째 대댓글",
        content : "꾸르꺄숑 꾸꾸으라룡",
        pw: "1234",
        time: "2021-02-02",
        like: 6,
        hate: 0,
      }
    ]
  },
  {
    name: "두번째",
    content : "꺄르르",
    pw: "1234",
    time: "2021-02-02",
    like: 76,
    hate: 53,
    otherComment:[
      {
        name: "두번째 대댓글",
        content : "꾸르꺄숑 꾸꾸으라룡",
        pw: "1234",
        time: "2021-02-02",
        like: 6,
        hate: 0,
      },
      {
        name: "두번째의 두번째 대댓글",
        content : "꾸르꺄숑 꾸꾸으라룡",
        pw: "1234",
        time: "2021-02-02",
        like: 6,
        hate: 0,
      },
    ],
  },
  {
    name: "세번째",
    content : "제발 돼라, 돼라 돼라",
    pw: "1234",
    time: "2021-01-03",
    like: 96,
    hate: 33,
    otherComment:[
      {
        name: "세번째 대댓글",
        content : "꾸르꺄숑 꾸꾸으라룡",
        pw: "1234",
        time: "2021-02-02",
        like: 6,
        hate: 0,
      }
    ]
  },
]
// 댓글 보여 주기
function readComment(data) {
  const commentListEl = document.querySelector('.comment-list');
  data.forEach((el, i)=>{
    let commentBoxDiv = document.createElement('div');
    commentBoxDiv.setAttribute('class','comment-box');
    commentBoxDiv.innerHTML = `
    <div class="box-head">
      <span class="comment-nickname">${el.name}</span>
      <span class="comment-period">${el.time}</span>
      <button class="btn btn-update-comment">수정</button>
      <button class="btn btn-delete-comment">삭제</button>
    </div>
    <div class="box-body">${el.content}</div>
    <div class="box-btn-group">
      <button class="like"><i class="far fa-thumbs-up"></i> ${el.like}</button>
      <button class="hate"><i class="far fa-thumbs-down"></i> ${el.hate}</button>
      <button class="btn-plus-comment">답글</button>
    </div>
    `;
    commentListEl.append(commentBoxDiv);

    if (el.otherComment.length !== 0) {
      readPlusComment(el.otherComment , i)
      plusCommentAddListener();
    }
  })
}
// 대댓글 보여주기
function readPlusComment(others, i) {
  let commentBoxEl = document.querySelectorAll('.comment-box');
  let readPlusDiv = document.createElement('div');
  readPlusDiv.innerHTML =`
  <div class="read-plus-comment">
    <div class="triangle">▼</div>&ensp;
    <span class="show-comment">답글 ${others.length}개 보기</span>
    <div class="plus-comment-list hidden"></div>
  </div>
  `;
  commentBoxEl[i].append(readPlusDiv);

  let plusCommentListEl = commentBoxEl[i].querySelector('.plus-comment-list');
  others.forEach((el)=>{
    let commentBoxDiv = document.createElement('div');
    commentBoxDiv.setAttribute('class','comment-box-plus');
    commentBoxDiv.innerHTML = `
    <div class="box-head">
      <span class="comment-nickname">${el.name}</span>
      <span class="comment-period">${el.time}</span>
      <button class="btn btn-update-comment">수정</button>
      <button class="btn btn-delete-comment">삭제</button>
    </div>
    <div class="box-body">${el.content}</div>
    <div class="box-btn-group">
      <button class="like"><i class="far fa-thumbs-up"></i> ${el.like}</button>
      <button class="hate"><i class="far fa-thumbs-down"></i> ${el.hate}</button>
      <button class="btn-plus-comment">답글</button>
    </div>
    `;
    plusCommentListEl.append(commentBoxDiv);
  })
}



// 대댓글 보기,숨기기
function togglePlusComment(event) {
  event.target.nextElementSibling.classList.toggle('hidden');
  event.target.parentElement.firstElementChild.classList.toggle('rotate');
  // event.target.previousElementSiblling.classList.toggle('rotate');
}
function plusCommentAddListener() {
  const plusCommentEl = document.querySelectorAll('.show-comment');
  plusCommentEl.forEach((el)=>{
    el.addEventListener('click',togglePlusComment);
  })
}

// 댓글 카운트
function commentCount(data) {
  let commentCountEl = document.querySelector('.comment-count');
  commentCountEl.textContent = `댓글 ${data.length}개`;
}


// 댓글 추가 기능
function addComment(){
  const inputNickname = document.querySelector('.input-nickname');
  const inputComment = document.querySelector('.input-comment');

  console.log(inputNickname.value);
  console.log(inputComment.value);

}

commentCount(data)
readComment(data);






